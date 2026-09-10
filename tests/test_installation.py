from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import tooling.installer as installer_module
from tooling.errors import IntegrityError
from tooling.installer import install, recover_upgrade, upgrade
from tooling.projection import BEGIN, END, validate_workspace


SOURCE = Path(__file__).resolve().parents[1]


def init_repository(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=path, check=True)
    return path


def snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }


def stage_recovery_marker(
    source: Path, target: Path, *, suffix: str = "a" * 32
) -> tuple[Path, Path]:
    """Build the same sealed backup and hash inventory as a real upgrade."""

    record = json.loads((target / ".knowledge-sdlc/install.json").read_text())
    old_paths = sorted(
        set(record["owned_files"]) | {".knowledge-sdlc/install.json", "AGENTS.md"}
    )
    old_hashes = {
        relative: hashlib.sha256((target / relative).read_bytes()).hexdigest()
        for relative in old_paths
    }
    backup_relative = f".knowledge-sdlc/.upgrade-backup-{suffix}"
    backup = target / backup_relative
    for relative in old_paths:
        destination = backup / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target / relative, destination)

    planned = installer_module.plan_workspace(source, None)
    prior_agents = (target / "AGENTS.md").read_bytes()
    start, end, _ = installer_module._block_slice(prior_agents)
    planned["AGENTS.md"] = (
        prior_agents[:start] + planned["AGENTS.md"] + prior_agents[end:]
    )
    planned = {
        relative: content
        for relative, content in planned.items()
        if not relative.startswith("ai_docs/")
    }
    new_hashes = {
        relative: hashlib.sha256(content).hexdigest()
        for relative, content in planned.items()
    }
    marker = target / ".knowledge-sdlc/UPGRADE_RECOVERY.json"
    marker.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "backup": backup_relative,
                "old_hashes": old_hashes,
                "new_hashes": new_hashes,
            }
        ),
        encoding="utf-8",
    )
    return marker, backup


class InstallationTests(unittest.TestCase):
    def test_install_requires_an_existing_git_repository_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-target-") as raw:
            missing = Path(raw) / "missing"
            with self.assertRaises(IntegrityError):
                install(SOURCE, missing)

            plain = Path(raw) / "plain"
            plain.mkdir()
            with self.assertRaises(IntegrityError):
                install(SOURCE, plain)

            fake = Path(raw) / "fake"
            fake.mkdir()
            (fake / ".git").write_text("not a repository\n", encoding="utf-8")
            with self.assertRaises(IntegrityError):
                install(SOURCE, fake)

    def test_fresh_dry_run_reports_plan_without_changing_client_repository(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-install-preview-") as raw:
            target = init_repository(Path(raw) / "workspace")
            agents = target / "AGENTS.md"
            agents.write_text(
                "# Client instructions\n\nKeep these.\n", encoding="utf-8"
            )
            client_skill = target / ".agents/skills/client-method/SKILL.md"
            client_skill.parent.mkdir(parents=True)
            client_skill.write_text("# Client method\n", encoding="utf-8")
            before = snapshot(target)

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "tooling.installer",
                    "--source-root",
                    str(SOURCE),
                    "--dry-run",
                    str(target),
                ],
                cwd=SOURCE,
                text=True,
                capture_output=True,
                check=True,
            )
            result = json.loads(completed.stdout)

            self.assertEqual(snapshot(target), before)
            self.assertEqual(result["operation"], "install")
            self.assertEqual(result["mode"], "dry-run")
            self.assertTrue(result["existing_agents_md"])
            self.assertEqual(result["agents_action"], "append-managed-block")
            self.assertTrue(result["semantic_review_required"])
            self.assertFalse(result["writes_performed"])
            self.assertTrue(result["preflight_passed"])
            self.assertNotIn("validation_passed", result)
            self.assertIn("AGENTS.md", result["planned_files"])

    def test_fresh_install_is_contained_complete_and_nonduplicative(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-install-") as raw:
            target = init_repository(Path(raw) / "workspace")
            result = install(SOURCE, target)
            self.assertTrue(result["validation_passed"])
            self.assertTrue((target / ".agents/skills/knowledge-work/SKILL.md").is_file())
            self.assertFalse((target / ".knowledge-sdlc/skills").exists())
            self.assertFalse(any((target / ".knowledge-sdlc").rglob("*.py")))
            self.assertTrue((target / "ai_docs/initiatives/index.md").is_file())
            self.assertFalse((target / "ai_docs/domain-charter.md").exists())
            self.assertFalse((target / "ai_docs/LEARNINGS.md").exists())
            record = json.loads((target / ".knowledge-sdlc/install.json").read_text())
            self.assertEqual(record["schema_version"], 1)
            self.assertEqual(validate_workspace(target, SOURCE), [])
            managed = target / ".knowledge-sdlc/recipes/professional-research.md"
            managed.write_text(managed.read_text() + "\nmutation\n", encoding="utf-8")
            self.assertTrue(any("hash mismatch" in item for item in validate_workspace(target, SOURCE)))

    def test_collision_and_symlink_are_fail_closed_without_partial_install(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-install-") as raw:
            target = init_repository(Path(raw) / "workspace")
            collision = target / ".knowledge-sdlc/recipes/professional-research.md"
            collision.parent.mkdir(parents=True)
            collision.write_text("client owned\n", encoding="utf-8")
            before = snapshot(target)
            with self.assertRaises(IntegrityError):
                install(SOURCE, target)
            self.assertEqual(snapshot(target), before)

            linked_target = init_repository(Path(raw) / "linked")
            (linked_target / ".agents").symlink_to(Path(raw) / "outside", target_is_directory=True)
            with self.assertRaises(IntegrityError):
                install(SOURCE, linked_target)
            self.assertFalse((Path(raw) / "outside").exists())

    def test_existing_agents_bytes_are_preserved_around_one_managed_block(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-install-") as raw:
            target = init_repository(Path(raw) / "workspace")
            agents = target / "AGENTS.md"
            prefix = b"# Client contract\n\nKeep exactly.\n"
            agents.write_bytes(prefix)
            install(SOURCE, target)
            data = agents.read_bytes()
            self.assertTrue(data.startswith(prefix))
            self.assertEqual(data.count(BEGIN.encode()), 1)
            self.assertEqual(data.count(END.encode()), 1)

    def test_receipted_upgrade_preserves_project_state_and_refuses_edited_block(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-upgrade-") as raw:
            base = Path(raw)
            target = init_repository((base / "workspace").resolve())
            install(SOURCE, target)
            project = target / "ai_docs/project-owned-note.md"
            project.write_text("Project-owned note.\n", encoding="utf-8")
            project_hash = hashlib.sha256(project.read_bytes()).hexdigest()

            next_source = base / "next-source"
            shutil.copytree(SOURCE, next_source, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__", ".pytest_cache"))
            (next_source / ".knowledge-sdlc/VERSION").write_text("0.6.1-test\n", encoding="utf-8")
            agents = next_source / "AGENTS.md"
            agents.write_text(agents.read_text() + "\nUpgrade test sentence.\n", encoding="utf-8")
            dry = upgrade(next_source, target, apply=False)
            self.assertEqual(dry["mode"], "dry-run")
            upgrade(next_source, target, apply=True)
            self.assertEqual((target / ".knowledge-sdlc/VERSION").read_text().strip(), "0.6.1-test")
            self.assertEqual(hashlib.sha256(project.read_bytes()).hexdigest(), project_hash)
            self.assertIn("Upgrade test sentence", (target / "AGENTS.md").read_text())

            data = (target / "AGENTS.md").read_text()
            (target / "AGENTS.md").write_text(data.replace("Upgrade test sentence", "User edited managed block"), encoding="utf-8")
            with self.assertRaises(IntegrityError):
                upgrade(next_source, target, apply=False)

    def test_upgrade_refuses_a_new_managed_path_that_collides_with_client_content(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-upgrade-collision-") as raw:
            base = Path(raw)
            target = init_repository(base / "workspace")
            install(SOURCE, target)
            collision = target / ".knowledge-sdlc/templates/future-template.md"
            collision.write_text("client owned\n", encoding="utf-8")
            before = snapshot(target)

            next_source = base / "next-source"
            shutil.copytree(SOURCE, next_source, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__", ".pytest_cache"))
            (next_source / ".knowledge-sdlc/templates/future-template.md").write_text("new managed template\n", encoding="utf-8")
            with self.assertRaises(IntegrityError):
                upgrade(next_source, target, apply=True)
            self.assertEqual(snapshot(target), before)

    def test_recovery_rejects_marker_paths_outside_the_target(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-recovery-") as raw:
            base = Path(raw)
            target = init_repository(base / "workspace")
            install(SOURCE, target)
            outside = base / "outside"
            outside.write_text("must remain\n", encoding="utf-8")
            marker = target / ".knowledge-sdlc/UPGRADE_RECOVERY.json"
            marker.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "backup": "../../outside",
                        "old_hashes": {"../../outside": "0" * 64},
                        "new_hashes": {"AGENTS.md": "0" * 64},
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaises(IntegrityError):
                recover_upgrade(SOURCE, target)
            self.assertEqual(outside.read_text(encoding="utf-8"), "must remain\n")

    def test_recovery_rejects_forged_client_path_without_deleting_it(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-recovery-forged-") as raw:
            target = init_repository((Path(raw) / "workspace").resolve())
            install(SOURCE, target)
            marker, _ = stage_recovery_marker(SOURCE, target)
            client = target / "client-owned.md"
            client.write_text("must remain\n", encoding="utf-8")
            payload = json.loads(marker.read_text())
            payload["new_hashes"]["client-owned.md"] = hashlib.sha256(
                client.read_bytes()
            ).hexdigest()
            marker.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaises(IntegrityError):
                recover_upgrade(SOURCE, target)
            self.assertEqual(client.read_text(encoding="utf-8"), "must remain\n")
            self.assertTrue(marker.exists())

    def test_recovery_refuses_an_incomplete_backup_before_restoring_anything(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-recovery-incomplete-") as raw:
            target = init_repository(Path(raw) / "workspace")
            install(SOURCE, target)
            marker, backup = stage_recovery_marker(SOURCE, target)
            version = target / ".knowledge-sdlc/VERSION"
            version.write_text("interrupted\n", encoding="utf-8")
            (backup / ".knowledge-sdlc/VERSION").unlink()

            with self.assertRaises(IntegrityError):
                recover_upgrade(SOURCE, target)
            self.assertEqual(version.read_text(encoding="utf-8"), "interrupted\n")
            self.assertTrue(marker.exists())

    def test_parent_swap_between_preflight_and_commit_cannot_escape(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-swap-") as raw:
            base = Path(raw)
            target = init_repository(base / "workspace")
            outside = base / "outside"
            outside.mkdir()
            original = installer_module._create_parents

            def swap_parent(root: Path, paths: set[str]) -> list[Path]:
                created = original(root, paths)
                agents = root / ".agents"
                shutil.rmtree(agents)
                agents.symlink_to(outside, target_is_directory=True)
                return created

            with patch("tooling.installer._create_parents", side_effect=swap_parent):
                with self.assertRaises(IntegrityError):
                    install(SOURCE, target)
            self.assertEqual(list(outside.iterdir()), [])

    def test_late_parent_swap_cannot_return_success_or_leave_escaped_file(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-late-swap-") as raw:
            base = Path(raw)
            target = init_repository((base / "workspace").resolve())
            outside = base / "outside"
            outside.mkdir()
            real_link = installer_module.os.link
            trigger = target / "ai_docs/initiatives/index.md"
            swapped = False

            def swap_at_link(source: Path, destination: Path, *args, **kwargs):
                nonlocal swapped
                destination = Path(destination)
                if destination == trigger and not swapped:
                    moved = outside / "reference"
                    destination.parent.rename(moved)
                    destination.parent.symlink_to(moved, target_is_directory=True)
                    swapped = True
                return real_link(source, destination, *args, **kwargs)

            with patch("tooling.installer.os.link", side_effect=swap_at_link):
                with self.assertRaises(IntegrityError):
                    install(SOURCE, target)

            self.assertTrue(swapped)
            self.assertFalse((outside / "initiatives/index.md").exists())
            self.assertFalse((target / "ai_docs/initiatives").exists())

    def test_failed_post_commit_validation_rolls_back_the_fresh_install(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-post-validate-") as raw:
            target = init_repository(Path(raw) / "workspace")
            client = target / ".agents/skills/client-method/SKILL.md"
            client.parent.mkdir(parents=True)
            client.write_text("# Client method\n", encoding="utf-8")
            before = snapshot(target)

            with patch(
                "tooling.installer.validate_workspace",
                return_value=["forced final validation defect"],
            ):
                with self.assertRaises(IntegrityError):
                    install(SOURCE, target)

            self.assertEqual(snapshot(target), before)

    def test_existing_agents_change_is_captured_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-agents-race-") as raw:
            target = init_repository((Path(raw) / "workspace").resolve())
            agents = target / "AGENTS.md"
            agents.write_text("initial client rule\n", encoding="utf-8")
            real_replace = installer_module.os.replace

            def mutate_before_capture(source: Path, destination: Path, *args, **kwargs):
                if Path(source) == agents:
                    agents.write_text("concurrent client rule\n", encoding="utf-8")
                return real_replace(source, destination, *args, **kwargs)

            with patch("tooling.installer.os.replace", side_effect=mutate_before_capture):
                with self.assertRaises(IntegrityError):
                    install(SOURCE, target)

            self.assertEqual(
                agents.read_text(encoding="utf-8"), "concurrent client rule\n"
            )
            self.assertFalse((target / ".knowledge-sdlc").exists())

    def test_interrupted_upgrade_marker_restores_recorded_backup(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-recover-valid-") as raw:
            target = init_repository(Path(raw) / "workspace")
            install(SOURCE, target)
            relative = ".knowledge-sdlc/VERSION"
            original = (target / relative).read_bytes()
            marker, _ = stage_recovery_marker(SOURCE, target)
            (target / relative).write_text("interrupted\n", encoding="utf-8")
            result = recover_upgrade(SOURCE, target)
            self.assertTrue(result["restored"])
            self.assertEqual((target / relative).read_bytes(), original)
            self.assertFalse(marker.exists())

    def test_upgrade_race_at_new_managed_path_preserves_client_bytes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-upgrade-race-") as raw:
            base = Path(raw)
            target = init_repository(base / "workspace")
            install(SOURCE, target)
            next_source = base / "next-source"
            shutil.copytree(
                SOURCE,
                next_source,
                ignore=shutil.ignore_patterns(
                    ".git", "dist", "__pycache__", ".pytest_cache"
                ),
            )
            relative = ".knowledge-sdlc/templates/future-template.md"
            (next_source / relative).write_text(
                "new managed template\n", encoding="utf-8"
            )
            collision = target / relative
            original_create_parents = installer_module._create_parents

            def inject_client_file(root: Path, paths: set[str]) -> list[Path]:
                created = original_create_parents(root, paths)
                collision.write_text("client arrived after preflight\n", encoding="utf-8")
                return created

            with patch(
                "tooling.installer._create_parents", side_effect=inject_client_file
            ):
                with self.assertRaises(IntegrityError):
                    upgrade(next_source, target, apply=True)

            self.assertEqual(
                collision.read_text(encoding="utf-8"),
                "client arrived after preflight\n",
            )
            self.assertTrue((target / installer_module.RECOVERY).exists())


if __name__ == "__main__":
    unittest.main()
