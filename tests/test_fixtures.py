from __future__ import annotations

import unittest
import zipfile
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1]
FIXTURE = SOURCE / "examples/manual-exercises/fixtures/expert-method-and-protected-work/Acorn-operating-model-variant.xlsx"


class FixtureTests(unittest.TestCase):
    def test_workbook_variant_contains_features_that_a_candidate_must_preserve(self) -> None:
        with zipfile.ZipFile(FIXTURE) as archive:
            names = set(archive.namelist())
            workbook = archive.read("xl/workbook.xml").decode("utf-8")
            sheets = "".join(
                archive.read(name).decode("utf-8")
                for name in names
                if name.startswith("xl/worksheets/sheet") and name.endswith(".xml")
            )
            self.assertIn("Variant Model", workbook)
            self.assertIn("Audit &amp; Sources", workbook)
            self.assertIn("dataValidations", sheets)
            self.assertIn("'Audit &amp; Sources'!$C$5", sheets)
            self.assertTrue(any(name.startswith("xl/tables/table") for name in names))
            self.assertTrue(any("comments" in name for name in names))


if __name__ == "__main__":
    unittest.main()
