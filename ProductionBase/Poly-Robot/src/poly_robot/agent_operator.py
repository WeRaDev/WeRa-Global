from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Protocol
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


def _clamp_confidence(value: Any) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if parsed < 0:
        return 0.0
    if parsed > 1:
        return 1.0
    return round(parsed, 4)


def _trim_text(value: Any, *, max_length: int = 512) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return f"{text[: max_length - 3]}..."


def _normalize_action_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    cleaned: list[str] = []
    for item in value:
        item_text = _trim_text(item, max_length=160)
        if not item_text:
            continue
        cleaned.append(item_text)
        if len(cleaned) >= 6:
            break
    return cleaned


def _normalize_mode(value: Any) -> str:
    mode = str(value or "advisory").strip().lower()
    if mode not in {"advisory", "strategy"}:
        return "advisory"
    return mode


def _normalize_scenario_hint(value: Any) -> str:
    hint = _trim_text(value, max_length=128).strip()
    if not hint:
        return ""
    return "".join(
        character
        for character in hint
        if character.isalnum() or character in {"_", "-", "."}
    ).strip()


def _is_bare_false_token(text: str) -> bool:
    return text.strip() == "False"


def _extract_json_object(text: str) -> dict[str, Any] | None:
    stripped = text.strip()
    if not stripped:
        return None
    try:
        payload = json.loads(stripped)
    except json.JSONDecodeError:
        first_brace = stripped.find("{")
        last_brace = stripped.rfind("}")
        if first_brace < 0 or last_brace <= first_brace:
            return None
        try:
            payload = json.loads(stripped[first_brace : last_brace + 1])
        except json.JSONDecodeError:
            return None
    if not isinstance(payload, dict):
        return None
    return payload


class AgentOperatorUnavailableError(RuntimeError):
    pass


class AgentOperatorClient(Protocol):
    provider: str
    model: str

    def complete(
        self,
        *,
        prompt: str,
        timeout_seconds: float,
    ) -> str: ...


@dataclass(frozen=True)
class ClaudeApiClient:
    model: str
    api_key_env: str = "ANTHROPIC_API_KEY"
    endpoint_url: str = "https://api.anthropic.com/v1/messages"
    max_output_tokens: int = 500
    temperature: float = 0.1
    anthropic_version: str = "2023-06-01"
    provider: str = "claude_api"

    def _resolve_api_key(self) -> str:
        env_name = self.api_key_env.strip()
        if not env_name:
            raise AgentOperatorUnavailableError(
                "agent_operator_api_key_env_not_configured"
            )
        api_key = os.environ.get(env_name, "").strip()
        if not api_key:
            raise AgentOperatorUnavailableError(
                f"agent_operator_api_key_missing:{env_name}"
            )
        return api_key

    @staticmethod
    def _extract_text(payload: dict[str, Any]) -> str:
        content = payload.get("content")
        if not isinstance(content, list):
            raise ValueError("claude_response_missing_content")
        text_chunks: list[str] = []
        for item in content:
            if not isinstance(item, dict):
                continue
            if str(item.get("type")) != "text":
                continue
            text_value = item.get("text")
            if text_value is None:
                continue
            text_chunks.append(str(text_value))
        response_text = "\n".join(chunk for chunk in text_chunks if chunk.strip()).strip()
        if not response_text:
            raise ValueError("claude_response_text_empty")
        return response_text

    def complete(
        self,
        *,
        prompt: str,
        timeout_seconds: float,
    ) -> str:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be > 0")
        api_key = self._resolve_api_key()
        payload = {
            "model": self.model,
            "max_tokens": int(self.max_output_tokens),
            "temperature": float(self.temperature),
            "messages": [{"role": "user", "content": prompt}],
        }
        request = Request(
            self.endpoint_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "X-API-Key": api_key,
                "anthropic-version": self.anthropic_version,
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=timeout_seconds) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                response_payload = json.loads(response.read().decode(charset))
        except HTTPError as exc:
            raise RuntimeError(f"claude_http_error:{exc.code}") from exc
        except URLError as exc:
            raise RuntimeError("claude_network_error") from exc
        except TimeoutError as exc:
            raise RuntimeError("claude_timeout") from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError("claude_invalid_json_response") from exc
        if not isinstance(response_payload, dict):
            raise RuntimeError("claude_invalid_response_payload")
        return self._extract_text(response_payload)

@dataclass(frozen=True)
class OpenFangApiClient:
    agent_id: str
    base_url: str = "http://127.0.0.1:4200"
    auth_token_env: str = ""
    provider: str = "openfang_api"
    model: str = "openfang_agent"

    def _resolve_agent_id(self) -> str:
        resolved = str(self.agent_id or "").strip()
        if not resolved:
            raise AgentOperatorUnavailableError(
                "agent_operator_openfang_agent_id_missing"
            )
        return resolved

    def _resolve_auth_token(self) -> str:
        env_name = str(self.auth_token_env or "").strip()
        if not env_name:
            return ""
        token = os.environ.get(env_name, "").strip()
        if not token:
            raise AgentOperatorUnavailableError(
                f"agent_operator_openfang_auth_token_missing:{env_name}"
            )
        return token

    def _build_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        auth_token = self._resolve_auth_token()
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        return headers

    def _request_json(
        self,
        *,
        method: str,
        path: str,
        timeout_seconds: float,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        base_url = str(self.base_url or "").strip().rstrip("/")
        if not base_url:
            raise AgentOperatorUnavailableError(
                "agent_operator_openfang_base_url_missing"
            )
        request = Request(
            f"{base_url}{path}",
            data=(
                None
                if payload is None
                else json.dumps(payload, separators=(",", ":")).encode("utf-8")
            ),
            headers=self._build_headers(),
            method=method,
        )
        try:
            with urlopen(request, timeout=timeout_seconds) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                body = response.read().decode(charset)
        except HTTPError as exc:
            raise RuntimeError(f"openfang_http_error:{exc.code}") from exc
        except URLError as exc:
            raise RuntimeError("openfang_network_error") from exc
        except TimeoutError as exc:
            raise RuntimeError("openfang_timeout") from exc
        try:
            response_payload = json.loads(body)
        except json.JSONDecodeError as exc:
            raise RuntimeError("openfang_invalid_json_response") from exc
        if not isinstance(response_payload, dict):
            raise RuntimeError("openfang_invalid_response_payload")
        return response_payload

    def complete(
        self,
        *,
        prompt: str,
        timeout_seconds: float,
    ) -> str:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be > 0")
        agent_id = self._resolve_agent_id()
        self._request_json(
            method="GET",
            path="/api/health",
            timeout_seconds=timeout_seconds,
        )
        response_payload = self._request_json(
            method="POST",
            path=f"/api/agents/{agent_id}/message",
            timeout_seconds=timeout_seconds,
            payload={"message": prompt},
        )
        response_text = str(response_payload.get("response", "")).strip()
        if not response_text:
            raise RuntimeError("openfang_response_text_empty")
        return response_text

def _compact_cycle_context(cycle_context: dict[str, Any]) -> dict[str, Any]:
    compact: dict[str, Any] = {}
    scalar_keys = (
        "cycle_index",
        "scenario_name",
        "ingestion_mode",
        "ingestion_status",
        "ingestion_degraded_streak",
        "risk_allowed_count",
        "filled_trade_count",
        "partial_fill_count",
        "exit_candidate_count",
        "confirmed_exit_count",
        "forced_exit_count",
        "expected_gross_edge_value",
        "expected_net_edge_value",
        "expected_net_edge_value_on_fills",
        "expected_value_after_execution_cost",
        "total_execution_cost",
        "total_fees_paid",
        "total_slippage_cost",
        "execution_cost_to_expected_net_ratio",
    )
    for key in scalar_keys:
        if key in cycle_context:
            compact[key] = cycle_context.get(key)

    ingestion_reasons = cycle_context.get("ingestion_reasons")
    if isinstance(ingestion_reasons, list):
        compact["ingestion_reasons"] = [
            _trim_text(reason, max_length=80) for reason in ingestion_reasons[:8]
        ]

    portfolio = cycle_context.get("portfolio")
    if isinstance(portfolio, dict):
        compact["portfolio"] = {
            "bankroll": portfolio.get("bankroll"),
            "current_equity": portfolio.get("current_equity"),
            "net_pnl": portfolio.get("net_pnl"),
            "open_notional": portfolio.get("open_notional"),
            "open_positions": portfolio.get("open_positions"),
            "total_exposure_fraction": portfolio.get("total_exposure_fraction"),
            "daily_drawdown_fraction": portfolio.get("daily_drawdown_fraction"),
        }

    operator_controls = cycle_context.get("operator_controls")
    if isinstance(operator_controls, dict):
        compact["operator_controls"] = {
            "kill_switch_active": bool(
                operator_controls.get("kill_switch_active", False)
            ),
            "cancel_all_requested": bool(
                operator_controls.get("cancel_all_requested", False)
            ),
            "cancel_all_acknowledged": bool(
                operator_controls.get("cancel_all_acknowledged", False)
            ),
        }

    available_scenarios = cycle_context.get("available_scenarios")
    if isinstance(available_scenarios, list):
        compact["available_scenarios"] = [
            str(item).strip()
            for item in available_scenarios[:12]
            if str(item).strip()
        ]

    open_positions_detail = cycle_context.get("open_positions_detail")
    if isinstance(open_positions_detail, list):
        compact["open_positions_detail_count"] = len(open_positions_detail)
    closed_positions_recent = cycle_context.get("closed_positions_recent")
    if isinstance(closed_positions_recent, list):
        compact["closed_positions_recent_count"] = len(closed_positions_recent)

    return compact


class AgentOperator:
    def __init__(
        self,
        *,
        client: AgentOperatorClient,
        timeout_seconds: float = 8.0,
        enabled: bool = True,
    ) -> None:
        self.client = client
        self.timeout_seconds = timeout_seconds
        self.enabled = enabled

    @staticmethod
    def _build_prompt(cycle_context: dict[str, Any]) -> str:
        mode = _normalize_mode(cycle_context.get("agent_operator_mode"))
        serialized_context = json.dumps(
            _compact_cycle_context(cycle_context), indent=2, sort_keys=True
        )
        return (
            "You are an operator advisor for Poly-Robot.\n"
            f"Mode: {mode}.\n"
            "Output format (strict, no markdown, no prose outside output):\n"
            "A) If context is insufficient, output exactly: False\n"
            "B) Otherwise output one JSON object with keys:\n"
            "{"
            "\"summary\": string, "
            "\"profitability_hypothesis\": string, "
            "\"risk_posture\": \"increase\"|\"reduce\"|\"neutral\", "
            "\"confidence\": number in [0,1], "
            "\"recommended_actions\": array of short actionable strings, "
            "\"scenario_hint\": string, "
            "\"state\": optional string (OK or REJECTED:<reason_code>)"
            "}\n"
            "Rules:\n"
            "- Keep summary under 220 characters.\n"
            "- Keep recommended_actions to at most 4 items.\n"
            "- Do not suggest bypassing kill switch, drawdown limits, or risk caps.\n"
            "- Prefer execution-cost and edge-capture improvements.\n"
            "- If mode=strategy, scenario_hint must be one of available_scenarios or empty.\n"
            + f"Cycle context:\n{serialized_context}\n"
        )

    def _fallback_result(
        self,
        *,
        status: str,
        reason: str,
        reason_detail: str = "",
    ) -> dict[str, Any]:
        return {
            "status": status,
            "reason": reason,
            "reason_detail": _trim_text(reason_detail, max_length=256),
            "provider": self.client.provider,
            "model": self.client.model,
            "mode": "advisory",
            "generated_at": _utc_now_iso(),
            "summary": "",
            "profitability_hypothesis": "",
            "risk_posture": "neutral",
            "confidence": None,
            "recommended_actions": [],
            "scenario_hint": "",
        }

    def infer(self, *, cycle_context: dict[str, Any]) -> dict[str, Any]:
        mode = _normalize_mode(cycle_context.get("agent_operator_mode"))
        if not self.enabled:
            fallback = self._fallback_result(
                status="DISABLED",
                reason="agent_operator_disabled",
            )
            fallback["mode"] = mode
            return fallback
        prompt = self._build_prompt(cycle_context)
        try:
            response_text = self.client.complete(
                prompt=prompt,
                timeout_seconds=self.timeout_seconds,
            )
        except AgentOperatorUnavailableError as exc:
            fallback = self._fallback_result(
                status="UNAVAILABLE",
                reason=str(exc),
                reason_detail=str(exc),
            )
            fallback["mode"] = mode
            return fallback
        except Exception as exc:  # pragma: no cover - defensive fail-open
            fallback = self._fallback_result(
                status="ERROR",
                reason=exc.__class__.__name__,
                reason_detail=str(exc),
            )
            fallback["mode"] = mode
            return fallback
        if _is_bare_false_token(response_text):
            return {
                "status": "UNAVAILABLE",
                "reason": "factual_unavailable_false",
                "provider": self.client.provider,
                "model": self.client.model,
                "mode": mode,
                "generated_at": _utc_now_iso(),
                "summary": "",
                "profitability_hypothesis": "",
                "risk_posture": "neutral",
                "confidence": None,
                "recommended_actions": [],
                "scenario_hint": "",
            }

        parsed = _extract_json_object(response_text)
        if parsed is None:
            return {
                "status": "OK",
                "reason": "unstructured_response",
                "provider": self.client.provider,
                "model": self.client.model,
                "mode": mode,
                "generated_at": _utc_now_iso(),
                "summary": _trim_text(response_text),
                "profitability_hypothesis": "",
                "risk_posture": "neutral",
                "confidence": None,
                "recommended_actions": [],
                "scenario_hint": "",
            }

        risk_posture = str(parsed.get("risk_posture", "neutral")).strip().lower()
        if risk_posture not in {"increase", "reduce", "neutral"}:
            risk_posture = "neutral"
        raw_state = str(parsed.get("state", "")).strip()
        normalized_status = "OK"
        normalized_reason = ""
        if raw_state.upper().startswith("REJECTED:"):
            normalized_status = "REJECTED"
            normalized_reason = raw_state.split(":", 1)[1].strip()
        elif raw_state:
            normalized_status = raw_state.upper()
        return {
            "status": normalized_status,
            "reason": normalized_reason,
            "provider": self.client.provider,
            "model": self.client.model,
            "mode": mode,
            "generated_at": _utc_now_iso(),
            "summary": _trim_text(parsed.get("summary", "")),
            "profitability_hypothesis": _trim_text(
                parsed.get("profitability_hypothesis", "")
            ),
            "risk_posture": risk_posture,
            "confidence": _clamp_confidence(parsed.get("confidence")),
            "recommended_actions": _normalize_action_list(
                parsed.get("recommended_actions")
            ),
            "scenario_hint": _normalize_scenario_hint(parsed.get("scenario_hint", "")),
        }


class AgencyGateway:
    def __init__(self, operators_by_mode: dict[str, AgentOperator]) -> None:
        self.operators_by_mode = dict(operators_by_mode)

    def skipped_result(self, *, reason: str, mode: str) -> dict[str, Any]:
        operator = self.operators_by_mode.get(mode)
        if operator is None:
            return {
                "status": "DISABLED",
                "reason": reason,
                "reason_detail": "",
                "provider": "none",
                "model": "none",
                "mode": mode,
                "generated_at": _utc_now_iso(),
                "summary": "",
                "profitability_hypothesis": "",
                "risk_posture": "neutral",
                "confidence": None,
                "recommended_actions": [],
                "scenario_hint": "",
            }
        return {
            "status": "SKIPPED",
            "reason": reason,
            "reason_detail": "",
            "provider": operator.client.provider,
            "model": operator.client.model,
            "mode": mode,
            "generated_at": _utc_now_iso(),
            "summary": "",
            "profitability_hypothesis": "",
            "risk_posture": "neutral",
            "confidence": None,
            "recommended_actions": [],
            "scenario_hint": "",
        }

    def infer_roles(
        self,
        *,
        base_cycle_context: dict[str, Any],
        requested_role_modes: dict[str, str],
        all_role_modes: dict[str, str],
        operators_enabled: bool,
        disabled_reason: str = "agent_operators_stopped_by_control",
        role_not_requested_reason: str = "agent_operator_role_not_requested_by_mode",
    ) -> dict[str, dict[str, Any]]:
        role_results: dict[str, dict[str, Any]] = {}
        if not operators_enabled:
            for role_name, role_mode in all_role_modes.items():
                role_results[role_name] = self.skipped_result(
                    reason=disabled_reason,
                    mode=role_mode,
                )
            return role_results

        for role_name, role_mode in all_role_modes.items():
            if role_name not in requested_role_modes:
                role_results[role_name] = self.skipped_result(
                    reason=role_not_requested_reason,
                    mode=role_mode,
                )
                continue
            operator = self.operators_by_mode.get(role_mode)
            if operator is None:
                role_results[role_name] = self.skipped_result(
                    reason="agent_operator_mode_not_configured",
                    mode=role_mode,
                )
                continue
            role_results[role_name] = operator.infer(
                cycle_context={
                    **base_cycle_context,
                    "agent_operator_role": role_name,
                    "agent_operator_mode": role_mode,
                }
            )
        return role_results
