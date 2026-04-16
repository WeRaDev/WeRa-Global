from pathlib import Path

from src.bild.har_endpoints import (
    EndpointRecord,
    extract_endpoint_records,
    load_har,
    records_to_markdown,
)


def _fixture_har_payload() -> dict:
    return {
        "log": {
            "entries": [
                {
                    "request": {
                        "method": "GET",
                        "url": "https://www.leroymerlin.pt/api/v1/search?q=tile&store=pt",
                    },
                    "response": {"status": 200},
                },
                {
                    "request": {
                        "method": "POST",
                        "url": "https://www.leroymerlin.pt/api/v1/cart/add",
                    },
                    "response": {"status": 201},
                },
                {
                    "request": {
                        "method": "GET",
                        "url": "https://other.host/api/v1/ignore",
                    },
                    "response": {"status": 200},
                },
            ]
        }
    }


def test_extract_endpoint_records_filters_by_host() -> None:
    records = extract_endpoint_records(
        _fixture_har_payload(), host_contains="leroymerlin"
    )
    assert len(records) == 2
    assert records[0].host == "www.leroymerlin.pt"


def test_records_to_markdown_contains_paths() -> None:
    records = [
        EndpointRecord(
            method="GET",
            host="www.leroymerlin.pt",
            path="/api/v1/search",
            query_keys=("q",),
            status_code=200,
        )
    ]
    markdown = records_to_markdown(records)
    assert "GET /api/v1/search" in markdown
    assert "query_keys: `q`" in markdown


def test_load_har_reads_file(tmp_path: Path) -> None:
    har_path = tmp_path / "capture.har"
    har_path.write_text('{"log": {"entries": []}}', encoding="utf-8")
    payload = load_har(har_path)
    assert payload["log"]["entries"] == []
