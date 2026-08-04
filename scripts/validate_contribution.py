#!/usr/bin/env python3
"""Validate paper/resource contribution issues against Readme.md.

Parses GitHub Issue Form bodies, checks field syntax, and detects duplicates
by name, arXiv ID, and GitHub repository URL.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_README = ROOT / "Readme.md"

FIELD_ALIASES: dict[str, str] = {
    "name": "name",
    "paper url": "paper_url",
    "code url": "code_url",
    "project url": "project_url",
    "year": "year",
    "category": "category",
    "description": "description",
    "tags": "tags",
    "resource type": "resource_type",
    "checklist": "checklist",
}

ARXIV_RE = re.compile(
    r"(?:https?://)?(?:www\.)?arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?(?:\.pdf)?",
    re.IGNORECASE,
)
GITHUB_RE = re.compile(
    r"(?:https?://)?(?:www\.)?github\.com/([^/\s?#]+)/([^/\s?#]+)",
    re.IGNORECASE,
)
HTTP_URL_RE = re.compile(r"^https?://[^\s]+$", re.IGNORECASE)
TAG_RE = re.compile(r"`([^`]+)`")
YEAR_RE = re.compile(r"^(19|20)\d{2}$")
NAME_ENTRY_RE = re.compile(r"^\s*-\s+\*\*(?:\[)?([^*\]\n]+)(?:\])?", re.MULTILINE)
HEADING_ENTRY_RE = re.compile(r"^###\s+(.+)$", re.MULTILINE)

SECTION_HEADING_HINTS = {
    "surveys",
    "benchmarks",
    "evaluation",
    "evaluation & benchmarks",
    "vector databases",
    "search infrastructure",
    "embedding models",
    "notable",
    "major trends",
    "emerging directions",
    "representative",
    "research themes",
    "popular frameworks",
    "adding a new entry",
    "inclusion criteria",
}


@dataclass
class Finding:
    level: str  # error | warning | info
    code: str
    message: str


@dataclass
class ValidationResult:
    ok: bool
    kind: str
    fields: dict[str, str] = field(default_factory=dict)
    findings: list[Finding] = field(default_factory=list)
    duplicates: list[dict[str, str]] = field(default_factory=list)
    rendered_entry: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "kind": self.kind,
            "fields": self.fields,
            "findings": [asdict(f) for f in self.findings],
            "duplicates": self.duplicates,
            "rendered_entry": self.rendered_entry,
        }


def parse_issue_body(body: str) -> dict[str, str]:
    """Parse GitHub Issue Form markdown into a field dict."""
    if not body or not body.strip():
        return {}

    parts = re.split(r"^###\s+", body, flags=re.MULTILINE)
    fields: dict[str, str] = {}
    for part in parts:
        part = part.strip()
        if not part:
            continue
        lines = part.splitlines()
        raw_label = lines[0].strip().rstrip(":")
        value = "\n".join(lines[1:]).strip()
        # Issue forms sometimes leave "_No response_" for optional empties.
        if value in {"_No response_", "None", "N/A", "n/a"}:
            value = ""
        key = FIELD_ALIASES.get(raw_label.lower())
        if key:
            fields[key] = value
    return fields


def detect_kind(fields: dict[str, str], labels: list[str] | None, title: str | None) -> str:
    label_set = {label.lower() for label in (labels or [])}
    if "contribution: paper" in label_set or (title or "").lower().startswith("[paper]"):
        return "paper"
    if "contribution: resource" in label_set or (title or "").lower().startswith("[resource]"):
        return "resource"
    if fields.get("paper_url") and not fields.get("code_url") and not fields.get("project_url"):
        return "paper"
    if fields.get("resource_type"):
        return "resource"
    if fields.get("paper_url"):
        return "paper"
    return "resource"


def normalize_arxiv_id(url_or_id: str) -> str | None:
    match = ARXIV_RE.search(url_or_id.strip())
    if match:
        return match.group(1)
    bare = re.fullmatch(r"(\d{4}\.\d{4,5})(?:v\d+)?", url_or_id.strip())
    if bare:
        return bare.group(1)
    return None


def normalize_github_repo(url: str) -> str | None:
    match = GITHUB_RE.search(url.strip())
    if not match:
        return None
    owner = match.group(1).lower()
    repo = match.group(2).lower().removesuffix(".git")
    if owner in {"orgs", "settings", "features", "topics", "sponsors"}:
        return None
    return f"{owner}/{repo}"


def normalize_url(url: str) -> str:
    parsed = urlparse(url.strip())
    host = (parsed.netloc or "").lower().removeprefix("www.")
    path = (parsed.path or "").rstrip("/")
    return f"{host}{path}".lower()


def normalize_name(name: str) -> str:
    text = name.strip().lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s.+-]", "", text)
    return text


def is_valid_http_url(url: str) -> bool:
    if not HTTP_URL_RE.match(url.strip()):
        return False
    parsed = urlparse(url.strip())
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def validate_tags(tags: str) -> list[str]:
    return [tag.strip() for tag in TAG_RE.findall(tags) if tag.strip()]


def _is_section_heading(title: str) -> bool:
    normalized = title.strip().lower()
    # Strip leading emoji / symbols for comparison.
    normalized = re.sub(r"^[^\w]+", "", normalized)
    if not normalized or len(normalized) > 80:
        return True
    if any(hint in normalized for hint in SECTION_HEADING_HINTS):
        return True
    return False


def extract_readme_index(readme_text: str) -> dict[str, Any]:
    arxiv_ids: dict[str, list[int]] = {}
    github_repos: dict[str, list[int]] = {}
    urls: dict[str, list[int]] = {}
    names: dict[str, list[int]] = {}

    for match in NAME_ENTRY_RE.finditer(readme_text):
        name = match.group(1).strip()
        if name:
            names.setdefault(normalize_name(name), []).append(
                readme_text.count("\n", 0, match.start()) + 1
            )

    for match in HEADING_ENTRY_RE.finditer(readme_text):
        title = match.group(1).strip()
        if _is_section_heading(title):
            continue
        names.setdefault(normalize_name(title), []).append(
            readme_text.count("\n", 0, match.start()) + 1
        )

    for match in ARXIV_RE.finditer(readme_text):
        line = readme_text.count("\n", 0, match.start()) + 1
        arxiv_ids.setdefault(match.group(1), []).append(line)

    for match in GITHUB_RE.finditer(readme_text):
        owner = match.group(1).lower()
        repo = match.group(2).lower().removesuffix(".git")
        if owner in {"orgs", "settings", "features", "topics", "sponsors"}:
            continue
        line = readme_text.count("\n", 0, match.start()) + 1
        github_repos.setdefault(f"{owner}/{repo}", []).append(line)

    url_re = re.compile(r"https?://[^\s)\]>`\"']+", re.IGNORECASE)
    for match in url_re.finditer(readme_text):
        line = readme_text.count("\n", 0, match.start()) + 1
        urls.setdefault(normalize_url(match.group(0)), []).append(line)

    return {
        "arxiv_ids": arxiv_ids,
        "github_repos": github_repos,
        "urls": urls,
        "names": names,
    }


def render_entry(kind: str, fields: dict[str, str]) -> str:
    name = fields.get("name", "Project Name").strip()
    lines = [f"- **{name}**"]
    paper_url = fields.get("paper_url", "").strip()
    code_url = fields.get("code_url", "").strip()
    project_url = fields.get("project_url", "").strip()
    description = " ".join(fields.get("description", "").split())
    tags = fields.get("tags", "").strip()

    if paper_url:
        lines.append(f"  - 📄 Paper: {paper_url}")
    if code_url:
        lines.append(f"  - 💻 Code: {code_url}")
    if project_url:
        lines.append(f"  - 🌐 Project: {project_url}")
    if description:
        lines.append(f"  - {description}")
    if tags:
        lines.append(f"  {tags}")
    return "\n".join(lines)


def validate_fields(kind: str, fields: dict[str, str]) -> list[Finding]:
    findings: list[Finding] = []

    name = fields.get("name", "").strip()
    if not name:
        findings.append(Finding("error", "missing_name", "Name is required."))
    elif len(name) < 2:
        findings.append(Finding("error", "short_name", "Name is too short."))
    elif len(name) > 200:
        findings.append(Finding("error", "long_name", "Name must be at most 200 characters."))

    year = fields.get("year", "").strip()
    if not year:
        findings.append(Finding("error", "missing_year", "Year is required."))
    elif not YEAR_RE.match(year):
        findings.append(Finding("error", "invalid_year", f"Year `{year}` is not a valid 4-digit year."))

    category = fields.get("category", "").strip()
    if not category:
        findings.append(Finding("error", "missing_category", "Category is required."))

    description = fields.get("description", "").strip()
    if not description:
        findings.append(Finding("error", "missing_description", "Description is required."))
    elif len(description) < 20:
        findings.append(
            Finding("error", "short_description", "Description should be at least ~20 characters.")
        )
    elif len(description) > 600:
        findings.append(
            Finding("warning", "long_description", "Description is long; prefer 1–2 concise sentences.")
        )

    tags_raw = fields.get("tags", "").strip()
    if not tags_raw:
        findings.append(Finding("error", "missing_tags", "Tags are required."))
    else:
        tags = validate_tags(tags_raw)
        if not tags:
            findings.append(
                Finding(
                    "error",
                    "invalid_tags",
                    "Tags must use backtick syntax, e.g. `RAG` `GraphRAG`.",
                )
            )
        leftover = TAG_RE.sub("", tags_raw).strip()
        if leftover and not re.fullmatch(r"[\s,;|/]+", leftover):
            findings.append(
                Finding(
                    "warning",
                    "tag_noise",
                    f"Unexpected text around tags was ignored: `{leftover}`.",
                )
            )

    paper_url = fields.get("paper_url", "").strip()
    code_url = fields.get("code_url", "").strip()
    project_url = fields.get("project_url", "").strip()

    if kind == "paper":
        if not paper_url:
            findings.append(Finding("error", "missing_paper_url", "Paper URL is required for papers."))
        elif not is_valid_http_url(paper_url):
            findings.append(Finding("error", "invalid_paper_url", f"Paper URL is invalid: `{paper_url}`"))
        elif normalize_arxiv_id(paper_url) is None and "arxiv.org" in paper_url.lower():
            findings.append(
                Finding(
                    "error",
                    "invalid_arxiv",
                    "arXiv URL must look like `https://arxiv.org/abs/xxxx.xxxxx`.",
                )
            )
        elif normalize_arxiv_id(paper_url) is None:
            findings.append(
                Finding(
                    "warning",
                    "non_arxiv_paper",
                    "Paper URL is not an arXiv abs/pdf link; preferred when available.",
                )
            )
    else:
        if not code_url and not project_url:
            findings.append(
                Finding(
                    "error",
                    "missing_resource_link",
                    "Resources require at least a Code URL or Project URL.",
                )
            )
        if paper_url and not is_valid_http_url(paper_url):
            findings.append(Finding("error", "invalid_paper_url", f"Paper URL is invalid: `{paper_url}`"))

    for label, url in (("code_url", code_url), ("project_url", project_url)):
        if not url:
            continue
        if not is_valid_http_url(url):
            findings.append(Finding("error", f"invalid_{label}", f"Invalid URL: `{url}`"))
        elif label == "code_url" and "github.com" in url.lower() and normalize_github_repo(url) is None:
            findings.append(
                Finding(
                    "error",
                    "invalid_github",
                    "GitHub Code URL must look like `https://github.com/owner/repo`.",
                )
            )

    if kind == "resource" and not fields.get("resource_type", "").strip():
        findings.append(
            Finding("warning", "missing_resource_type", "Resource Type was not provided.")
        )

    return findings


def find_duplicates(fields: dict[str, str], index: dict[str, Any]) -> list[dict[str, str]]:
    duplicates: list[dict[str, str]] = []

    name = normalize_name(fields.get("name", ""))
    if name and name in index["names"]:
        for line in index["names"][name]:
            duplicates.append(
                {
                    "type": "name",
                    "value": fields.get("name", "").strip(),
                    "line": str(line),
                }
            )

    paper_url = fields.get("paper_url", "").strip()
    arxiv_id = normalize_arxiv_id(paper_url) if paper_url else None
    if arxiv_id and arxiv_id in index["arxiv_ids"]:
        for line in index["arxiv_ids"][arxiv_id]:
            duplicates.append(
                {
                    "type": "arxiv",
                    "value": arxiv_id,
                    "line": str(line),
                }
            )

    covered_lines: set[str] = {item["line"] for item in duplicates}

    for url_field in ("code_url", "project_url", "paper_url"):
        url = fields.get(url_field, "").strip()
        if not url:
            continue
        repo = normalize_github_repo(url)
        if repo and repo in index["github_repos"]:
            for line in index["github_repos"][repo]:
                duplicates.append(
                    {
                        "type": "github",
                        "value": repo,
                        "line": str(line),
                    }
                )
                covered_lines.add(str(line))
            continue

        # Avoid double-reporting arXiv abs/pdf URLs already caught by arxiv id.
        if normalize_arxiv_id(url):
            continue

        normalized = normalize_url(url)
        if normalized and normalized in index["urls"]:
            for line in index["urls"][normalized]:
                if str(line) in covered_lines:
                    continue
                duplicates.append(
                    {
                        "type": "url",
                        "value": url,
                        "line": str(line),
                    }
                )

    # Deduplicate identical findings.
    seen: set[tuple[str, str, str]] = set()
    unique: list[dict[str, str]] = []
    for item in duplicates:
        key = (item["type"], item["value"], item["line"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique


def validate_contribution(
    body: str,
    readme_path: Path = DEFAULT_README,
    labels: list[str] | None = None,
    title: str | None = None,
) -> ValidationResult:
    fields = parse_issue_body(body)
    kind = detect_kind(fields, labels, title)
    findings = validate_fields(kind, fields)

    duplicates: list[dict[str, str]] = []
    if readme_path.exists():
        index = extract_readme_index(readme_path.read_text(encoding="utf-8"))
        duplicates = find_duplicates(fields, index)
    else:
        findings.append(
            Finding("error", "missing_readme", f"README not found at `{readme_path}`.")
        )

    if duplicates:
        findings.append(
            Finding(
                "error",
                "duplicate",
                f"Found {len(duplicates)} possible duplicate match(es) in Readme.md.",
            )
        )

    has_errors = any(f.level == "error" for f in findings)
    return ValidationResult(
        ok=not has_errors,
        kind=kind,
        fields=fields,
        findings=findings,
        duplicates=duplicates,
        rendered_entry=render_entry(kind, fields) if fields.get("name") else "",
    )


def render_markdown_report(result: ValidationResult) -> str:
    status = "✅ Validation passed" if result.ok else "❌ Validation failed"
    lines = [
        "## Contribution validation",
        "",
        f"**Status:** {status}",
        f"**Type:** `{result.kind}`",
        "",
    ]

    errors = [f for f in result.findings if f.level == "error"]
    warnings = [f for f in result.findings if f.level == "warning"]

    if errors:
        lines.append("### Errors")
        for item in errors:
            lines.append(f"- `{item.code}`: {item.message}")
        lines.append("")

    if warnings:
        lines.append("### Warnings")
        for item in warnings:
            lines.append(f"- `{item.code}`: {item.message}")
        lines.append("")

    if result.duplicates:
        lines.append("### Possible duplicates in `Readme.md`")
        for dup in result.duplicates:
            lines.append(f"- **{dup['type']}** `{dup['value']}` (line {dup['line']})")
        lines.append("")

    if result.rendered_entry:
        year = result.fields.get("year", "YYYY")
        category = result.fields.get("category", "Category")
        lines.extend(
            [
                "### Suggested README snippet",
                "",
                f"Place under **{year} → {category}**:",
                "",
                "```markdown",
                result.rendered_entry,
                "```",
                "",
            ]
        )

    if result.ok:
        lines.append(
            "_Maintainers: this issue looks ready to turn into a PR. "
            "Please confirm category placement before merging._"
        )
    else:
        lines.append(
            "_Please edit this issue to fix the errors above. "
            "Validation will re-run automatically on update._"
        )

    return "\n".join(lines).rstrip() + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--body-file",
        type=Path,
        help="Path to a file containing the issue body. Use - for stdin.",
    )
    parser.add_argument("--body", help="Raw issue body string.")
    parser.add_argument("--title", default="", help="Issue title (used to detect kind).")
    parser.add_argument(
        "--labels",
        default="",
        help="Comma-separated issue labels.",
    )
    parser.add_argument(
        "--readme",
        type=Path,
        default=DEFAULT_README,
        help="Path to Readme.md",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        help="Optional path to write machine-readable JSON results.",
    )
    parser.add_argument(
        "--markdown-out",
        type=Path,
        help="Optional path to write the markdown report.",
    )
    parser.add_argument(
        "--fail-on-duplicate",
        action="store_true",
        default=True,
        help="Treat duplicates as validation failures (default: true).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.body is not None:
        body = args.body
    elif args.body_file is not None:
        if str(args.body_file) == "-":
            body = sys.stdin.read()
        else:
            body = args.body_file.read_text(encoding="utf-8")
    else:
        parser.error("Provide --body or --body-file")

    labels = [part.strip() for part in args.labels.split(",") if part.strip()]
    result = validate_contribution(
        body=body,
        readme_path=args.readme,
        labels=labels,
        title=args.title,
    )
    report = render_markdown_report(result)

    if args.json_out:
        args.json_out.write_text(json.dumps(result.to_dict(), indent=2) + "\n", encoding="utf-8")
    if args.markdown_out:
        args.markdown_out.write_text(report, encoding="utf-8")

    print(report)
    if result.ok:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
