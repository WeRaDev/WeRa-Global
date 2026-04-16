from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_session_state(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)
    validate_session_state(payload)
    return payload


def validate_session_state(payload: Any) -> None:
    if not isinstance(payload, dict):
        raise ValueError("Session state must be a JSON object.")
    if "cookies" not in payload:
        raise ValueError("Session state missing 'cookies' key.")
    if "origins" not in payload:
        raise ValueError("Session state missing 'origins' key.")
    cookies = payload["cookies"]
    origins = payload["origins"]
    if not isinstance(cookies, list):
        raise ValueError("'cookies' must be a list.")
    if not isinstance(origins, list):
        raise ValueError("'origins' must be a list.")


def count_domain_cookies(
    payload: dict[str, Any], domain_substring: str = "leroymerlin"
) -> int:
    cookies = payload.get("cookies", [])
    if not isinstance(cookies, list):
        raise ValueError("'cookies' must be a list.")
    normalized_match = domain_substring.lower()
    return sum(
        1
        for cookie in cookies
        if isinstance(cookie, dict)
        and "domain" in cookie
        and normalized_match in str(cookie["domain"]).lower()
    )


def summarize_session(
    payload: dict[str, Any], domain_substring: str = "leroymerlin"
) -> dict[str, int]:
    cookies = payload.get("cookies", [])
    origins = payload.get("origins", [])
    return {
        "cookie_entries": len(cookies) if isinstance(cookies, list) else 0,
        "origin_entries": len(origins) if isinstance(origins, list) else 0,
        "domain_cookie_entries": count_domain_cookies(payload, domain_substring),
    }
