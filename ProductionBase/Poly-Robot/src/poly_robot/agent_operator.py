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
        available_scenarios_clause = ""
        raw_available_scenarios = cycle_context.get("available_scenarios")
        if isinstance(raw_available_scenarios, list):
            normalized_available_scenarios = [
                str(item).strip()
                for item in raw_available_scenarios
                if str(item).strip()
            ]
            if normalized_available_scenarios:
                available_scenarios_clause = (
                    "Available scenarios for strategy mode: "
                    f"{normalized_available_scenarios}.\n"
                )
        serialized_context = json.dumps(cycle_context, indent=2, sort_keys=True)
        return (
            "# agents.md — v2\n"
            "System name: AgentOperator — Operator Layer for Poly-Robot.\n"
            "Architecture: two cooperative roles (Supervisor + Strategist) wrapping "
            "Poly-Robot.\n"
            "Source of truth for mechanics: POLY_ROBOT_ECONOMY_UNIFIED_SPEC.md.\n"
            "Phase reality: TRL4, advisory_only LLM calibration, and cost-attribution "
            "economics (net_pnl is execution-cost drag until MTM is implemented).\n"
            "Covenant:\n"
            "- Loyalty to user bankroll; if no action is justified, say so.\n"
            "- Calm, specific, non-hype tone.\n"
            "- Distinct refusal modes: factual unavailability -> bare token False; "
            "gate-driven refusal -> structured REJECTED:<reason_code> state.\n"
            "- Reversibility language must acknowledge spread/slippage/liquidity costs.\n"
            "Operational constraints:\n"
            "- Do not invent mechanics or override engine probabilities/confidence.\n"
            "- Defer to risk gates and reason codes exactly as emitted.\n"
            "- Use cost-aware language: gross_edge_bps, net_edge_bps, "
            "expected_slippage_bps, fee_rate_bps.\n"
            f"Operating mode: {mode}.\n"
            "Given the cycle context JSON below, produce one of two allowed outputs:\n"
            "A) If factual truth is unavailable in provided context, output exactly:\n"
            "False\n"
            "B) Otherwise output a strict JSON object with keys:\n"
            "{"
            "\"summary\": string, "
            "\"profitability_hypothesis\": string, "
            "\"risk_posture\": \"increase\"|\"reduce\"|\"neutral\", "
            "\"confidence\": number in [0,1], "
            "\"recommended_actions\": array of short actionable strings, "
            "\"scenario_hint\": string, "
            "\"state\": optional string (OK or REJECTED:<reason_code>)"
            "}\n"
            "Constraints:\n"
            "- Never suggest bypassing kill switch, drawdown limits, or risk caps.\n"
            "- Prefer execution-cost and edge-capture improvements.\n"
            "- Keep recommendations concrete and testable in next cycle.\n\n"
            "- When mode is strategy, scenario_hint should be one of available "
            "scenarios if suitable, otherwise empty string.\n"
            + available_scenarios_clause
            + f"Cycle context:\n{serialized_context}\n"
        )

    def _fallback_result(
        self,
        *,
        status: str,
        reason: str,
    ) -> dict[str, Any]:
        return {
            "status": status,
            "reason": reason,
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
            fallback = self._fallback_result(status="UNAVAILABLE", reason=str(exc))
            fallback["mode"] = mode
            return fallback
        except Exception as exc:  # pragma: no cover - defensive fail-open
            fallback = self._fallback_result(
                status="ERROR",
                reason=exc.__class__.__name__,
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
