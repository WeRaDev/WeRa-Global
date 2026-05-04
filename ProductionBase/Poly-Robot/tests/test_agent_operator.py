from __future__ import annotations
import json
import sys

import unittest
from pathlib import Path
from unittest.mock import patch


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.agent_operator import (  # noqa: E402
    AgentOperator,
    AgentOperatorUnavailableError,
    OpenFangApiClient,
)


class _StubClient:
    def __init__(self, response: str | None = None, error: Exception | None = None):
        self.provider = "stub"
        self.model = "stub-model"
        self._response = response or ""
        self._error = error

    def complete(self, *, prompt: str, timeout_seconds: float) -> str:
        del prompt, timeout_seconds
        if self._error is not None:
            raise self._error
        return self._response


class AgentOperatorTests(unittest.TestCase):
    def test_disabled_returns_fail_open_payload(self) -> None:
        operator = AgentOperator(client=_StubClient(response="{}"), enabled=False)

        result = operator.infer(cycle_context={"cycle_index": 1})

        self.assertEqual(result["status"], "DISABLED")
        self.assertEqual(result["reason"], "agent_operator_disabled")
        self.assertEqual(result["provider"], "stub")
        self.assertEqual(result["model"], "stub-model")

    def test_unstructured_response_is_captured_as_summary(self) -> None:
        operator = AgentOperator(
            client=_StubClient(response="Advisory: reduce slippage by tightening spread.")
        )

        result = operator.infer(cycle_context={"cycle_index": 2})

        self.assertEqual(result["status"], "OK")
        self.assertEqual(result["reason"], "unstructured_response")
        self.assertIn("reduce slippage", result["summary"])
        self.assertEqual(result["risk_posture"], "neutral")

    def test_structured_response_is_normalized(self) -> None:
        operator = AgentOperator(
            client=_StubClient(
                response="""
{
  "summary": "Capture spread on high-liquidity names.",
  "profitability_hypothesis": "Prioritize lower execution-cost opportunities.",
  "risk_posture": "increase",
  "confidence": 1.7,
  "recommended_actions": [
    "Raise min volume threshold",
    "Lower max slippage tolerance"
  ],
  "scenario_hint": "liquidity_crunch"
}
""".strip()
            )
        )

        result = operator.infer(cycle_context={"cycle_index": 3})

        self.assertEqual(result["status"], "OK")
        self.assertEqual(result["risk_posture"], "increase")
        self.assertEqual(result["confidence"], 1.0)
        self.assertEqual(len(result["recommended_actions"]), 2)
        self.assertEqual(result["scenario_hint"], "liquidity_crunch")

    def test_client_error_returns_fail_open_error_status(self) -> None:
        operator = AgentOperator(client=_StubClient(error=RuntimeError("boom")))

        result = operator.infer(cycle_context={"cycle_index": 4})

        self.assertEqual(result["status"], "ERROR")
        self.assertEqual(result["reason"], "RuntimeError")
        self.assertEqual(result["summary"], "")

    def test_unknown_mode_defaults_to_advisory(self) -> None:
        operator = AgentOperator(
            client=_StubClient(
                response='{"summary":"ok","scenario_hint":"baseline"}'
            )
        )

        result = operator.infer(
            cycle_context={"cycle_index": 5, "agent_operator_mode": "custom-mode"}
        )

        self.assertEqual(result["status"], "OK")
        self.assertEqual(result["mode"], "advisory")

    def test_scenario_hint_is_sanitized(self) -> None:
        operator = AgentOperator(
            client=_StubClient(
                response='{"summary":"ok","scenario_hint":"liquidity crunch!!/../../"}'
            )
        )

        result = operator.infer(
            cycle_context={"cycle_index": 6, "agent_operator_mode": "strategy"}
        )

        self.assertEqual(result["status"], "OK")
        self.assertEqual(result["mode"], "strategy")
        self.assertEqual(result["scenario_hint"], "liquiditycrunch....")

    def test_bare_false_response_maps_to_unavailable(self) -> None:
        operator = AgentOperator(client=_StubClient(response="False"))

        result = operator.infer(cycle_context={"cycle_index": 7})

        self.assertEqual(result["status"], "UNAVAILABLE")
        self.assertEqual(result["reason"], "factual_unavailable_false")
        self.assertEqual(result["summary"], "")

    def test_structured_rejected_state_is_parsed(self) -> None:
        operator = AgentOperator(
            client=_StubClient(
                response='{"state":"REJECTED:non_positive_net_edge_after_costs","summary":"rejected"}'
            )
        )

        result = operator.infer(cycle_context={"cycle_index": 8})

        self.assertEqual(result["status"], "REJECTED")
        self.assertEqual(result["reason"], "non_positive_net_edge_after_costs")
        self.assertEqual(result["summary"], "rejected")
    def test_prompt_compacts_large_context_lists_to_counts(self) -> None:
        cycle_context = {
            "cycle_index": 9,
            "agent_operator_mode": "strategy",
            "available_scenarios": ["baseline", "liquidity_crunch"],
            "open_positions_detail": [
                {"market_id": f"m{i}", "note": "x" * 400} for i in range(120)
            ],
            "closed_positions_recent": [
                {"market_id": f"c{i}", "note": "y" * 400} for i in range(80)
            ],
            "portfolio": {
                "current_equity": 1000.0,
                "open_positions": 6,
                "total_exposure_fraction": 0.2,
            },
        }

        prompt = AgentOperator._build_prompt(cycle_context)

        self.assertIn('"open_positions_detail_count": 120', prompt)
        self.assertIn('"closed_positions_recent_count": 80', prompt)
        self.assertNotIn('"open_positions_detail": [', prompt)
        self.assertNotIn('"closed_positions_recent": [', prompt)

class _StubHeaders:
    @staticmethod
    def get_content_charset() -> str:
        return "utf-8"


class _StubHttpResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self._payload = payload
        self.headers = _StubHeaders()

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self) -> "_StubHttpResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        del exc_type, exc, tb


class OpenFangApiClientTests(unittest.TestCase):
    def test_missing_agent_id_raises_unavailable(self) -> None:
        client = OpenFangApiClient(agent_id="")
        with self.assertRaises(AgentOperatorUnavailableError):
            client.complete(prompt="hello", timeout_seconds=1.0)

    def test_complete_uses_health_then_message_and_returns_response_text(self) -> None:
        client = OpenFangApiClient(
            agent_id="advisory-agent",
            base_url="http://127.0.0.1:4200",
        )
        with patch(
            "poly_robot.agent_operator.urlopen",
            side_effect=[
                _StubHttpResponse({"status": "ok"}),
                _StubHttpResponse({"response": "{\"summary\":\"ok\"}"}),
            ],
        ) as mock_urlopen:
            response_text = client.complete(
                prompt="cycle context",
                timeout_seconds=1.0,
            )

        self.assertEqual(response_text, "{\"summary\":\"ok\"}")
        self.assertEqual(mock_urlopen.call_count, 2)


if __name__ == "__main__":
    unittest.main()
