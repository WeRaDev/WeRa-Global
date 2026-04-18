#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def run_check(
    script_path: Path,
    fixture_root: Path,
    expected_exit_code: int,
    failures: list[str],
) -> None:
    command = [sys.executable, str(script_path), "--root", str(fixture_root)]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == expected_exit_code:
        return

    failures.append(
        f"[fixture-check] {script_path.name} on {fixture_root.name} expected exit {expected_exit_code} but got {result.returncode}"
    )
    if result.stdout:
        failures.append(f"[fixture-check:stdout] {result.stdout.strip()}")
    if result.stderr:
        failures.append(f"[fixture-check:stderr] {result.stderr.strip()}")


def main() -> int:
    root = repo_root()
    scripts_dir = root / "kb-governance" / "ci" / "scripts"
    fixtures_dir = root / "kb-governance" / "ci" / "fixtures"

    positive_root = fixtures_dir / "positive"
    negative_root = fixtures_dir / "negative"

    checks = (
        (scripts_dir / "kb_canonical_validate.py", positive_root, 0),
        (scripts_dir / "kb_governance_routing_check.py", positive_root, 0),
        (scripts_dir / "kb_canonical_validate.py", negative_root, 1),
        (scripts_dir / "kb_governance_routing_check.py", negative_root, 1),
    )

    failures: list[str] = []
    for script_path, fixture_root, expected_exit_code in checks:
        if not script_path.exists():
            failures.append(f"[fixture-check] missing script: {script_path}")
            continue
        if not fixture_root.exists():
            failures.append(f"[fixture-check] missing fixture root: {fixture_root}")
            continue
        run_check(script_path, fixture_root, expected_exit_code, failures)

    if failures:
        print("kb_quality_gate_fixtures: FAILED")
        for item in failures:
            print(f"- {item}")
        return 1

    print("kb_quality_gate_fixtures: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
