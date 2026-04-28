#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run_check(name: str, command: list[str]) -> dict[str, object]:
    result = subprocess.run(command, capture_output=True, text=True)
    return {
        "name": name,
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "status": "passed" if result.returncode == 0 else "failed",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run periodic KB drift detection checks and produce a consolidated report."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root path (defaults to auto-detected repo root).",
    )
    parser.add_argument(
        "--report-json",
        type=Path,
        default=None,
        help="Optional report output path (relative paths resolve from repo root).",
    )
    parser.add_argument(
        "--inventory-output",
        type=Path,
        default=None,
        help="Optional inventory output path for kb_inventory_baseline.py.",
    )
    parser.add_argument(
        "--strict-formal-proof",
        action="store_true",
        help="Treat kb_formal_proof_gate failure as blocking (default: non-blocking warning).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve() if args.root is not None else repo_root()
    scripts_dir = root / "kb-governance" / "ci" / "scripts"
    python = sys.executable

    inventory_output_arg: list[str] = []
    if args.inventory_output is not None:
        inventory_output = (
            args.inventory_output
            if args.inventory_output.is_absolute()
            else root / args.inventory_output
        )
        inventory_output_arg = ["--output-json", str(inventory_output)]

    checks = [
        (
            "kb_canonical_validate",
            True,
            [
                python,
                str(scripts_dir / "kb_canonical_validate.py"),
                "--root",
                str(root),
            ],
        ),
        (
            "kb_governance_routing_check",
            True,
            [
                python,
                str(scripts_dir / "kb_governance_routing_check.py"),
                "--root",
                str(root),
            ],
        ),
        (
            "kb_formal_proof_gate",
            args.strict_formal_proof,
            [
                python,
                str(scripts_dir / "kb_formal_proof_gate.py"),
                "--root",
                str(root),
            ],
        ),
        (
            "kb_rewrite_links_and_index_verify",
            True,
            [
                python,
                str(scripts_dir / "kb_rewrite_links_and_index.py"),
                "--root",
                str(root),
                "--mode",
                "verify",
            ],
        ),
        (
            "kb_migrate_legacy_docs_verify",
            True,
            [
                python,
                str(scripts_dir / "kb_migrate_legacy_docs.py"),
                "--root",
                str(root),
                "--mode",
                "verify",
                "--statuses",
                "canonicalized",
                "--migration-modes",
                "move,mirror_stub",
            ],
        ),
        (
            "kb_inventory_baseline",
            True,
            [
                python,
                str(scripts_dir / "kb_inventory_baseline.py"),
                "--root",
                str(root),
                *inventory_output_arg,
            ],
        ),
    ]

    results: list[dict[str, object]] = []
    for name, blocking, command in checks:
        outcome = run_check(name, command)
        outcome["blocking"] = blocking
        results.append(outcome)

    failed = [item for item in results if item["returncode"] != 0]
    blocking_failures = [
        item for item in failed if bool(item.get("blocking"))
    ]

    report = {
        "overall_status": "failed" if blocking_failures else "passed",
        "root": root.as_posix(),
        "checks": results,
        "failed_checks": [item["name"] for item in failed],
        "blocking_failed_checks": [item["name"] for item in blocking_failures],
    }

    if args.report_json is not None:
        report_path = args.report_json if args.report_json.is_absolute() else root / args.report_json
        write_text(report_path, json.dumps(report, indent=2, sort_keys=True) + "\n")

    if blocking_failures:
        print("kb_drift_detection: FAILED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    print("kb_drift_detection: PASSED")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
