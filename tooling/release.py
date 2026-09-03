from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from .contracts import validate_source
from .projection import plan_plugin, validate_plugin
from .util import sha256_bytes, sha256_file


def _git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()


def _archive_tree(source: Path, archive: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        archive,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as bundle:
        for path in sorted(source.rglob("*")):
            if path.is_symlink():
                raise RuntimeError(f"release package contains a symlink: {path}")
            if not path.is_file():
                continue
            relative = path.relative_to(source).as_posix()
            data = path.read_bytes()
            info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, data)
            files[relative] = sha256_bytes(data)
    return files


def _plugin(staging: Path, name: str, files: dict[str, bytes]) -> Path:
    plugin = staging / name
    for relative, content in files.items():
        path = plugin / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    return plugin


def _assert_version_consistency(files: dict[str, bytes], version: str) -> None:
    observed = {
        "Codex manifest": str(json.loads(files[".codex-plugin/plugin.json"])["version"]),
        "Claude manifest": str(json.loads(files[".claude-plugin/plugin.json"])["version"]),
        "bundled VERSION": files["resources/.knowledge-sdlc/VERSION"]
        .decode("utf-8")
        .strip(),
    }
    mismatches = {
        name: value for name, value in observed.items() if value != version
    }
    if mismatches:
        raise RuntimeError(
            f"release version {version!r} disagrees with package identities: {mismatches}"
        )


def build_release(root: Path, output_dir: Path) -> dict[str, Any]:
    root = root.resolve()
    output_dir = (
        output_dir.resolve()
        if output_dir.is_absolute()
        else (root / output_dir).resolve()
    )
    status = _git(root, "status", "--porcelain", "--untracked-files=all")
    if status:
        raise RuntimeError("release requires a clean committed working tree")

    version = (root / ".knowledge-sdlc" / "VERSION").read_text(
        encoding="utf-8"
    ).strip()
    commit = _git(root, "rev-parse", "HEAD")
    output_dir.parent.mkdir(parents=True, exist_ok=True)

    archive_name = f"knowledge-work-sdlc-harness-v{version}.zip"
    manifest_name = f"knowledge-work-sdlc-v{version}-MANIFEST.json"

    with tempfile.TemporaryDirectory(
        prefix=".knowledge-work-sdlc-release-", dir=output_dir.parent
    ) as raw:
        staging = Path(raw)
        defects = validate_source(root)
        if defects:
            raise RuntimeError(
                "release source contracts fail: "
                + "; ".join(item.message for item in defects[:8])
            )
        plugin_files = plan_plugin(root)
        plugin_defects = validate_plugin(plugin_files, root)
        if plugin_defects:
            raise RuntimeError(
                "release plugin projection fails: " + "; ".join(plugin_defects[:8])
            )
        _assert_version_consistency(plugin_files, version)
        package_roots = {
            "harness": _plugin(
                staging, "harness", plugin_files
            )
        }

        packages: dict[str, dict[str, Any]] = {}
        for name, package_root in package_roots.items():
            archive = staging / archive_name
            inventory = _archive_tree(package_root, archive)
            packages[name] = {
                "archive": archive.name,
                "sha256": sha256_file(archive),
                "file_count": len(inventory),
                "files": inventory,
            }

        manifest = {
            "schema_version": 1,
            "version": version,
            "source_commit": commit,
            "packages": packages,
        }
        manifest_path = staging / manifest_name
        manifest_path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        output_dir.mkdir(parents=True, exist_ok=True)
        os.replace(staging / archive_name, output_dir / archive_name)
        os.replace(manifest_path, output_dir / manifest_name)

    return {
        **manifest,
        "manifest_path": str(output_dir / manifest_name),
        "package_paths": {
            name: str(output_dir / details["archive"])
            for name, details in packages.items()
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build deterministic consumer archives from a clean committed source tree."
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--output-dir", default="dist")
    args = parser.parse_args()
    result = build_release(Path(args.root), Path(args.output_dir))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
