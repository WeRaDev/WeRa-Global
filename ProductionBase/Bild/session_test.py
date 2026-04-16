from __future__ import annotations

import argparse
from pathlib import Path

from src.bild.session_state import load_session_state, summarize_session


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate local Playwright storageState structure without exposing secret values."
        )
    )
    parser.add_argument(
        "--session-file",
        default="auth_example.json",
        help="Path to session JSON file (storageState format).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run structure checks only and avoid network operations.",
    )
    args = parser.parse_args()

    session_path = Path(args.session_file)
    if not session_path.exists():
        print(f"Session file not found: {session_path}")
        print("Create one via headed login capture and store it outside git.")
        return 1

    session_data = load_session_state(session_path)
    summary = summarize_session(session_data)
    print("Session structure: OK")
    print(f"Cookie entries: {summary['cookie_entries']}")
    print(f"Origin entries: {summary['origin_entries']}")
    print(f"Leroy Merlin cookie entries: {summary['domain_cookie_entries']}")

    if args.dry_run:
        print("Dry-run mode: no network checks executed.")
        return 0

    print("Network checks are intentionally disabled in scaffold stage.")
    print("Implement authenticated endpoint probe after Sprint 1 HAR mapping.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
