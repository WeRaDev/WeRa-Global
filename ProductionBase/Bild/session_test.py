from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _load_session_state(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError("Session state must be a JSON object.")
    if "cookies" not in data:
        raise ValueError("Session state missing 'cookies' key.")
    if "origins" not in data:
        raise ValueError("Session state missing 'origins' key.")
    return data


def _count_leroy_cookies(session_data: dict[str, Any]) -> int:
    cookies = session_data.get("cookies", [])
    if not isinstance(cookies, list):
        raise ValueError("'cookies' must be a list.")
    return sum(
        1
        for cookie in cookies
        if isinstance(cookie, dict)
        and "domain" in cookie
        and "leroymerlin" in str(cookie["domain"]).lower()
    )


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

    session_data = _load_session_state(session_path)
    leroy_cookie_count = _count_leroy_cookies(session_data)
    print("Session structure: OK")
    print(f"Cookie entries: {len(session_data.get('cookies', []))}")
    print(f"Leroy Merlin cookie entries: {leroy_cookie_count}")

    if args.dry_run:
        print("Dry-run mode: no network checks executed.")
        return 0

    print("Network checks are intentionally disabled in scaffold stage.")
    print("Implement authenticated endpoint probe after Sprint 1 HAR mapping.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

