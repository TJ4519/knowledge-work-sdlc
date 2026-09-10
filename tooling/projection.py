from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .contracts import discover_methods, discover_recipes, reference_paths, validate_source
from .errors import IntegrityError
from .util import (
    parse_frontmatter,
    render_frontmatter,
    sha256_bytes,
    sha256_file,
)


BEGIN = "<!-- KNOWLEDGE-WORK-SDLC:BEGIN -->"
END = "<!-- KNOWLEDGE-WORK-SDLC:END -->"
SPINE_TEMPLATES = {
    "initiatives/index.md": "initiative-index.md",
}


def _safe_path(relative: str) -> None:
    path = Path(relative)
    if not relative or path.is_absolute() or ".." in path.parts:
        raise IntegrityError(f"unsafe projected path: {relative}")


def _regular_files(directory: Path, root: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    if directory.is_symlink() or not directory.is_dir():
        raise IntegrityError(f"canonical directory missing or linked: {directory}")
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise IntegrityError(f"canonical tree contains a symlink: {path}")
        if path.is_file():
            relative = path.relative_to(root).as_posix()
            _safe_path(relative)
            files[relative] = path.read_bytes()
    return files


INTERNAL_METHOD_FIELDS = {"body", "path", "source_path", "source_sha256", "kind"}
CLAUDE_TOOL_NAMES = {
    "Shell": "Bash",
}


def _contract_metadata(method: dict[str, Any], *, projected_name: str | None = None) -> dict[str, Any]:
    metadata = {
        key: value for key, value in method.items() if key not in INTERNAL_METHOD_FIELDS
    }
    if projected_name is not None:
        metadata["canonical_name"] = method["name"]
        metadata["name"] = projected_name
        metadata["canonical_source"] = method["source_path"]
        metadata["canonical_sha256"] = method["source_sha256"]
    return metadata


def portable_skill(method: dict[str, Any]) -> bytes:
    metadata = _contract_metadata(method)
    return render_frontmatter(metadata, method["body"].rstrip() + "\n").encode("utf-8")


def plugin_skill(method: dict[str, Any]) -> bytes:
    metadata = _contract_metadata(method, projected_name=method["name"])
    binding = """## Native host binding

This is a generated provider projection of one canonical source method. It
uses project `ai_docs/` for state. Resolve the shared managed method root as
`../../resources/.knowledge-sdlc/` from this `SKILL.md`. Logical
`.knowledge-sdlc/...` cues, including declared reference dependencies, resolve
under that root rather than under the client or this skill directory. Bundled
recipes, templates and references are method inputs, not project facts. This projection does
not launch another runtime or confer authority.
"""
    return render_frontmatter(
        metadata, binding + "\n" + method["body"].rstrip() + "\n"
    ).encode("utf-8")


def plugin_agent(method: dict[str, Any]) -> bytes:
    metadata = _contract_metadata(method, projected_name=f"kw-{method['name']}")
    metadata["tools"] = [
        CLAUDE_TOOL_NAMES.get(tool, tool) for tool in method["allowed_tools"]
    ]
    binding = (
        f"\n## Native host binding\n\nCanonical source: `{method['source_path']}`  \n"
        f"Canonical SHA-256: `{method['source_sha256']}`\n\n"
        "Bundled recipes, templates and references resolve at `../resources/.knowledge-sdlc/` "
        "from this agent file. The run record and named artefacts are the handoff. "
        "Native identity is optional observation.\n"
    )
    return render_frontmatter(metadata, method["body"].rstrip() + binding).encode("utf-8")


def managed_agents_block(root: Path) -> bytes:
    body = (root / "AGENTS.md").read_bytes()
    try:
        text = body.decode("utf-8").rstrip()
    except UnicodeDecodeError as exc:
        raise IntegrityError("source AGENTS.md is not UTF-8") from exc
    if BEGIN in text or END in text:
        raise IntegrityError("source AGENTS.md contains installation markers")
    version = (root / ".knowledge-sdlc" / "VERSION").read_text(encoding="utf-8").strip()
    metadata = f"<!-- managed-version: {version}; source-sha256: {sha256_bytes(body)} -->"
    return f"{BEGIN}\n{metadata}\n{text}\n{END}\n".encode("utf-8")


def merge_agents(existing: bytes | None, block: bytes) -> bytes:
    if existing is None:
        return block
    try:
        text = existing.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise IntegrityError("existing AGENTS.md is not UTF-8") from exc
    if BEGIN in text or END in text:
        raise IntegrityError("existing managed AGENTS.md requires explicit upgrade")
    separator = b"" if existing.endswith(b"\n\n") else (b"\n" if existing.endswith(b"\n") else b"\n\n")
    return existing + separator + block


def _project_instance(template: bytes) -> bytes:
    text = template.decode("utf-8")
    if "document_state: template" in text:
        text = text.replace("document_state: template", "document_state: project-instance", 1)
    return text.encode("utf-8")


def plan_workspace(root: Path, existing_agents: bytes | None = None) -> dict[str, bytes]:
    root = root.resolve()
    defects = validate_source(root)
    if defects:
        raise IntegrityError("source contracts fail: " + "; ".join(item.message for item in defects[:8]))
    files: dict[str, bytes] = {
        ".knowledge-sdlc/VERSION": (root / ".knowledge-sdlc" / "VERSION").read_bytes(),
    }
    for name in ("agents", "recipes", "templates"):
        files.update(_regular_files(root / ".knowledge-sdlc" / name, root))
    for path in reference_paths(root):
        files[path.relative_to(root).as_posix()] = path.read_bytes()

    methods = discover_methods(root)
    for name, method in methods.items():
        if method["kind"] == "skill":
            files[f".agents/skills/{name}/SKILL.md"] = portable_skill(method)

    template_root = root / ".knowledge-sdlc" / "templates"
    for destination, template_name in SPINE_TEMPLATES.items():
        files[f"ai_docs/{destination}"] = _project_instance((template_root / template_name).read_bytes())
    block = managed_agents_block(root)
    files["AGENTS.md"] = merge_agents(existing_agents, block)
    owned_paths = {
        path: sha256_bytes(content)
        for path, content in files.items()
        if path != "AGENTS.md" and not path.startswith("ai_docs/")
    }
    install_record = {
        "schema_version": 1,
        "version": (root / ".knowledge-sdlc/VERSION").read_text(encoding="utf-8").strip(),
        "managed_agents_block_sha256": sha256_bytes(block),
        "owned_files": dict(sorted(owned_paths.items())),
    }
    files[".knowledge-sdlc/install.json"] = (
        json.dumps(install_record, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    validate_workspace_plan(files, methods)
    return dict(sorted(files.items()))


def _resource_files(root: Path) -> dict[str, bytes]:
    files = {"resources/.knowledge-sdlc/VERSION": (root / ".knowledge-sdlc/VERSION").read_bytes()}
    for tree in ("recipes", "templates"):
        for source, content in _regular_files(root / ".knowledge-sdlc" / tree, root).items():
            relative = Path(source).relative_to(".knowledge-sdlc").as_posix()
            files[f"resources/.knowledge-sdlc/{relative}"] = content
    for path in reference_paths(root):
        files[f"resources/{path.relative_to(root).as_posix()}"] = path.read_bytes()
    return files


def _plugin_documentation(root: Path) -> dict[str, bytes]:
    files = {
        "README.md": (root / "docs" / "plugin-package.md").read_bytes(),
        "DESIGN.md": (root / "DESIGN.md").read_bytes(),
        "CHANGELOG.md": (root / "CHANGELOG.md").read_bytes(),
        "LICENSE.md": (root / "LICENSE.md").read_bytes(),
    }
    consumer_docs = (
        "docs/getting-started.md",
        "docs/methodology.md",
        "docs/guides/composition-and-review.md",
        "docs/guides/continuity-and-recovery.md",
        "docs/guides/expert-extensions.md",
        "docs/guides/buy-side-method.md",
        "docs/guides/installation-and-providers.md",
        "docs/guides/personalisation.md",
        "docs/guides/protected-work-and-capabilities.md",
    )
    for relative in consumer_docs:
        files[relative] = (root / relative).read_bytes()
    return files


def plan_plugin(root: Path) -> dict[str, bytes]:
    root = root.resolve()
    defects = validate_source(root)
    if defects:
        raise IntegrityError("source contracts fail: " + "; ".join(item.message for item in defects[:8]))
    version = (root / ".knowledge-sdlc/VERSION").read_text(encoding="utf-8").strip()
    codex = {
        "name": "knowledge-work-sdlc",
        "version": version,
        "description": "File-native commissioning, evidence, review, continuity, and governed learning.",
        "author": {"name": "Knowledge Work SDLC"},
        "skills": "./skills/",
        "interface": {
            "displayName": "Knowledge Work SDLC",
            "shortDescription": "Run defensible professional commissions.",
            "longDescription": (
                "Turn natural professional commissions into evidence-bearing, "
                "correctable work with durable continuation, protected inputs, "
                "independent challenge, and governed learning."
            ),
            "developerName": "Knowledge Work SDLC",
            "category": "Productivity",
            "capabilities": ["Interactive", "Write"],
            "defaultPrompt": [
                "Turn this commission into defensible work.",
                "Continue the active initiative from its next step.",
                "Import and curate this expert method for project use.",
            ],
        },
    }
    claude = {
        "name": "knowledge-work-sdlc",
        "version": version,
        "description": "Native professional commissioning and governed continuity.",
        "author": {"name": "Knowledge Work SDLC"},
    }
    files: dict[str, bytes] = {
        ".codex-plugin/plugin.json": (json.dumps(codex, indent=2, sort_keys=True) + "\n").encode(),
        ".claude-plugin/plugin.json": (json.dumps(claude, indent=2, sort_keys=True) + "\n").encode(),
    }
    files.update(_resource_files(root))
    files.update(_plugin_documentation(root))
    for name, method in discover_methods(root).items():
        if method["kind"] == "skill":
            files[f"skills/{name}/SKILL.md"] = plugin_skill(method)
        else:
            files[f"agents/kw-{name}.md"] = plugin_agent(method)
    validate_plugin_plan(files, discover_methods(root), discover_recipes(root))
    return dict(sorted(files.items()))


def validate_workspace_plan(files: dict[str, bytes], methods: dict[str, dict[str, Any]]) -> None:
    for relative in files:
        _safe_path(relative)
        if relative.endswith(".py"):
            raise IntegrityError(f"workspace projection contains Python: {relative}")
    if any(path.startswith(".knowledge-sdlc/skills/") for path in files):
        raise IntegrityError("workspace contains a duplicate canonical skill corpus")
    expected = {f".agents/skills/{name}/SKILL.md" for name, item in methods.items() if item["kind"] == "skill"}
    actual = {path for path in files if path.startswith(".agents/skills/")}
    if actual != expected:
        raise IntegrityError("workspace skill projection is incomplete or contains extras")
    if "ai_docs/initiatives/index.md" not in files:
        raise IntegrityError("workspace projection lacks the initiative index")
    for method in methods.values():
        for reference in method["references"]:
            if reference not in files:
                raise IntegrityError(f"workspace reference resource missing: {reference}")


def validate_plugin_plan(
    files: dict[str, bytes], methods: dict[str, dict[str, Any]], recipes: dict[str, dict[str, Any]]
) -> None:
    for relative in files:
        _safe_path(relative)
    for manifest in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
        if manifest not in files or json.loads(files[manifest])["name"] != "knowledge-work-sdlc":
            raise IntegrityError(f"invalid plugin manifest: {manifest}")
    expected_skills = {f"skills/{name}/SKILL.md" for name, item in methods.items() if item["kind"] == "skill"}
    expected_agents = {f"agents/kw-{name}.md" for name, item in methods.items() if item["kind"] == "agent"}
    if {path for path in files if path.startswith("skills/")} != expected_skills:
        raise IntegrityError("plugin skill projection mismatch")
    if {path for path in files if path.startswith("agents/")} != expected_agents:
        raise IntegrityError("plugin agent projection mismatch")
    for name in recipes:
        if f"resources/.knowledge-sdlc/recipes/{name}.md" not in files:
            raise IntegrityError(f"plugin recipe resource missing: {name}")
    for method in methods.values():
        for reference in method["references"]:
            if f"resources/{reference}" not in files:
                raise IntegrityError(f"plugin reference resource missing: {reference}")


def validate_workspace(root: Path, source_root: Path) -> list[str]:
    """Compare an installed workspace with an explicit canonical source tree."""

    root = root.resolve()
    defects: list[str] = []
    record_path = root / ".knowledge-sdlc/install.json"
    try:
        if record_path.is_symlink() or not record_path.is_file():
            raise ValueError("install.json is missing or linked")
        record = json.loads(record_path.read_text(encoding="utf-8"))
        owned = record["owned_files"]
        if record.get("schema_version") != 1 or not isinstance(owned, dict):
            raise ValueError("install.json shape is invalid")
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        return [str(exc)]
    for relative, expected_hash in owned.items():
        try:
            _safe_path(relative)
        except IntegrityError as exc:
            defects.append(str(exc))
            continue
        path = root / relative
        if path.is_symlink() or not path.is_file():
            defects.append(f"managed workspace file missing or linked: {relative}")
        elif sha256_file(path) != expected_hash:
            defects.append(f"managed workspace file hash mismatch: {relative}")

    actual_method_files = {
        path.relative_to(root).as_posix()
        for path in (root / ".knowledge-sdlc").rglob("*")
        if path.is_file() and not path.is_symlink()
        and path.name not in {"install.json", "UPGRADE_RECOVERY.json"}
        and ".upgrade-backup-" not in path.as_posix()
    }
    expected_method_files = {
        path for path in owned if path.startswith(".knowledge-sdlc/")
    }
    if actual_method_files != expected_method_files:
        defects.append("installed .knowledge-sdlc path set differs from the ownership record")
    if (root / ".knowledge-sdlc/skills").exists():
        defects.append("installed workspace contains duplicate canonical skill bodies")
    if any(path.endswith(".py") for path in owned):
        defects.append("installed ownership record contains Python")

    expected_runtime_files = {
        path for path in owned if path.startswith(".agents/skills/")
    }
    for relative in expected_runtime_files:
        current = root
        for part in Path(relative).parts[:-1]:
            current = current / part
            if current.is_symlink() or not current.is_dir():
                defects.append(f"installed runtime skill path is unsafe: {relative}")
                break

    agents = root / "AGENTS.md"
    try:
        data = agents.read_bytes()
        begin, end = BEGIN.encode(), END.encode()
        if data.count(begin) != 1 or data.count(end) != 1:
            raise ValueError("managed AGENTS block is missing or ambiguous")
        start = data.index(begin)
        finish = data.index(end, start) + len(end)
        if finish < len(data) and data[finish : finish + 1] == b"\n":
            finish += 1
        if sha256_bytes(data[start:finish]) != record.get("managed_agents_block_sha256"):
            raise ValueError("managed AGENTS block hash mismatch")
    except (OSError, ValueError) as exc:
        defects.append(str(exc))
    index = root / "ai_docs/initiatives/index.md"
    if index.is_symlink() or not index.is_file():
        defects.append("initiative index is missing or unsafe")

    expected = plan_workspace(source_root.resolve(), None)
    expected_record = json.loads(expected[".knowledge-sdlc/install.json"])
    if record.get("owned_files") != expected_record.get("owned_files"):
        defects.append("installed ownership hashes do not match canonical source projection")
    if record.get("managed_agents_block_sha256") != expected_record.get("managed_agents_block_sha256"):
        defects.append("installed AGENTS block does not match canonical source projection")
    return sorted(defects)


def validate_plugin(files: dict[str, bytes], source_root: Path) -> list[str]:
    """Compare a plugin packet with an explicit canonical source tree."""

    try:
        expected = plan_plugin(source_root.resolve())
    except (IntegrityError, OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"canonical plugin projection failed: {exc}"]
    defects: list[str] = []
    missing = sorted(set(expected) - set(files))
    extras = sorted(set(files) - set(expected))
    if missing:
        defects.append(f"plugin paths missing: {missing}")
    if extras:
        defects.append(f"plugin paths unexpected: {extras}")
    changed = sorted(
        path for path in set(expected) & set(files) if expected[path] != files[path]
    )
    if changed:
        defects.append(f"plugin projection bytes differ: {changed}")
    return defects


def inventory(files: dict[str, bytes]) -> list[dict[str, str]]:
    return [{"path": path, "sha256": sha256_bytes(content)} for path, content in sorted(files.items())]
