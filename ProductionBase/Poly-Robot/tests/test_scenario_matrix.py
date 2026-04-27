from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.llm_policy import load_calibration_policy  # noqa: E402
from poly_robot.replay_harness import load_events_from_jsonl  # noqa: E402
from poly_robot.scenario_matrix import build_scenario_matrix_report  # noqa: E402
from poly_robot.scenario_pack import load_scenario_pack  # noqa: E402
from poly_robot.schemas import SCENARIO_MATRIX_REPORT_SCHEMA_VERSION  # noqa: E402


PROFILE_PATH = (
    ROOT_DIR / "config" / "parameters" / "profiles" / "mvp_test_token.v1.json"
)
CALIBRATION_POLICY_PATH = (
    ROOT_DIR / "config" / "calibration" / "llm_reliability.v1.json"
)
SCENARIO_PACK_PATH = ROOT_DIR / "config" / "replay" / "scenario_pack.v1.json"
REPLAY_FIXTURE_PATH = ROOT_DIR / "tests" / "fixtures" / "replay_events.jsonl"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class ScenarioMatrixTests(unittest.TestCase):
    def test_report_is_deterministic_for_same_inputs(self) -> None:
        profile_payload = _load_json(PROFILE_PATH)
        calibration_payload = _load_json(CALIBRATION_POLICY_PATH)
        parameters = profile_payload["values"]
        calibration_policy = load_calibration_policy(CALIBRATION_POLICY_PATH)
        scenario_pack = load_scenario_pack(SCENARIO_PACK_PATH)
        events = load_events_from_jsonl(REPLAY_FIXTURE_PATH)

        report_a = build_scenario_matrix_report(
            base_events=events,
            parameters=parameters,
            calibration_policy=calibration_policy,
            profile_payload=profile_payload,
            calibration_policy_payload=calibration_payload,
            scenario_pack=scenario_pack,
            scenario_pack_path=str(SCENARIO_PACK_PATH),
            events_path=str(REPLAY_FIXTURE_PATH),
            profile_path=str(PROFILE_PATH),
            calibration_policy_path=str(CALIBRATION_POLICY_PATH),
            bankroll=1000.0,
            scenario_names=["baseline", "liquidity_crunch"],
        )
        report_b = build_scenario_matrix_report(
            base_events=events,
            parameters=parameters,
            calibration_policy=calibration_policy,
            profile_payload=profile_payload,
            calibration_policy_payload=calibration_payload,
            scenario_pack=scenario_pack,
            scenario_pack_path=str(SCENARIO_PACK_PATH),
            events_path=str(REPLAY_FIXTURE_PATH),
            profile_path=str(PROFILE_PATH),
            calibration_policy_path=str(CALIBRATION_POLICY_PATH),
            bankroll=1000.0,
            scenario_names=["baseline", "liquidity_crunch"],
        )

        self.assertEqual(
            report_a["schema_version"], SCENARIO_MATRIX_REPORT_SCHEMA_VERSION
        )
        self.assertEqual(report_a["report_hash"], report_b["report_hash"])
        self.assertEqual(report_a["aggregate"]["scenario_count"], 2)
        self.assertEqual(report_a["outcomes"][0]["scenario_name"], "baseline")
        self.assertEqual(report_a["outcomes"][1]["scenario_name"], "liquidity_crunch")
        self.assertGreaterEqual(
            report_a["outcomes"][0]["allowed_trade_count"],
            report_a["outcomes"][1]["allowed_trade_count"],
        )


if __name__ == "__main__":
    unittest.main()
