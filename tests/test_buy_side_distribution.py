from __future__ import annotations

import contextlib
import io
import json
import posixpath
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tooling.contracts import discover_methods, discover_recipes, source_inventory, validate_source
from tooling.errors import IntegrityError
from tooling.installer import install, main as installer_main, upgrade
from tooling.projection import BEGIN, END, plan_plugin, plan_workspace, validate_plugin_plan, validate_workspace
from tooling.util import sha256_file

SOURCE = Path(__file__).resolve().parents[1]
SKILLS = (
    "derive-buy-side-decision-to-data",
    "produce-evidence-bound-model-candidate",
    "challenge-frozen-buy-side-candidate",
    "verify-discriminating-buy-side-claims",
)
REFERENCE = ".knowledge-sdlc/references/buy-side-method/semantic-contracts.md"


def source_copy(parent: Path) -> Path:
    root = parent / "source"
    shutil.copytree(SOURCE, root, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__", ".pytest_cache"))
    return root


def git_client(parent: Path) -> Path:
    target = parent / "client"
    target.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=target, check=True)
    return target


class BuySideDistributionTests(unittest.TestCase):
    def test_conflicting_recovery_modes_are_rejected_before_dispatch(self) -> None:
        for other in ("--dry-run", "--upgrade", "--apply"):
            with (
                self.subTest(other=other),
                patch.object(sys, "argv", ["installer", "--recover", other, "/unused-target"]),
                patch("tooling.installer.recover_upgrade", return_value={}) as recovery,
                contextlib.redirect_stderr(io.StringIO()),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                with self.assertRaises(SystemExit) as stopped:
                    installer_main()
                self.assertEqual(stopped.exception.code, 2)
                recovery.assert_not_called()

    def test_standalone_preview_upgrade_and_recovery_routes_remain_available(self) -> None:
        routes = [
            (["--dry-run"], "preview_install", None),
            (["--upgrade", "--dry-run"], "upgrade", False),
            (["--upgrade", "--apply"], "upgrade", True),
            (["--recover"], "recover_upgrade", None),
        ]
        for flags, target, apply in routes:
            with (
                self.subTest(flags=flags),
                patch.object(sys, "argv", ["installer", *flags, "/unused-target"]),
                patch("tooling.installer." + target, return_value={}) as dispatch,
                contextlib.redirect_stdout(io.StringIO()),
            ):
                self.assertEqual(installer_main(), 0)
                dispatch.assert_called_once()
                if apply is not None:
                    self.assertEqual(dispatch.call_args.kwargs, {"apply": apply})

    def test_all_four_skills_and_their_shared_resources_reach_both_projections(self) -> None:
        methods = discover_methods(SOURCE)
        workspace, plugin = plan_workspace(SOURCE), plan_plugin(SOURCE)
        source_files = {row["path"]: row["sha256"] for row in source_inventory(SOURCE)}
        for name in SKILLS:
            self.assertIn(name, set(methods))
            self.assertIn(f".agents/skills/{name}/SKILL.md", workspace)
            self.assertIn(f"skills/{name}/SKILL.md", plugin)
            self.assertTrue(methods[name]["references"])
            for ref in methods[name]["references"]:
                self.assertIn(ref, source_files)
                self.assertEqual(source_files[ref], sha256_file(SOURCE / ref))
                self.assertEqual(workspace[ref], (SOURCE / ref).read_bytes())
                packaged = "resources/" + ref
                self.assertEqual(plugin[packaged], workspace[ref])
                logical_tail = Path(ref).relative_to(".knowledge-sdlc").as_posix()
                resolved = posixpath.normpath(posixpath.join("skills", name, "../../resources/.knowledge-sdlc", logical_tail))
                self.assertEqual(resolved, packaged)
                self.assertIn(b"../../resources/.knowledge-sdlc/", plugin[f"skills/{name}/SKILL.md"])
        refs = [p for p in workspace if p.startswith(".knowledge-sdlc/references/")]
        self.assertTrue(refs)
        self.assertFalse(any(p.startswith("ai_docs/methods/") for p in workspace))
        self.assertFalse(any(p.startswith("buy-side-method/") for p in workspace))
        self.assertFalse(any(p.endswith(".py") for p in workspace))
        incomplete = dict(plugin)
        incomplete.pop("resources/" + REFERENCE)
        with self.assertRaises(IntegrityError):
            validate_plugin_plan(incomplete, methods, discover_recipes(SOURCE))

    def test_missing_unsafe_and_linked_reference_dependencies_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-buy-side-source-") as raw:
            root = source_copy(Path(raw))
            reference = root / REFERENCE
            reference.unlink()
            self.assertTrue(any(x.code == "method-reference-missing" for x in validate_source(root)))
            with self.assertRaises(IntegrityError):
                plan_workspace(root)
            shutil.copy2(SOURCE / REFERENCE, reference)
            method = root / ".knowledge-sdlc/skills" / SKILLS[0] / "SKILL.md"
            original = method.read_text()
            method.write_text(original.replace(REFERENCE, ".knowledge-sdlc/references/../../outside.md", 1))
            self.assertTrue(any(x.code == "method-reference-path" for x in validate_source(root)))
            method.write_text(original)
            reference.unlink()
            reference.symlink_to(SOURCE / REFERENCE)
            self.assertTrue(any(x.code == "reference-tree" for x in validate_source(root)))
            with self.assertRaises(IntegrityError):
                plan_plugin(root)

    def test_indirect_reference_link_is_not_hidden_by_direct_dependencies(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-buy-side-link-") as raw:
            root = source_copy(Path(raw))
            (root / ".knowledge-sdlc/references/buy-side-method/capability-and-runtime-binding.md").unlink()
            self.assertTrue(any(x.code == "reference-link" for x in validate_source(root)))
            with self.assertRaises(IntegrityError):
                plan_workspace(root)

    def test_normal_install_leaves_client_policy_and_originals_unconfigured(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-buy-side-install-") as raw:
            target = git_client(Path(raw))
            original = b"# Analyst rules\nDo not change my forecasts without asking.\n"
            (target / "AGENTS.md").write_bytes(original)
            model = target / "analyst-model.txt"
            model.write_bytes(b"client-owned protected placeholder\n")
            result = install(SOURCE, target)
            self.assertTrue(result["validation_passed"])
            self.assertEqual(validate_workspace(target, SOURCE), [])
            self.assertTrue((target / "AGENTS.md").read_bytes().startswith(original))
            self.assertEqual((target / "AGENTS.md").read_text().count(BEGIN), 1)
            self.assertEqual((target / "AGENTS.md").read_text().count(END), 1)
            self.assertEqual(model.read_bytes(), b"client-owned protected placeholder\n")
            self.assertEqual(
                [p.relative_to(target).as_posix() for p in (target / "ai_docs").rglob("*") if p.is_file()],
                ["ai_docs/initiatives/index.md"],
            )
            record = json.loads((target / ".knowledge-sdlc/install.json").read_text())
            self.assertIn(REFERENCE, set(record["owned_files"]))
            for name in SKILLS:
                self.assertTrue((target / f".agents/skills/{name}/SKILL.md").is_file())

    def test_unowned_native_skill_collision_stops_without_overwriting(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-buy-side-collision-") as raw:
            target = git_client(Path(raw))
            existing = target / ".agents/skills" / SKILLS[0] / "SKILL.md"
            existing.parent.mkdir(parents=True)
            existing.write_bytes(b"private old method\n")
            with self.assertRaises(IntegrityError):
                install(SOURCE, target)
            self.assertEqual(existing.read_bytes(), b"private old method\n")
            self.assertFalse((target / ".knowledge-sdlc/install.json").exists())

    def test_reference_upgrade_is_owned_but_client_edits_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-buy-side-upgrade-") as raw:
            parent = Path(raw)
            source = source_copy(parent)
            target = git_client(parent)
            install(source, target)
            index = target / "ai_docs/initiatives/index.md"
            index.write_bytes(b"# Real client initiative\n")
            reference = source / REFERENCE
            reference.write_text(reference.read_text() + "\nUpdated explanation.\n")
            self.assertEqual(upgrade(source, target, apply=False)["mode"], "dry-run")
            self.assertTrue(upgrade(source, target, apply=True)["validation_passed"])
            self.assertEqual((target / REFERENCE).read_bytes(), reference.read_bytes())
            self.assertEqual(index.read_bytes(), b"# Real client initiative\n")
            (target / REFERENCE).write_bytes(b"client's intentional edit\n")
            with self.assertRaises(IntegrityError):
                upgrade(source, target, apply=True)
            self.assertEqual((target / REFERENCE).read_bytes(), b"client's intentional edit\n")


if __name__ == "__main__":
    unittest.main()
