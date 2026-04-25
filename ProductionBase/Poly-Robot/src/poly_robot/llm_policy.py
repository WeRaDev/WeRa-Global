from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CalibrationThresholds:
    min_samples: int
    max_brier_score: float
    max_expected_calibration_error: float


@dataclass(frozen=True)
class CalibrationStatus:
    proven: bool
    sample_count: int
    brier_score: float
    expected_calibration_error: float
    last_evaluated_at: str


@dataclass(frozen=True)
class CalibrationPolicy:
    thresholds: CalibrationThresholds
    status: CalibrationStatus


def _clamp_probability(value: float) -> float:
    return min(max(value, 0.0), 1.0)


def load_calibration_policy(path: Path) -> CalibrationPolicy:
    payload = json.loads(path.read_text(encoding="utf-8"))
    thresholds = payload.get("thresholds", {})
    status = payload.get("status", {})

    return CalibrationPolicy(
        thresholds=CalibrationThresholds(
            min_samples=int(thresholds.get("min_samples", 0)),
            max_brier_score=float(thresholds.get("max_brier_score", 1.0)),
            max_expected_calibration_error=float(
                thresholds.get("max_expected_calibration_error", 1.0)
            ),
        ),
        status=CalibrationStatus(
            proven=bool(status.get("proven", False)),
            sample_count=int(status.get("sample_count", 0)),
            brier_score=float(status.get("brier_score", 1.0)),
            expected_calibration_error=float(
                status.get("expected_calibration_error", 1.0)
            ),
            last_evaluated_at=str(status.get("last_evaluated_at", "")),
        ),
    )


def is_calibration_proven(policy: CalibrationPolicy | None) -> bool:
    if policy is None:
        return False
    status = policy.status
    thresholds = policy.thresholds
    return (
        status.proven
        and status.sample_count >= thresholds.min_samples
        and status.brier_score <= thresholds.max_brier_score
        and status.expected_calibration_error
        <= thresholds.max_expected_calibration_error
    )


def resolve_effective_mode(
    requested_mode: str, policy: CalibrationPolicy | None
) -> str:
    if requested_mode == "advisory_only":
        return "advisory_only"
    return requested_mode if is_calibration_proven(policy) else "advisory_only"


def merge_confidence(
    *,
    base_confidence: float,
    llm_confidence: float | None,
    requested_mode: str,
    policy: CalibrationPolicy | None,
) -> tuple[float, bool, str, str]:
    effective_mode = resolve_effective_mode(requested_mode, policy)
    normalized_base = _clamp_probability(base_confidence)

    if llm_confidence is None:
        return normalized_base, False, effective_mode, "llm_confidence_missing"

    normalized_llm = _clamp_probability(llm_confidence)
    if effective_mode == "advisory_only":
        advisory_reason = (
            "advisory_mode"
            if requested_mode == "advisory_only"
            else "calibration_not_proven"
        )
        return normalized_base, False, effective_mode, advisory_reason

    merged = _clamp_probability((normalized_base * 0.7) + (normalized_llm * 0.3))
    return merged, True, effective_mode, "calibrated_merge"
