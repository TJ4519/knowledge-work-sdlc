from __future__ import annotations

import json
import hashlib
import os
import posixpath
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tooling.contracts import discover_methods
from tooling.projection import BEGIN, END, plan_plugin, plan_workspace, validate_plugin, validate_plugin_plan, validate_workspace, validate_workspace_plan
from tooling.util import parse_frontmatter


SOURCE = Path(__file__).resolve().parents[1]


class DistributionTests(unittest.TestCase):
    def test_workspace_and_plugin_projection_are_stable_across_processes(self) -> None:
        script = """
import hashlib
import json
from pathlib import Path
from tooling.projection import plan_plugin, plan_workspace

root = Path.cwd()

def digest(files):
    value = hashlib.sha256()
    for path, content in sorted(files.items()):
        value.update(path.encode("utf-8"))
        value.update(b"\\0")
        value.update(content)
        value.update(b"\\0")
    return value.hexdigest()

print(json.dumps([digest(plan_workspace(root)), digest(plan_plugin(root))]))
"""
        results = []
        for seed in ("1", "2", "3", "4"):
            environment = dict(os.environ, PYTHONHASHSEED=seed)
            completed = subprocess.run(
                [sys.executable, "-c", script],
                cwd=SOURCE,
                env=environment,
                text=True,
                capture_output=True,
                check=True,
            )
            results.append(json.loads(completed.stdout))
        self.assertEqual(results, [results[0]] * len(results))

    def test_workspace_has_one_runtime_skill_corpus_and_only_earned_spine(self) -> None:
        methods = discover_methods(SOURCE)
        files = plan_workspace(SOURCE)
        validate_workspace_plan(files, methods)
        self.assertFalse(any(path.startswith(".knowledge-sdlc/skills/") for path in files))
        expected = {name for name, item in methods.items() if item["kind"] == "skill"}
        actual = {Path(path).parent.name for path in files if path.startswith(".agents/skills/")}
        self.assertEqual(actual, expected)
        self.assertIn("ai_docs/initiatives/index.md", files)
        self.assertNotIn("ai_docs/domain-charter.md", files)
        self.assertNotIn("ai_docs/LEARNINGS.md", files)
        self.assertNotIn("ai_docs/methods/README.md", files)
        self.assertFalse(any(path.endswith(".py") for path in files))
        projected = files[".agents/skills/kw-orchestration/SKILL.md"]
        with tempfile.TemporaryDirectory(prefix="kw-frontmatter-") as raw:
            path = Path(raw) / "SKILL.md"
            path.write_bytes(projected)
            metadata, body = parse_frontmatter(path)
        canonical = methods["kw-orchestration"]
        self.assertEqual(body.strip(), canonical["body"].strip())
        for field in ("inputs", "outputs", "allowed_tools", "excluded_context", "independence", "authority"):
            self.assertEqual(metadata[field], canonical[field])

    def test_plugin_projection_is_complete_but_not_provider_execution(self) -> None:
        files = plan_plugin(SOURCE)
        methods = discover_methods(SOURCE)
        from tooling.contracts import discover_recipes

        validate_plugin_plan(files, methods, discover_recipes(SOURCE))
        codex_manifest = json.loads(files[".codex-plugin/plugin.json"])
        self.assertEqual(codex_manifest["name"], "knowledge-work-sdlc")
        self.assertTrue(codex_manifest["interface"]["longDescription"])
        self.assertEqual(len(codex_manifest["interface"]["defaultPrompt"]), 3)
        self.assertEqual(json.loads(files[".claude-plugin/plugin.json"])["name"], "knowledge-work-sdlc")
        self.assertIn("skills/knowledge-work/SKILL.md", files)
        self.assertIn("agents/kw-thesis-challenger.md", files)
        self.assertIn("resources/.knowledge-sdlc/recipes/professional-research.md", files)
        self.assertIn("README.md", files)
        self.assertIn("DESIGN.md", files)
        self.assertIn("LICENSE.md", files)
        self.assertIn("docs/getting-started.md", files)
        self.assertNotIn("docs/guides/maintaining-the-harness.md", files)
        self.assertNotIn("docs/plugin-package.md", files)
        self.assertFalse(any(path.startswith("examples/") for path in files))
        self.assertFalse(any(path.startswith("hooks/") for path in files))
        self.assertFalse(any(path.startswith("scripts/") for path in files))
        self.assertFalse(any(path.endswith(".py") for path in files))
        self.assertIn(
            b"../../resources/.knowledge-sdlc/",
            files["skills/knowledge-work/SKILL.md"],
        )
        self.assertIn(
            b"If the index is absent and no initiative content exists",
            files["skills/knowledge-work/SKILL.md"],
        )
        with tempfile.TemporaryDirectory(prefix="kw-agent-frontmatter-") as raw:
            path = Path(raw) / "agent.md"
            path.write_bytes(files["agents/kw-thesis-challenger.md"])
            metadata, _ = parse_frontmatter(path)
        self.assertEqual(metadata["canonical_name"], "thesis-challenger")
        self.assertEqual(metadata["inputs"], methods["thesis-challenger"]["inputs"])
        self.assertEqual(metadata["authority"], methods["thesis-challenger"]["authority"])
        self.assertEqual(
            metadata["tools"],
            ["Read", "Grep", "Bash", "WebSearch", "WebFetch", "Write"],
        )
        self.assertNotIn("Agent", metadata["tools"])
        self.assertEqual(validate_plugin(files, SOURCE), [])

        # Canonical body preservation is checked independently of the plan
        # validator, which otherwise compares a projection with itself.
        workspace = plan_workspace(SOURCE)
        for name, method in methods.items():
            if method["kind"] != "skill":
                continue
            with tempfile.TemporaryDirectory(prefix="kw-body-projection-") as raw:
                native = Path(raw) / "SKILL.md"
                native.write_bytes(workspace[f".agents/skills/{name}/SKILL.md"])
                _, body = parse_frontmatter(native)
                self.assertEqual(body.strip(), method["body"].strip(), name)
                native.write_bytes(files[f"skills/{name}/SKILL.md"])
                _, body = parse_frontmatter(native)
                self.assertTrue(body.rstrip().endswith(method["body"].rstrip()), name)
                self.assertEqual(body.count(method["body"].strip()), 1, name)

        link = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        missing_links: list[str] = []
        for source, content in files.items():
            if not source.endswith(".md"):
                continue
            for raw in link.findall(content.decode("utf-8")):
                target = raw.split("#", 1)[0]
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                resolved = posixpath.normpath(
                    posixpath.join(posixpath.dirname(source), target)
                )
                if resolved not in files:
                    missing_links.append(f"{source} -> {raw}")
        self.assertEqual(missing_links, [])

        mutated = dict(files)
        mutated["skills/knowledge-work/SKILL.md"] += b"\nmutation\n"
        self.assertTrue(any("bytes differ" in item for item in validate_plugin(mutated, SOURCE)))

    def test_workspace_validation_allows_an_ambient_runtime_skill(self) -> None:
        from tooling.installer import install

        with tempfile.TemporaryDirectory(prefix="kw-workspace-validation-") as raw:
            target = Path(raw) / "workspace"
            target.mkdir()
            subprocess.run(
                ["git", "init", "-q", "-b", "main"], cwd=target, check=True
            )
            ambient = target / ".agents/skills/client-method/SKILL.md"
            ambient.parent.mkdir(parents=True)
            content = b"# Client-owned method\n"
            ambient.write_bytes(content)
            install(SOURCE, target)
            self.assertEqual(validate_workspace(target, SOURCE), [])
            self.assertEqual(ambient.read_bytes(), content)

    def test_plugin_validation_rejects_an_unexpected_projection_path(self) -> None:
        files = plan_plugin(SOURCE)
        files["rogue.txt"] = b"ambient instruction\n"
        defects = validate_plugin(files, SOURCE)
        self.assertTrue(any("paths unexpected" in item for item in defects))

    def test_exact_validators_reject_self_consistent_but_noncanonical_objects(self) -> None:
        fake_plugin = {
            ".codex-plugin/plugin.json": b'{"name":"knowledge-work-sdlc"}',
            ".claude-plugin/plugin.json": b'{"name":"knowledge-work-sdlc"}',
            "resources/.knowledge-sdlc/VERSION": b"fake\n",
        }
        self.assertTrue(validate_plugin(fake_plugin, SOURCE))

        with tempfile.TemporaryDirectory(prefix="kw-fake-workspace-") as raw:
            target = Path(raw)
            block = f"{BEGIN}\nfake\n{END}\n".encode()
            (target / "AGENTS.md").write_bytes(block)
            (target / ".knowledge-sdlc").mkdir()
            (target / ".knowledge-sdlc/install.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "owned_files": {},
                        "managed_agents_block_sha256": hashlib.sha256(
                            block
                        ).hexdigest(),
                    }
                ),
                encoding="utf-8",
            )
            index = target / "ai_docs/initiatives/index.md"
            index.parent.mkdir(parents=True, exist_ok=True)
            index.write_text("# Initiative index\n", encoding="utf-8")
            defects = validate_workspace(target, SOURCE)
            self.assertTrue(
                any("canonical source projection" in item for item in defects),
                defects,
            )

    def test_projection_changes_when_the_canonical_method_changes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-projection-") as raw:
            root = Path(raw) / "source"
            import shutil

            shutil.copytree(SOURCE, root, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__", ".pytest_cache"))
            before = plan_workspace(root)[".agents/skills/kw-work-order/SKILL.md"]
            canonical = root / ".knowledge-sdlc/skills/kw-work-order/SKILL.md"
            canonical.write_text(canonical.read_text(encoding="utf-8") + "\nProjection sentinel.\n", encoding="utf-8")
            after = plan_workspace(root)[".agents/skills/kw-work-order/SKILL.md"]
            self.assertNotEqual(before, after)
            self.assertIn(b"Projection sentinel", after)


if __name__ == "__main__":
    unittest.main()
