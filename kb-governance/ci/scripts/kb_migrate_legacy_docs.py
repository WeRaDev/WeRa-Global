#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ENTRY_START_RE = re.compile(r"^\s*-\s+legacy_path:\s*(.+)\s*$")
FIELD_RE = re.compile(r"^\s{4}([a-z_]+):\s*(.+)\s*$")


@dataclass(frozen=True)
class ManifestEntry:
    legacy_path: str
    canonical_path: str
    primary_domain: str
    doc_class: str
    migration_mode: str
    required_metadata_profile: str
    owner_role: str
    temporal_scope: str
    status: str


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


def clean_yaml_scalar(value: str) -> str:
    cleaned = value.split(" #", 1)[0].strip()
    if cleaned.startswith(("'", '"')) and cleaned.endswith(("'", '"')) and len(cleaned) >= 2:
        cleaned = cleaned[1:-1]
    return cleaned


def parse_manifest_entries(manifest_path: Path) -> list[ManifestEntry]:
    text = read_text(manifest_path)
    lines = text.splitlines()

    in_entries = False
    current: dict[str, str] | None = None
    entries: list[dict[str, str]] = []

    for line in lines:
        if not in_entries:
            if line.strip() == "entries:":
                in_entries = True
            continue

        start_match = ENTRY_START_RE.match(line)
        if start_match:
            if current is not None:
                entries.append(current)
            current = {"legacy_path": clean_yaml_scalar(start_match.group(1))}
            continue

        if current is None:
            continue

        field_match = FIELD_RE.match(line)
        if field_match:
            key = field_match.group(1).strip()
            value = clean_yaml_scalar(field_match.group(2))
            current[key] = value
            continue

        if line and not line.startswith(" "):
            break

    if current is not None:
        entries.append(current)

    required_fields = {
        "legacy_path",
        "canonical_path",
        "primary_domain",
        "doc_class",
        "migration_mode",
        "required_metadata_profile",
        "owner_role",
        "temporal_scope",
        "status",
    }

    parsed: list[ManifestEntry] = []
    for raw in entries:
        missing = sorted(required_fields - set(raw))
        if missing:
            raise ValueError(
                f"manifest entry for {raw.get('legacy_path', '<unknown>')} missing required fields: {missing}"
            )
        parsed.append(
            ManifestEntry(
                legacy_path=raw["legacy_path"],
                canonical_path=raw["canonical_path"],
                primary_domain=raw["primary_domain"],
                doc_class=raw["doc_class"],
                migration_mode=raw["migration_mode"],
                required_metadata_profile=raw["required_metadata_profile"],
                owner_role=raw["owner_role"],
                temporal_scope=raw["temporal_scope"],
                status=raw["status"],
            )
        )
    return parsed


def is_compatibility_stub(text: str) -> bool:
    return "canonical_reference:" in text and "deprecation:" in text


def inject_consolidation_provenance(source_text: str, source_rel_path: str, today: str) -> str:
    if "## Consolidation provenance" in source_text:
        return source_text if source_text.endswith("\n") else f"{source_text}\n"

    lines = source_text.splitlines()
    provenance_block = [
        "",
        "## Consolidation provenance",
        "- consolidation_actor: `WARP`",
        f"- consolidation_source: `{source_rel_path}`",
        f"- consolidation_date: `{today}`",
        "- consolidation_status: `canonicalized`",
        "",
    ]

    heading_index = -1
    for index, line in enumerate(lines):
        if line.lstrip().startswith("#"):
            heading_index = index
            break

    if heading_index >= 0:
        merged = lines[: heading_index + 1] + provenance_block + lines[heading_index + 1 :]
    else:
        merged = provenance_block[1:] + lines

    return "\n".join(merged).rstrip() + "\n"


def build_compatibility_stub(entry: ManifestEntry, today: str) -> str:
    title = Path(entry.legacy_path).name
    return (
        f"# Compatibility Stub — {title}\n\n"
        "This legacy path is retained for compatibility during KB canonicalization.\n\n"
        "canonical_reference:\n"
        f"  path: {entry.canonical_path}\n"
        "  status: canonical\n"
        f"  last_verified: {today}\n\n"
        "migration:\n"
        f"  source: {entry.legacy_path}\n"
        f"  mode: {entry.migration_mode}\n"
        f"  owner_role: {entry.owner_role}\n\n"
        "deprecation:\n"
        "  policy: mirror-stub-until-phase-c-cutover\n"
        "  cutover_target: remove-after-readme-canonical-switch\n"
        "  owner: migration steward\n"
    )


def select_entries(
    entries: list[ManifestEntry],
    statuses: set[str],
    migration_modes: set[str],
    legacy_paths: set[str] | None,
) -> list[ManifestEntry]:
    selected: list[ManifestEntry] = []
    for entry in entries:
        if entry.status not in statuses:
            continue
        if entry.migration_mode not in migration_modes:
            continue
        if legacy_paths is not None and entry.legacy_path not in legacy_paths:
            continue
        selected.append(entry)
    return selected


def update_manifest_statuses(
    manifest_path: Path,
    migrated_legacy_paths: set[str],
) -> None:
    lines = read_text(manifest_path).splitlines()
    output: list[str] = []
    current_legacy_path: str | None = None

    for line in lines:
        start_match = ENTRY_START_RE.match(line)
        if start_match:
            current_legacy_path = clean_yaml_scalar(start_match.group(1))
            output.append(line)
            continue

        status_match = re.match(r"^(\s{4}status:\s*)(\S+)\s*$", line)
        if (
            status_match
            and current_legacy_path is not None
            and current_legacy_path in migrated_legacy_paths
        ):
            output.append(f"{status_match.group(1)}canonicalized")
            continue

        output.append(line)

    write_text(manifest_path, "\n".join(output).rstrip() + "\n")


def run_dry_run(root: Path, entries: list[ManifestEntry]) -> dict[str, object]:
    operations: list[dict[str, str]] = []
    for entry in entries:
        source = root / entry.legacy_path
        target = root / entry.canonical_path
        operation = {
            "legacy_path": entry.legacy_path,
            "canonical_path": entry.canonical_path,
            "source_exists": "yes" if source.exists() else "no",
            "target_exists": "yes" if target.exists() else "no",
            "migration_mode": entry.migration_mode,
            "status": entry.status,
        }
        operations.append(operation)
    return {
        "mode": "dry-run",
        "selected_entry_count": len(entries),
        "operations": operations,
    }


def run_apply(
    root: Path,
    manifest_path: Path,
    entries: list[ManifestEntry],
    today: str,
) -> dict[str, object]:
    migrated_legacy_paths: set[str] = set()
    operations: list[dict[str, str]] = []
    failures: list[str] = []

    for entry in entries:
        source = root / entry.legacy_path
        target = root / entry.canonical_path

        if not source.exists():
            failures.append(f"missing source for migration: {entry.legacy_path}")
            continue

        source_text = read_text(source)

        if not target.exists():
            if is_compatibility_stub(source_text):
                failures.append(
                    f"source already stubbed but target missing for {entry.legacy_path}"
                )
                continue
            canonical_text = inject_consolidation_provenance(
                source_text,
                entry.legacy_path,
                today,
            )
            write_text(target, canonical_text)

        refreshed_source_text = read_text(source)
        if not is_compatibility_stub(refreshed_source_text):
            write_text(source, build_compatibility_stub(entry, today))

        migrated_legacy_paths.add(entry.legacy_path)
        operations.append(
            {
                "legacy_path": entry.legacy_path,
                "canonical_path": entry.canonical_path,
                "result": "migrated",
            }
        )

    if migrated_legacy_paths:
        update_manifest_statuses(manifest_path, migrated_legacy_paths)

    return {
        "mode": "apply",
        "selected_entry_count": len(entries),
        "migrated_count": len(migrated_legacy_paths),
        "operations": operations,
        "failures": failures,
    }


def run_verify(root: Path, entries: list[ManifestEntry]) -> dict[str, object]:
    failures: list[str] = []
    checks: list[dict[str, str]] = []

    for entry in entries:
        source = root / entry.legacy_path
        target = root / entry.canonical_path
        target_ok = target.exists()
        source_stub_ok = source.exists() and is_compatibility_stub(read_text(source))
        provenance_ok = (
            target_ok and "## Consolidation provenance" in read_text(target)
        )

        checks.append(
            {
                "legacy_path": entry.legacy_path,
                "canonical_path": entry.canonical_path,
                "target_exists": "yes" if target_ok else "no",
                "source_is_stub": "yes" if source_stub_ok else "no",
                "target_has_provenance": "yes" if provenance_ok else "no",
            }
        )

        if not target_ok:
            failures.append(f"missing canonical target: {entry.canonical_path}")
        if not source_stub_ok:
            failures.append(f"legacy source is not compatibility stub: {entry.legacy_path}")
        if not provenance_ok:
            failures.append(
                f"canonical target missing consolidation provenance: {entry.canonical_path}"
            )

    return {
        "mode": "verify",
        "selected_entry_count": len(entries),
        "checks": checks,
        "failures": failures,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Manifest-driven migration runner for KB legacy-to-canonical consolidation."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root path (defaults to auto-detected repo root).",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("kb-governance/migration/kb-legacy-map-v1.yaml"),
        help="Manifest path (relative paths resolve from repo root).",
    )
    parser.add_argument(
        "--mode",
        choices=("dry-run", "apply", "verify"),
        default="dry-run",
        help="Execution mode.",
    )
    parser.add_argument(
        "--statuses",
        default="planned",
        help="Comma-separated manifest statuses to include.",
    )
    parser.add_argument(
        "--migration-modes",
        default="move",
        help="Comma-separated migration modes to include.",
    )
    parser.add_argument(
        "--legacy-path",
        action="append",
        default=None,
        help="Optional legacy path filter; may be supplied multiple times.",
    )
    parser.add_argument(
        "--report-json",
        type=Path,
        default=None,
        help="Optional JSON report output path (relative paths resolve from repo root).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve() if args.root is not None else repo_root()
    manifest_path = args.manifest if args.manifest.is_absolute() else root / args.manifest
    statuses = {item.strip() for item in args.statuses.split(",") if item.strip()}
    migration_modes = {
        item.strip() for item in args.migration_modes.split(",") if item.strip()
    }
    legacy_paths = (
        {item.strip() for item in args.legacy_path if item.strip()}
        if args.legacy_path
        else None
    )

    if not manifest_path.exists():
        print(f"kb_migrate_legacy_docs: FAILED (manifest not found: {manifest_path})")
        return 1

    try:
        entries = parse_manifest_entries(manifest_path)
    except ValueError as error:
        print(f"kb_migrate_legacy_docs: FAILED ({error})")
        return 1

    selected = select_entries(entries, statuses, migration_modes, legacy_paths)
    today = dt.date.today().isoformat()

    if args.mode == "dry-run":
        result = run_dry_run(root, selected)
    elif args.mode == "apply":
        result = run_apply(root, manifest_path, selected, today)
    else:
        result = run_verify(root, selected)

    if args.report_json is not None:
        report_path = args.report_json if args.report_json.is_absolute() else root / args.report_json
        write_text(report_path, json.dumps(result, indent=2, sort_keys=True) + "\n")

    failure_count = len(result.get("failures", []))
    if failure_count:
        print("kb_migrate_legacy_docs: FAILED")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1

    print("kb_migrate_legacy_docs: PASSED")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
