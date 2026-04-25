from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.parameter_governance import validate_files  # noqa: E402


CATALOG_PATH = ROOT_DIR / "config" / "parameters" / "catalog.v1.json"
PROFILE_PATH = ROOT_DIR / "config" / "parameters" / "profiles" / "mvp_test_token.v1.json"
BASELINE_PATH = ROOT_DIR / "config" / "parameters" / "baselines" / "mvp_test_token.freeze.v1.json"
CALIBRATION_POLICY_PATH = ROOT_DIR / "config" / "calibration" / "llm_reliability.v1.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


class ParameterGovernanceValidationTests(unittest.TestCase):
    def test_profile_validates_against_catalog_and_baseline(self) -> None:
        result = validate_files(
            CATALOG_PATH, PROFILE_PATH, BASELINE_PATH, CALIBRATION_POLICY_PATH
        )
        self.assertTrue(result.ok, result.errors)

    def test_missing_required_parameter_fails(self) -> None:
        profile = _load(PROFILE_PATH)
        profile["values"].pop("risk.kelly_cap_fraction")

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_profile = Path(tmp_dir) / "profile.json"
            _write(temp_profile, profile)
            result = validate_files(
                CATALOG_PATH, temp_profile, BASELINE_PATH, CALIBRATION_POLICY_PATH
            )

        self.assertFalse(result.ok)
        self.assertTrue(
            any("missing required parameter risk.kelly_cap_fraction" in error for error in result.errors),
            result.errors,
        )

    def test_out_of_range_value_fails(self) -> None:
        profile = _load(PROFILE_PATH)
        profile["values"]["risk.max_daily_drawdown_fraction"] = 0.8

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_profile = Path(tmp_dir) / "profile.json"
            _write(temp_profile, profile)
            result = validate_files(
                CATALOG_PATH, temp_profile, BASELINE_PATH, CALIBRATION_POLICY_PATH
            )

        self.assertFalse(result.ok)
        self.assertTrue(
            any(
                "risk.max_daily_drawdown_fraction" in error and "above maximum" in error
                for error in result.errors
            ),
            result.errors,
        )

    def test_frozen_change_without_arch_ticket_fails(self) -> None:
        profile = _load(PROFILE_PATH)
        profile["values"]["scanner.min_price_gap"] = 0.08
        profile["governance"]["change_ticket"] = "CFG-2001"

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_profile = Path(tmp_dir) / "profile.json"
            _write(temp_profile, profile)
            result = validate_files(
                CATALOG_PATH, temp_profile, BASELINE_PATH, CALIBRATION_POLICY_PATH
            )

        self.assertFalse(result.ok)
        self.assertTrue(
            any("frozen parameter scanner.min_price_gap changed" in error for error in result.errors),
            result.errors,
        )

    def test_frozen_change_with_arch_ticket_passes(self) -> None:
        profile = _load(PROFILE_PATH)
        profile["values"]["scanner.min_price_gap"] = 0.08
        profile["governance"]["change_ticket"] = "ARCH-4321"
        profile["governance"]["approved_by"] = ["strategy-lead"]

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_profile = Path(tmp_dir) / "profile.json"
            _write(temp_profile, profile)
            result = validate_files(
                CATALOG_PATH, temp_profile, BASELINE_PATH, CALIBRATION_POLICY_PATH
            )

        self.assertTrue(result.ok, result.errors)

    def test_non_advisory_mode_fails_with_unproven_calibration(self) -> None:
        profile = _load(PROFILE_PATH)
        profile["values"]["brain.llm_probability_calibration"] = "isotonic"

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_profile = Path(tmp_dir) / "profile.json"
            _write(temp_profile, profile)
            result = validate_files(
                CATALOG_PATH, temp_profile, BASELINE_PATH, CALIBRATION_POLICY_PATH
            )

        self.assertFalse(result.ok)
        self.assertTrue(
            any("calibration reliability thresholds are not proven" in error for error in result.errors),
            result.errors,
        )

    def test_non_advisory_mode_passes_with_proven_calibration(self) -> None:
        profile = _load(PROFILE_PATH)
        profile["values"]["brain.llm_probability_calibration"] = "isotonic"

        calibration_policy = _load(CALIBRATION_POLICY_PATH)
        calibration_policy["status"] = {
            "proven": True,
            "sample_count": 9000,
            "brier_score": 0.15,
            "expected_calibration_error": 0.02,
            "last_evaluated_at": "2026-04-25T13:00:00Z",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_profile = Path(tmp_dir) / "profile.json"
            temp_calibration_policy = Path(tmp_dir) / "calibration.json"
            _write(temp_profile, profile)
            _write(temp_calibration_policy, calibration_policy)
            result = validate_files(
                CATALOG_PATH, temp_profile, BASELINE_PATH, temp_calibration_policy
            )

        self.assertTrue(result.ok, result.errors)


if __name__ == "__main__":
    unittest.main()
