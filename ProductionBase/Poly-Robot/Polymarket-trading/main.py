import asyncio
import os
from typing import Any, Dict, List

from polyApi.py_clob_client.client import AsyncClobClient
from polyApi.py_clob_client.constants import END_CURSOR

DEFAULT_HOST = "https://clob.polymarket.com"
TARGET_SLUG = os.getenv("POLY_TARGET_SLUG", "btc-updown-15m")
TARGET_CONDITION_ID = os.getenv("POLY_TARGET_CONDITION_ID")
QUESTION_FILTER = os.getenv(
    "POLY_QUESTION_FILTER", "Bitcoin Up or Down - January"
).lower()


async def fetch_market_tokens(slug: str, host: str) -> List[Dict[str, str]]:
    """
    Iterate through markets and collect token IDs/outcome info for a given slug.
    """
    client = AsyncClobClient(host)
    next_cursor = "MA=="
    matches: List[Dict[str, str]] = []

    try:
        page_index = 0
        while next_cursor and next_cursor != END_CURSOR:
            response = await client.get_markets(next_cursor)
            next_cursor = response.get("next_cursor")
            page_index += 1

            for market in response.get("data", []):
                market_slug = market.get("market_slug")
                question = market.get("question", "")
                print(market)
                if _should_log_market(market_slug, question):
                    # print(
                    #     f"[page {page_index}] slug={market_slug} "
                    #     f"question={question} "
                    #     f"conditionId={market.get('condition_id')}"
                    # )
                    if "bitcoin up or down" in question.lower():
                        print(market)

                if not _matches_target_market(market_slug, question, slug):
                    continue
                matches.extend(_extract_outcome_rows(market))
                if matches:
                    # Once we've captured the target market, stop iterating pages.
                    next_cursor = END_CURSOR
                    break

            if not next_cursor:
                break
    finally:
        await client.aclose()

    return matches


async def fetch_market_tokens_by_condition(condition_id: str, host: str) -> List[Dict[str, str]]:
    """
    Fetch a single market by condition id (no pagination required).
    """
    client = AsyncClobClient(host)
    try:
        market = await client.get_market(condition_id)
    finally:
        await client.aclose()

    payload = market.get("data") if isinstance(market, dict) else market
    if not payload:
        return []
    payload["conditionId"] = payload.get("conditionId", condition_id)
    market_slug = payload.get("market_slug") or payload.get("slug")
    question = payload.get("question", "")
    if _should_log_market(market_slug, question):
        print(
            f"[condition match] slug={market_slug} question={question} "
            f"conditionId={condition_id}"
        )
    return _extract_outcome_rows(payload)


def _extract_outcome_rows(market: Dict[str, Any]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    market_slug = market.get("market_slug") or market.get("slug") or ""
    condition_id = market.get("condition_id", "") or market.get("conditionId", "")
    for outcome in market.get("outcomes", []):
        rows.append(
            {
                "market": market_slug,
                "tokenId": outcome.get("tokenId"),
                "outcome": outcome.get("name"),
                "conditionId": condition_id,
            }
        )
    return rows


def _should_log_market(slug: str, question: str) -> bool:
    haystack = f"{slug or ''} {question or ''}".lower()
    return "15m" in haystack or "bitcoin" in haystack


def _matches_target_market(slug: str, question: str, target_slug: str) -> bool:
    if slug and target_slug:
        return slug == target_slug
    if QUESTION_FILTER:
        return QUESTION_FILTER in (question or "").lower()
    return False


async def main():
    host = os.getenv("CLOB_API_URL", DEFAULT_HOST)
    condition_id = TARGET_CONDITION_ID

    if condition_id:
        print(f"Fetching Polymarket token IDs for condition '{condition_id}'...")
        results = await fetch_market_tokens_by_condition(condition_id, host)
    else:
        slug = TARGET_SLUG
        print(f"Searching for Polymarket token IDs matching slug '{slug}'...")
        results = await fetch_market_tokens(slug, host)

    if not results:
        print("No markets matched. Verify the slug or try another cursor/endpoint.")
        return

    print("Found the following outcomes:")
    for entry in results:
        print(
            f"- outcome={entry['outcome']} tokenId={entry['tokenId']} "
            f"conditionId={entry['conditionId']}"
        )


if __name__ == "__main__":
    asyncio.run(main())
