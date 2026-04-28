from pathlib import Path

import pytest

from src.bild.session_state import (
    count_domain_cookies,
    load_session_state,
    summarize_session,
    validate_session_state,
)


def test_validate_session_state_accepts_valid_payload() -> None:
    payload = {"cookies": [], "origins": []}
    validate_session_state(payload)


def test_validate_session_state_rejects_missing_keys() -> None:
    with pytest.raises(ValueError, match="missing 'cookies'"):
        validate_session_state({"origins": []})


def test_summarize_session_counts_cookie_and_origin_entries() -> None:
    payload = {
        "cookies": [
            {"domain": ".leroymerlin.pt"},
            {"domain": ".example.com"},
            {"domain": ".leroymerlin.es"},
        ],
        "origins": [{"origin": "https://leroymerlin.pt"}],
    }
    summary = summarize_session(payload)
    assert summary["cookie_entries"] == 3
    assert summary["origin_entries"] == 1
    assert summary["domain_cookie_entries"] == 2


def test_load_session_state_from_file(tmp_path: Path) -> None:
    data_path = tmp_path / "state.json"
    data_path.write_text('{"cookies": [], "origins": []}', encoding="utf-8")
    payload = load_session_state(data_path)
    assert payload["cookies"] == []
    assert count_domain_cookies(payload) == 0
