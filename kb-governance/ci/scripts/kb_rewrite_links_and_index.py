#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from kb_migrate_legacy_docs import parse_manifest_entries

README_INDEX_ROW_RE = re.compile(r"^(\|\s*(\d+)\s*\|\s*`)([^`]+)(`\s*\|.*)$")
NUMBERED_DOC_FILENAME = re.compile(r"^\d{2}-.+\.md$")
BACKTICK_FILE_REF_RE = re.compile(r"`([^`\n]+\.md)`")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def rel_to_kb(path: str) -> str:
    return path[len("KnowledgeBase/") :] if path.startswith("KnowledgeBase/") else path


def discover_numbered_canonical_paths(kb_root: Path) -> dict[str, str]:
    discovered: dict[str, str] = {}
    for path in sorted(kb_root.glob("kb-*/docs/**/*.md")):
        match = re.match(r"^(\d{2})-", path.name)
        if not match:
            continue
        number = match.group(1)
        if number not in discovered:
            discovered[number] = path.relative_to(kb_root).as_posix()
    return discovered


def build_manifest_maps(root: Path) -> tuple[dict[str, str], dict[str, str]]:
    manifest_path = root / "kb-governance" / "migration" / "kb-legacy-map-v1.yaml"
    if not manifest_path.exists():
        return {}, {}

    entries = parse_manifest_entries(manifest_path)
    by_legacy_rel: dict[str, str] = {}
    by_legacy_basename: dict[str, str] = {}
    for entry in entries:
        if not entry.legacy_path.startswith("KnowledgeBase/"):
            continue
        legacy_rel = rel_to_kb(entry.legacy_path)
        canonical_rel = rel_to_kb(entry.canonical_path)
        by_legacy_rel[legacy_rel] = canonical_rel
        by_legacy_basename[Path(legacy_rel).name] = canonical_rel
    return by_legacy_rel, by_legacy_basename


def resolve_readme_index_path(
    raw_path: str,
    by_legacy_rel: dict[str, str],
    by_legacy_basename: dict[str, str],
    numbered_canonical: dict[str, str],
) -> str:
    normalized = rel_to_kb(raw_path)
    if normalized in by_legacy_rel:
        return by_legacy_rel[normalized]

    basename = Path(normalized).name
    if basename in by_legacy_basename and normalized == basename:
        return by_legacy_basename[basename]

    number_match = re.match(r"^(\d{2})-", basename)
    if number_match:
        mapped = numbered_canonical.get(number_match.group(1))
        if mapped is not None:
            return mapped

    return normalized


def rewrite_readme(
    root: Path,
    readme_path: Path,
    by_legacy_rel: dict[str, str],
    by_legacy_basename: dict[str, str],
    numbered_canonical: dict[str, str],
) -> dict[str, object]:
    original_text = read_text(readme_path)
    lines = original_text.splitlines()
    kb_root = root / "KnowledgeBase"

    rewritten_rows = 0
    removed_rows = 0
    removed_row_paths: list[str] = []
    output_lines: list[str] = []

    for line in lines:
        match = README_INDEX_ROW_RE.match(line)
        if match is None:
            output_lines.append(line)
            continue

        path_value = match.group(3).strip()
        resolved = resolve_readme_index_path(
            path_value,
            by_legacy_rel,
            by_legacy_basename,
            numbered_canonical,
        )
        target_path = kb_root / resolved
        if resolved != path_value:
            rewritten_rows += 1

        if not target_path.exists():
            removed_rows += 1
            removed_row_paths.append(path_value)
            continue

        output_lines.append(f"{match.group(1)}{resolved}{match.group(4)}")

    rewritten_text = "\n".join(output_lines).rstrip() + "\n"
    cutover_note = (
        "> Legacy top-level files are compatibility stubs. The canonical source-of-truth paths listed below are under `kb-*/docs/...`.\n"
    )
    if cutover_note not in rewritten_text and "## File Index\n" in rewritten_text:
        rewritten_text = rewritten_text.replace(
            "## File Index\n\n",
            f"## File Index\n\n{cutover_note}\n",
            1,
        )

    changed = rewritten_text != original_text
    if changed:
        write_text(readme_path, rewritten_text)

    return {
        "path": readme_path.relative_to(root).as_posix(),
        "changed": changed,
        "rewritten_rows": rewritten_rows,
        "removed_rows": removed_rows,
        "removed_row_paths": removed_row_paths,
    }


def rewrite_wiki_seed_file(
    root: Path,
    file_path: Path,
    by_legacy_basename: dict[str, str],
) -> dict[str, object]:
    original_text = read_text(file_path)
    rewritten_text = original_text

    replacement_count = 0
    for legacy_basename, canonical_rel in by_legacy_basename.items():
        full_legacy = f"KnowledgeBase/{legacy_basename}"
        full_canonical = f"KnowledgeBase/{canonical_rel}"

        if f"`{full_legacy}`" in rewritten_text:
            rewritten_text = rewritten_text.replace(
                f"`{full_legacy}`",
                f"`{full_canonical}`",
            )
            replacement_count += 1
        if f"`{legacy_basename}`" in rewritten_text:
            rewritten_text = rewritten_text.replace(
                f"`{legacy_basename}`",
                f"`{full_canonical}`",
            )
            replacement_count += 1

    changed = rewritten_text != original_text
    if changed:
        write_text(file_path, rewritten_text)

    return {
        "path": file_path.relative_to(root).as_posix(),
        "changed": changed,
        "replacements": replacement_count,
    }


def verify_readme_index(root: Path, readme_path: Path) -> list[str]:
    kb_root = root / "KnowledgeBase"
    errors: list[str] = []
    for line in read_text(readme_path).splitlines():
        match = README_INDEX_ROW_RE.match(line)
        if match is None:
            continue
        file_path = match.group(3).strip()
        normalized = rel_to_kb(file_path)
        if NUMBERED_DOC_FILENAME.fullmatch(Path(normalized).name) and "/" not in normalized:
            errors.append(
                f"[index-cutover] README File Index still points to top-level legacy path: {file_path}"
            )
            continue
        if not (kb_root / normalized).exists():
            errors.append(
                f"[index-cutover] README File Index path does not exist: {file_path}"
            )
    return errors


def verify_wiki_references(root: Path, wiki_files: list[Path]) -> list[str]:
    errors: list[str] = []
    for wiki_file in wiki_files:
        for reference in BACKTICK_FILE_REF_RE.findall(read_text(wiki_file)):
            normalized = reference
            candidate = root / normalized
            if not candidate.exists():
                if normalized.startswith("KnowledgeBase/"):
                    errors.append(
                        f"[index-cutover] wiki reference does not exist in {wiki_file.relative_to(root).as_posix()}: {reference}"
                    )
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rewrite and verify KB README/wiki indexes against canonical migration mappings."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root path (defaults to auto-detected repo root).",
    )
    parser.add_argument(
        "--mode",
        choices=("apply", "verify"),
        default="verify",
        help="Whether to rewrite files (apply) or only verify cutover compliance.",
    )
    parser.add_argument(
        "--report-json",
        type=Path,
        default=None,
        help="Optional report output path (relative paths resolve from repo root).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve() if args.root is not None else repo_root()

    kb_root = root / "KnowledgeBase"
    readme_path = kb_root / "README.md"
    wiki_files = [
        root / "kb-governance" / "wiki-seed" / "Home.md",
        root / "kb-governance" / "wiki-seed" / "Domain-Index.md",
        root / "kb-governance" / "wiki-seed" / "Governance-Index.md",
    ]

    by_legacy_rel, by_legacy_basename = build_manifest_maps(root)
    numbered_canonical = discover_numbered_canonical_paths(kb_root)

    report: dict[str, object] = {
        "mode": args.mode,
        "files": [],
        "errors": [],
    }

    if args.mode == "apply":
        if readme_path.exists():
            report["files"].append(
                rewrite_readme(
                    root,
                    readme_path,
                    by_legacy_rel,
                    by_legacy_basename,
                    numbered_canonical,
                )
            )
        for wiki_file in wiki_files:
            if wiki_file.exists():
                report["files"].append(
                    rewrite_wiki_seed_file(
                        root,
                        wiki_file,
                        by_legacy_basename,
                    )
                )

    errors: list[str] = []
    if readme_path.exists():
        errors.extend(verify_readme_index(root, readme_path))
    errors.extend(verify_wiki_references(root, [path for path in wiki_files if path.exists()]))
    report["errors"] = errors

    if args.report_json is not None:
        report_path = args.report_json if args.report_json.is_absolute() else root / args.report_json
        write_text(report_path, json.dumps(report, indent=2, sort_keys=True) + "\n")

    if errors:
        print("kb_rewrite_links_and_index: FAILED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    print("kb_rewrite_links_and_index: PASSED")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
