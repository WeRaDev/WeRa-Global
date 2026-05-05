import os
import time
from typing import Iterable, Tuple

from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from web3.exceptions import Web3RPCError


load_dotenv()

# Settings
PRIVATE_KEY = os.getenv("POLY_PRIVATE_KEY")
RPC_URL = "https://polygon-rpc.com"
CHAIN_ID = int(os.getenv("CHAIN_ID", "0"))
GAS_PRICE_MULTIPLIER = float(os.getenv("POLY_GAS_MULTIPLIER", "1.15"))

# Official Polygon / Polymarket addresses
USDC_ADDRESS = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
CTF_ADDRESS = "0x4D97DCd97eC945f40cF65F87097ACe5EA0476045"
EXCHANGE_ADDRESSES: Tuple[Tuple[str, str], ...] = (
    ("CLOB Exchange", "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E"),
    ("Neg-Risk Exchange", "0xC5d563A36AE78145C45a50134d48A1215220f80a"),
    ("Neg-Risk Adapter", "0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296"),
)

# ABI for approve and setApprovalForAll
ERC20_ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "_spender", "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function",
    }
]

ERC1155_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "operator", "type": "address"},
            {"internalType": "bool", "name": "approved", "type": "bool"},
        ],
        "name": "setApprovalForAll",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    }
]


def _suggest_gas_price(w3: Web3) -> int:
    base = w3.eth.gas_price
    bumped = int(base * GAS_PRICE_MULTIPLIER)
    return bumped if bumped > base else base + 1


def _send_tx(w3: Web3, tx) -> bool:
    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"Tx sent: {tx_hash.hex()}")
    retries = 0
    while True:
        try:
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            break
        except Exception as exc:
            code = getattr(exc, "code", None)
            message = getattr(exc, "message", "")
            if not message and exc.args:
                message = str(exc.args[0])
            hit_limit = (
                code == -32090
                or ("call rate limit exhausted" in message.lower())
                or ("too many requests" in message.lower())
            )
            if hit_limit and retries < 5:
                wait_for = 10 + retries * 2
                print(f"Rate limit hit; waiting {wait_for}s before retry...")
                time.sleep(wait_for)
                retries += 1
                continue
            raise
    if receipt.status == 1:
        print("Success")
        return True
    print("Transaction failed")
    return False


def _approve_all(
    w3: Web3,
    my_address: str,
    usdc,
    ctf,
    operators: Iterable[Tuple[str, str]],
) -> None:
    nonce = w3.eth.get_transaction_count(my_address, "pending")
    max_amount = 2**256 - 1

    for label, operator in operators:
        gas_price = _suggest_gas_price(w3)
        print(f"Approving USDC for {label} ({operator})...")
        approve_tx = usdc.functions.approve(operator, max_amount).build_transaction(
            {
                "from": my_address,
                "nonce": nonce,
                "gas": 120_000,
                "gasPrice": gas_price,
                "chainId": CHAIN_ID,
            }
        )
        if not _send_tx(w3, approve_tx):
            return
        nonce += 1

        gas_price = _suggest_gas_price(w3)
        print(f"setApprovalForAll for Conditional Tokens -> {label}...")
        ctf_tx = ctf.functions.setApprovalForAll(operator, True).build_transaction(
            {
                "from": my_address,
                "nonce": nonce,
                "gas": 150_000,
                "gasPrice": gas_price,
                "chainId": CHAIN_ID,
            }
        )
        if not _send_tx(w3, ctf_tx):
            return
        nonce += 1


def main():
    if not PRIVATE_KEY:
        print("Error: missing POLY_PRIVATE_KEY in .env")
        return
    if CHAIN_ID == 0:
        print("Error: CHAIN_ID must be set explicitly (e.g. 137 for Polygon mainnet)")
        return

    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    
    if not w3.is_connected():
        print("Error: unable to connect to Polygon RPC")
        return

    account = w3.eth.account.from_key(PRIVATE_KEY)
    my_address = account.address
    print(f"Wallet: {my_address}")

    usdc = w3.eth.contract(address=USDC_ADDRESS, abi=ERC20_ABI)
    ctf = w3.eth.contract(address=CTF_ADDRESS, abi=ERC1155_ABI)

    _approve_all(w3, my_address, usdc, ctf, EXCHANGE_ADDRESSES)


if __name__ == "__main__":
    main()
