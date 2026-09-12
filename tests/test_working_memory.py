"""Mechanical integration checks, not model-behaviour or benefit evaluations."""
from __future__ import annotations

import json
import posixpath
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
SKILL = ".knowledge-sdlc/skills/kw-recall/SKILL.md"
REFERENCE = ".knowledge-sdlc/references/working-memory.md"
PRODUCERS_AND_CONSUMERS = (
    "kw-orchestration", "evidence-explorer", "research-synthesis-producer",
    "protected-artifact-producer", "produce-evidence-bound-model-candidate",
    "verify-discriminating-buy-side-claims", "kw-reconciliation-control", "reconciler",
)


def source_copy(destination: Path) -> Path:
    root = destination / "source"
    shutil.copytree(SOURCE, root, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
    return root


def client_at(destination: Path) -> Path:
    destination.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=destination, check=True)
    return destination


def state_bytes(client: Path) -> dict[str, bytes]:
    return {str(p.relative_to(client)): p.read_bytes()
            for p in (client / "ai_docs").rglob("*") if p.is_file()}


class WorkingMemoryTests(unittest.TestCase):
    def test_recall_contract_and_existing_producers_resolve(self) -> None:
        self.assertEqual(validate_source(SOURCE), [])
        methods = discover_methods(SOURCE)
        recall = methods["kw-recall"]
        self.assertEqual(recall["kind"], "skill")
        self.assertFalse(recall["fresh_context"])
        self.assertEqual(recall["inputs"], ["meaning", "run-record"])
        self.assertEqual(recall["outputs"], [])
        self.assertEqual(set(recall["optional_outputs"]), {"evidence-map", "candidate-research"})
        self.assertNotIn("Task", recall["allowed_tools"])
        self.assertIn("unselected-reusable-lesson", recall["excluded_context"])
        for name in (*PRODUCERS_AND_CONSUMERS, "kw-recall"):
            with self.subTest(method=name):
                self.assertIn(REFERENCE, methods[name]["references"])

    def test_no_recipe_unconditionally_requires_recall(self) -> None:
        for recipe in discover_recipes(SOURCE).values():
            for step in recipe["composition"]:
                if step.get("method") == "kw-recall":
                    self.assertTrue(step.get("optional"))
                    self.assertTrue(step.get("trigger"))

    def test_current_recovery_keeps_exclusions(self) -> None:
        prime = discover_methods(SOURCE)["kw-prime"]
        self.assertTrue({"old-transcript", "superseded-artefacts",
                         "unrelated-initiative-content", "unselected-reusable-lesson"}
                        <= set(prime["excluded_context"]))
        # This is a routing-text contract check, not evidence that a model obeys it.
        self.assertIn("kw-recall", prime["body"])
        self.assertIn("previously pending production action", prime["body"])

    def test_shared_reference_and_skill_survive_both_projections(self) -> None:
        methods = discover_methods(SOURCE)
        workspace, plugin = plan_workspace(SOURCE), plan_plugin(SOURCE)
        expected = (SOURCE / REFERENCE).read_bytes()
        self.assertEqual(workspace[REFERENCE], expected)
        self.assertEqual(plugin["resources/" + REFERENCE], expected)
        self.assertEqual(validate_plugin(plugin, SOURCE), [])
        self.assertIn(".agents/skills/kw-recall/SKILL.md", workspace)
        self.assertIn("skills/kw-recall/SKILL.md", plugin)
        resolved = posixpath.normpath(posixpath.join(
            "skills/kw-recall", "../../resources/.knowledge-sdlc", "references/working-memory.md"))
        self.assertEqual(resolved, "resources/" + REFERENCE)
        with tempfile.TemporaryDirectory() as raw:
            projected = Path(raw) / "SKILL.md"
            projected.write_bytes(workspace[".agents/skills/kw-recall/SKILL.md"])
            metadata, body = parse_frontmatter(projected)
        self.assertEqual(body.strip(), methods["kw-recall"]["body"].strip())
        self.assertEqual(metadata["excluded_context"], methods["kw-recall"]["excluded_context"])
        for manifest in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
            self.assertEqual(json.loads(plugin[manifest])["name"], "knowledge-work-sdlc")
        self.assertIn("docs/guides/working-memory.md", plugin)

    def test_install_has_no_new_memory_authority_or_runtime(self) -> None:
        for projected in (plan_workspace(SOURCE), plan_plugin(SOURCE)):
            self.assertFalse(any(path.endswith(".py") for path in projected))
            self.assertFalse(any("semantic-working-memory" in path for path in projected))
        state = {p for p in plan_workspace(SOURCE) if p.startswith("ai_docs/")}
        self.assertEqual(state, {"ai_docs/initiatives/index.md"})

    def test_missing_and_linked_shared_reference_fail_validation(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = source_copy(Path(raw))
            ref = root / REFERENCE
            data = ref.read_bytes()
            ref.unlink()
            self.assertTrue(any(d.code == "method-reference-missing" for d in validate_source(root)))
            with self.assertRaises(IntegrityError):
                plan_plugin(root)
            external = Path(raw) / "external.md"
            external.write_bytes(data)
            ref.symlink_to(external)
            self.assertTrue(any(d.code == "reference-tree" for d in validate_source(root)))

    def test_changed_reference_invalidates_installed_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            client = client_at(Path(raw) / "client")
            install(SOURCE, client)
            self.assertEqual(validate_workspace(client, SOURCE), [])
            (client / REFERENCE).write_text("# Incorrect replacement\n")
            self.assertTrue(validate_workspace(client, SOURCE))

    def test_upgrade_and_removal_preserve_legacy_project_state(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            root = source_copy(base)
            client = client_at(base / "client")
            install(SOURCE, client)
            old = client / "ai_docs/initiatives/legacy"
            old.mkdir(parents=True)
            (old / "candidate-r1.md").write_text("# Legacy model\nQ1 actual: 80.\n")
            (old / "decision-r1.md").write_text("# Historical decision\nRationale not retained.\n")
            before = state_bytes(client)
            # A changed managed method updates without migrating client knowledge.
            ref = root / REFERENCE
            ref.write_text(ref.read_text() + "\nAdditional explanatory guidance.\n")
            upgrade(root, client, apply=True)
            self.assertEqual(state_bytes(client), before)
            self.assertEqual(validate_workspace(client, root), [])
            # Mechanical owned-file removal check only; it does not establish
            # that deleting a skill while retaining its callers is usable rollback.
            # Operational rollback restores the complete earlier method revision.
            shutil.rmtree(root / ".knowledge-sdlc/skills/kw-recall")
            upgrade(root, client, apply=True)
            self.assertFalse((client / ".agents/skills/kw-recall/SKILL.md").exists())
            self.assertEqual(state_bytes(client), before)
            self.assertEqual(validate_workspace(client, root), [])

    def test_new_skill_collision_does_not_overwrite_client_skill(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            client = client_at(Path(raw) / "client")
            path = client / ".agents/skills/kw-recall/SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text("# Client-owned existing skill\n")
            original = path.read_bytes()
            with self.assertRaises(IntegrityError):
                install(SOURCE, client)
            self.assertEqual(path.read_bytes(), original)
            self.assertFalse((client / ".knowledge-sdlc/install.json").exists())

    def test_exercise_is_staged_and_not_packaged_into_production(self) -> None:
        fixture = SOURCE / "examples/manual-exercises/fixtures/semantic-working-memory"
        self.assertEqual({p.name for p in fixture.iterdir()},
                         {"stage-1", "stage-2", "stage-3", "stage-4"})
        self.assertTrue((fixture / "stage-1/source.md").is_file())
        self.assertTrue((fixture / "stage-2/source.md").is_file())
        self.assertTrue((fixture / "stage-3/request.md").is_file())
        self.assertTrue((fixture / "stage-4/questions.md").is_file())
        self.assertNotIn("Review notes", (fixture / "stage-1/request.md").read_text())
        self.assertFalse(any("semantic-working-memory" in p for p in plan_workspace(SOURCE)))


if __name__ == "__main__":
    unittest.main()
