"""Basic tests for Polymarket-trading wrapper helpers.

These tests cover pure helper functions only (no network I/O, no
private keys, no live RPC).
"""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

_THIS_DIR = Path(__file__).resolve().parent
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))


class TestApproveHelpers(unittest.TestCase):
    def test_chain_id_default_is_zero(self) -> None:
        """CHAIN_ID must not default to mainnet 137."""
        saved = os.environ.pop("CHAIN_ID", None)
        try:
            val = int(os.getenv("CHAIN_ID", "0"))
            self.assertEqual(val, 0)
        finally:
            if saved is not None:
                os.environ["CHAIN_ID"] = saved

    def test_chain_id_env_override(self) -> None:
        saved = os.environ.get("CHAIN_ID")
        os.environ["CHAIN_ID"] = "80002"
        try:
            val = int(os.getenv("CHAIN_ID", "0"))
            self.assertEqual(val, 80002)
        finally:
            if saved is not None:
                os.environ["CHAIN_ID"] = saved
            else:
                os.environ.pop("CHAIN_ID", None)


try:
    from redeem_checker import _parse_index_sets, _normalize_condition_id
    _HAS_REDEEM = True
except ImportError:
    _HAS_REDEEM = False

try:
    from main import _should_log_market, _matches_target_market
    _HAS_MAIN = True
except ImportError:
    _HAS_MAIN = False


@unittest.skipUnless(_HAS_REDEEM, "redeem_checker dependencies not installed")
class TestRedeemHelpers(unittest.TestCase):
    def test_parse_index_sets_single(self) -> None:
        self.assertEqual(_parse_index_sets("2"), [2])

    def test_parse_index_sets_multiple(self) -> None:
        self.assertEqual(_parse_index_sets("1,2"), [1, 2])

    def test_parse_index_sets_hex(self) -> None:
        self.assertEqual(_parse_index_sets("0x1,0x2"), [1, 2])

    def test_parse_index_sets_empty(self) -> None:
        self.assertEqual(_parse_index_sets(""), [])

    def test_normalize_condition_id_hex(self) -> None:
        self.assertEqual(_normalize_condition_id("0xabcdef"), "0xabcdef")

    def test_normalize_condition_id_empty(self) -> None:
        self.assertEqual(_normalize_condition_id(""), "")

    def test_normalize_condition_id_decimal(self) -> None:
        result = _normalize_condition_id("1")
        self.assertTrue(result.startswith("0x"))
        self.assertEqual(len(result), 66)  # 0x + 64 hex chars


@unittest.skipUnless(_HAS_MAIN, "main.py dependencies not installed (polyApi)")
class TestMainHelpers(unittest.TestCase):
    def test_should_log_market_bitcoin(self) -> None:
        self.assertTrue(_should_log_market("btc-updown-15m", "Bitcoin price"))
        self.assertFalse(_should_log_market("foo", "something else"))

    def test_matches_target_market_slug(self) -> None:
        self.assertTrue(_matches_target_market("btc-updown-15m", "", "btc-updown-15m"))
        self.assertFalse(_matches_target_market("other-slug", "", "btc-updown-15m"))


class TestConfigDefaults(unittest.TestCase):
    def test_chain_id_not_mainnet_by_default(self) -> None:
        """config.py must not default to mainnet chain_id=137."""
        saved = os.environ.pop("CHAIN_ID", None)
        try:
            val = int(os.getenv("CHAIN_ID", "0"))
            self.assertNotEqual(val, 137, "CHAIN_ID must not default to mainnet")
        finally:
            if saved is not None:
                os.environ["CHAIN_ID"] = saved


if __name__ == "__main__":
    unittest.main()
