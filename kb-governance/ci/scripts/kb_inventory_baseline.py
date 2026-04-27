#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NUMBERED_DOC_FILENAME = re.compile(r"^\d{2}-.+\.md$")
README_INDEX_ROW = re.compile(r"^\|\s*\d+\s*\|\s*`([^`]+)`\s*\|", re.MULTILINE)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def normalize_relative_paths(paths: list[Path], root: Path) -> list[str]:
    return sorted(path.relative_to(root).as_posix() for path in paths)


def collect_inventory(root: Path) -> dict[str, object]:
    kb_root = root / "KnowledgeBase"
    if not kb_root.exists():
        raise FileNotFoundError("missing KnowledgeBase/ root")

    top_level_md_files = sorted(path.name for path in kb_root.glob("*.md"))
    top_level_numbered_docs = [
        name for name in top_level_md_files if NUMBERED_DOC_FILENAME.fullmatch(name)
    ]
    top_level_non_numbered_docs = [
        name for name in top_level_md_files if name not in top_level_numbered_docs
    ]

    canonical_domain_docs = normalize_relative_paths(
        list(kb_root.glob("kb-*/docs/**/*.md")),
        root,
    )

    templates_root = kb_root / "templates"
    template_docs = (
        normalize_relative_paths(list(templates_root.glob("*.md")), root)
        if templates_root.exists()
        else []
    )

    domain_coverage: dict[str, dict[str, object]] = {}
    for domain_dir in sorted(path for path in kb_root.glob("kb-*") if path.is_dir()):
        docs = normalize_relative_paths(list(domain_dir.glob("docs/**/*.md")), root)
        domain_coverage[domain_dir.name] = {
            "docs_count": len(docs),
            "docs": docs,
        }

    readme_missing_top_level_targets: list[str] = []
    readme_path = kb_root / "README.md"
    if readme_path.exists():
        readme_text = read_text(readme_path)
        for rel_target in README_INDEX_ROW.findall(readme_text):
            if not (kb_root / rel_target).exists():
                readme_missing_top_level_targets.append(rel_target)

    return {
        "kb_root": "KnowledgeBase",
        "legacy_top_level_numbered_count": len(top_level_numbered_docs),
        "legacy_top_level_numbered_docs": top_level_numbered_docs,
        "legacy_top_level_non_numbered_count": len(top_level_non_numbered_docs),
        "legacy_top_level_non_numbered_docs": top_level_non_numbered_docs,
        "canonical_domain_doc_count": len(canonical_domain_docs),
        "canonical_domain_docs": canonical_domain_docs,
        "template_doc_count": len(template_docs),
        "template_docs": template_docs,
        "domain_coverage": domain_coverage,
        "readme_missing_top_level_targets": sorted(set(readme_missing_top_level_targets)),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate baseline inventory for legacy-to-canonical KB migration."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root path to inspect (defaults to auto-detected repo root).",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=None,
        help="Output path for inventory JSON report (relative paths resolve from repo root).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve() if args.root is not None else repo_root()

    try:
        report = collect_inventory(root)
    except FileNotFoundError as error:
        print(f"kb_inventory_baseline: FAILED ({error})")
        return 1

    report["generator"] = "kb_inventory_baseline.py"
    report["repo_root"] = root.as_posix()

    if args.output_json is not None:
        output_path = args.output_json
        if not output_path.is_absolute():
            output_path = root / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        printable = (
            output_path.relative_to(root).as_posix()
            if output_path.is_relative_to(root)
            else output_path.as_posix()
        )
        print(f"kb_inventory_baseline: WROTE {printable}")
    else:
        print(json.dumps(report, indent=2, sort_keys=True))

    return 0


if __name__ == "__main__":
    sys.exit(main())
