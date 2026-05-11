#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
CANONICAL_CLIENT_DIR = (
    ROOT_DIR / "Polymarket-trading" / "polyArbBot" / "polyApi" / "py_clob_client"
)
LEGACY_DUPLICATE_DIR = (
    ROOT_DIR / "Polymarket-trading" / "polyArbBot" / "py_clob_client"
)


def main() -> int:
    if not CANONICAL_CLIENT_DIR.is_dir():
        print(
            "[FAIL] missing canonical py_clob_client directory:",
            CANONICAL_CLIENT_DIR,
            file=sys.stderr,
        )
        return 1

    if LEGACY_DUPLICATE_DIR.exists():
        print(
            "[FAIL] duplicate py_clob_client tree detected; keep only canonical path.",
            file=sys.stderr,
        )
        print(f"  canonical: {CANONICAL_CLIENT_DIR}", file=sys.stderr)
        print(f"  duplicate: {LEGACY_DUPLICATE_DIR}", file=sys.stderr)
        return 1

    print(f"[OK] py_clob_client canonical path: {CANONICAL_CLIENT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
