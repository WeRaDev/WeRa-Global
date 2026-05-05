#!/usr/bin/env python3
"""Generate a rich synthetic replay fixture for stress testing and parameter sweeps.

Produces JSONL events following the MarketEvent schema with diverse
market characteristics, varying signal quality, and realistic timestamp
progression across multiple days.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.shared.schemas import EVENT_SCHEMA_VERSION  # noqa: E402


def _stable_id(seed: str) -> str:
    return hashlib.sha256(seed.encode()).hexdigest()[:16]


def _clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


MARKET_TEMPLATES = [
    {"slug": "us-election-2028-winner", "question": "Who will win the 2028 US presidential election?", "base_liquidity": 500_000, "base_hours": 120},
    {"slug": "fed-rate-decision-jun", "question": "Will the Fed cut rates in June?", "base_liquidity": 200_000, "base_hours": 48},
    {"slug": "btc-above-100k-eoy", "question": "Will Bitcoin be above $100k by end of year?", "base_liquidity": 350_000, "base_hours": 96},
    {"slug": "eth-merge-v2-date", "question": "Will Ethereum ship the next major upgrade by Q3?", "base_liquidity": 150_000, "base_hours": 72},
    {"slug": "ai-regulation-eu-pass", "question": "Will the EU AI Act enforcement begin on schedule?", "base_liquidity": 80_000, "base_hours": 168},
    {"slug": "spacex-starship-orbit", "question": "Will Starship achieve stable orbit this quarter?", "base_liquidity": 120_000, "base_hours": 36},
    {"slug": "nvidia-earnings-beat", "question": "Will NVIDIA beat Q2 earnings estimates?", "base_liquidity": 400_000, "base_hours": 24},
    {"slug": "uk-snap-election-2026", "question": "Will the UK call a snap election in 2026?", "base_liquidity": 60_000, "base_hours": 144},
    {"slug": "openai-ipo-2026", "question": "Will OpenAI IPO before end of 2026?", "base_liquidity": 250_000, "base_hours": 120},
    {"slug": "trump-indictment-verdict", "question": "Will Trump be found guilty in pending trial?", "base_liquidity": 300_000, "base_hours": 60},
]


def _generate_market_variants(
    templates: list[dict], rng: random.Random, *, variant_count: int = 5
) -> list[dict]:
    """Expand templates with numeric variants to reach target market count."""
    markets: list[dict] = []
    for template in templates:
        for i in range(variant_count):
            variant = dict(template)
            variant["slug"] = f"{template['slug']}-v{i}"
            variant["question"] = f"{template['question']} (variant {i})"
            variant["base_liquidity"] = template["base_liquidity"] * rng.uniform(0.5, 2.0)
            variant["base_hours"] = max(4, template["base_hours"] + rng.randint(-12, 24))
            markets.append(variant)
    return markets


def _generate_events(
    markets: list[dict],
    *,
    events_per_market: int = 10,
    start_time: datetime,
    interval_minutes: int = 30,
) -> list[dict]:
    """Generate MarketEvent JSONL rows for each market across time."""
    events: list[dict] = []
    rng = random.Random(42)  # nosec B311 - seeded for deterministic fixture generation

    for market in markets:
        slug = market["slug"]
        base_midpoint = rng.uniform(0.15, 0.85)
        base_prob = _clamp(base_midpoint + rng.uniform(-0.05, 0.15), 0.05, 0.95)
        liquidity = market["base_liquidity"]
        hours_to_res = market["base_hours"]

        for t in range(events_per_market):
            ts = start_time + timedelta(minutes=t * interval_minutes)
            drift = rng.gauss(0, 0.01)
            midpoint = _clamp(base_midpoint + drift * (t + 1), 0.02, 0.98)
            prob = _clamp(base_prob + rng.gauss(0, 0.005) * (t + 1), 0.02, 0.98)
            depth = max(500, liquidity * rng.uniform(0.001, 0.01))
            volume_24h = liquidity * rng.uniform(0.05, 0.3)

            checks_passed = sum([
                prob >= 0.55,
                volume_24h > 10_000,
                rng.random() > 0.4,
                midpoint < 0.7,
            ])
            confidence = _clamp(0.55 + 0.1 * checks_passed, 0.5, 0.99)
            votes = 2 if checks_passed >= 3 else (1 if checks_passed >= 1 else 0)

            event_seed = f"{slug}-{t}-{ts.isoformat()}"
            event = {
                "schema_version": EVENT_SCHEMA_VERSION,
                "event_id": _stable_id(event_seed),
                "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "market_id": _stable_id(slug),
                "question": market["question"],
                "midpoint": round(midpoint, 6),
                "estimated_probability": round(prob, 6),
                "bids_depth_usd": round(depth, 2),
                "asks_depth_usd": round(depth * rng.uniform(0.8, 1.2), 2),
                "liquidity_usd": round(liquidity, 2),
                "hours_to_resolution": round(max(4, hours_to_res - t * 0.5), 1),
                "check_signals": {
                    "base_rate": prob >= 0.55,
                    "news": volume_24h > 10_000,
                    "whale": rng.random() > 0.6,
                    "disposition": midpoint < 0.7,
                },
                "base_confidence": round(confidence, 4),
                "llm_confidence": None,
                "consensus_buy_votes": votes,
                "metadata": {
                    "volume_24h_usd": round(volume_24h, 2),
                },
            }
            events.append(event)

    events.sort(key=lambda e: (e["timestamp"], e["event_id"]))
    return events


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate synthetic replay fixture")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT_DIR / "tests" / "fixtures" / "replay_events_rich.jsonl",
        help="Output JSONL path",
    )
    parser.add_argument(
        "--markets", type=int, default=50, help="Target market count"
    )
    parser.add_argument(
        "--events-per-market", type=int, default=10, help="Events per market"
    )
    args = parser.parse_args(argv)

    templates = MARKET_TEMPLATES
    rng = random.Random(42)  # nosec B311 - seeded for deterministic fixture generation
    variant_count = max(1, math.ceil(args.markets / len(templates)))
    markets = _generate_market_variants(templates, rng, variant_count=variant_count)[
        : args.markets
    ]

    start_time = datetime(2026, 5, 1, 0, 0, 0, tzinfo=UTC)
    events = _generate_events(
        markets,
        events_per_market=args.events_per_market,
        start_time=start_time,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(event, separators=(",", ":")) + "\n")

    print(
        f"Generated synthetic fixture: markets={len(markets)} "
        f"events={len(events)} output={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
