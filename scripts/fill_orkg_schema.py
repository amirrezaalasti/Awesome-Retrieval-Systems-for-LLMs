#!/usr/bin/env python3
"""Fill ORKG template fields from extracted documents using OpenRouter + reference verification."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import requests
import yaml
from dotenv import load_dotenv

from reference_verifier import VerificationResult, verify_reference
from document_enrichment import assess_document, document_is_usable, is_invalid_reference

ROOT = Path(__file__).resolve().parents[1]
ORKG_DIR = ROOT / "orkg"
TEMPLATE_PATH = ORKG_DIR / "template_orkg.yml"
DEFAULT_EXTRACTED = ROOT / "extracted"
DEFAULT_OUTPUT_NAME = "orkg.json"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "z-ai/glm-5.2"


def load_template(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def build_field_instructions(template: dict[str, Any]) -> str:
    lines = [
        "Extract the following fields. For EVERY field provide:",
        '- "value": the extracted answer obeying type/options constraints',
        '- "reference": an EXACT verbatim quote copied from the document (15-80 words) that supports the value',
        "",
        "Fields:",
    ]
    for field in template["fields"]:
        line = f'- {field["name"]} ({field["type"]})'
        if field.get("required"):
            line += " [required]"
        line += f': {field["description"]}'
        if field.get("options"):
            line += f' Allowed: {json.dumps(field["options"])}'
        if field.get("range"):
            line += f' Range: {field["range"]}'
        lines.append(line)
    return "\n".join(lines)


def truncate_document(text: str, max_chars: int = 55000) -> str:
    if len(text) <= max_chars:
        return text
    head = int(max_chars * 0.65)
    tail = max_chars - head
    return (
        text[:head]
        + "\n\n[... document truncated for context window ...]\n\n"
        + text[-tail:]
    )


def call_openrouter(
    *,
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
    temperature: float = 0.1,
) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/amirrezaalasti/Awesome-Retrieval-Systems-for-LLMs",
        "X-Title": "Awesome Retrieval Systems ORKG Extractor",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "response_format": {"type": "json_object"},
    }
    resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=180)
    resp.raise_for_status()
    data = resp.json()
    content = data["choices"][0]["message"].get("content")
    if not content or not str(content).strip():
        raise ValueError(f"Empty response from model {model}")
    return str(content)


def parse_llm_json(content: str) -> dict[str, Any]:
    content = content.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def extraction_prompt(
    template: dict[str, Any],
    document: str,
    metadata: dict[str, Any],
) -> list[dict[str, str]]:
    field_instructions = build_field_instructions(template)
    system = (
        "You are a meticulous research assistant extracting structured metadata "
        "about retrieval systems for LLMs. Return ONLY valid JSON. "
        "Each field must be an object with keys 'value' and 'reference'. "
        "The reference MUST be copied verbatim from the document without paraphrasing."
    )
    user = f"""Template: {template['template_name']}
Description: {template['description']}

Source metadata:
{json.dumps(metadata, indent=2)}

{field_instructions}

Rules:
- Use only allowed enum/multiselect options exactly as written.
- For multiselect fields, value must be a JSON array.
- release_year must be an integer between 2019 and 2026.
- paper_artifact and code_artifact should be URLs when present, else null.
- If unknown, use null value and empty string reference only when truly absent.
- NEVER use placeholder text such as "Loading...", "N/A", or "Unknown" as a reference.
- Every non-empty reference must be a verbatim quote of at least 12 characters from the document.

Document:
---
{document}
---

Return JSON shaped like:
{{
  "system_name": {{"value": "...", "reference": "..."}},
  "release_year": {{"value": 2020, "reference": "..."}},
  ...
}}
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def fix_prompt(
    template: dict[str, Any],
    document: str,
    current: dict[str, Any],
    failures: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    system = (
        "You previously extracted metadata but some references could not be verified "
        "in the source document. Fix ONLY the listed fields. "
        "Return valid JSON with the same top-level field keys, each as {{value, reference}}. "
        "References must be exact verbatim quotes from the document."
    )
    user = f"""Failed fields and verification info:
{json.dumps(failures, indent=2)}

Current extraction:
{json.dumps(current, indent=2)}

Allowed field constraints:
{build_field_instructions(template)}

Document:
---
{document}
---
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def validate_field_value(field: dict[str, Any], raw_value: Any) -> Any:
    field_type = field["type"]
    name = field["name"]

    if raw_value is None:
        if field.get("required"):
            raise ValueError(f"{name} is required")
        return None

    if field_type == "string":
        return str(raw_value)
    if field_type == "integer":
        value = int(raw_value)
        if "range" in field:
            lo, hi = field["range"]
            if not lo <= value <= hi:
                raise ValueError(f"{name} out of range")
        return value
    if field_type == "url":
        return str(raw_value) if raw_value else None
    if field_type == "enum":
        if raw_value not in field["options"]:
            raise ValueError(f"{name} invalid enum: {raw_value}")
        return raw_value
    if field_type == "multiselect":
        if not isinstance(raw_value, list):
            raise ValueError(f"{name} must be a list")
        invalid = [v for v in raw_value if v not in field["options"]]
        if invalid:
            raise ValueError(f"{name} invalid options: {invalid}")
        return raw_value
    return raw_value


def verify_extraction(
    template: dict[str, Any],
    llm_fields: dict[str, Any],
    document: str,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    verified_output: dict[str, Any] = {}
    failures: dict[str, dict[str, Any]] = {}

    field_defs = {f["name"]: f for f in template["fields"]}

    for name, field_def in field_defs.items():
        entry = llm_fields.get(name, {})
        if not isinstance(entry, dict):
            entry = {"value": entry, "reference": ""}

        value = entry.get("value")
        reference = str(entry.get("reference") or "").strip()
        field_result: dict[str, Any] = {
            "value": value,
            "reference": reference,
        }

        try:
            field_result["value"] = validate_field_value(field_def, value)
        except ValueError as exc:
            field_result["verified"] = False
            field_result["verification_score"] = 0.0
            field_result["verification_method"] = "schema_validation_failed"
            field_result["error"] = str(exc)
            verified_output[name] = field_result
            failures[name] = {
                "reason": "schema_validation_failed",
                "error": str(exc),
                "reference": reference,
                "value": value,
            }
            continue

        if field_def.get("required") and (value is None or value == "" or value == []):
            field_result["verified"] = False
            field_result["verification_score"] = 0.0
            field_result["verification_method"] = "missing_required_value"
            verified_output[name] = field_result
            failures[name] = {
                "reason": "missing_required_value",
                "reference": reference,
                "value": value,
            }
            continue

        if not reference and value not in (None, "", []):
            field_result["verified"] = False
            field_result["verification_score"] = 0.0
            field_result["verification_method"] = "missing_reference"
            verified_output[name] = field_result
            failures[name] = {
                "reason": "missing_reference",
                "reference": reference,
                "value": value,
            }
            continue

        if not reference:
            field_result["verified"] = True
            field_result["verification_score"] = 1.0
            field_result["verification_method"] = "not_applicable"
            verified_output[name] = field_result
            continue

        if is_invalid_reference(reference):
            field_result["verified"] = False
            field_result["verification_score"] = 0.0
            field_result["verification_method"] = "invalid_reference"
            verified_output[name] = field_result
            failures[name] = {
                "reason": "invalid_reference",
                "reference": reference,
                "value": value,
            }
            continue

        result: VerificationResult = verify_reference(reference, document)
        field_result["verified"] = result.found
        field_result["verification_score"] = result.score
        field_result["verification_method"] = result.method
        if result.matched_span:
            field_result["matched_span"] = result.matched_span
        verified_output[name] = field_result

        if not result.found:
            failures[name] = {
                "reason": "reference_not_found",
                "reference": reference,
                "value": value,
                "score": result.score,
                "method": result.method,
            }

    return verified_output, failures


def discover_items(extracted_dir: Path) -> list[Path]:
    items: list[Path] = []
    for metadata_path in sorted(extracted_dir.glob("*/papers/*/metadata.json")):
        items.append(metadata_path.parent)
    for metadata_path in sorted(extracted_dir.glob("*/software/*/metadata.json")):
        items.append(metadata_path.parent)
    return items


def process_item(
    item_dir: Path,
    *,
    template: dict[str, Any],
    api_key: str,
    model: str,
    max_attempts: int,
    max_doc_chars: int,
    force: bool,
) -> dict[str, Any]:
    metadata_path = item_dir / "metadata.json"
    content_path = item_dir / "content.md"
    output_path = item_dir / DEFAULT_OUTPUT_NAME

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if metadata.get("status") != "success":
        return {"path": str(item_dir), "status": "skipped", "reason": metadata.get("status")}

    if output_path.exists() and not force:
        existing = json.loads(output_path.read_text(encoding="utf-8"))
        meta = existing.get("extraction_metadata", {})
        if meta.get("all_references_verified") and meta.get("status") != "insufficient_content":
            return {"path": str(item_dir), "status": "skipped", "reason": "already_exists"}

    if not content_path.exists():
        return {"path": str(item_dir), "status": "skipped", "reason": "missing_content"}

    content_info = assess_document(item_dir)
    document = content_path.read_text(encoding="utf-8")
    if content_info.get("strategy") == "readme_md":
        document = (item_dir / "readme.md").read_text(encoding="utf-8")

    if not document_is_usable(document):
        output = {
            "template_name": template["template_name"],
            "source": {
                "year": metadata.get("year"),
                "type": metadata.get("type"),
                "slug": metadata.get("slug"),
                "source_url": metadata.get("source_url"),
            },
            "fields": {},
            "extraction_metadata": {
                "status": "insufficient_content",
                "reason": content_info.get("reason"),
                "content_chars": content_info.get("content_chars"),
                "content_preview": content_info.get("content_preview"),
                "marked_at": datetime.now(timezone.utc).isoformat(),
            },
        }
        output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return {
            "path": str(item_dir),
            "status": "marked_insufficient",
            "reason": content_info.get("reason"),
        }

    document = truncate_document(document, max_doc_chars)
    attempts = 0
    llm_fields: dict[str, Any] = {}
    verified_fields: dict[str, Any] = {}
    failures: dict[str, dict[str, Any]] = {}

    while attempts < max_attempts:
        attempts += 1
        if attempts == 1:
            messages = extraction_prompt(template, document, metadata)
        else:
            messages = fix_prompt(template, document, llm_fields, failures)

        raw = call_openrouter(api_key=api_key, model=model, messages=messages)
        llm_fields = parse_llm_json(raw)
        verified_fields, failures = verify_extraction(template, llm_fields, document)
        if not failures:
            break

    all_verified = not failures
    output = {
        "template_name": template["template_name"],
        "source": {
            "year": metadata.get("year"),
            "type": metadata.get("type"),
            "slug": metadata.get("slug"),
            "source_url": metadata.get("source_url"),
        },
        "fields": verified_fields,
        "extraction_metadata": {
            "model": model,
            "attempts": attempts,
            "all_references_verified": all_verified,
            "failed_fields": list(failures.keys()),
            "extracted_at": datetime.now(timezone.utc).isoformat(),
        },
    }
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return {
        "path": str(item_dir),
        "status": "success" if all_verified else "partial",
        "failed_fields": list(failures.keys()),
        "output": str(output_path),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fill ORKG schema JSON via OpenRouter")
    parser.add_argument("--template", type=Path, default=TEMPLATE_PATH)
    parser.add_argument("--extracted", type=Path, default=DEFAULT_EXTRACTED)
    parser.add_argument("--model", default=os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL))
    parser.add_argument("--year", type=int, action="append")
    parser.add_argument("--type", choices=["paper", "software"], action="append")
    parser.add_argument("--slug", action="append", help="Process only matching slug substrings")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--max-doc-chars", type=int, default=55000)
    parser.add_argument("--delay", type=float, default=1.0)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> int:
    load_dotenv(ROOT / ".env")
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("OPENROUTER_API_KEY not set in .env", file=sys.stderr)
        return 1

    args = parse_args()
    template = load_template(args.template)
    items = discover_items(args.extracted)

    if args.year:
        items = [p for p in items if json.loads((p / "metadata.json").read_text())["year"] in args.year]
    if args.type:
        items = [p for p in items if json.loads((p / "metadata.json").read_text())["type"] in args.type]
    if args.slug:
        items = [p for p in items if any(s in p.name for s in args.slug)]
    if args.limit:
        items = items[: args.limit]

    results: list[dict[str, Any]] = []
    for item_dir in items:
        print(f"Processing {item_dir.relative_to(args.extracted)}")
        try:
            result = process_item(
                item_dir,
                template=template,
                api_key=api_key,
                model=args.model,
                max_attempts=args.max_attempts,
                max_doc_chars=args.max_doc_chars,
                force=args.force,
            )
        except Exception as exc:  # noqa: BLE001
            result = {"path": str(item_dir), "status": "error", "error": str(exc)}
        results.append(result)
        time.sleep(args.delay)

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "total": len(results),
        "success": sum(1 for r in results if r["status"] == "success"),
        "partial": sum(1 for r in results if r["status"] == "partial"),
        "skipped": sum(1 for r in results if r["status"] == "skipped"),
        "marked_insufficient": sum(1 for r in results if r["status"] == "marked_insufficient"),
        "errors": sum(1 for r in results if r["status"] == "error"),
        "items": results,
    }
    manifest_path = args.extracted / "orkg_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(
        f"\nDone: {manifest['success']} verified, "
        f"{manifest['partial']} partial, "
        f"{manifest['marked_insufficient']} marked insufficient, "
        f"{manifest['skipped']} skipped, "
        f"{manifest['errors']} errors"
    )
    return 0 if manifest["errors"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
