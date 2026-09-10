from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path
from typing import Any

from .errors import IntegrityError
from .projection import BEGIN, END, managed_agents_block, plan_workspace, validate_workspace
from .util import sha256_bytes, sha256_file


RECOVERY = ".knowledge-sdlc/UPGRADE_RECOVERY.json"


def _regular_bytes(path: Path, label: str) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise IntegrityError(f"{label} is not a regular file: {path}")
    return path.read_bytes()


def _target_path(raw: Path) -> Path:
    expanded = raw.expanduser()
    if expanded.is_symlink() or not expanded.is_dir():
        raise IntegrityError("installation target must be an existing real directory")
    target = expanded.resolve()
    git_marker = target / ".git"
    if git_marker.is_symlink() or not (
        git_marker.is_dir() or git_marker.is_file()
    ):
        raise IntegrityError("installation target must be a Git repository root")
    try:
        completed = subprocess.run(
            ["git", "-C", str(target), "rev-parse", "--show-toplevel"],
            text=True,
            capture_output=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise IntegrityError("installation target must be a Git repository root") from exc
    if Path(completed.stdout.strip()).resolve() != target:
        raise IntegrityError("installation target must be the Git repository root")
    return target


def _safe_relative(relative: str) -> None:
    path = Path(relative)
    if not relative or path.is_absolute() or ".." in path.parts:
        raise IntegrityError(f"unsafe installation path: {relative}")


def _assert_parent_chain(target: Path, relative: str) -> None:
    _safe_relative(relative)
    if target.is_symlink() or (target.exists() and not target.is_dir()):
        raise IntegrityError("installation target was replaced or is unsafe")
    current = target
    for part in Path(relative).parts[:-1]:
        current = current / part
        if current.is_symlink():
            raise IntegrityError(f"installation path crosses a symlink: {relative}")
        if current.exists() and not current.is_dir():
            raise IntegrityError(f"installation path crosses a non-directory: {relative}")


def _write_stage(stage: Path, files: dict[str, bytes]) -> None:
    for relative, content in sorted(files.items()):
        destination = stage / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as handle:
            handle.write(content)


def _snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha256_file(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }


def _validate_stage(stage: Path, planned: dict[str, bytes]) -> None:
    expected = {path: sha256_bytes(content) for path, content in planned.items()}
    actual = _snapshot(stage)
    if actual != expected:
        raise IntegrityError("staged installation differs from the complete plan")


def _create_parents(target: Path, paths: set[str]) -> list[Path]:
    created: list[Path] = []
    for relative in sorted(paths, key=lambda item: (len(Path(item).parts), item)):
        parent = (target / relative).parent
        missing: list[Path] = []
        cursor = parent
        while cursor != target and not cursor.exists():
            missing.append(cursor)
            cursor = cursor.parent
        if cursor.is_symlink() or not cursor.is_dir():
            raise IntegrityError(f"unsafe installation parent: {parent}")
        for directory in reversed(missing):
            directory.mkdir()
            created.append(directory)
    return created


def _fresh_preflight(target: Path, planned: dict[str, bytes]) -> None:
    if (target / RECOVERY).exists() or (target / RECOVERY).is_symlink():
        raise IntegrityError("an interrupted upgrade requires --recover")
    for relative in planned:
        _assert_parent_chain(target, relative)
        destination = target / relative
        if destination.is_symlink():
            raise IntegrityError(f"installation destination is a symlink: {relative}")
        if destination.exists() and relative != "AGENTS.md":
            raise IntegrityError(f"installation collision: {relative}")
        if relative == "AGENTS.md" and destination.exists() and not destination.is_file():
            raise IntegrityError("existing AGENTS.md is not a regular file")


def _validate_committed_plan(target: Path, planned: dict[str, bytes]) -> None:
    for relative, expected in planned.items():
        _assert_parent_chain(target, relative)
        path = target / relative
        if (
            path.is_symlink()
            or not path.is_file()
            or sha256_file(path) != sha256_bytes(expected)
        ):
            raise IntegrityError(
                f"committed installation escaped or differs from plan: {relative}"
            )


def _commit_fresh(
    target: Path,
    stage: Path,
    planned: dict[str, bytes],
    existing_agents: bytes | None,
    source_root: Path,
) -> None:
    created_root = False
    created_dirs: list[Path] = []
    created_files: list[Path] = []
    agents = target / "AGENTS.md"
    agents_existed = existing_agents is not None
    backup = stage.parent / "AGENTS.original"
    agents_captured = False
    agents_installed = False
    rollback_errors: list[str] = []
    try:
        if not target.exists():
            target.mkdir()
            created_root = True
        created_dirs = _create_parents(target, set(planned))
        for relative in sorted(path for path in planned if path != "AGENTS.md"):
            _assert_parent_chain(target, relative)
            destination = target / relative
            if destination.exists() or destination.is_symlink():
                raise IntegrityError(f"installation target changed after preflight: {relative}")
            os.link(stage / relative, destination)
            created_files.append(destination)
        if agents_existed:
            _assert_parent_chain(target, "AGENTS.md")
            if agents.is_symlink() or not agents.is_file():
                raise IntegrityError("AGENTS.md changed after preflight")
            os.replace(agents, backup)
            agents_captured = True
            if backup.read_bytes() != existing_agents:
                os.replace(backup, agents)
                agents_captured = False
                raise IntegrityError("AGENTS.md changed after planning")
            os.link(stage / "AGENTS.md", agents)
            agents_installed = True
        else:
            os.link(stage / "AGENTS.md", agents)
            created_files.append(agents)
        _validate_committed_plan(target, planned)
        defects = validate_workspace(target, source_root)
        if defects:
            raise IntegrityError(
                "installed workspace failed canonical validation: "
                + "; ".join(defects[:8])
            )
    except Exception as exc:
        if agents_installed:
            try:
                _assert_parent_chain(target, "AGENTS.md")
                if (
                    agents.is_file()
                    and not agents.is_symlink()
                    and sha256_file(agents) == sha256_bytes(planned["AGENTS.md"])
                ):
                    agents.unlink()
                else:
                    rollback_errors.append(
                        "AGENTS.md changed during rollback; original retained separately"
                    )
            except Exception as rollback_exc:
                rollback_errors.append(f"AGENTS.md: {rollback_exc}")
        if agents_captured and backup.exists():
            try:
                if agents.exists() or agents.is_symlink():
                    recovery = target / "AGENTS.md.pre-install-recovery"
                    if recovery.exists() or recovery.is_symlink():
                        raise IntegrityError(
                            "both AGENTS.md and AGENTS.md.pre-install-recovery are occupied"
                        )
                    os.link(backup, recovery)
                    rollback_errors.append(
                        "concurrent AGENTS.md preserved; original is AGENTS.md.pre-install-recovery"
                    )
                else:
                    os.replace(backup, agents)
                    agents_captured = False
            except Exception as rollback_exc:
                rollback_errors.append(f"AGENTS.md original: {rollback_exc}")
        for path in reversed(created_files):
            try:
                path.unlink(missing_ok=True)
            except Exception as rollback_exc:
                rollback_errors.append(f"{path}: {rollback_exc}")
        for directory in reversed(created_dirs):
            try:
                if directory.is_symlink():
                    directory.unlink()
                else:
                    directory.rmdir()
            except Exception:
                pass
        if created_root:
            try:
                target.rmdir()
            except Exception:
                pass
        if rollback_errors:
            raise IntegrityError("install failed and rollback was incomplete: " + "; ".join(rollback_errors)) from exc
        raise IntegrityError(f"install failed; target restored: {exc}") from exc
    finally:
        if not rollback_errors:
            backup.unlink(missing_ok=True)


def install(source_root: Path, target_root: Path) -> dict[str, Any]:
    source_root = source_root.resolve()
    target = _target_path(target_root)
    existing = _regular_bytes(target / "AGENTS.md", "existing AGENTS.md") if (target / "AGENTS.md").exists() else None
    planned = plan_workspace(source_root, existing)
    _fresh_preflight(target, planned)
    stage_container = Path(tempfile.mkdtemp(prefix=f".{target.name}.knowledge-sdlc-", dir=target.parent))
    stage = stage_container / "payload"
    try:
        stage.mkdir()
        _write_stage(stage, planned)
        _validate_stage(stage, planned)
        _commit_fresh(target, stage, planned, existing, source_root)
    finally:
        shutil.rmtree(stage_container, ignore_errors=True)
    return {
        "operation": "install",
        "target": str(target),
        "installed_files": sorted(planned),
        "installed_file_count": len(planned),
        "validation_passed": True,
    }


def preview_install(source_root: Path, target_root: Path) -> dict[str, Any]:
    """Plan and validate a fresh install without changing the target."""

    source_root = source_root.resolve()
    target = _target_path(target_root)
    agents_path = target / "AGENTS.md"
    existing = (
        _regular_bytes(agents_path, "existing AGENTS.md")
        if agents_path.exists()
        else None
    )
    planned = plan_workspace(source_root, existing)
    _fresh_preflight(target, planned)
    block = managed_agents_block(source_root)
    return {
        "operation": "install",
        "mode": "dry-run",
        "target": str(target),
        "existing_agents_md": existing is not None,
        "existing_agents_sha256": (
            sha256_bytes(existing) if existing is not None else None
        ),
        "agents_action": (
            "append-managed-block" if existing is not None else "create"
        ),
        "managed_agents_block_sha256": sha256_bytes(block),
        "planned_files": sorted(planned),
        "planned_file_count": len(planned),
        "semantic_review_required": True,
        "writes_performed": False,
        "preflight_passed": True,
    }


def _block_slice(data: bytes) -> tuple[int, int, bytes]:
    begin, end = BEGIN.encode(), END.encode()
    if data.count(begin) != 1 or data.count(end) != 1:
        raise IntegrityError("managed AGENTS.md block is missing or ambiguous")
    start = data.index(begin)
    finish = data.index(end, start) + len(end)
    if finish < len(data) and data[finish : finish + 1] == b"\n":
        finish += 1
    return start, finish, data[start:finish]


def _load_install_record(target: Path) -> dict[str, Any]:
    path = target / ".knowledge-sdlc/install.json"
    if path.is_symlink() or not path.is_file():
        raise IntegrityError("upgrade requires a recognised install.json; legacy migration is separate")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1 or not isinstance(payload.get("owned_files"), dict):
        raise IntegrityError("unrecognised install.json")
    return payload


def _verify_owned(target: Path, record: dict[str, Any]) -> None:
    for relative, expected in record["owned_files"].items():
        _assert_parent_chain(target, relative)
        path = target / relative
        if path.is_symlink() or not path.is_file() or sha256_file(path) != expected:
            raise IntegrityError(f"managed file was edited or replaced: {relative}")
    agents = _regular_bytes(target / "AGENTS.md", "managed AGENTS.md")
    _, _, block = _block_slice(agents)
    if sha256_bytes(block) != record.get("managed_agents_block_sha256"):
        raise IntegrityError("managed AGENTS.md block was edited")


def _upgrade_plan(source: Path, target: Path, record: dict[str, Any]) -> tuple[dict[str, bytes], set[str]]:
    existing_agents = _regular_bytes(target / "AGENTS.md", "managed AGENTS.md")
    start, end, _ = _block_slice(existing_agents)
    fresh = plan_workspace(source, None)
    new_block = fresh["AGENTS.md"]
    fresh["AGENTS.md"] = existing_agents[:start] + new_block + existing_agents[end:]
    for path in list(fresh):
        if path.startswith("ai_docs/"):
            del fresh[path]
    old_owned = set(record["owned_files"]) | {".knowledge-sdlc/install.json", "AGENTS.md"}
    for relative in fresh:
        _assert_parent_chain(target, relative)
        destination = target / relative
        if relative not in old_owned and (destination.exists() or destination.is_symlink()):
            raise IntegrityError(f"new managed path collides with client content: {relative}")
    return fresh, old_owned - set(fresh)


def _write_marker(target: Path, payload: dict[str, Any]) -> None:
    marker = target / RECOVERY
    marker.parent.mkdir(parents=True, exist_ok=True)
    temporary = marker.with_name(marker.name + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, marker)


def recover_upgrade(source_root: Path, target_root: Path) -> dict[str, Any]:
    source_root = source_root.resolve()
    target = _target_path(target_root)
    marker = target / RECOVERY
    if marker.is_symlink() or not marker.is_file():
        raise IntegrityError("no recoverable upgrade marker exists")
    payload = json.loads(marker.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise IntegrityError("upgrade marker schema is not recognised")
    backup_relative = payload.get("backup")
    if not isinstance(backup_relative, str) or not re.fullmatch(
        r"\.knowledge-sdlc/\.upgrade-backup-[0-9a-f]{32}", backup_relative
    ):
        raise IntegrityError("upgrade marker names an invalid backup")
    _assert_parent_chain(target, f"{backup_relative}/payload")
    backup = target / backup_relative
    try:
        backup.resolve().relative_to(target.resolve())
    except ValueError as exc:
        raise IntegrityError("upgrade backup escapes the target") from exc
    if backup.is_symlink() or not backup.is_dir():
        raise IntegrityError("upgrade backup is missing or unsafe")

    old_hashes = payload.get("old_hashes")
    new_hashes = payload.get("new_hashes")
    if not isinstance(old_hashes, dict) or not isinstance(new_hashes, dict):
        raise IntegrityError("upgrade marker hash inventories are invalid")
    entries = list(old_hashes.items()) + list(new_hashes.items())
    if any(
        not isinstance(path, str)
        or not isinstance(digest, str)
        or not re.fullmatch(r"[0-9a-f]{64}", digest)
        for path, digest in entries
    ):
        raise IntegrityError("upgrade marker contains invalid path/hash entries")
    for relative in list(old_hashes) + list(new_hashes):
        _safe_relative(relative)

    backup_record_path = backup / ".knowledge-sdlc/install.json"
    if backup_record_path.is_symlink() or not backup_record_path.is_file():
        raise IntegrityError("upgrade backup lacks the prior ownership record")
    backup_record = json.loads(backup_record_path.read_text(encoding="utf-8"))
    expected_old = set(backup_record.get("owned_files", {})) | {
        ".knowledge-sdlc/install.json",
        "AGENTS.md",
    }
    if set(old_hashes) != expected_old:
        raise IntegrityError("upgrade marker old paths do not match prior ownership")
    for relative, expected_hash in old_hashes.items():
        _assert_parent_chain(backup, relative)
        backup_file = backup / relative
        if (
            backup_file.is_symlink()
            or not backup_file.is_file()
            or sha256_file(backup_file) != expected_hash
        ):
            raise IntegrityError(f"upgrade backup is incomplete or changed: {relative}")

    expected_plan = plan_workspace(source_root, None)
    prior_agents = (backup / "AGENTS.md").read_bytes()
    start, end, _ = _block_slice(prior_agents)
    expected_plan["AGENTS.md"] = (
        prior_agents[:start] + expected_plan["AGENTS.md"] + prior_agents[end:]
    )
    for relative in list(expected_plan):
        if relative.startswith("ai_docs/"):
            del expected_plan[relative]
    expected_new_hashes = {
        relative: sha256_bytes(content) for relative, content in expected_plan.items()
    }
    if new_hashes != expected_new_hashes:
        raise IntegrityError("upgrade marker new paths do not match canonical source projection")

    preserved_new = sorted(
        relative
        for relative in set(new_hashes) - set(old_hashes)
        if (target / relative).exists() or (target / relative).is_symlink()
    )
    for relative in sorted(old_hashes):
        _assert_parent_chain(target, relative)
        source = backup / relative
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(destination.name + ".recovery-tmp")
        shutil.copy2(source, temporary)
        os.replace(temporary, destination)
    _verify_owned(target, backup_record)
    if preserved_new:
        raise IntegrityError(
            "prior owned bytes were restored, but previously unowned paths were preserved for manual inspection: "
            + ", ".join(preserved_new)
        )
    marker.unlink()
    shutil.rmtree(backup, ignore_errors=True)
    return {"operation": "recover", "target": str(target), "restored": True}


def upgrade(source_root: Path, target_root: Path, *, apply: bool) -> dict[str, Any]:
    source = source_root.resolve()
    target = _target_path(target_root)
    if (target / RECOVERY).exists() or (target / RECOVERY).is_symlink():
        raise IntegrityError("an interrupted upgrade requires --recover")
    record = _load_install_record(target)
    _verify_owned(target, record)
    planned, removed = _upgrade_plan(source, target, record)
    changes = sorted(set(planned) | removed)
    result = {
        "operation": "upgrade",
        "mode": "apply" if apply else "dry-run",
        "target": str(target),
        "from_version": record.get("version"),
        "to_version": (source / ".knowledge-sdlc/VERSION").read_text(encoding="utf-8").strip(),
        "changed_or_checked_paths": changes,
    }
    if not apply:
        return result

    stage_container = Path(tempfile.mkdtemp(prefix=f".{target.name}.knowledge-sdlc-upgrade-", dir=target.parent))
    stage = stage_container / "payload"
    backup_rel = f".knowledge-sdlc/.upgrade-backup-{uuid.uuid4().hex}"
    backup = target / backup_rel
    old_paths = sorted((set(record["owned_files"]) | {".knowledge-sdlc/install.json", "AGENTS.md"}))
    old_owned = set(old_paths)
    old_hashes = {relative: sha256_file(target / relative) for relative in old_paths}
    new_hashes = {relative: sha256_bytes(content) for relative, content in planned.items()}
    created_new: list[str] = []
    try:
        stage.mkdir()
        _write_stage(stage, planned)
        _validate_stage(stage, planned)
        backup.mkdir(parents=True)
        for relative in old_paths:
            source_path = target / relative
            if source_path.is_file() and not source_path.is_symlink():
                destination = backup / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_path, destination)
        _write_marker(
            target,
            {
                "schema_version": 1,
                "backup": backup_rel,
                "old_hashes": dict(sorted(old_hashes.items())),
                "new_hashes": dict(sorted(new_hashes.items())),
            },
        )
        _create_parents(target, set(planned))
        for relative, expected_bytes in sorted(planned.items()):
            _assert_parent_chain(target, relative)
            destination = target / relative
            if destination.is_symlink():
                raise IntegrityError(f"upgrade destination became a symlink: {relative}")
            if relative not in old_owned:
                if destination.exists():
                    raise IntegrityError(
                        f"new managed path appeared after preflight: {relative}"
                    )
                os.link(stage / relative, destination)
                created_new.append(relative)
            else:
                if (
                    not destination.is_file()
                    or sha256_file(destination) != old_hashes[relative]
                ):
                    raise IntegrityError(
                        f"managed path changed after preflight: {relative}"
                    )
                os.replace(stage / relative, destination)
        for relative in sorted(removed, reverse=True):
            path = target / relative
            if (
                path.is_file()
                and not path.is_symlink()
                and sha256_file(path) == old_hashes[relative]
            ):
                path.unlink()
        new_record = _load_install_record(target)
        _verify_owned(target, new_record)
        (target / RECOVERY).unlink()
        shutil.rmtree(backup, ignore_errors=True)
    except Exception as exc:
        for relative in reversed(created_new):
            path = target / relative
            try:
                _assert_parent_chain(target, relative)
                if (
                    path.is_file()
                    and not path.is_symlink()
                    and sha256_file(path) == new_hashes[relative]
                ):
                    path.unlink()
            except IntegrityError:
                pass
        try:
            recover_upgrade(source, target)
        except Exception as recovery_exc:
            raise IntegrityError(f"upgrade failed and requires manual recovery: {recovery_exc}") from exc
        raise IntegrityError(f"upgrade failed; prior managed bytes restored: {exc}") from exc
    finally:
        shutil.rmtree(stage_container, ignore_errors=True)
    result["validation_passed"] = True
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install or upgrade the repository-local Knowledge Work lifecycle.",
        allow_abbrev=False,
    )
    parser.add_argument("--source-root", default=".")
    parser.add_argument("--upgrade", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--recover", action="store_true")
    parser.add_argument("target")
    args = parser.parse_args()
    if args.recover and (args.upgrade or args.apply or args.dry_run):
        parser.error("--recover cannot be combined with --upgrade, --apply, or --dry-run")
    if args.apply and args.dry_run:
        parser.error("choose --apply or --dry-run")
    if args.apply and not args.upgrade:
        parser.error("--apply requires --upgrade")
    try:
        if args.recover:
            result = recover_upgrade(Path(args.source_root), Path(args.target))
        elif args.upgrade:
            result = upgrade(Path(args.source_root), Path(args.target), apply=args.apply and not args.dry_run)
        elif args.dry_run:
            result = preview_install(Path(args.source_root), Path(args.target))
        else:
            result = install(Path(args.source_root), Path(args.target))
    except (IntegrityError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"install failed: {exc}")
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
