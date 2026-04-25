from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SUPPORTED_PARAMETER_TYPES = {"number", "integer", "boolean", "string", "enum"}
SUPPORTED_MUTABILITY = {"phase_frozen", "tunable", "runtime"}
REQUIRED_PARAMETER_FIELDS = {"key", "type", "required", "mutability", "owner", "description"}


@dataclass
class ValidationResult:
    errors: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _matches_type(value: Any, parameter_type: str) -> bool:
    if parameter_type == "number":
        return _is_number(value)
    if parameter_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if parameter_type == "boolean":
        return isinstance(value, bool)
    if parameter_type in {"string", "enum"}:
        return isinstance(value, str)
    return False


def _validate_common_constraints(spec: dict[str, Any], value: Any) -> list[str]:
    errors: list[str] = []
    parameter_type = spec["type"]
    key = spec["key"]

    if parameter_type in {"number", "integer"}:
        minimum = spec.get("minimum")
        maximum = spec.get("maximum")
        if minimum is not None and value < minimum:
            errors.append(f"{key}: value {value} is below minimum {minimum}.")
        if maximum is not None and value > maximum:
            errors.append(f"{key}: value {value} is above maximum {maximum}.")

    if parameter_type == "enum":
        allowed_values = spec.get("allowed_values")
        if not isinstance(allowed_values, list) or not allowed_values:
            errors.append(f"{key}: enum parameter must define non-empty allowed_values.")
        elif value not in allowed_values:
            errors.append(f"{key}: value {value!r} is not in allowed_values {allowed_values}.")

    return errors

def _calibration_policy_is_proven(calibration_policy: dict[str, Any]) -> bool:
    thresholds = calibration_policy.get("thresholds", {})
    status = calibration_policy.get("status", {})

    min_samples = int(thresholds.get("min_samples", 0))
    max_brier_score = float(thresholds.get("max_brier_score", 1.0))
    max_ece = float(thresholds.get("max_expected_calibration_error", 1.0))

    sample_count = int(status.get("sample_count", 0))
    brier_score = float(status.get("brier_score", 1.0))
    ece = float(status.get("expected_calibration_error", 1.0))
    proven_flag = bool(status.get("proven", False))

    return (
        proven_flag
        and sample_count >= min_samples
        and brier_score <= max_brier_score
        and ece <= max_ece
    )


def _validate_llm_calibration_gate(
    profile: dict[str, Any], calibration_policy: dict[str, Any] | None
) -> list[str]:
    errors: list[str] = []
    profile_values = profile.get("values")
    if not isinstance(profile_values, dict):
        return errors

    mode = str(profile_values.get("brain.llm_probability_calibration", "advisory_only"))
    if mode == "advisory_only":
        return errors

    if calibration_policy is None:
        return [
            "Profile: non-advisory LLM mode requires --calibration-policy with proven reliability status."
        ]

    if not _calibration_policy_is_proven(calibration_policy):
        errors.append(
            "Profile: non-advisory LLM mode is blocked because calibration reliability thresholds are not proven."
        )
    return errors


def _validate_default(spec: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    key = spec.get("key", "<unknown>")
    default = spec.get("default")
    parameter_type = spec.get("type")

    if parameter_type is None:
        return [f"{key}: missing required field type."]
    if default is None:
        return [f"{key}: missing required field default."]
    if not _matches_type(default, parameter_type):
        return [f"{key}: default value {default!r} does not match type {parameter_type}."]

    errors.extend(_validate_common_constraints(spec, default))
    return errors


def build_catalog_index(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {parameter["key"]: parameter for parameter in catalog.get("parameters", [])}


def validate_catalog(catalog: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if "catalog_version" not in catalog:
        errors.append("Catalog: missing catalog_version.")
    if "phase" not in catalog:
        errors.append("Catalog: missing phase.")

    parameters = catalog.get("parameters")
    if not isinstance(parameters, list) or not parameters:
        errors.append("Catalog: parameters must be a non-empty list.")
        return errors

    seen_keys: set[str] = set()
    for idx, parameter in enumerate(parameters):
        prefix = f"Catalog parameter[{idx}]"
        if not isinstance(parameter, dict):
            errors.append(f"{prefix}: must be an object.")
            continue

        missing = REQUIRED_PARAMETER_FIELDS - set(parameter.keys())
        if missing:
            errors.append(f"{prefix}: missing required fields {sorted(missing)}.")

        key = parameter.get("key")
        if isinstance(key, str):
            if key in seen_keys:
                errors.append(f"Catalog: duplicate parameter key {key}.")
            seen_keys.add(key)
        else:
            errors.append(f"{prefix}: key must be a string.")
            continue

        parameter_type = parameter.get("type")
        if parameter_type not in SUPPORTED_PARAMETER_TYPES:
            errors.append(f"{key}: unsupported parameter type {parameter_type!r}.")

        mutability = parameter.get("mutability")
        if mutability not in SUPPORTED_MUTABILITY:
            errors.append(f"{key}: unsupported mutability {mutability!r}.")

        errors.extend(_validate_default(parameter))

    return errors


def _validate_required_and_unknown_keys(
    profile_values: dict[str, Any], catalog_index: dict[str, dict[str, Any]]
) -> list[str]:
    errors: list[str] = []

    required_keys = {key for key, spec in catalog_index.items() if spec.get("required")}
    missing_keys = sorted(required_keys - set(profile_values.keys()))
    unknown_keys = sorted(set(profile_values.keys()) - set(catalog_index.keys()))

    for key in missing_keys:
        errors.append(f"Profile: missing required parameter {key}.")
    for key in unknown_keys:
        errors.append(f"Profile: unknown parameter {key}.")

    return errors


def _validate_frozen_changes(
    catalog_index: dict[str, dict[str, Any]],
    profile: dict[str, Any],
    baseline: dict[str, Any] | None,
) -> list[str]:
    if baseline is None:
        return []

    errors: list[str] = []
    baseline_values = baseline.get("values")
    if not isinstance(baseline_values, dict):
        return ["Baseline: values must be an object."]

    profile_values = profile.get("values", {})
    governance = profile.get("governance", {})
    change_ticket = str(governance.get("change_ticket", "")).strip()
    approved_by = governance.get("approved_by", [])

    for key, spec in catalog_index.items():
        if spec.get("mutability") != "phase_frozen":
            continue
        if key not in baseline_values or key not in profile_values:
            continue

        if baseline_values[key] == profile_values[key]:
            continue

        ticket_prefix = spec.get("change_control", {}).get("ticket_prefix", "ARCH-")
        if not change_ticket.startswith(ticket_prefix):
            errors.append(
                f"Profile: frozen parameter {key} changed without required ticket prefix {ticket_prefix}."
            )
        if not isinstance(approved_by, list) or len(approved_by) == 0:
            errors.append(
                f"Profile: frozen parameter {key} changed but governance.approved_by is missing."
            )

    return errors


def validate_profile(
    catalog: dict[str, Any],
    profile: dict[str, Any],
    baseline: dict[str, Any] | None = None,
    calibration_policy: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    catalog_version = catalog.get("catalog_version")
    profile_catalog_version = profile.get("catalog_version")

    if profile_catalog_version != catalog_version:
        errors.append(
            f"Profile: catalog_version mismatch. expected {catalog_version}, got {profile_catalog_version}."
        )

    profile_values = profile.get("values")
    if not isinstance(profile_values, dict):
        errors.append("Profile: values must be an object.")
        return errors

    catalog_index = build_catalog_index(catalog)
    errors.extend(_validate_required_and_unknown_keys(profile_values, catalog_index))

    for key, value in profile_values.items():
        spec = catalog_index.get(key)
        if spec is None:
            continue

        parameter_type = spec["type"]
        if not _matches_type(value, parameter_type):
            errors.append(f"{key}: value {value!r} does not match type {parameter_type}.")
            continue

        errors.extend(_validate_common_constraints(spec, value))

    errors.extend(_validate_frozen_changes(catalog_index, profile, baseline))
    errors.extend(_validate_llm_calibration_gate(profile, calibration_policy))
    return errors


def validate_files(
    catalog_path: Path,
    profile_path: Path,
    baseline_path: Path | None = None,
    calibration_policy_path: Path | None = None,
) -> ValidationResult:
    errors: list[str] = []
    try:
        catalog = load_json(catalog_path)
        profile = load_json(profile_path)
        baseline = load_json(baseline_path) if baseline_path else None
        calibration_policy = (
            load_json(calibration_policy_path) if calibration_policy_path else None
        )
    except ValueError as exc:
        return ValidationResult(errors=[str(exc)])

    errors.extend(validate_catalog(catalog))
    if errors:
        return ValidationResult(errors=errors)

    errors.extend(validate_profile(catalog, profile, baseline, calibration_policy))
    return ValidationResult(errors=errors)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate Poly-Robot parameter governance catalog/profile consistency."
    )
    parser.add_argument("--catalog", type=Path, required=True, help="Path to parameter catalog JSON.")
    parser.add_argument("--profile", type=Path, required=True, help="Path to parameter profile JSON.")
    parser.add_argument(
        "--baseline",
        type=Path,
        required=False,
        help="Optional path to frozen baseline JSON for phase-frozen change checks.",
    )
    parser.add_argument(
        "--calibration-policy",
        type=Path,
        required=False,
        help=(
            "Optional path to LLM calibration policy; required when "
            "brain.llm_probability_calibration is not advisory_only."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    result = validate_files(args.catalog, args.profile, args.baseline, args.calibration_policy)
    if result.ok:
        print("Parameter governance validation passed.")
        return 0

    print("Parameter governance validation failed:")
    for error in result.errors:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
