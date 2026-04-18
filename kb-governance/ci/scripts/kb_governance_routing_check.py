#!/usr/bin/env python3
from __future__ import annotations
import argparse

import re
import sys
from pathlib import Path

VALID_TEMPORAL_SCOPES = {"current", "past", "future", "mixed"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def normalize_metadata_enum(raw_value: str) -> str:
    value = raw_value.split("#", 1)[0].strip().lower()
    value = value.strip().strip("`'\"")
    value = value.rstrip(",.;")
    value = value.strip("`'\"")
    return value


def check_event_files(root: Path, errors: list[str]) -> None:
    events_dir = root / "KnowledgeBase" / "kb-governance" / "docs" / "events"
    if not events_dir.exists():
        errors.append("[routing] missing events directory: KnowledgeBase/kb-governance/docs/events")
        return

    temporal_pattern = re.compile(r"temporal_scope\s*:\s*([^\n\r]+)")
    for path in sorted(events_dir.rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        text = read_text(path)
        if "governance_event:" not in text:
            errors.append(f"[routing] missing governance_event block in {rel}")
            continue
        if "documents:" not in text or "decisions:" not in text or "open_actions:" not in text:
            errors.append(f"[routing] incomplete governance_event structure in {rel}")

        matches = temporal_pattern.findall(text)
        if not matches:
            errors.append(f"[routing] missing temporal_scope in governance event {rel}")
        for scope in matches:
            normalized = normalize_metadata_enum(scope)
            if normalized not in VALID_TEMPORAL_SCOPES:
                errors.append(
                    f"[routing] invalid temporal_scope '{scope.strip()}' (normalized '{normalized}') in {rel}; expected one of {sorted(VALID_TEMPORAL_SCOPES)}"
                )


def check_contract_routing_signals(root: Path, errors: list[str]) -> None:
    contracts_dir = root / "KnowledgeBase" / "kb-governance" / "docs" / "contracts"
    if not contracts_dir.exists():
        errors.append(
            "[routing] missing contracts directory: KnowledgeBase/kb-governance/docs/contracts"
        )
        return

    for path in sorted(contracts_dir.rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        text = read_text(path)
        required_signals = ("temporal_scope", "WeRa Capital", "WeRa STAK", "WeRa Association")
        missing = [token for token in required_signals if token not in text]
        if missing:
            errors.append(
                f"[routing] missing routing signal(s) {missing} in contract {rel}"
            )

def collect_errors(root: Path) -> list[str]:
    errors: list[str] = []
    check_event_files(root, errors)
    check_contract_routing_signals(root, errors)
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate governance routing structures and temporal-scope readiness."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root path to validate (defaults to auto-detected repo root).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve() if args.root is not None else repo_root()
    errors = collect_errors(root)

    if errors:
        print("kb_governance_routing_check: FAILED")
        for item in errors:
            print(f"- {item}")
        return 1

    print("kb_governance_routing_check: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
