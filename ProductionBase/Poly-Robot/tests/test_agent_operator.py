from __future__ import annotations
import sys

import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.agent_operator import AgentOperator  # noqa: E402


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


if __name__ == "__main__":
    unittest.main()
