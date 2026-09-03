from __future__ import annotations

import tempfile
import unittest
import zipfile
import json
from pathlib import Path

from tooling.projection import plan_plugin
from tooling.release import _archive_tree, _assert_version_consistency


SOURCE = Path(__file__).resolve().parents[1]


class PackagingTests(unittest.TestCase):
    def test_archive_is_deterministic_and_inventory_is_exact(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kw-archive-") as raw:
            base = Path(raw)
            source = base / "source"
            source.mkdir()
            (source / "b.txt").write_text("b\n", encoding="utf-8")
            (source / "a.txt").write_text("a\n", encoding="utf-8")
            one, two = base / "one.zip", base / "two.zip"
            self.assertEqual(_archive_tree(source, one), _archive_tree(source, two))
            self.assertEqual(one.read_bytes(), two.read_bytes())
            with zipfile.ZipFile(one) as archive:
                self.assertEqual(archive.namelist(), ["a.txt", "b.txt"])

    def test_release_version_must_match_every_packaged_identity(self) -> None:
        files = plan_plugin(SOURCE)
        version = (SOURCE / ".knowledge-sdlc/VERSION").read_text().strip()
        _assert_version_consistency(files, version)
        mutated = dict(files)
        manifest = json.loads(mutated[".codex-plugin/plugin.json"])
        manifest["version"] = "9.9.9"
        mutated[".codex-plugin/plugin.json"] = json.dumps(manifest).encode()
        with self.assertRaises(RuntimeError):
            _assert_version_consistency(mutated, version)


if __name__ == "__main__":
    unittest.main()
