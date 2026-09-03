from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from tooling.contracts import discover_methods, discover_recipes, source_inventory, validate_source


SOURCE = Path(__file__).resolve().parents[1]


def copy_method_source(destination: Path) -> Path:
    root = destination / "source"
    (root / ".knowledge-sdlc").mkdir(parents=True)
    for name in ("agents", "skills", "recipes", "templates"):
        shutil.copytree(SOURCE / ".knowledge-sdlc" / name, root / ".knowledge-sdlc" / name)
    shutil.copy2(SOURCE / ".knowledge-sdlc/VERSION", root / ".knowledge-sdlc/VERSION")
    shutil.copy2(SOURCE / "AGENTS.md", root / "AGENTS.md")
    return root


class ContractTests(unittest.TestCase):
    def test_actual_source_relations_close(self) -> None:
        self.assertEqual(validate_source(SOURCE), [])
        self.assertTrue(discover_methods(SOURCE))
        self.assertTrue(discover_recipes(SOURCE))

    def test_unknown_method_and_unsupported_output_are_detected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-contract-") as raw:
            root = copy_method_source(Path(raw))
            recipe = root / ".knowledge-sdlc/recipes/professional-research.md"
            text = recipe.read_text(encoding="utf-8")
            recipe.write_text(text.replace('"method":"thesis-challenger"', '"method":"missing-challenger"', 1), encoding="utf-8")
            defects = validate_source(root)
            self.assertTrue(any(item.code == "recipe-method-resolution" for item in defects))

            recipe.write_text(text.replace('"provides":["candidate-research"]', '"provides":["invented-output"]', 1), encoding="utf-8")
            defects = validate_source(root)
            self.assertTrue(any(item.code == "recipe-method-contract" for item in defects))

    def test_retired_model_selector_is_rejected_but_prose_is_not_semantically_linted(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-contract-") as raw:
            root = copy_method_source(Path(raw))
            skill = root / ".knowledge-sdlc/skills/kw-work-order/SKILL.md"
            before = source_inventory(root)
            text = skill.read_text(encoding="utf-8")
            skill.write_text(text.replace("primitive: skill\n", "primitive: skill\nmodel_profile: strongest\n", 1), encoding="utf-8")
            self.assertTrue(any(item.code == "retired-model-field" for item in validate_source(root)))

            skill.write_text(text + "\nA harmless explanatory sentence.\n", encoding="utf-8")
            self.assertEqual(validate_source(root), [])
            self.assertNotEqual(source_inventory(root), before)


if __name__ == "__main__":
    unittest.main()
