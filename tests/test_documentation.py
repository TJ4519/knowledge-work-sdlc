from __future__ import annotations

import re
import unittest
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1]
DOCS = [
    SOURCE / "README.md",
    SOURCE / "DESIGN.md",
    *sorted((SOURCE / "docs").rglob("*.md")),
    *sorted((SOURCE / "examples").rglob("*.md")),
]
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class DocumentationTests(unittest.TestCase):
    def test_relative_documentation_links_resolve(self) -> None:
        missing: list[str] = []
        for document in DOCS:
            for raw in LINK.findall(document.read_text(encoding="utf-8")):
                target = raw.split("#", 1)[0]
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                if not (document.parent / target).resolve().exists():
                    missing.append(f"{document.relative_to(SOURCE)} -> {raw}")
        self.assertEqual(missing, [])

    def test_reader_route_and_runtime_names_match_current_source(self) -> None:
        readme = (SOURCE / "README.md").read_text(encoding="utf-8")
        design = (SOURCE / "DESIGN.md").read_text(encoding="utf-8")
        agents = (SOURCE / "AGENTS.md").read_text(encoding="utf-8")
        for name in ("docs/methodology.md", "DESIGN.md", "docs/getting-started.md", "docs/guides"):
            self.assertIn(name, readme)
        self.assertIn("knowledge-work", agents)
        self.assertIn("kw-prime", agents)
        self.assertIn("kw-orchestration", agents)
        self.assertNotIn("kw-intake", readme + design + agents)
        self.assertNotIn("stages.json", readme + design + agents)
        self.assertNotIn("intents.json", readme + design + agents)

    def test_current_turn_provenance_cannot_be_inferred_from_delegation_lineage(self) -> None:
        entry = (SOURCE / ".knowledge-sdlc/skills/knowledge-work/SKILL.md").read_text()
        disposition = (SOURCE / ".knowledge-sdlc/skills/kw-candidate-disposition/SKILL.md").read_text()
        meaning = (SOURCE / ".knowledge-sdlc/templates/meaning.md").read_text()
        for text in (entry, disposition, meaning):
            self.assertIn("delegation", text)
            self.assertIn("current", text)
        self.assertIn("workspace-recorded", entry)


if __name__ == "__main__":
    unittest.main()
