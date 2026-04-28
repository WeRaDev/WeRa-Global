from __future__ import annotations

import math
from dataclasses import dataclass

from .llm_policy import CalibrationPolicy, is_calibration_proven, resolve_effective_mode


def _clamp_probability(value: float) -> float:
    return min(max(value, 0.001), 0.999)


def _safe_ratio(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return 0.0
    return numerator / denominator


def _logit(probability: float) -> float:
    clamped = _clamp_probability(probability)
    return math.log(clamped / (1.0 - clamped))


def _sigmoid(value: float) -> float:
    if value >= 0:
        exp_component = math.exp(-value)
        return 1.0 / (1.0 + exp_component)
    exp_component = math.exp(value)
    return exp_component / (1.0 + exp_component)


def calibration_reliability_score(policy: CalibrationPolicy | None) -> float:
    if policy is None:
        return 0.0

    thresholds = policy.thresholds
    status = policy.status
    sample_score = min(
        1.0,
        max(
            0.0,
            _safe_ratio(float(status.sample_count), float(max(thresholds.min_samples, 1))),
        ),
    )
    brier_score = max(
        0.0,
        1.0
        - _safe_ratio(
            max(0.0, float(status.brier_score)),
            max(float(thresholds.max_brier_score), 1e-6),
        ),
    )
    expected_calibration_error_score = max(
        0.0,
        1.0
        - _safe_ratio(
            max(0.0, float(status.expected_calibration_error)),
            max(float(thresholds.max_expected_calibration_error), 1e-6),
        ),
    )
    normalized = (
        sample_score + brier_score + expected_calibration_error_score
    ) / 3.0
    if status.proven and is_calibration_proven(policy):
        normalized = min(1.0, normalized + 0.1)
    return min(max(normalized, 0.0), 1.0)


def _apply_isotonic_style_transform(
    *,
    raw_probability: float,
    midpoint: float,
    reliability_score: float,
) -> float:
    normalized_midpoint = _clamp_probability(midpoint)
    anchor_probability = (raw_probability * 0.8) + (normalized_midpoint * 0.2)
    centered_distance = anchor_probability - 0.5
    sharpen_factor = 1.0 + (0.35 * reliability_score)
    return _clamp_probability(0.5 + (centered_distance * sharpen_factor))


def _apply_platt_style_transform(
    *,
    raw_probability: float,
    midpoint: float,
    reliability_score: float,
) -> float:
    normalized_midpoint = _clamp_probability(midpoint)
    logit_scale = 1.0 + (0.5 * reliability_score)
    midpoint_shift = (normalized_midpoint - 0.5) * 0.2
    transformed = (_logit(raw_probability) * logit_scale) + midpoint_shift
    return _clamp_probability(_sigmoid(transformed))


@dataclass(frozen=True)
class ProbabilityOracleResult:
    probability: float
    raw_probability: float
    drift: float
    drift_abs: float
    source: str
    effective_mode: str
    calibration_proven: bool
    reliability_score: float


def resolve_probability(
    *,
    estimated_probability: float,
    midpoint: float,
    requested_mode: str,
    policy: CalibrationPolicy | None,
) -> ProbabilityOracleResult:
    raw_probability = _clamp_probability(estimated_probability)
    effective_mode = resolve_effective_mode(requested_mode, policy)
    reliability_score = calibration_reliability_score(policy)
    calibration_proven = is_calibration_proven(policy)

    if effective_mode == "advisory_only":
        return ProbabilityOracleResult(
            probability=raw_probability,
            raw_probability=raw_probability,
            drift=0.0,
            drift_abs=0.0,
            source="heuristic_fallback",
            effective_mode=effective_mode,
            calibration_proven=calibration_proven,
            reliability_score=reliability_score,
        )

    if effective_mode == "isotonic":
        calibrated_probability = _apply_isotonic_style_transform(
            raw_probability=raw_probability,
            midpoint=midpoint,
            reliability_score=reliability_score,
        )
        source = "calibrated_isotonic"
    elif effective_mode == "platt":
        calibrated_probability = _apply_platt_style_transform(
            raw_probability=raw_probability,
            midpoint=midpoint,
            reliability_score=reliability_score,
        )
        source = "calibrated_platt"
    else:
        calibrated_probability = raw_probability
        source = "heuristic_fallback"

    drift = calibrated_probability - raw_probability
    return ProbabilityOracleResult(
        probability=calibrated_probability,
        raw_probability=raw_probability,
        drift=round(drift, 6),
        drift_abs=round(abs(drift), 6),
        source=source,
        effective_mode=effective_mode,
        calibration_proven=calibration_proven,
        reliability_score=round(reliability_score, 6),
    )
