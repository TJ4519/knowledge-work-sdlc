"""Distribution and authority-contract checks; not live-agent evaluations."""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tooling.contracts import discover_methods, discover_recipes, validate_source
from tooling.errors import IntegrityError
from tooling.installer import install, upgrade
from tooling.projection import plan_plugin, plan_workspace, validate_plugin, validate_workspace
from tooling.util import parse_frontmatter

SOURCE = Path(__file__).resolve().parents[1]
REPLAY = ".knowledge-sdlc/skills/kw-replay/SKILL.md"
REFERENCE = ".knowledge-sdlc/references/working-memory.md"


def client(path: Path) -> Path:
    path.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=path, check=True)
    return path


def snapshot(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*")
            if p.is_file() and ".git" not in p.relative_to(root).parts}


class ContinuityReplayTests(unittest.TestCase):
    def test_replay_is_one_optional_inline_procedure(self) -> None:
        self.assertEqual(validate_source(SOURCE), [])
        methods = discover_methods(SOURCE)
        replay = methods["kw-replay"]
        self.assertEqual(replay["kind"], "skill")
        self.assertFalse(replay["fresh_context"])
        self.assertNotIn("Task", replay["allowed_tools"])
        self.assertEqual(replay["outputs"], [])
        self.assertEqual(set(replay["optional_outputs"]), {"work-order", "candidate-research"})
        self.assertIn("previous-answer-as-truth", replay["excluded_context"])
        for recipe in discover_recipes(SOURCE).values():
            for step in recipe["composition"]:
                if step.get("method") == "kw-replay":
                    self.assertTrue(step.get("optional"))
                    self.assertTrue(step.get("trigger"))

    def test_current_recovery_keeps_its_read_boundary(self) -> None:
        prime = discover_methods(SOURCE)["kw-prime"]
        self.assertEqual(prime["inputs"], ["initiative-catalogue", "run-record"])
        self.assertNotIn("Task", prime["allowed_tools"])
        self.assertTrue({"old-transcript", "superseded-artefacts",
                         "unrelated-initiative-content", "unselected-reusable-lesson"}
                        <= set(prime["excluded_context"]))

    def test_replay_and_recall_preserve_their_bodies_in_both_packages(self) -> None:
        methods = discover_methods(SOURCE)
        ws, plugin = plan_workspace(SOURCE), plan_plugin(SOURCE)
        for name in ("kw-replay", "kw-recall", "kw-orchestration"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as raw:
                path = Path(raw) / "SKILL.md"
                path.write_bytes(ws[f".agents/skills/{name}/SKILL.md"])
                metadata, body = parse_frontmatter(path)
                self.assertEqual(body.strip(), methods[name]["body"].strip())
                self.assertEqual(metadata["authority"], methods[name]["authority"])
                path.write_bytes(plugin[f"skills/{name}/SKILL.md"])
                metadata, body = parse_frontmatter(path)
                self.assertTrue(body.rstrip().endswith(methods[name]["body"].rstrip()))
                self.assertEqual(metadata["allowed_tools"], methods[name]["allowed_tools"])
        self.assertEqual(plugin["docs/guides/replay-and-comparison.md"],
                         (SOURCE / "docs/guides/replay-and-comparison.md").read_bytes())
        self.assertEqual(validate_plugin(plugin, SOURCE), [])

    def test_no_replay_runtime_or_evaluation_answers_enter_workspace(self) -> None:
        for projection in (plan_workspace(SOURCE), plan_plugin(SOURCE)):
            self.assertFalse(any(p.endswith(".py") for p in projection))
            self.assertFalse(any(p.startswith("examples/") for p in projection))
        self.assertEqual({p for p in plan_workspace(SOURCE) if p.startswith("ai_docs/")},
                         {"ai_docs/initiatives/index.md"})

    def test_private_client_work_and_model_policy_survive_upgrade(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            prior = root / "prior"
            shutil.copytree(SOURCE, prior, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
            # An earlier complete source, not a malformed subset of the new method.
            prior_skill = prior / REPLAY
            prior_skill.write_text(prior_skill.read_text().replace(
                "# Replay work and compare execution choices", "# Earlier replay procedure"))
            target = client(root / "client")
            install(prior, target)
            state = target / "ai_docs"
            (state / "model-policy.md").write_text("Current model choice: unchanged.\n")
            history = state / "initiatives/private-research"
            history.mkdir()
            (history / "decision.md").write_text("Private prior decision.\n")
            (history / "candidate.md").write_text("Private current work.\n")
            before = snapshot(state)
            preview = upgrade(SOURCE, target, apply=False)
            self.assertEqual(preview["mode"], "dry-run")
            self.assertEqual(snapshot(state), before)
            upgrade(SOURCE, target, apply=True)
            self.assertEqual(snapshot(state), before)
            self.assertEqual(validate_workspace(target, SOURCE), [])
            self.assertIn(b"# Replay work and compare execution choices",
                          (target / ".agents/skills/kw-replay/SKILL.md").read_bytes())

    def test_collision_refuses_without_partial_or_private_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = client(Path(raw) / "client")
            p = target / ".agents/skills/kw-replay/SKILL.md"
            p.parent.mkdir(parents=True)
            p.write_text("# My own procedure\n")
            (target / "notes.md").write_text("Client material\n")
            before = snapshot(target)
            with self.assertRaises(IntegrityError):
                install(SOURCE, target)
            self.assertEqual(snapshot(target), before)

    def test_corrupt_replay_is_detected_and_upgrade_does_not_hide_it(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = client(Path(raw) / "client")
            install(SOURCE, target)
            p = target / ".agents/skills/kw-replay/SKILL.md"
            p.write_text("# Changed locally; do not overwrite this silently\n")
            before = snapshot(target)
            self.assertTrue(validate_workspace(target, SOURCE))
            with self.assertRaises(IntegrityError):
                upgrade(SOURCE, target, apply=True)
            self.assertEqual(snapshot(target), before)

    def test_missing_shared_dependency_prevents_a_partial_package(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "source"
            shutil.copytree(SOURCE, root, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
            (root / REFERENCE).unlink()
            self.assertTrue(validate_source(root))
            with self.assertRaises(IntegrityError):
                plan_plugin(root)

    def test_tampered_packaged_replay_fails_exact_validation(self) -> None:
        plugin = plan_plugin(SOURCE)
        plugin["skills/kw-replay/SKILL.md"] = plugin["skills/kw-replay/SKILL.md"].replace(
            b"do not change live work or model defaults", b"change live work and model defaults")
        self.assertTrue(validate_plugin(plugin, SOURCE))

    def test_versions_agree_and_developer_exercise_is_not_a_production_input(self) -> None:
        version = (SOURCE / ".knowledge-sdlc/VERSION").read_text().strip()
        self.assertEqual(json.loads((SOURCE / "package.json").read_text())["version"], version)
        self.assertEqual(json.loads((SOURCE / "package-lock.json").read_text())["version"], version)
        self.assertTrue((SOURCE / "examples/manual-exercises/journeys/continuity-and-replay.md").is_file())
        self.assertNotIn("examples/manual-exercises/journeys/continuity-and-replay.md", plan_plugin(SOURCE))


if __name__ == "__main__":
    unittest.main()
