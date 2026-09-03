from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none", "~"}:
        return None
    if value[0] in '[{"' or value[0] == "'":
        if value[0] == "'" and value[-1:] == "'":
            return value[1:-1]
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON-style frontmatter value: {value!r}") from exc
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?(?:\d+\.\d*|\d*\.\d+)", value):
        return float(value)
    return value


def parse_frontmatter_text(
    text: str, *, source: str = "<memory>"
) -> tuple[dict[str, Any], str]:
    """Parse this repository's deliberately small frontmatter dialect."""

    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"unterminated frontmatter: {source}")
    raw = text[4:end]
    body = text[end + 5 :]
    data: dict[str, Any] = {}
    for line_no, line in enumerate(raw.splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[:1].isspace():
            raise ValueError(
                f"nested or multiline frontmatter is unsupported in {source}:{line_no}"
            )
        if ":" not in line:
            raise ValueError(
                f"invalid frontmatter line in {source}:{line_no}: {line!r}"
            )
        key, value = line.split(":", 1)
        key = key.strip()
        if not re.fullmatch(r"[A-Za-z0-9_-]+", key):
            raise ValueError(f"invalid frontmatter key in {path}:{line_no}: {key!r}")
        data[key] = _parse_scalar(value)
    return data, body


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    """Parse frontmatter from a UTF-8 file."""

    return parse_frontmatter_text(
        path.read_text(encoding="utf-8"), source=str(path)
    )


def _render_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, (int, float)):
        return str(value)
    # JSON string literals are a strict, portable subset of YAML scalars.
    # Always quoting strings avoids YAML reinterpreting values such as
    # ``true`` or rejecting otherwise ordinary prose containing ``: ``.
    return json.dumps(str(value), ensure_ascii=False)


def render_frontmatter(data: dict[str, Any], body: str) -> str:
    lines = ["---"]
    for key, value in data.items():
        lines.append(f"{key}: {_render_scalar(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.lstrip()
