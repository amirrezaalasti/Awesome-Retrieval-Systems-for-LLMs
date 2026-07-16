"""Verify LLM-provided evidence quotes against source documents."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher


@dataclass
class VerificationResult:
    found: bool
    score: float
    method: str
    matched_span: str | None = None


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text


def _best_fuzzy_span(reference: str, document: str, window_pad: int = 40) -> tuple[float, str | None]:
  ref_norm = normalize_text(reference)
  if not ref_norm:
      return 0.0, None

  doc_norm = normalize_text(document)
  ref_len = len(ref_norm)
  if ref_len == 0:
      return 0.0, None

  best_score = 0.0
  best_span: str | None = None

  # Slide over normalized document with windows sized around the reference length.
  step = max(8, ref_len // 6)
  max_window = min(len(doc_norm), ref_len + window_pad * 2)
  for start in range(0, max(1, len(doc_norm) - ref_len + 1), step):
      for window in range(max(ref_len, ref_len - window_pad), max_window + 1, max(12, ref_len // 4)):
          end = min(len(doc_norm), start + window)
          candidate = doc_norm[start:end]
          score = SequenceMatcher(None, ref_norm, candidate).ratio()
          if score > best_score:
              best_score = score
              raw_start = max(0, start - 20)
              raw_end = min(len(document), end + 20)
              best_span = document[raw_start:raw_end].strip()

  return best_score, best_span


def verify_reference(
    reference: str,
    document: str,
    *,
    exact_threshold: float = 1.0,
    fuzzy_threshold: float = 0.82,
) -> VerificationResult:
    if not reference or not reference.strip():
        return VerificationResult(found=False, score=0.0, method="empty_reference")

    ref = reference.strip()
    if ref in document:
        return VerificationResult(found=True, score=1.0, method="exact", matched_span=ref)

    ref_norm = normalize_text(ref)
    doc_norm = normalize_text(document)
    if ref_norm and ref_norm in doc_norm:
        return VerificationResult(found=True, score=0.99, method="normalized_exact", matched_span=ref)

    fuzzy_score, span = _best_fuzzy_span(ref, document)
    if fuzzy_score >= fuzzy_threshold:
        return VerificationResult(
            found=True,
            score=round(fuzzy_score, 4),
            method="fuzzy",
            matched_span=span,
        )

    token_ref = set(re.findall(r"[a-z0-9]+", ref_norm))
    token_doc = set(re.findall(r"[a-z0-9]+", doc_norm))
    if token_ref:
        overlap = len(token_ref & token_doc) / len(token_ref)
        if overlap >= 0.9:
            return VerificationResult(
                found=True,
                score=round(overlap, 4),
                method="token_overlap",
                matched_span=ref,
            )
        if overlap >= 0.75:
            return VerificationResult(
                found=False,
                score=round(overlap, 4),
                method="token_overlap_partial",
                matched_span=ref,
            )

    return VerificationResult(found=False, score=round(fuzzy_score, 4), method="fuzzy", matched_span=span)
