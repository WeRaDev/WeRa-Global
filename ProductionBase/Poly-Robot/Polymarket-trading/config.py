import os

from dotenv import load_dotenv


load_dotenv()


def _require_env(var_name: str) -> str:
    value = os.getenv(var_name, "").strip()
    if value:
        return value
    raise RuntimeError(
        f"Missing required environment variable '{var_name}'. "
        "Set it in your shell or .env (never commit secrets)."
    )


api_key = _require_env("POLYMARKET_API_KEY")
api_secret = _require_env("POLYMARKET_API_SECRET")
passphrase = _require_env("POLYMARKET_API_PASSPHRASE")
private_key = os.getenv("POLY_PRIVATE_KEY", "").strip()
host = os.getenv("CLOB_API_URL", "https://clob.polymarket.com").strip()
if not host:
    host = "https://clob.polymarket.com"
chain_id: int = int(os.getenv("CHAIN_ID", "0"))
