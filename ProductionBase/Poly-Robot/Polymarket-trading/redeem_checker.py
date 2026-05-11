import argparse
import os
import time
from typing import List

from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware


load_dotenv()

# Настройки
PRIVATE_KEY = os.getenv("POLY_PRIVATE_KEY")
RPC_URL = "https://polygon-rpc.com"
CHAIN_ID = int(os.getenv("CHAIN_ID", "137"))
GAS_PRICE_MULTIPLIER = float(os.getenv("POLY_GAS_MULTIPLIER", "1.15"))

# Адреса (официальные Polygon / Polymarket)
USDC_ADDRESS = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
CTF_ADDRESS = "0x4D97DCd97eC945f40cF65F87097ACe5EA0476045"
HASH_ZERO = "0x" + "00" * 32

# Укажи здесь дефолты, чтобы запускать без аргументов в PyCharm
def _default_condition_id() -> str:
    env_val = os.getenv("POLY_REDEEM_CONDITION_ID", "")
    if env_val:
        return env_val
    try:
        from streams.settings import WebsocketSettings

        ws_settings = WebsocketSettings()
        return ws_settings.markets[0] if ws_settings.markets else ""
    except Exception:
        return ""

#Entry orders not fully filled yet; stopping to avoid bad averages.

DEFAULT_CONDITION_ID = "0x01ddad254073fc17589bb3cf7830893e7e8aae2e193e1493571e54fe92cf5553"
DEFAULT_INDEX_SETS = os.getenv("POLY_REDEEM_INDEX_SETS", "2")

# ABI для redeemPositions
CTF_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "collateralToken", "type": "address"},
            {"internalType": "bytes32", "name": "parentCollectionId", "type": "bytes32"},
            {"internalType": "bytes32", "name": "conditionId", "type": "bytes32"},
            {"internalType": "uint256[]", "name": "indexSets", "type": "uint256[]"},
        ],
        "name": "redeemPositions",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    }
]


def _suggest_gas_price(w3: Web3) -> int:
    base = w3.eth.gas_price
    bumped = int(base * GAS_PRICE_MULTIPLIER)
    return bumped if bumped > base else base + 1


def _send_tx(w3: Web3, tx) -> str:
    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"🚀 Tx sent: {tx_hash.hex()}")
    retries = 0
    while True:
        try:
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            break
        except Exception as exc:
            message = str(exc)
            hit_limit = (
                "call rate limit exhausted" in message.lower()
                or "too many requests" in message.lower()
            )
            if hit_limit and retries < 5:
                wait_for = 10 + retries * 2
                print(f"⏳ Rate limit hit; waiting {wait_for}s before retry...")
                time.sleep(wait_for)
                retries += 1
                continue
            raise
    if receipt.status == 1:
        print("✅ Success")
        return tx_hash.hex()
    raise RuntimeError("❌ Transaction failed")


def redeem_positions(
    condition_id: str,
    index_sets: List[int],
    collateral_token: str = USDC_ADDRESS,
    parent_collection_id: str = HASH_ZERO,
) -> str:
    if not PRIVATE_KEY:
        raise RuntimeError("Нет POLY_PRIVATE_KEY в .env")

    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    if not w3.is_connected():
        raise RuntimeError("Не удалось подключиться к Polygon RPC")

    account = w3.eth.account.from_key(PRIVATE_KEY)
    my_address = account.address
    ctf = w3.eth.contract(address=CTF_ADDRESS, abi=CTF_ABI)

    tx = ctf.functions.redeemPositions(
        collateral_token,
        parent_collection_id,
        condition_id,
        index_sets,
    ).build_transaction(
        {
            "from": my_address,
            "nonce": w3.eth.get_transaction_count(my_address, "pending"),
            "gasPrice": _suggest_gas_price(w3),
            "chainId": CHAIN_ID,
        }
    )
    if "gas" not in tx:
        try:
            tx["gas"] = int(ctf.functions.redeemPositions(
                collateral_token,
                parent_collection_id,
                condition_id,
                index_sets,
            ).estimate_gas({"from": my_address}))
        except Exception:
            tx["gas"] = 300_000

    return _send_tx(w3, tx)


def _parse_index_sets(raw: str) -> List[int]:
    if not raw:
        return []
    return [int(item.strip(), 0) for item in raw.split(",") if item.strip()]


def _normalize_condition_id(raw: str) -> str:
    raw = raw.strip()
    if not raw:
        return raw
    if raw.startswith("0x"):
        return raw
    # allow decimal IDs (e.g. token ids) -> bytes32 hex
    as_int = int(raw, 10)
    return "0x" + as_int.to_bytes(32, "big").hex()


def main() -> None:
    parser = argparse.ArgumentParser(description="Redeem Polymarket positions")
    parser.add_argument("condition_id", nargs="?", help="Condition ID (0x...)")
    parser.add_argument(
        "index_sets",
        nargs="?",
        help="Comma-separated index sets (e.g. 1,2 or 0x1,0x2)",
    )
    parser.add_argument(
        "--collateral",
        default=USDC_ADDRESS,
        help="Collateral token address (default USDC)",
    )
    parser.add_argument(
        "--parent",
        default=HASH_ZERO,
        help="Parent collection ID (default 0x00..00)",
    )
    args = parser.parse_args()

    condition_id = _normalize_condition_id(args.condition_id or DEFAULT_CONDITION_ID)
    index_sets_raw = args.index_sets or DEFAULT_INDEX_SETS

    if not condition_id:
        raise RuntimeError("condition_id пустой (задай аргумент или DEFAULT_CONDITION_ID)")

    index_sets = _parse_index_sets(index_sets_raw)
    if not index_sets:
        raise RuntimeError("index_sets пустой")

    tx_hash = redeem_positions(
        condition_id,
        index_sets,
        collateral_token=args.collateral,
        parent_collection_id=args.parent,
    )
    print(f"✅ Redeem tx: {tx_hash}")


if __name__ == "__main__":
    main()
