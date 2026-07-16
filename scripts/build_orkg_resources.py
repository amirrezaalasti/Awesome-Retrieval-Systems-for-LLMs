#!/usr/bin/env python3
"""Aggregate verified orkg.json files into a single ORKG resources YAML."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
ORKG_DIR = ROOT / "orkg"
TEMPLATE_PATH = ORKG_DIR / "template_orkg.yml"
DEFAULT_EXTRACTED = ROOT / "extracted"
DEFAULT_OUTPUT = ORKG_DIR / "orkg_resources.yml"


def load_template(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def field_names(template: dict[str, Any]) -> list[str]:
    return [field["name"] for field in template.get("fields", [])]


def simplify_field(entry: dict[str, Any] | Any) -> dict[str, Any]:
    if not isinstance(entry, dict):
        return {"value": entry, "reference": "", "verified": False}

    simplified: dict[str, Any] = {
        "value": entry.get("value"),
        "reference": entry.get("reference", ""),
        "verified": entry.get("verified", False),
    }
    if "verification_score" in entry:
        simplified["verification_score"] = entry["verification_score"]
    if "verification_method" in entry:
        simplified["verification_method"] = entry["verification_method"]
    if entry.get("error"):
        simplified["error"] = entry["error"]
    return simplified


def extraction_quality(data: dict[str, Any]) -> tuple[int, int, str]:
    meta = data.get("extraction_metadata", {})
    if meta.get("status") == "insufficient_content":
        return (0, 0, "")
    verified_count = sum(
        1
        for field in data.get("fields", {}).values()
        if isinstance(field, dict) and field.get("verified")
    )
    all_verified = 1 if meta.get("all_references_verified") else 0
    extracted_at = str(meta.get("extracted_at") or meta.get("marked_at") or "")
    return (all_verified, verified_count, extracted_at)


def build_paper_block(data: dict[str, Any], appearances: list[int]) -> dict[str, Any]:
    source = data.get("source", {})
    fields = data.get("fields", {})
    system_name_field = fields.get("system_name", {})
    label = system_name_field.get("value") if isinstance(system_name_field, dict) else None

    paper: dict[str, Any] = {
        "label": label or source.get("slug"),
        "type": source.get("type"),
        "source_url": source.get("source_url"),
        "catalog_years": sorted(set(appearances)),
    }
    if source.get("slug"):
        paper["slug"] = source["slug"]
    return paper


def build_properties_block(data: dict[str, Any], template_fields: list[str]) -> dict[str, Any]:
    fields = data.get("fields", {})
    properties: dict[str, Any] = {}
    for name in template_fields:
        if name in fields:
            properties[name] = simplify_field(fields[name])
    for name, entry in fields.items():
        if name not in properties:
            properties[name] = simplify_field(entry)
    return properties


def collect_entries(extracted_dir: Path, template: dict[str, Any]) -> tuple[list[dict], list[dict]]:
    template_fields = field_names(template)
    grouped: dict[str, list[tuple[Path, dict[str, Any]]]] = {}

    for orkg_path in sorted(extracted_dir.glob("*/*/*/orkg.json")):
        data = json.loads(orkg_path.read_text(encoding="utf-8"))
        source_url = (data.get("source") or {}).get("source_url")
        if not source_url:
            continue
        grouped.setdefault(source_url, []).append((orkg_path, data))

    resources: list[dict[str, Any]] = []
    insufficient: list[dict[str, Any]] = []

    for source_url, items in sorted(grouped.items(), key=lambda item: item[0]):
        best_path, best_data = max(items, key=lambda item: extraction_quality(item[1]))
        meta = best_data.get("extraction_metadata", {})
        appearances = sorted({(entry[1].get("source") or {}).get("year") for entry in items if (entry[1].get("source") or {}).get("year")})

        if meta.get("status") == "insufficient_content" or not best_data.get("fields"):
            insufficient.append(
                {
                    "paper": build_paper_block(best_data, appearances),
                    "status": "insufficient_content",
                    "reason": meta.get("reason"),
                    "content_preview": meta.get("content_preview"),
                    "source_paths": [str(path.parent.relative_to(extracted_dir)) for path, _ in items],
                }
            )
            continue

        resource_id = (best_data.get("source") or {}).get("slug") or source_url
        resources.append(
            {
                "id": resource_id,
                "paper": build_paper_block(best_data, appearances),
                "properties": build_properties_block(best_data, template_fields),
                "provenance": {
                    "source_path": str(best_path.parent.relative_to(extracted_dir)),
                    "duplicate_paths": [
                        str(path.parent.relative_to(extracted_dir))
                        for path, _ in items
                        if path != best_path
                    ],
                    "model": meta.get("model"),
                    "extracted_at": meta.get("extracted_at"),
                    "all_references_verified": meta.get("all_references_verified", False),
                },
            }
        )

    return resources, insufficient


def build_document(template: dict[str, Any], resources: list[dict], insufficient: list[dict]) -> dict[str, Any]:
    return {
        "template_name": template.get("template_name"),
        "description": template.get("description"),
        "fields": template.get("fields", []),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "resources": resources,
        "insufficient_resources": insufficient,
        "stats": {
            "resources": len(resources),
            "insufficient_resources": len(insufficient),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build ORKG resources YAML from orkg.json files")
    parser.add_argument("--template", type=Path, default=TEMPLATE_PATH)
    parser.add_argument("--extracted", type=Path, default=DEFAULT_EXTRACTED)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    template = load_template(args.template)
    resources, insufficient = collect_entries(args.extracted, template)
    document = build_document(template, resources, insufficient)

    args.output.write_text(
        yaml.safe_dump(document, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )

    print(f"Wrote {args.output}")
    print(f"  resources: {len(resources)}")
    print(f"  insufficient_resources: {len(insufficient)}")


if __name__ == "__main__":
    main()
