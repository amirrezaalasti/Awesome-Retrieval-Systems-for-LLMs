#!/usr/bin/env python3
"""Upload resources from orkg_resources.yml to ORKG as template instances."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from ast import literal_eval
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from orkg import ORKG
from orkg.client.templates.components import Template

ROOT = Path(__file__).resolve().parents[1]
ORKG_DIR = ROOT / "orkg"
DEFAULT_INPUT = ORKG_DIR / "orkg_resources.yml"
DEFAULT_MANIFEST = ROOT / "orkg_upload_manifest.json"
DEFAULT_TEMPLATE_ID = "R1903336"
DEFAULT_TEMPLATE_CLASS = "C138270"  # https://orkg.org/classes/C138270


@dataclass(frozen=True)
class TemplateFieldSpec:
    field_name: str
    predicate_id: str
    max_cardinality: int | None


@dataclass(frozen=True)
class TemplateConfig:
    template_id: str
    template_class: str
    template_name: str
    fields: tuple[TemplateFieldSpec, ...]


def load_resources(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def arxiv_doi(source_url: str) -> str | None:
    match = re.search(r"arxiv\.org/abs/([\d.]+)", source_url, re.I)
    if not match:
        return None
    return f"10.48550/arXiv.{match.group(1)}"


def paper_title(resource: dict[str, Any]) -> str:
    paper = resource.get("paper", {})
    properties = resource.get("properties", {})
    system_name = (properties.get("system_name") or {}).get("value")
    return str(system_name or paper.get("label") or resource.get("id") or "Untitled")


def publication_year(resource: dict[str, Any]) -> int | None:
    years = resource.get("paper", {}).get("catalog_years") or []
    if years:
        return int(min(years))
    return None


def field_definitions(document: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {field["name"]: field for field in document.get("fields", [])}


def load_template_config(client: ORKG, template_id: str) -> TemplateConfig:
    template = Template(client, template_id)
    fields = tuple(
        TemplateFieldSpec(
            field_name=component.get_clean_name(),
            predicate_id=component.predicate_id,
            max_cardinality=component.max_cardinality,
        )
        for component in template.components
    )
    return TemplateConfig(
        template_id=template.template_id,
        template_class=template.template_class,
        template_name=template.template_name,
        fields=fields,
    )


def instance_label(resource: dict[str, Any]) -> str:
    return f"{paper_title(resource)} — retrieval profile"


def template_instance_headers(client: ORKG) -> dict[str, str]:
    return {
        **(client.templates.auth or {}),
        "Content-Type": "application/vnd.orkg.template-instance.v1+json;charset=UTF-8",
        "Accept": "application/vnd.orkg.template-instance.v1+json",
    }


def paper_v2_headers(client: ORKG) -> dict[str, str]:
    return {
        **(client.papers.auth or {}),
        "Content-Type": "application/vnd.orkg.paper.v2+json;charset=UTF-8",
        "Accept": "application/vnd.orkg.paper.v2+json",
    }


def resolve_option_resource_id(
    client: ORKG,
    label: str,
    cache: dict[str, str],
) -> str:
    if label in cache:
        return cache[label]

    found = client.resources.get(q=label, exact=True, size=1)
    if found.succeeded and found.content:
        items = found.content if isinstance(found.content, list) else [found.content]
        for item in items:
            if item.get("label", "").strip() == label.strip():
                resource_id = item["id"]
                cache[label] = resource_id
                return resource_id

    client.backend._append_slash = True
    response = client.backend.resources.POST(
        json={"label": label, "classes": []},
        headers=client.resources.auth,
    )
    if not response.ok:
        raise RuntimeError(f"Failed to create ORKG resource for {label!r}: {response.text}")

    resource_id = extract_id_from_location(response.headers.get("Location", ""))
    if not resource_id:
        wrapped = client.wrap_response(response)
        if isinstance(wrapped.content, dict) and wrapped.content.get("id"):
            resource_id = wrapped.content["id"]
    if not resource_id:
        raise RuntimeError(f"Failed to resolve ORKG resource id for {label!r}")

    cache[label] = resource_id
    return resource_id


def build_template_statements(
    properties: dict[str, Any],
    template_config: TemplateConfig,
    *,
    client: ORKG | None = None,
    option_cache: dict[str, str] | None = None,
) -> dict[str, list[str]]:
    statements: dict[str, list[str]] = {}
    cache = option_cache if option_cache is not None else {}
    counter = 0

    for spec in template_config.fields:
        field = properties.get(spec.field_name) or {}
        value = field.get("value")
        if value is None or value == "" or value == []:
            continue

        values = value if isinstance(value, list) else [value]
        if spec.max_cardinality == 1:
            values = values[:1]

        object_ids: list[str] = []
        for item in values:
            label = str(item)
            if client is not None:
                object_ids.append(resolve_option_resource_id(client, label, cache))
            else:
                counter += 1
                object_ids.append(f"#temp_option_{counter}")

        if object_ids:
            statements[spec.predicate_id] = object_ids

    return statements


def build_template_instance_payload(
    resource: dict[str, Any],
    template_config: TemplateConfig,
    *,
    client: ORKG | None = None,
    option_cache: dict[str, str] | None = None,
) -> dict[str, Any]:
    properties = resource.get("properties", {})
    return {
        "label": instance_label(resource),
        "statements": build_template_statements(
            properties,
            template_config,
            client=client,
            option_cache=option_cache,
        ),
        "extraction_method": "AI_GENERATED_WITH_MANUAL_REVIEW",
    }


def build_paper_payload(resource: dict[str, Any], research_field: str) -> dict[str, Any]:
    paper = resource.get("paper", {})
    source_url = paper.get("source_url", "")
    year = publication_year(resource)
    doi = arxiv_doi(source_url)

    identifiers: dict[str, list[str]] = {}
    if doi:
        identifiers["doi"] = [doi]

    publication_info: dict[str, Any] = {"url": source_url}
    if year:
        publication_info["published_year"] = year

    title = paper_title(resource)

    return {
        "title": title,
        "research_fields": [research_field],
        "identifiers": identifiers,
        "publication_info": publication_info,
        "authors": [
            {
                "id": None,
                "name": "Awesome Retrieval Systems for LLMs",
                "identifiers": None,
                "homepage": "https://github.com/amirrezaalasti/Awesome-Retrieval-Systems-for-LLMs",
            }
        ],
        "contents": {"literals": {}, "predicates": {}, "contributions": []},
        "organizations": [],
        "observatories": [],
        "extraction_method": "AI_GENERATED_WITH_MANUAL_REVIEW",
        "sdgs": None,
    }


def connect_orkg(host: str, email: str, password: str) -> ORKG:
    client = ORKG(host=host, creds=(email, password))
    if not client.ping():
        raise ConnectionError(f"ORKG host unreachable: {host}")
    return client


def extract_paper_id(response: Any) -> str | None:
    if getattr(response, "url", None):
        return str(response.url).rstrip("/").split("/")[-1]
    content = getattr(response, "content", None)
    if isinstance(content, dict) and "id" in content:
        return content["id"]
    return None


def parse_orkg_error(content: Any) -> dict[str, Any] | None:
    if isinstance(content, bytes):
        try:
            content = json.loads(content.decode())
        except json.JSONDecodeError:
            return None
    elif isinstance(content, str):
        raw = content.strip()
        if raw.startswith("b'") or raw.startswith('b"'):
            try:
                content = json.loads(literal_eval(raw))  # noqa: S307
            except (SyntaxError, ValueError, json.JSONDecodeError):
                try:
                    content = json.loads(raw)
                except json.JSONDecodeError:
                    return None
        else:
            try:
                content = json.loads(raw)
            except json.JSONDecodeError:
                return None
    return content if isinstance(content, dict) else None


def paper_list_from_response(content: Any) -> list[dict[str, Any]]:
    if isinstance(content, dict):
        items = content.get("content", content)
        if isinstance(items, list):
            return items
        if items.get("id"):
            return [items]
    if isinstance(content, list):
        return content
    return []


def extract_id_from_location(location: str) -> str | None:
    if not location:
        return None
    resource_id = location.rstrip("/").split("/")[-1]
    return resource_id if resource_id.startswith("R") else None


def create_paper_record(client: ORKG, paper_payload: dict[str, Any]) -> tuple[str | None, dict[str, Any] | None]:
    client.backend._append_slash = False
    response = client.backend.papers.POST(json=paper_payload, headers=paper_v2_headers(client))
    if response.ok:
        paper_id = extract_id_from_location(response.headers.get("Location", ""))
        if paper_id:
            return paper_id, None
    return None, parse_orkg_error(response.content) or {"message": response.text}


def create_template_instance(
    client: ORKG,
    template_id: str,
    instance_payload: dict[str, Any],
) -> tuple[str | None, dict[str, Any] | None]:
    client.backend._append_slash = False
    response = client.backend.templates(template_id).instances.POST(
        json=instance_payload,
        headers=template_instance_headers(client),
    )
    if response.ok:
        instance_id = extract_id_from_location(response.headers.get("Location", ""))
        if instance_id:
            return instance_id, None
    return None, parse_orkg_error(response.content) or {"message": response.text}


def link_paper_contribution(client: ORKG, paper_id: str, instance_id: str) -> dict[str, Any] | None:
    client.backend._append_slash = True
    response = client.backend.statements.POST(
        json={
            "subject_id": paper_id,
            "predicate_id": "P31",
            "object_id": instance_id,
        },
        headers=client.statements.auth,
    )
    if response.ok:
        return None
    return parse_orkg_error(response.content) or {"message": response.text}


def paper_identifier(paper_payload: dict[str, Any]) -> str | None:
    doi_values = (paper_payload.get("identifiers") or {}).get("doi") or []
    return doi_values[0] if doi_values else None


def ensure_paper_id(
    client: ORKG,
    paper_payload: dict[str, Any],
    *,
    on_duplicate: str,
) -> tuple[str | None, str | None, dict[str, Any] | None]:
    identifier = paper_identifier(paper_payload)
    title = paper_payload["title"]
    existing_id = find_existing_paper_id(client, identifier=identifier, title=title)
    if existing_id:
        if on_duplicate == "skip":
            return None, "paper_already_exists", {
                "paper_id": existing_id,
                "duplicate_identifier": identifier,
            }
        if on_duplicate == "error":
            return None, None, {
                "type": "orkg:problem:paper_already_exists",
                "paper_id": existing_id,
                "duplicate_identifier": identifier,
            }
        return existing_id, "merged", None

    paper_id, error = create_paper_record(client, paper_payload)
    if paper_id:
        return paper_id, "created", None

    if error and error.get("type") == "orkg:problem:paper_already_exists":
        identifier = error.get("paper_identifier") or identifier
        existing_id = find_existing_paper_id(client, identifier=identifier, title=title)
        if not existing_id:
            return None, None, {
                "error": "Paper already exists on ORKG, but lookup by identifier/title failed.",
                "duplicate_identifier": identifier,
            }
        if on_duplicate == "skip":
            return None, "paper_already_exists", {
                "paper_id": existing_id,
                "duplicate_identifier": identifier,
            }
        return existing_id, "merged", None

    return None, None, error


def find_existing_paper_id(
    client: ORKG,
    *,
    identifier: str | None,
    title: str,
) -> str | None:
    headers = {
        **(client.papers.auth or {}),
        "Accept": "application/vnd.orkg.paper.v2+json",
    }
    client.backend._append_slash = False

    if identifier:
        head_response = client.backend.papers.HEAD(params={"doi": identifier}, headers=headers)
        if head_response.ok:
            paper_id = extract_id_from_location(head_response.headers.get("Location", ""))
            if paper_id:
                return paper_id

        response = client.papers.by_doi(identifier)
        if response.succeeded:
            papers = paper_list_from_response(response.content)
            if papers:
                return papers[0].get("id")

    response = client.papers.by_title(title)
    if response.succeeded:
        papers = paper_list_from_response(response.content)
        for paper in papers:
            if paper.get("title", paper.get("label", "")).strip().lower() == title.strip().lower():
                return paper.get("id")
        if len(papers) == 1:
            return papers[0].get("id")
    return None


def index_manifest_items(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in items if item.get("id")}


def merge_manifest_items(
    previous_items: list[dict[str, Any]],
    run_items: list[dict[str, Any]],
    *,
    catalog_ids: list[str],
) -> list[dict[str, Any]]:
    merged = index_manifest_items(previous_items)
    merged.update(index_manifest_items(run_items))

    ordered: list[dict[str, Any]] = []
    seen: set[str] = set()
    for resource_id in catalog_ids:
        if resource_id in merged:
            ordered.append(merged[resource_id])
            seen.add(resource_id)
    for resource_id, item in merged.items():
        if resource_id not in seen:
            ordered.append(item)
    return ordered


def manifest_stats(items: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "total": len(items),
        "success": sum(1 for item in items if item.get("status") == "success"),
        "merged": sum(1 for item in items if item.get("action") == "merged"),
        "created": sum(1 for item in items if item.get("action") == "created"),
        "reused": sum(1 for item in items if item.get("action") == "reused"),
        "dry_run_items": sum(1 for item in items if item.get("status") == "dry_run"),
        "errors": sum(1 for item in items if item.get("status") == "error"),
        "skipped": sum(1 for item in items if item.get("status") == "skipped"),
    }


def find_existing_template_instance_on_paper(
    client: ORKG,
    paper_id: str,
    *,
    label: str,
    template_class: str,
) -> str | None:
    paper = client.papers.by_id(paper_id).content
    for contribution in paper.get("contributions", []):
        instance_id = contribution.get("id")
        if not instance_id or contribution.get("label") != label:
            continue
        resource = client.resources.by_id(instance_id)
        if not resource.succeeded:
            continue
        classes = resource.content.get("classes") or []
        if template_class in classes:
            return instance_id
    return None


def paper_has_contribution_link(client: ORKG, paper_id: str, instance_id: str) -> bool:
    statements = client.statements.get_by_subject(subject_id=paper_id, size=200).content
    return any(
        statement.get("predicate", {}).get("id") == "P31"
        and statement.get("object", {}).get("id") == instance_id
        for statement in statements
    )


def upload_resource(
    client: ORKG,
    resource: dict[str, Any],
    *,
    research_field: str,
    template_config: TemplateConfig,
    option_cache: dict[str, str],
    dry_run: bool,
    on_duplicate: str,
) -> dict[str, Any]:
    paper_payload = build_paper_payload(resource, research_field)
    instance_payload = build_template_instance_payload(
        resource,
        template_config,
        client=None if dry_run else client,
        option_cache=option_cache,
    )

    result: dict[str, Any] = {
        "id": resource.get("id"),
        "title": paper_payload["title"],
        "source_url": resource.get("paper", {}).get("source_url"),
        "status": "pending",
        "template_id": template_config.template_id,
        "template_class": template_config.template_class,
    }

    if dry_run:
        result["status"] = "dry_run"
        result["paper_payload"] = paper_payload
        result["template_instance_payload"] = instance_payload
        return result

    paper_id, paper_action, paper_error = ensure_paper_id(
        client,
        paper_payload,
        on_duplicate=on_duplicate,
    )
    if paper_action == "paper_already_exists":
        result["status"] = "skipped"
        result["reason"] = "paper_already_exists"
        result.update(paper_error or {})
        if paper_id and client.host:
            result["orkg_url"] = f"{client.host}/paper/{paper_id}"
        return result
    if paper_error:
        result["status"] = "error"
        result["error"] = paper_error
        return result
    if not paper_id:
        result["status"] = "error"
        result["error"] = "Failed to resolve ORKG paper id."
        return result

    label = instance_payload["label"]
    existing_instance_id = find_existing_template_instance_on_paper(
        client,
        paper_id,
        label=label,
        template_class=template_config.template_class,
    )
    if existing_instance_id:
        if not paper_has_contribution_link(client, paper_id, existing_instance_id):
            link_error = link_paper_contribution(client, paper_id, existing_instance_id)
            if link_error:
                result["status"] = "error"
                result["error"] = link_error
                result["paper_id"] = paper_id
                result["template_instance_id"] = existing_instance_id
                return result
        result["status"] = "success"
        result["action"] = "reused"
        result["paper_id"] = paper_id
        result["template_instance_id"] = existing_instance_id
        result["orkg_url"] = f"{client.host}/paper/{paper_id}" if client.host else None
        result["template_instance_url"] = (
            f"{client.host}/templates/{template_config.template_id}/instances/{existing_instance_id}"
            if client.host
            else None
        )
        result["template_class_url"] = (
            f"{client.host}/classes/{template_config.template_class}?noRedirect"
            if client.host
            else None
        )
        return result

    instance_id, instance_error = create_template_instance(
        client, template_config.template_id, instance_payload
    )
    if instance_error or not instance_id:
        result["status"] = "error"
        result["error"] = instance_error or "Failed to create template instance."
        result["paper_id"] = paper_id
        return result

    link_error = link_paper_contribution(client, paper_id, instance_id)
    if link_error:
        result["status"] = "error"
        result["error"] = link_error
        result["paper_id"] = paper_id
        result["template_instance_id"] = instance_id
        return result

    result["status"] = "success"
    result["action"] = paper_action
    result["paper_id"] = paper_id
    result["template_instance_id"] = instance_id
    result["orkg_url"] = f"{client.host}/paper/{paper_id}" if client.host else None
    result["template_instance_url"] = (
        f"{client.host}/templates/{template_config.template_id}/instances/{instance_id}"
        if client.host
        else None
    )
    result["template_class_url"] = (
        f"{client.host}/classes/{template_config.template_class}?noRedirect"
        if client.host
        else None
    )
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload orkg_resources.yml entries to ORKG (paper first, then properties)"
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--host", default=os.getenv("ORKG_HOST", "https://sandbox.orkg.org"))
    parser.add_argument("--research-field", default=os.getenv("ORKG_RESEARCH_FIELD", "R11"))
    parser.add_argument(
        "--template-id",
        default=os.getenv("ORKG_TEMPLATE_ID", DEFAULT_TEMPLATE_ID),
        help=f"ORKG template id for retrieval profiles (default: {DEFAULT_TEMPLATE_ID})",
    )
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--id", dest="resource_ids", action="append", help="Upload only matching resource id")
    parser.add_argument("--delay", type=float, default=1.0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Upload even if id exists in manifest")
    parser.add_argument(
        "--on-duplicate",
        choices=("merge", "skip", "error"),
        default="merge",
        help="When ORKG already has the paper: add contribution (merge), skip, or fail (default: merge)",
    )
    return parser.parse_args()


def main() -> int:
    load_dotenv(ROOT / ".env")
    args = parse_args()

    email = os.getenv("ORKG_EMAIL")
    password = os.getenv("ORKG_PASSWORD")
    if not args.dry_run and (not email or not password):
        print("Set ORKG_EMAIL and ORKG_PASSWORD in .env for live uploads.", file=sys.stderr)
        return 1

    document = load_resources(args.input)
    resources = document.get("resources", [])

    if args.resource_ids:
        resources = [r for r in resources if r.get("id") in args.resource_ids]
    if args.limit:
        resources = resources[: args.limit]

    previous: dict[str, Any] = {}
    if args.manifest.exists():
        previous = json.loads(args.manifest.read_text(encoding="utf-8"))

    previous_items = previous.get("items", [])
    previous_by_id = index_manifest_items(previous_items)
    catalog_ids = [resource["id"] for resource in document.get("resources", []) if resource.get("id")]

    uploaded_ids = {
        item_id
        for item_id, item in previous_by_id.items()
        if item.get("status") == "success" and item.get("template_instance_id")
    }

    client = None
    option_cache: dict[str, str] = {}
    template_config: TemplateConfig | None = None
    if not args.dry_run:
        client = connect_orkg(args.host, email, password)
        template_config = load_template_config(client, args.template_id)
        if template_config.template_class != DEFAULT_TEMPLATE_CLASS:
            print(
                f"Warning: template {args.template_id} class is "
                f"{template_config.template_class}, expected {DEFAULT_TEMPLATE_CLASS}.",
                file=sys.stderr,
            )
    else:
        template_config = TemplateConfig(
            template_id=args.template_id,
            template_class=DEFAULT_TEMPLATE_CLASS,
            template_name="Awesome Retrieval Systems for LLMs",
            fields=tuple(
                TemplateFieldSpec(field["name"], f"P_{field['name']}", None)
                for field in document.get("fields", [])
                if field.get("type") in {"enum", "multiselect"}
            ),
        )

    run_results: list[dict[str, Any]] = []
    for resource in resources:
        resource_id = resource.get("id")
        if not args.force and resource_id in uploaded_ids:
            prior = previous_by_id.get(resource_id)
            if prior:
                run_results.append(dict(prior))
            else:
                run_results.append({"id": resource_id, "status": "skipped", "reason": "already_uploaded"})
            continue

        print(f"Uploading {resource_id} …")
        try:
            result = upload_resource(
                client,
                resource,
                research_field=args.research_field,
                template_config=template_config,
                option_cache=option_cache,
                dry_run=args.dry_run,
                on_duplicate=args.on_duplicate,
            )
        except Exception as exc:  # noqa: BLE001
            result = {"id": resource_id, "status": "error", "error": str(exc)}
        run_results.append(result)
        if not args.dry_run:
            time.sleep(args.delay)

    merged_items = merge_manifest_items(
        previous_items,
        run_results,
        catalog_ids=catalog_ids,
    )
    totals = manifest_stats(merged_items)
    run_totals = manifest_stats(run_results)

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "host": args.host,
        "research_field": args.research_field,
        "template_id": args.template_id,
        "template_class": template_config.template_class if template_config else DEFAULT_TEMPLATE_CLASS,
        "dry_run_mode": args.dry_run,
        "on_duplicate": args.on_duplicate,
        **totals,
        "last_run": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            **run_totals,
        },
        "items": merged_items,
    }
    args.manifest.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(
        f"\nThis run: {run_totals['success']} uploaded "
        f"({run_totals['created']} created, {run_totals['merged']} merged, "
        f"{run_totals['reused']} reused), "
        f"{run_totals['skipped']} skipped, "
        f"{run_totals['errors']} errors"
    )
    print(
        f"Manifest total: {manifest['success']} success / {manifest['total']} items"
    )
    print(f"Manifest: {args.manifest}")
    return 0 if manifest["errors"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
