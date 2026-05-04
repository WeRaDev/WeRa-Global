from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from .contracts import MarketEvent


def _parse_iso_timestamp(timestamp: str) -> datetime | None:
    try:
        return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).astimezone(UTC)
    except ValueError:
        return None


def _hours_between(start_timestamp: str, end_timestamp: str) -> float:
    start = _parse_iso_timestamp(start_timestamp)
    end = _parse_iso_timestamp(end_timestamp)
    if start is None or end is None or end < start:
        return 0.0
    return (end - start).total_seconds() / 3600.0


def _extract_volume_metric(event: MarketEvent) -> float:
    metadata = event.metadata or {}
    for key in ("volume_usd", "volume_1h_usd", "volume_24h_usd", "recent_volume_usd"):
        raw = metadata.get(key)
        try:
            if raw is None:
                continue
            value = float(raw)
            if value > 0:
                return value
        except (TypeError, ValueError):
            continue
    return max(0.0, float(event.liquidity_usd))


@dataclass(frozen=True)
class PositionSnapshot:
    market_id: str
    entry_event_id: str
    opened_at: str
    entry_midpoint: float
    entry_estimated_probability: float
    reference_volume: float
    open_notional: float
    fill_count: int
    last_event_timestamp: str
    last_midpoint: float

    @staticmethod
    def from_fill(event: MarketEvent, *, filled_notional: float) -> "PositionSnapshot":
        return PositionSnapshot(
            market_id=event.market_id,
            entry_event_id=event.event_id,
            opened_at=event.timestamp,
            entry_midpoint=float(event.midpoint),
            entry_estimated_probability=float(event.estimated_probability),
            reference_volume=_extract_volume_metric(event),
            open_notional=max(0.0, float(filled_notional)),
            fill_count=1,
            last_event_timestamp=event.timestamp,
            last_midpoint=float(event.midpoint),
        )

    def register_fill(
        self, event: MarketEvent, *, filled_notional: float
    ) -> "PositionSnapshot":
        fill_size = max(0.0, float(filled_notional))
        if fill_size <= 0:
            return self
        updated_notional = self.open_notional + fill_size
        if updated_notional <= 0:
            return self
        weighted_midpoint = (
            (self.entry_midpoint * self.open_notional)
            + (float(event.midpoint) * fill_size)
        ) / updated_notional
        weighted_probability = (
            (self.entry_estimated_probability * self.open_notional)
            + (float(event.estimated_probability) * fill_size)
        ) / updated_notional
        weighted_volume = (
            (self.reference_volume * self.open_notional)
            + (_extract_volume_metric(event) * fill_size)
        ) / updated_notional
        return PositionSnapshot(
            market_id=self.market_id,
            entry_event_id=self.entry_event_id,
            opened_at=self.opened_at,
            entry_midpoint=float(weighted_midpoint),
            entry_estimated_probability=float(weighted_probability),
            reference_volume=float(weighted_volume),
            open_notional=float(updated_notional),
            fill_count=self.fill_count + 1,
            last_event_timestamp=event.timestamp,
            last_midpoint=float(event.midpoint),
        )


@dataclass(frozen=True)
class ExitDecision:
    should_exit: bool
    trigger_count: int
    confirmation_threshold: int
    reasons: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


class ExitModule:
    def __init__(
        self, parameters: dict[str, Any], *, confirmation_threshold: int = 2
    ) -> None:
        if confirmation_threshold <= 0:
            raise ValueError("confirmation_threshold must be > 0")
        self.target_capture_ratio = float(parameters["exit.target_capture_ratio"])
        self.volume_spike_multiplier = float(parameters["exit.volume_spike_multiplier"])
        self.stale_hours = float(parameters["exit.stale_hours"])
        self.stale_price_change_threshold = float(
            parameters["exit.stale_price_change_threshold"]
        )
        configured_max_holding_hours = float(
            parameters.get("exit.max_holding_hours", self.stale_hours)
        )
        self.max_holding_hours = max(self.stale_hours, configured_max_holding_hours)
        configured_inventory_aging_derisk_hours = float(
            parameters.get(
                "exit.inventory_aging_derisk_hours",
                self.max_holding_hours * 0.75,
            )
        )
        self.inventory_aging_derisk_hours = max(
            0.0,
            min(self.max_holding_hours, configured_inventory_aging_derisk_hours),
        )
        self.cap_pressure_exposure_threshold = min(
            1.0,
            max(
                0.0,
                float(
                    parameters.get(
                        "exit.cap_pressure_exposure_threshold",
                        1.1,
                    )
                ),
            ),
        )
        configured_cap_pressure_trigger_hours = float(
            parameters.get(
                "exit.cap_pressure_trigger_hours",
                self.inventory_aging_derisk_hours,
            )
        )
        self.cap_pressure_trigger_hours = max(
            0.0,
            min(self.max_holding_hours, configured_cap_pressure_trigger_hours),
        )
        configured_cap_pressure_force_exit_hours = float(
            parameters.get(
                "exit.cap_pressure_force_exit_hours",
                self.max_holding_hours,
            )
        )
        self.cap_pressure_force_exit_hours = max(
            self.cap_pressure_trigger_hours,
            min(self.max_holding_hours, configured_cap_pressure_force_exit_hours),
        )
        self.confirmation_threshold = confirmation_threshold

    def evaluate(
        self, *, event: MarketEvent, position: PositionSnapshot | None
    ) -> ExitDecision:
        if position is None:
            return ExitDecision(
                should_exit=False,
                trigger_count=0,
                confirmation_threshold=self.confirmation_threshold,
                reasons=("no_open_position",),
                metadata={
                    "triggers": {
                        "target_capture": False,
                        "abnormal_volume": False,
                        "stale_thesis": False,
                        "max_holding_time": False,
                        "inventory_aging_derisk": False,
                    },
                    "forced_exit": False,
                    "inventory_aging_derisk_active": False,
                },
            )

        expected_move = abs(
            position.entry_estimated_probability - position.entry_midpoint
        )
        realized_move = abs(float(event.midpoint) - position.entry_midpoint)
        capture_ratio = (realized_move / expected_move) if expected_move > 0 else 0.0
        target_capture_trigger = (
            expected_move > 0 and capture_ratio >= self.target_capture_ratio
        )

        current_volume = _extract_volume_metric(event)
        reference_volume = max(position.reference_volume, 1.0)
        volume_multiplier = current_volume / reference_volume
        abnormal_volume_trigger = volume_multiplier >= self.volume_spike_multiplier

        holding_hours = _hours_between(position.opened_at, event.timestamp)
        absolute_price_change = abs(float(event.midpoint) - position.entry_midpoint)
        stale_thesis_trigger = (
            holding_hours >= self.stale_hours
            and absolute_price_change <= self.stale_price_change_threshold
        )
        max_holding_time_trigger = holding_hours >= self.max_holding_hours
        current_total_exposure_fraction = 0.0
        try:
            current_total_exposure_fraction = max(
                0.0,
                float(event.metadata.get("current_total_exposure_fraction", 0.0)),
            )
        except (TypeError, ValueError):
            current_total_exposure_fraction = 0.0
        cap_pressure_active = (
            self.cap_pressure_exposure_threshold <= 1.0
            and current_total_exposure_fraction
            >= self.cap_pressure_exposure_threshold
        )
        cap_pressure_derisk_trigger = (
            cap_pressure_active and holding_hours >= self.cap_pressure_trigger_hours
        )
        cap_pressure_force_exit_trigger = (
            cap_pressure_active and holding_hours >= self.cap_pressure_force_exit_hours
        )
        inventory_aging_derisk_trigger = (
            not max_holding_time_trigger
            and holding_hours >= self.inventory_aging_derisk_hours
        )

        trigger_reasons: list[str] = []
        if target_capture_trigger:
            trigger_reasons.append("target_capture_ratio_reached")
        if abnormal_volume_trigger:
            trigger_reasons.append("abnormal_volume_spike_detected")
        if stale_thesis_trigger:
            trigger_reasons.append("stale_thesis_detected")
        if max_holding_time_trigger:
            trigger_reasons.append("max_holding_time_exceeded_force_exit")
        if cap_pressure_derisk_trigger:
            trigger_reasons.append("cap_pressure_inventory_derisk")

        trigger_count = len(trigger_reasons)
        forced_exit = max_holding_time_trigger or cap_pressure_force_exit_trigger
        should_exit = forced_exit or trigger_count >= self.confirmation_threshold
        if forced_exit:
            if cap_pressure_force_exit_trigger:
                trigger_reasons.append("cap_pressure_force_exit")
            if trigger_count == 1:
                trigger_reasons.append("exit_forced_single_trigger")
            else:
                trigger_reasons.append("exit_forced_with_supporting_triggers")
        elif should_exit:
            trigger_reasons.append("exit_multi_trigger_confirmed")
        elif trigger_count > 0:
            trigger_reasons.append("exit_multi_trigger_unconfirmed")
        if inventory_aging_derisk_trigger:
            trigger_reasons.append("inventory_aging_derisk_active")

        return ExitDecision(
            should_exit=should_exit,
            trigger_count=trigger_count,
            confirmation_threshold=self.confirmation_threshold,
            reasons=tuple(trigger_reasons),
            metadata={
                "triggers": {
                    "target_capture": target_capture_trigger,
                    "abnormal_volume": abnormal_volume_trigger,
                    "stale_thesis": stale_thesis_trigger,
                    "max_holding_time": max_holding_time_trigger,
                    "inventory_aging_derisk": inventory_aging_derisk_trigger,
                        "cap_pressure_inventory_derisk": cap_pressure_derisk_trigger,
                        "cap_pressure_force_exit": cap_pressure_force_exit_trigger,
                },
                "forced_exit": forced_exit,
                "inventory_aging_derisk_active": inventory_aging_derisk_trigger,
                "cap_pressure_active": cap_pressure_active,
                "current_total_exposure_fraction": round(
                    current_total_exposure_fraction,
                    6,
                ),
                "cap_pressure_exposure_threshold": (
                    self.cap_pressure_exposure_threshold
                ),
                "cap_pressure_trigger_hours_threshold": (
                    self.cap_pressure_trigger_hours
                ),
                "cap_pressure_force_exit_hours_threshold": (
                    self.cap_pressure_force_exit_hours
                ),
                "target_capture_ratio": round(capture_ratio, 6),
                "target_capture_threshold": self.target_capture_ratio,
                "expected_move": round(expected_move, 6),
                "realized_move": round(realized_move, 6),
                "volume_multiplier": round(volume_multiplier, 6),
                "volume_spike_threshold": self.volume_spike_multiplier,
                "reference_volume": round(reference_volume, 6),
                "current_volume": round(current_volume, 6),
                "holding_hours": round(holding_hours, 6),
                "stale_hours_threshold": self.stale_hours,
                "inventory_aging_derisk_hours_threshold": (
                    self.inventory_aging_derisk_hours
                ),
                "max_holding_hours_threshold": self.max_holding_hours,
                "absolute_price_change": round(absolute_price_change, 6),
                "stale_price_change_threshold": self.stale_price_change_threshold,
                "position_open_notional": round(position.open_notional, 4),
                "position_fill_count": position.fill_count,
            },
        )
