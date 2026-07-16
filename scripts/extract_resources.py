#!/usr/bin/env python3
"""Extract paper PDFs and software documentation using Docling.

Reads resources.json and writes organized output under extracted/{year}/papers|software/.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter

ROOT = Path(__file__).resolve().parents[1]
ORKG_DIR = ROOT / "orkg"
RESOURCES_PATH = ORKG_DIR / "resources.json"
DEFAULT_OUTPUT = ROOT / "extracted"

SESSION = requests.Session()
SESSION.headers.update(
    {
        "User-Agent": "Awesome-Retrieval-Systems-Extractor/1.0",
        "Accept": "text/html,application/xhtml+xml,application/json,*/*",
    }
)

GITHUB_RE = re.compile(r"https?://github\.com/([^/]+)/([^/?#]+)")
ARXIV_ABS_RE = re.compile(r"arxiv\.org/abs/([\d.]+)")
ARXIV_PDF_RE = re.compile(r"arxiv\.org/pdf/([\d.]+)")


def slugify_url(url: str) -> str:
    parsed = urlparse(url.rstrip("/"))
    host = parsed.netloc.replace(".", "-")
    path = re.sub(r"[^a-zA-Z0-9]+", "-", parsed.path.strip("/")).strip("-")
    query = re.sub(r"[^a-zA-Z0-9]+", "-", (parsed.query or "")).strip("-")
    parts = [p for p in (host, path, query) if p]
    slug = "-".join(parts)
    return slug[:120] or "source"


def load_resources(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def resolve_paper_source(url: str) -> tuple[str | None, str]:
    """Return (download_or_convert_url, source_type)."""
    arxiv_abs = ARXIV_ABS_RE.search(url)
    if arxiv_abs:
        paper_id = arxiv_abs.group(1)
        return f"https://arxiv.org/pdf/{paper_id}.pdf", "arxiv_pdf"

    arxiv_pdf = ARXIV_PDF_RE.search(url)
    if arxiv_pdf:
        return url if url.endswith(".pdf") else f"{url}.pdf", "arxiv_pdf"

    if "proceedings.neurips.cc" in url and "Abstract" in url:
        paper_hash = url.split("/hash/")[-1].split("-")[0]
        return (
            f"https://proceedings.neurips.cc/paper_files/paper/2024/file/{paper_hash}-Paper-Conference.pdf",
            "neurips_pdf",
        )

    if "arxiv.org/search" in url:
        return None, "arxiv_search"

    return url, "web"


def fetch_github_readme(owner: str, repo: str) -> tuple[str | None, dict[str, Any]]:
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    metadata: dict[str, Any] = {"owner": owner, "repo": repo, "api_url": api_url}

    repo_resp = SESSION.get(api_url, timeout=30)
    default_branch = "main"
    if repo_resp.status_code == 200:
        repo_data = repo_resp.json()
        default_branch = repo_data.get("default_branch") or "main"
        metadata.update(
            {
                "name": repo_data.get("name"),
                "full_name": repo_data.get("full_name"),
                "description": repo_data.get("description"),
                "homepage": repo_data.get("homepage"),
                "stars": repo_data.get("stargazers_count"),
                "topics": repo_data.get("topics", []),
                "license": (repo_data.get("license") or {}).get("spdx_id"),
                "default_branch": default_branch,
            }
        )
    elif repo_resp.status_code == 403:
        metadata["api_rate_limited"] = True

    readme_candidates = [
        f"https://raw.githubusercontent.com/{owner}/{repo}/{default_branch}/README.md",
        f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md",
        f"https://raw.githubusercontent.com/{owner}/{repo}/master/README.md",
    ]
    seen_urls: set[str] = set()
    for readme_url in readme_candidates:
        if readme_url in seen_urls:
            continue
        seen_urls.add(readme_url)
        readme_resp = SESSION.get(readme_url, timeout=30)
        if readme_resp.status_code == 200 and readme_resp.text.strip():
            metadata["readme_url"] = readme_url
            return readme_resp.text, metadata

    readme_api = f"https://api.github.com/repos/{owner}/{repo}/readme"
    readme_resp = SESSION.get(
        readme_api, timeout=30, headers={"Accept": "application/vnd.github.raw"}
    )
    if readme_resp.status_code == 200 and readme_resp.text.strip():
        metadata["readme_url"] = readme_api
        return readme_resp.text, metadata

    metadata["readme_error"] = (
        f"HTTP {readme_resp.status_code}" if readme_resp is not None else "not found"
    )
    return None, metadata


def download_binary(url: str, dest: Path) -> None:
    resp = SESSION.get(url, timeout=120, stream=True)
    resp.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)


def convert_with_docling(
    converter: DocumentConverter,
    *,
    source: str | Path | None = None,
    content: str | None = None,
    content_format: InputFormat = InputFormat.MD,
    name: str = "document",
) -> tuple[str, dict[str, Any]]:
    if source is not None:
        result = converter.convert(str(source))
    elif content is not None:
        result = converter.convert_string(content, format=content_format, name=name)
    else:
        raise ValueError("Either source or content must be provided")

    doc = result.document
    markdown = doc.export_to_markdown()
    structured = doc.export_to_dict()
    return markdown, structured


def process_paper(
    converter: DocumentConverter,
    year: int,
    url: str,
    output_dir: Path,
    force: bool,
) -> dict[str, Any]:
    slug = slugify_url(url)
    item_dir = output_dir / str(year) / "papers" / slug
    metadata_path = item_dir / "metadata.json"

    if metadata_path.exists() and not force:
        existing = json.loads(metadata_path.read_text(encoding="utf-8"))
        if existing.get("status") in {"success", "skipped"}:
            retry_skipped = existing.get("status") == "skipped" and (
                existing.get("readme_error", "").startswith("HTTP 403")
                or existing.get("message") == "README not available"
            )
            if not retry_skipped:
                return existing

    item_dir.mkdir(parents=True, exist_ok=True)
    metadata: dict[str, Any] = {
        "year": year,
        "type": "paper",
        "source_url": url,
        "slug": slug,
        "status": "pending",
        "extracted_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        source_url, source_type = resolve_paper_source(url)
        metadata["source_type"] = source_type

        if source_url is None:
            metadata["status"] = "skipped"
            metadata["message"] = "No single PDF available for search/listing URL"
            write_json(metadata_path, metadata)
            return metadata

        if source_type in {"arxiv_pdf", "neurips_pdf"}:
            pdf_path = item_dir / "source.pdf"
            if not pdf_path.exists() or force:
                download_binary(source_url, pdf_path)
            metadata["pdf_path"] = str(pdf_path.relative_to(output_dir))
            markdown, structured = convert_with_docling(converter, source=pdf_path)
        else:
            metadata["resolved_url"] = source_url
            markdown, structured = convert_with_docling(converter, source=source_url)

        (item_dir / "content.md").write_text(markdown, encoding="utf-8")
        write_json(item_dir / "content.json", structured)
        metadata["status"] = "success"
        metadata["content_chars"] = len(markdown)
    except Exception as exc:  # noqa: BLE001 - per-item failure should not stop batch
        metadata["status"] = "error"
        metadata["error"] = str(exc)

    write_json(metadata_path, metadata)
    return metadata


def process_software(
    converter: DocumentConverter,
    year: int,
    url: str,
    output_dir: Path,
    force: bool,
) -> dict[str, Any]:
    slug = slugify_url(url)
    item_dir = output_dir / str(year) / "software" / slug
    metadata_path = item_dir / "metadata.json"

    if metadata_path.exists() and not force:
        existing = json.loads(metadata_path.read_text(encoding="utf-8"))
        if existing.get("status") in {"success", "skipped"}:
            retry_skipped = existing.get("status") == "skipped" and (
                existing.get("readme_error", "").startswith("HTTP 403")
                or existing.get("message") == "README not available"
            )
            if not retry_skipped:
                return existing

    item_dir.mkdir(parents=True, exist_ok=True)
    metadata: dict[str, Any] = {
        "year": year,
        "type": "software",
        "source_url": url,
        "slug": slug,
        "status": "pending",
        "extracted_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        github_match = GITHUB_RE.match(url.rstrip("/"))
        if github_match:
            owner, repo = github_match.group(1), github_match.group(2)
            readme, gh_meta = fetch_github_readme(owner, repo)
            metadata.update(gh_meta)
            metadata["source_type"] = "github"

            if readme:
                (item_dir / "readme.md").write_text(readme, encoding="utf-8")
                markdown, structured = convert_with_docling(
                    converter,
                    content=readme,
                    content_format=InputFormat.MD,
                    name=f"{owner}-{repo}.md",
                )
            else:
                metadata["status"] = "skipped"
                metadata["message"] = "README not available"
                write_json(metadata_path, metadata)
                return metadata
        else:
            metadata["source_type"] = "website"
            markdown, structured = convert_with_docling(converter, source=url)

        (item_dir / "content.md").write_text(markdown, encoding="utf-8")
        write_json(item_dir / "content.json", structured)
        metadata["status"] = "success"
        metadata["content_chars"] = len(markdown)
    except Exception as exc:  # noqa: BLE001
        metadata["status"] = "error"
        metadata["error"] = str(exc)

    write_json(metadata_path, metadata)
    return metadata


def collect_existing_results(output_dir: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for metadata_path in sorted(output_dir.glob("*/papers/*/metadata.json")):
        results.append(json.loads(metadata_path.read_text(encoding="utf-8")))
    for metadata_path in sorted(output_dir.glob("*/software/*/metadata.json")):
        results.append(json.loads(metadata_path.read_text(encoding="utf-8")))
    return results


def build_manifest(results: list[dict[str, Any]], output_dir: Path) -> None:
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(results),
        "success": sum(1 for r in results if r.get("status") == "success"),
        "skipped": sum(1 for r in results if r.get("status") == "skipped"),
        "errors": sum(1 for r in results if r.get("status") == "error"),
        "items": results,
    }
    write_json(output_dir / "manifest.json", summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract resources with Docling")
    parser.add_argument("--resources", type=Path, default=RESOURCES_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--year", type=int, action="append", help="Limit to specific year(s)")
    parser.add_argument("--papers-only", action="store_true")
    parser.add_argument("--software-only", action="store_true")
    parser.add_argument("--limit", type=int, default=0, help="Max items per category per year (0 = all)")
    parser.add_argument("--force", action="store_true", help="Re-extract even if metadata exists")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests (seconds)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    resources = load_resources(args.resources)
    converter = DocumentConverter()
    results: list[dict[str, Any]] = []

    for entry in resources:
        year = entry["year"]
        if args.year and year not in args.year:
            continue

        paper_urls = entry.get("paper", [])
        software_urls = entry.get("software", [])

        if args.limit:
            paper_urls = paper_urls[: args.limit]
            software_urls = software_urls[: args.limit]

        if not args.software_only:
            for url in paper_urls:
                print(f"[paper {year}] {url}")
                result = process_paper(converter, year, url, args.output, args.force)
                results.append(result)
                time.sleep(args.delay)

        if not args.papers_only:
            for url in software_urls:
                print(f"[software {year}] {url}")
                result = process_software(converter, year, url, args.output, args.force)
                results.append(result)
                time.sleep(args.delay)

    build_manifest(collect_existing_results(args.output), args.output)
    results = collect_existing_results(args.output)
    success = sum(1 for r in results if r.get("status") == "success")
    print(f"\nDone: {success}/{len(results)} succeeded. Manifest: {args.output / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
