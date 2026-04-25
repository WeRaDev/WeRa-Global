from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable

from .contracts import MarketEvent


def stable_json_dumps(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def stable_hash(value: Any) -> str:
    digest = hashlib.sha256()
    digest.update(stable_json_dumps(value).encode("utf-8"))
    return digest.hexdigest()


def hash_events(events: Iterable[MarketEvent]) -> str:
    canonical_events = [
        event.to_dict() for event in sorted(events, key=lambda item: (item.timestamp, item.event_id))
    ]
    return stable_hash(canonical_events)
