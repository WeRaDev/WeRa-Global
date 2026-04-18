#!/usr/bin/env python3
from __future__ import annotations

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


def check_event_files(root: Path, errors: list[str]) -> None:
    events_dir = root / "KnowledgeBase" / "kb-governance" / "docs" / "events"
    if not events_dir.exists():
        errors.append("[routing] missing events directory: KnowledgeBase/kb-governance/docs/events")
        return

    temporal_pattern = re.compile(r"temporal_scope\s*:\s*([A-Za-z_-]+)")
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
            normalized = scope.strip().lower()
            if normalized not in VALID_TEMPORAL_SCOPES:
                errors.append(
                    f"[routing] invalid temporal_scope '{normalized}' in {rel}; expected one of {sorted(VALID_TEMPORAL_SCOPES)}"
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


def main() -> int:
    root = repo_root()
    errors: list[str] = []

    check_event_files(root, errors)
    check_contract_routing_signals(root, errors)

    if errors:
        print("kb_governance_routing_check: FAILED")
        for item in errors:
            print(f"- {item}")
        return 1

    print("kb_governance_routing_check: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
