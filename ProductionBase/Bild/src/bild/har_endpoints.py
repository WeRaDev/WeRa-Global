from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse


@dataclass(frozen=True)
class EndpointRecord:
    method: str
    host: str
    path: str
    query_keys: tuple[str, ...]
    status_code: int | None


def load_har(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)
    if not isinstance(payload, dict):
        raise ValueError("HAR payload must be a JSON object.")
    if "log" not in payload or not isinstance(payload["log"], dict):
        raise ValueError("HAR payload missing 'log' object.")
    return payload


def extract_endpoint_records(
    har_payload: dict[str, Any], host_contains: str = "leroymerlin"
) -> list[EndpointRecord]:
    entries = har_payload.get("log", {}).get("entries", [])
    if not isinstance(entries, list):
        raise ValueError("HAR 'log.entries' must be a list.")

    normalized_host_filter = host_contains.lower()
    records: dict[tuple[str, str, str], EndpointRecord] = {}

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        request = entry.get("request")
        if not isinstance(request, dict):
            continue
        method = str(request.get("method", "")).upper()
        url = str(request.get("url", ""))
        if not method or not url:
            continue

        parsed = urlparse(url)
        host = parsed.netloc.lower()
        if normalized_host_filter not in host:
            continue
        path = parsed.path or "/"
        query_keys = tuple(sorted(parse_qs(parsed.query).keys()))
        response = entry.get("response")
        status_code: int | None = None
        if isinstance(response, dict) and isinstance(response.get("status"), int):
            status_code = response["status"]

        key = (method, host, path)
        existing = records.get(key)
        if existing is None:
            records[key] = EndpointRecord(
                method=method,
                host=host,
                path=path,
                query_keys=query_keys,
                status_code=status_code,
            )
            continue
        merged_query_keys = tuple(sorted(set(existing.query_keys) | set(query_keys)))
        merged_status_code = (
            existing.status_code if existing.status_code is not None else status_code
        )
        records[key] = EndpointRecord(
            method=method,
            host=host,
            path=path,
            query_keys=merged_query_keys,
            status_code=merged_status_code,
        )

    return sorted(records.values(), key=lambda record: (record.host, record.path))


def records_to_markdown(records: list[EndpointRecord]) -> str:
    lines = [
        "# Observed endpoint candidates",
        "Generated from HAR capture. Secrets/tokens are intentionally excluded.",
        "",
    ]
    if not records:
        lines.append("No matching endpoints found.")
        return "\n".join(lines)

    for index, record in enumerate(records, start=1):
        query_keys = ", ".join(record.query_keys) if record.query_keys else "-"
        status_code = str(record.status_code) if record.status_code is not None else "-"
        lines.extend(
            [
                f"{index}. `{record.method} {record.path}`",
                f"   - host: `{record.host}`",
                f"   - query_keys: `{query_keys}`",
                f"   - status_code: `{status_code}`",
            ]
        )
    return "\n".join(lines)
