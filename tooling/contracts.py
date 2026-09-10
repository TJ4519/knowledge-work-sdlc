from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .util import parse_frontmatter, sha256_file


SAFE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
COMPOSITION = re.compile(r"```json\s*(\[.*?\])\s*```", re.DOTALL)
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
LIST_FIELDS = (
    "allowed_tools",
    "inputs",
    "optional_inputs",
    "excluded_context",
    "outputs",
    "optional_outputs",
    "required_capabilities",
    "optional_capabilities",
    "references",
)
RETIRED_FIELDS = {"model_profile", "model_floor"}
ALLOWED_TOOLS = {"Read", "Grep", "Shell", "Write", "Task", "WebSearch", "WebFetch"}
REQUIRED_SKILLS = {
    "knowledge-work",
    "kw-candidate-disposition",
    "kw-domain-charter",
    "kw-expert-extension",
    "kw-feedback-review",
    "kw-learning-governance",
    "kw-learning-outcome-review",
    "kw-learning-selection",
    "kw-meaning-consultation",
    "kw-model-allocation",
    "kw-orchestration",
    "kw-prime",
    "kw-protected-promotion",
    "kw-reconciliation-control",
    "kw-work-order",
}
REQUIRED_AGENTS = {
    "adjudicator",
    "evidence-explorer",
    "protected-artifact-producer",
    "reconciler",
    "rederivation-auditor",
    "research-synthesis-producer",
    "source-meaning-challenger",
    "thesis-challenger",
    "work-object-preparer",
}
REQUIRED_RECIPES = {
    "domain-method-adaptation",
    "knowledge-work-correction",
    "professional-challenge",
    "professional-research",
    "professional-source-interpretation",
    "protected-artifact-update",
}
REQUIRED_TEMPLATES = {
    "domain-charter.md",
    "domain-context.md",
    "expert-extension.md",
    "initiative-index.md",
    "meaning.md",
    "methods-directory.md",
    "model-policy.md",
    "protected-artifacts.md",
    "run-record.md",
    "source-policy.md",
    "work-order.md",
}


@dataclass(frozen=True)
class Defect:
    code: str
    path: str | None
    message: str


def _strings(value: Any) -> list[str]:
    if value in (None, ""):
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValueError("expected a JSON array of strings")
    return list(value)


def _safe_relative(path: str) -> bool:
    candidate = Path(path)
    return bool(path) and not candidate.is_absolute() and ".." not in candidate.parts


def _method_paths(root: Path) -> list[tuple[str, Path]]:
    base = root / ".knowledge-sdlc"
    return [
        *(("skill", path) for path in sorted((base / "skills").glob("*/SKILL.md"))),
        *(("agent", path) for path in sorted((base / "agents").glob("*.md"))),
    ]


def reference_paths(root: Path) -> list[Path]:
    """Shared authored Markdown resources; never project state or executables."""
    directory = root / ".knowledge-sdlc" / "references"
    if (root / ".knowledge-sdlc").is_symlink() or directory.is_symlink() or not directory.is_dir():
        return []
    return [path for path in sorted(directory.rglob("*.md"))
            if path.is_file() and not path.is_symlink()
            and not any((root / parent).is_symlink()
                        for parent in path.relative_to(root).parents)]


def _reference_defects(root: Path, methods: dict[str, dict[str, Any]]) -> list[Defect]:
    defects: list[Defect] = []
    directory = root / ".knowledge-sdlc" / "references"
    if ((root / ".knowledge-sdlc").is_symlink() or directory.is_symlink()
            or (directory.exists() and not directory.is_dir())):
        defects.append(Defect("reference-tree", ".knowledge-sdlc/references", "missing directory or linked tree"))
    elif directory.is_dir():
        for path in sorted(directory.rglob("*")):
            if path.is_symlink() or (path.is_file() and path.suffix != ".md"):
                defects.append(Defect("reference-tree", path.relative_to(root).as_posix(), "references must be regular Markdown files in an unlinked tree"))
    available = {path.relative_to(root).as_posix() for path in reference_paths(root)}
    # Shared guidance can itself depend on another shared document. Check that
    # mechanical edge too; a skill's direct declaration is not the whole tree.
    for path in reference_paths(root):
        for raw in MARKDOWN_LINK.findall(path.read_text(encoding="utf-8")):
            target = raw.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (path.parent / target).resolve()
            try:
                relative = resolved.relative_to(root).as_posix()
            except ValueError:
                relative = ""
            if relative not in available:
                defects.append(Defect("reference-link", path.relative_to(root).as_posix(), f"missing or unsafe shared reference link: {raw}"))
    for method in methods.values():
        for reference in method["references"]:
            if (not _safe_relative(reference)
                    or not reference.startswith(".knowledge-sdlc/references/")
                    or Path(reference).suffix != ".md"):
                defects.append(Defect("method-reference-path", method["source_path"], f"unsafe managed reference: {reference}"))
            elif reference not in available:
                defects.append(Defect("method-reference-missing", method["source_path"], f"missing or linked managed reference: {reference}"))
    return defects


def discover_methods(root: Path) -> dict[str, dict[str, Any]]:
    root = root.resolve()
    methods: dict[str, dict[str, Any]] = {}
    for kind, path in _method_paths(root):
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"method is not a regular file: {path}")
        metadata, body = parse_frontmatter(path)
        name = str(metadata.get("name", ""))
        expected = path.parent.name if kind == "skill" else path.stem
        if not SAFE_NAME.fullmatch(name) or name != expected:
            raise ValueError(f"method name/path mismatch: {path}")
        if name in methods:
            raise ValueError(f"duplicate method name: {name}")
        normalized = dict(metadata)
        for field in LIST_FIELDS:
            normalized[field] = _strings(normalized.get(field, []))
        normalized.update(
            kind=kind,
            body=body,
            path=path,
            source_path=path.relative_to(root).as_posix(),
            source_sha256=sha256_file(path),
        )
        methods[name] = normalized
    return methods


def discover_recipes(root: Path) -> dict[str, dict[str, Any]]:
    root = root.resolve()
    directory = root / ".knowledge-sdlc" / "recipes"
    recipes: dict[str, dict[str, Any]] = {}
    for path in sorted(directory.glob("*.md")):
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"recipe is not a regular file: {path}")
        metadata, body = parse_frontmatter(path)
        name = str(metadata.get("name", ""))
        if not SAFE_NAME.fullmatch(name) or name != path.stem:
            raise ValueError(f"recipe name/path mismatch: {path}")
        matches = COMPOSITION.findall(body)
        if len(matches) != 1:
            raise ValueError(f"recipe must contain one JSON composition block: {path}")
        composition = json.loads(matches[0])
        if not isinstance(composition, list) or not composition:
            raise ValueError(f"recipe composition must be a nonempty array: {path}")
        if name in recipes:
            raise ValueError(f"duplicate recipe name: {name}")
        recipes[name] = {
            **metadata,
            "initial_inputs": _strings(metadata.get("initial_inputs", [])),
            "composition": composition,
            "body": body,
            "path": path,
            "source_path": path.relative_to(root).as_posix(),
            "source_sha256": sha256_file(path),
        }
    return recipes


def _method_defects(methods: dict[str, dict[str, Any]]) -> list[Defect]:
    defects: list[Defect] = []
    for name, method in methods.items():
        path = method["source_path"]
        for field in RETIRED_FIELDS:
            if field in method:
                defects.append(Defect("retired-model-field", path, f"{name} declares {field}"))
        required = {
            "description",
            "primitive",
            "fresh_context",
            "independence",
            "allowed_tools",
            "inputs",
            "outputs",
            "authority",
            "standalone",
            "idempotency",
            "phase",
        }
        missing = sorted(field for field in required if field not in method)
        if missing:
            defects.append(Defect("method-fields", path, f"missing fields: {missing}"))
        if method.get("primitive") != method.get("kind"):
            defects.append(
                Defect(
                    "method-primitive",
                    path,
                    f"declares {method.get('primitive')!r}, expected {method.get('kind')!r}",
                )
            )
        if not isinstance(method.get("fresh_context"), bool):
            defects.append(Defect("method-freshness", path, "fresh_context must be boolean"))
        independence = method.get("independence")
        if not isinstance(independence, str) or not independence.strip():
            defects.append(Defect("method-independence", path, "independence must be nonempty"))
        unsupported_tools = sorted(set(method["allowed_tools"]) - ALLOWED_TOOLS)
        if unsupported_tools:
            defects.append(Defect("method-tools", path, f"unsupported tools: {unsupported_tools}"))
        for field in ("required_capabilities", "optional_capabilities"):
            unsafe = sorted(item for item in method[field] if not SAFE_NAME.fullmatch(item))
            if unsafe:
                defects.append(Defect("method-capabilities", path, f"unsafe {field}: {unsafe}"))
        for first, second in (
            ("inputs", "optional_inputs"),
            ("outputs", "optional_outputs"),
            ("required_capabilities", "optional_capabilities"),
        ):
            overlap = sorted(set(method[first]) & set(method[second]))
            if overlap:
                defects.append(Defect("method-field-overlap", path, f"{first}/{second}: {overlap}"))
        if method["outputs"] and "Write" not in method["allowed_tools"]:
            defects.append(Defect("durable-output-without-write", path, name))
    return defects


def _recipe_defects(
    recipes: dict[str, dict[str, Any]], methods: dict[str, dict[str, Any]]
) -> list[Defect]:
    defects: list[Defect] = []
    for recipe_name, recipe in recipes.items():
        path = recipe["source_path"]
        available = set(recipe["initial_inputs"])
        optional_available: set[str] = set()
        seen: set[str] = set()
        for index, step in enumerate(recipe["composition"]):
            if not isinstance(step, dict):
                defects.append(Defect("recipe-step-shape", path, f"step {index} is not an object"))
                continue
            step_id = str(step.get("id", ""))
            actor = str(step.get("actor", ""))
            optional = bool(step.get("optional", False))
            if not SAFE_NAME.fullmatch(step_id) or step_id in seen:
                defects.append(Defect("recipe-step-id", path, f"unsafe or duplicate id: {step_id!r}"))
            seen.add(step_id)
            if optional and not str(step.get("trigger", "")).strip():
                defects.append(Defect("optional-without-trigger", path, step_id))
            try:
                explicit_requires = _strings(step.get("requires", []))
                explicit_provides = _strings(step.get("provides", []))
            except ValueError as exc:
                defects.append(Defect("recipe-step-shape", path, f"{step_id}: {exc}"))
                continue

            if actor == "human":
                if step.get("method") not in (None, ""):
                    defects.append(Defect("human-method", path, step_id))
                requires, provides = explicit_requires, explicit_provides
            elif actor in {"skill", "agent"}:
                method_name = str(step.get("method", ""))
                method = methods.get(method_name)
                if method is None or method.get("kind") != actor:
                    defects.append(Defect("recipe-method-resolution", path, f"{step_id}: {actor}/{method_name}"))
                    continue
                supported_inputs = set(method["inputs"]) | set(method["optional_inputs"])
                supported_outputs = set(method["outputs"]) | set(method["optional_outputs"])
                requires = explicit_requires or list(method["inputs"])
                provides = explicit_provides or list(method["outputs"])
                unsupported_inputs = sorted(set(requires) - supported_inputs)
                unsupported_outputs = sorted(set(provides) - supported_outputs)
                weakened_inputs = sorted(set(method["inputs"]) - set(requires))
                weakened_outputs = sorted(set(method["outputs"]) - set(provides))
                if unsupported_inputs or unsupported_outputs or weakened_inputs or weakened_outputs:
                    defects.append(
                        Defect(
                            "recipe-method-contract",
                            path,
                            f"{step_id}: unsupported inputs={unsupported_inputs}, outputs={unsupported_outputs}; "
                            f"weakened inputs={weakened_inputs}, outputs={weakened_outputs}",
                        )
                    )
            else:
                defects.append(Defect("recipe-actor", path, f"{step_id}: {actor!r}"))
                continue

            possible = available | optional_available
            missing = sorted(set(requires) - (possible if optional else available))
            if missing:
                defects.append(Defect("recipe-dataflow", path, f"{step_id}: missing {missing}"))
            if optional:
                optional_available.update(provides)
            else:
                available.update(provides)
    return defects


def validate_source(root: Path) -> list[Defect]:
    root = root.resolve()
    defects: list[Defect] = []
    try:
        methods = discover_methods(root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [Defect("method-discovery", None, str(exc))]
    try:
        recipes = discover_recipes(root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [Defect("recipe-discovery", None, str(exc))]

    defects.extend(_method_defects(methods))
    defects.extend(_reference_defects(root, methods))
    defects.extend(_recipe_defects(recipes, methods))
    skills = {name for name, item in methods.items() if item["kind"] == "skill"}
    agents = {name for name, item in methods.items() if item["kind"] == "agent"}
    for code, missing in (
        ("required-skills", REQUIRED_SKILLS - skills),
        ("required-agents", REQUIRED_AGENTS - agents),
        ("required-recipes", REQUIRED_RECIPES - set(recipes)),
    ):
        if missing:
            defects.append(Defect(code, None, f"missing: {sorted(missing)}"))

    template_dir = root / ".knowledge-sdlc" / "templates"
    template_names = {path.name for path in template_dir.glob("*.md") if path.is_file()}
    missing_templates = REQUIRED_TEMPLATES - template_names
    if missing_templates:
        defects.append(Defect("required-templates", None, f"missing: {sorted(missing_templates)}"))

    for relative in (
        "AGENTS.md",
        ".knowledge-sdlc/VERSION",
    ):
        path = root / relative
        if path.is_symlink() or not path.is_file():
            defects.append(Defect("stable-source-surface", relative, "missing or linked"))

    for retired in (
        ".knowledge-sdlc/config/default-project.toml",
        ".knowledge-sdlc/config/intents.json",
        ".knowledge-sdlc/config/stages.json",
        ".knowledge-sdlc/profiles",
        ".knowledge-sdlc/skills/kw-intake",
    ):
        if (root / retired).exists() or (root / retired).is_symlink():
            defects.append(Defect("retired-taxonomy", retired, "retired surface remains"))
    return sorted(defects, key=lambda item: (item.code, item.path or "", item.message))


def source_inventory(root: Path) -> list[dict[str, str]]:
    root = root.resolve()
    paths: list[Path] = []
    paths.extend(path for _, path in _method_paths(root))
    paths.extend(sorted((root / ".knowledge-sdlc" / "recipes").glob("*.md")))
    paths.extend(sorted((root / ".knowledge-sdlc" / "templates").glob("*.md")))
    paths.extend(reference_paths(root))
    paths.extend(
        root / relative
        for relative in (
            "AGENTS.md",
            ".knowledge-sdlc/VERSION",
        )
    )
    return [
        {"path": path.relative_to(root).as_posix(), "sha256": sha256_file(path)}
        for path in sorted(paths)
        if path.is_file() and not path.is_symlink()
    ]


def report(root: Path) -> dict[str, Any]:
    defects = validate_source(root)
    return {
        "passed": not defects,
        "inventory": source_inventory(root),
        "defects": [asdict(item) for item in defects],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate mechanical Knowledge Work method contracts.", allow_abbrev=False)
    parser.add_argument("--source-root", required=True)
    args = parser.parse_args()
    result = report(Path(args.source_root))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
