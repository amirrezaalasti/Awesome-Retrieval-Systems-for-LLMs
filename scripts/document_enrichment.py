"""Detect unusable Docling extractions that should only be marked, not LLM-processed."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

PLACEHOLDER_CONTENT_RE = re.compile(
    r"^(loading\.?\.?\.?|please enable javascript|access denied|error 404|not found)\.?$",
    re.IGNORECASE,
)

INVALID_REFERENCE_RE = re.compile(
    r"^(loading\.?\.?\.?|n/?a|none|null|unknown|not available|not found|todo|tbd)\.?$",
    re.IGNORECASE,
)

MIN_USABLE_CHARS = 250


def document_is_usable(text: str) -> bool:
    stripped = text.strip()
    if len(stripped) < MIN_USABLE_CHARS:
        return False
    if PLACEHOLDER_CONTENT_RE.match(stripped):
        return False
    alpha_chars = sum(1 for c in stripped if c.isalpha())
    return alpha_chars >= 100


def is_invalid_reference(reference: str) -> bool:
    ref = reference.strip()
    if not ref:
        return False
    if len(ref) < 12:
        return True
    if INVALID_REFERENCE_RE.match(ref):
        return True
    if PLACEHOLDER_CONTENT_RE.match(ref):
        return True
    return False


def assess_document(item_dir: Path) -> dict[str, Any]:
    content_path = item_dir / "content.md"
    text = content_path.read_text(encoding="utf-8") if content_path.exists() else ""
    stripped = text.strip()

    info: dict[str, Any] = {
        "content_path": str(content_path.name) if content_path.exists() else None,
        "content_chars": len(stripped),
        "usable": document_is_usable(text),
    }

    if PLACEHOLDER_CONTENT_RE.match(stripped):
        info["reason"] = "placeholder_content"
    elif len(stripped) < MIN_USABLE_CHARS:
        info["reason"] = "too_short"
    elif sum(1 for c in stripped if c.isalpha()) < 100:
        info["reason"] = "insufficient_text"
    else:
        info["reason"] = None

    if stripped:
        info["content_preview"] = stripped[:120]

    readme_path = item_dir / "readme.md"
    if readme_path.exists():
        readme_text = readme_path.read_text(encoding="utf-8")
        if document_is_usable(readme_text):
            info["usable"] = True
            info["reason"] = None
            info["strategy"] = "readme_md"

    return info
