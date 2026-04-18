#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

VALID_TEMPORAL_SCOPES = {"current", "past", "future", "mixed"}
VALID_EVIDENCE_STATUS = {"verified", "unverified", "hypothesis"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def check_no_top_level_domain_dirs(root: Path, errors: list[str]) -> None:
    disallowed = {
        "kb-customers",
        "kb-channels",
        "kb-value-proposition",
        "kb-solution",
        "kb-revenue-streams",
        "kb-key-resources",
        "kb-key-activities",
        "kb-key-partners",
        "kb-cost-structure",
        "kb-problem",
        "kb-metrics",
        "kb-unfair-advantage",
    }
    for name in sorted(disallowed):
        candidate = root / name
        if candidate.exists():
            errors.append(
                f"[canonical-path] top-level domain directory must not exist outside KnowledgeBase/: {name}"
            )


def check_markdown_files(root: Path, errors: list[str]) -> None:
    kb_root = root / "KnowledgeBase"
    if not kb_root.exists():
        errors.append("[canonical-path] missing KnowledgeBase/ root")
        return

    email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b")
    temporal_pattern = re.compile(r"temporal_scope\s*:\s*([A-Za-z_-]+)")
    evidence_pattern = re.compile(r"evidence_status\s*:\s*([A-Za-z_-]+)")

    for path in sorted(kb_root.rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        text = read_text(path)

        # Metadata/provenance signal check for canonical domain docs.
        if rel.startswith("KnowledgeBase/kb-") and "/docs/" in rel:
            has_signal = any(
                marker in text
                for marker in (
                    "## Consolidation provenance",
                    "metadata:",
                    "governance_event:",
                    "temporal_scope",
                    "temporal_scope:",
                    "temporal_scope=",
                )
            )
            if not has_signal:
                errors.append(
                    f"[metadata] missing provenance/metadata signal in operational doc: {rel}"
                )

        # Temporal scope enum validation where temporal_scope is declared.
        for match in temporal_pattern.finditer(text):
            scope = match.group(1).strip().lower()
            if scope not in VALID_TEMPORAL_SCOPES:
                errors.append(
                    f"[temporal-scope] invalid value '{scope}' in {rel}; expected one of {sorted(VALID_TEMPORAL_SCOPES)}"
                )

        # Evidence status enum validation where evidence_status is declared.
        for match in evidence_pattern.finditer(text):
            status = match.group(1).strip().lower()
            if status not in VALID_EVIDENCE_STATUS:
                errors.append(
                    f"[evidence-status] invalid value '{status}' in {rel}; expected one of {sorted(VALID_EVIDENCE_STATUS)}"
                )

        # Privacy boundary check for case-focused files.
        if "case" in rel.lower():
            for match in email_pattern.finditer(text):
                domain = match.group(1).lower()
                if domain.endswith("example.com"):
                    continue
                errors.append(
                    f"[privacy] potential email-like identifier found in case-focused file {rel}: {match.group(0)}"
                )


def main() -> int:
    root = repo_root()
    errors: list[str] = []

    check_no_top_level_domain_dirs(root, errors)
    check_markdown_files(root, errors)

    if errors:
        print("kb_canonical_validate: FAILED")
        for item in errors:
            print(f"- {item}")
        return 1

    print("kb_canonical_validate: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
