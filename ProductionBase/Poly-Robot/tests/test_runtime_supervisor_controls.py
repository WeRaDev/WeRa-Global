from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
SCRIPT_PATH = ROOT_DIR / "scripts" / "run_runtime_supervisor.py"
PROFILE_PATH = (
    ROOT_DIR / "config" / "parameters" / "profiles" / "mvp_test_token.v1.json"
)
CALIBRATION_POLICY_PATH = (
    ROOT_DIR / "config" / "calibration" / "llm_reliability.v1.json"
)
SCENARIO_PACK_PATH = ROOT_DIR / "config" / "replay" / "scenario_pack.v1.json"
REPLAY_FIXTURE_PATH = ROOT_DIR / "tests" / "fixtures" / "replay_events.jsonl"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.schemas import (  # noqa: E402
    RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
    RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION,
)


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


class RuntimeSupervisorControlIntegrationTests(unittest.TestCase):
    def _start_mock_claude_server(
        self, *, response_text: str
    ) -> tuple[ThreadingHTTPServer, threading.Thread, str]:
        class _MockClaudeHandler(BaseHTTPRequestHandler):
            def do_POST(self) -> None:  # noqa: N802
                content_length = int(self.headers.get("Content-Length", "0"))
                if content_length > 0:
                    self.rfile.read(content_length)
                body = {
                    "content": [
                        {
                            "type": "text",
                            "text": response_text,
                        }
                    ]
                }
                encoded = json.dumps(body).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)

            def log_message(self, format: str, *args) -> None:  # noqa: A003
                del format, args
                return

        server = ThreadingHTTPServer(("127.0.0.1", 0), _MockClaudeHandler)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        host, port = server.server_address
        return server, worker, f"http://{host}:{port}/v1/messages"

    def _run_supervisor(
        self,
        *,
        temp_root: Path,
        control_state_payload: dict,
        cycles: int,
        scenario: str = "baseline",
        cycle_output: bool = False,
        extra_args: list[str] | None = None,
        env: dict[str, str] | None = None,
        disable_single_supervisor_lock: bool = True,
    ) -> tuple[subprocess.CompletedProcess[str], Path, Path, Path, Path]:
        state_path = temp_root / "runtime_state.json"
        journal_path = temp_root / "runtime_journal.jsonl"
        control_state_path = temp_root / "operator_control_state.json"
        audit_path = temp_root / "operator_action_audit.jsonl"
        _write_json(control_state_path, control_state_payload)

        command = [
            sys.executable,
            str(SCRIPT_PATH),
            "--events",
            str(REPLAY_FIXTURE_PATH),
            "--profile",
            str(PROFILE_PATH),
            "--calibration-policy",
            str(CALIBRATION_POLICY_PATH),
            "--scenario-pack",
            str(SCENARIO_PACK_PATH),
            "--scenario",
            scenario,
            "--cycles",
            str(cycles),
            "--max-retries",
            "0",
            "--retry-backoff-seconds",
            "0",
            "--state-path",
            str(state_path),
            "--journal-path",
            str(journal_path),
            "--control-state-path",
            str(control_state_path),
            "--control-audit-path",
            str(audit_path),
        ]
        if cycle_output:
            command.extend(["--cycle-output-dir", str(temp_root / "cycles")])
        if disable_single_supervisor_lock:
            command.append("--disable-single-supervisor-lock")
        if extra_args:
            command.extend(extra_args)

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )
        return result, state_path, journal_path, control_state_path, audit_path

    def test_pause_control_skips_cycle_execution(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            control_state = {
                "schema_version": RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
                "updated_at": "2026-01-01T00:00:00Z",
                "control_version": 5,
                "paused": True,
                "restart_requested": False,
                "kill_switch_active": False,
                "cancel_all_requested": False,
                "selected_scenario": "baseline",
                "agent_operator_enabled": True,
                "agent_operator_mode": "advisory",
                "last_annotation": "",
            }
            result, state_path, journal_path, _, _ = self._run_supervisor(
                temp_root=root,
                control_state_payload=control_state,
                cycles=2,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            state = _read_json(state_path)
            self.assertEqual(
                state["schema_version"], RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION
            )
            self.assertEqual(state["cycle_index"], 2)
            metadata = state["worker_results"][0]["last_metadata"]
            self.assertEqual(metadata["cycle_status"], "PAUSED")
            self.assertEqual(metadata["events"], 0)
            stages = {
                (row.get("payload") or {}).get("stage")
                for row in _read_jsonl(journal_path)
                if row.get("event_type") == "worker_heartbeat"
            }
            self.assertIn("control_pause_gate", stages)

    def test_restart_request_is_acknowledged_and_stops_early(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            control_state = {
                "schema_version": RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
                "updated_at": "2026-01-01T00:00:00Z",
                "control_version": 3,
                "paused": False,
                "restart_requested": True,
                "kill_switch_active": False,
                "cancel_all_requested": False,
                "selected_scenario": "baseline",
                "agent_operator_enabled": True,
                "agent_operator_mode": "advisory",
                "last_annotation": "",
            }
            result, state_path, _, control_state_path, audit_path = (
                self._run_supervisor(
                    temp_root=root,
                    control_state_payload=control_state,
                    cycles=3,
                )
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            self.assertIn("stopped_by_control_restart=True", result.stdout)
            state = _read_json(state_path)
            self.assertEqual(state["cycle_index"], 1)
            metadata = state["worker_results"][0]["last_metadata"]
            self.assertEqual(metadata["cycle_status"], "RESTART_REQUESTED")

            updated_control_state = _read_json(control_state_path)
            self.assertFalse(updated_control_state["restart_requested"])
            audit_events = _read_jsonl(audit_path)
            self.assertTrue(audit_events)
            self.assertEqual(
                audit_events[-1]["action"], "graceful_restart_acknowledged"
            )

    def test_selected_scenario_from_control_state_is_used_for_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            control_state = {
                "schema_version": RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
                "updated_at": "2026-01-01T00:00:00Z",
                "control_version": 8,
                "paused": False,
                "restart_requested": False,
                "kill_switch_active": False,
                "cancel_all_requested": False,
                "selected_scenario": "liquidity_crunch",
                "last_annotation": "",
            }
            result, state_path, _, _, _ = self._run_supervisor(
                temp_root=root,
                control_state_payload=control_state,
                cycles=1,
                cycle_output=True,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            state = _read_json(state_path)
            metadata = state["worker_results"][0]["last_metadata"]
            self.assertEqual(metadata["cycle_status"], "EXECUTED")
            self.assertEqual(metadata["selected_scenario"], "liquidity_crunch")

            cycle_report = _read_json(root / "cycles" / "cycle_001.json")
            self.assertEqual(
                cycle_report["run_context"]["scenario_name"], "liquidity_crunch"
            )

    def test_agent_operator_fail_open_metadata_is_written_to_run_context(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            control_state = {
                "schema_version": RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
                "updated_at": "2026-01-01T00:00:00Z",
                "control_version": 9,
                "paused": False,
                "restart_requested": False,
                "kill_switch_active": False,
                "cancel_all_requested": False,
                "selected_scenario": "baseline",
                "agent_operator_enabled": True,
                "agent_operator_mode": "advisory",
                "last_annotation": "",
            }
            env = dict(os.environ)
            env.pop("POLY_ROBOT_TEST_MISSING_CLAUDE_KEY", None)
            result, state_path, _, _, _ = self._run_supervisor(
                temp_root=root,
                control_state_payload=control_state,
                cycles=1,
                cycle_output=True,
                extra_args=[
                    "--agent-operator-enabled",
                    "--agent-operator-api-key-env",
                    "POLY_ROBOT_TEST_MISSING_CLAUDE_KEY",
                ],
                env=env,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            state = _read_json(state_path)
            metadata = state["worker_results"][0]["last_metadata"]
            self.assertEqual(metadata["agent_operator_status"], "UNAVAILABLE")
            cycle_report = _read_json(root / "cycles" / "cycle_001.json")
            advisory = cycle_report["run_context"]["agent_operator"]
            self.assertEqual(advisory["status"], "UNAVAILABLE")
            self.assertIn(
                "agent_operator_api_key_missing",
                advisory["reason"],
            )

    def test_agent_operator_openfang_fail_open_metadata_is_written_to_run_context(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            control_state = {
                "schema_version": RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
                "updated_at": "2026-01-01T00:00:00Z",
                "control_version": 10,
                "paused": False,
                "restart_requested": False,
                "kill_switch_active": False,
                "cancel_all_requested": False,
                "selected_scenario": "baseline",
                "agent_operator_enabled": True,
                "agent_operator_mode": "advisory",
                "last_annotation": "",
            }
            result, state_path, _, _, _ = self._run_supervisor(
                temp_root=root,
                control_state_payload=control_state,
                cycles=1,
                cycle_output=True,
                extra_args=[
                    "--agent-operator-enabled",
                    "--agent-operator-backend",
                    "openfang_api",
                ],
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            state = _read_json(state_path)
            metadata = state["worker_results"][0]["last_metadata"]
            self.assertEqual(metadata["agent_operator_status"], "UNAVAILABLE")
            self.assertEqual(metadata["agent_operator_provider"], "openfang_api")
            cycle_report = _read_json(root / "cycles" / "cycle_001.json")
            advisory = cycle_report["run_context"]["agent_operator"]
            self.assertEqual(advisory["status"], "UNAVAILABLE")
            self.assertEqual(
                advisory["reason"],
                "agent_operator_openfang_agent_id_missing",
            )
    def test_advisory_mode_runs_supervisor_role_and_skips_strategist_role(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            control_state = {
                "schema_version": RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
                "updated_at": "2026-01-01T00:00:00Z",
                "control_version": 11,
                "paused": False,
                "restart_requested": False,
                "kill_switch_active": False,
                "cancel_all_requested": False,
                "selected_scenario": "baseline",
                "agent_operator_enabled": True,
                "agent_operator_mode": "advisory",
                "last_annotation": "",
            }
            response_text = json.dumps(
                {
                    "summary": "Maintain baseline posture.",
                    "profitability_hypothesis": "Edge remains stable.",
                    "risk_posture": "neutral",
                    "confidence": 0.6,
                    "recommended_actions": [],
                    "scenario_hint": "",
                }
            )
            server, worker, endpoint = self._start_mock_claude_server(
                response_text=response_text
            )
            try:
                env = dict(os.environ)
                env["POLY_ROBOT_TEST_AGENT_KEY"] = "test-key"
                result, state_path, _, _, _ = self._run_supervisor(
                    temp_root=root,
                    control_state_payload=control_state,
                    cycles=1,
                    cycle_output=True,
                    extra_args=[
                        "--agent-operator-enabled",
                        "--agent-operator-api-key-env",
                        "POLY_ROBOT_TEST_AGENT_KEY",
                        "--agent-operator-endpoint-url",
                        endpoint,
                    ],
                    env=env,
                )
            finally:
                server.shutdown()
                server.server_close()
                worker.join(timeout=5)

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            state = _read_json(state_path)
            metadata = state["worker_results"][0]["last_metadata"]
            self.assertIsInstance(metadata.get("open_positions_detail"), list)
            self.assertIsInstance(metadata.get("closed_positions_recent"), list)
            for row in metadata["open_positions_detail"] + metadata["closed_positions_recent"]:
                self.assertIn("verification_url", row)

            cycle_report = _read_json(root / "cycles" / "cycle_001.json")
            run_context = cycle_report["run_context"]
            self.assertIsInstance(run_context.get("open_positions_detail"), list)
            self.assertIsInstance(run_context.get("closed_positions_recent"), list)

            agent_operators = run_context["agent_operators"]
            self.assertEqual(agent_operators["supervisor"]["status"], "OK")
            self.assertEqual(agent_operators["supervisor"]["mode"], "advisory")
            self.assertEqual(agent_operators["strategist"]["status"], "SKIPPED")
            self.assertEqual(
                agent_operators["strategist"]["reason"],
                "agent_operator_role_not_requested_by_mode",
            )

    def test_strategy_mode_applies_valid_scenario_hint_for_future_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            control_state = {
                "schema_version": RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
                "updated_at": "2026-01-01T00:00:00Z",
                "control_version": 12,
                "paused": False,
                "restart_requested": False,
                "kill_switch_active": False,
                "cancel_all_requested": False,
                "selected_scenario": "baseline",
                "agent_operator_enabled": True,
                "agent_operator_mode": "strategy",
                "agent_operator_strategy_auto_apply": True,
                "last_annotation": "",
            }
            response_text = json.dumps(
                {
                    "summary": "Shift toward stress scenario.",
                    "profitability_hypothesis": "Pre-position for volatility.",
                    "risk_posture": "neutral",
                    "confidence": 0.7,
                    "recommended_actions": ["Switch scenario for next cycle"],
                    "scenario_hint": "liquidity_crunch",
                }
            )
            server, worker, endpoint = self._start_mock_claude_server(
                response_text=response_text
            )
            try:
                env = dict(os.environ)
                env["POLY_ROBOT_TEST_AGENT_KEY"] = "test-key"
                result, state_path, _, control_state_path, _ = self._run_supervisor(
                    temp_root=root,
                    control_state_payload=control_state,
                    cycles=1,
                    cycle_output=True,
                    extra_args=[
                        "--agent-operator-api-key-env",
                        "POLY_ROBOT_TEST_AGENT_KEY",
                        "--agent-operator-endpoint-url",
                        endpoint,
                    ],
                    env=env,
                )
            finally:
                server.shutdown()
                server.server_close()
                worker.join(timeout=5)

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            state = _read_json(state_path)
            metadata = state["worker_results"][0]["last_metadata"]
            self.assertEqual(metadata["agent_operator_mode"], "strategy")
            self.assertEqual(
                metadata["agent_operator_strategy_scenario_hint"],
                "liquidity_crunch",
            )
            self.assertTrue(metadata["agent_operator_strategy_scenario_applied"])
            self.assertEqual(
                metadata["agent_operator_strategy_scenario_rejected_reason"], ""
            )
            self.assertEqual(metadata["selected_scenario"], "baseline")
            strategy_candidate_id = str(
                metadata.get("agent_operator_strategy_candidate_id", "")
            ).strip()
            self.assertTrue(strategy_candidate_id.startswith("cand-"))
            learning_recommendation = metadata.get("agent_operator_learning_recommendation")
            self.assertIsInstance(learning_recommendation, dict)
            self.assertTrue(
                str(learning_recommendation.get("recommendation_id", "")).startswith(
                    "rec-"
                )
            )
            learning_candidate = metadata.get("agent_operator_learning_candidate")
            self.assertIsInstance(learning_candidate, dict)
            self.assertEqual(learning_candidate.get("candidate_id"), strategy_candidate_id)
            outcome_attribution = metadata.get(
                "agent_operator_learning_outcome_attribution"
            )
            self.assertIsInstance(outcome_attribution, dict)
            self.assertEqual(outcome_attribution.get("attributed_count"), 0)
            self.assertEqual(metadata.get("agent_operator_learning_record_error"), "")
            self.assertEqual(
                metadata.get("agent_operator_learning_outcome_attribution_error"), ""
            )

            updated_control_state = _read_json(control_state_path)
            self.assertEqual(
                updated_control_state["selected_scenario"], "liquidity_crunch"
            )
            self.assertEqual(
                updated_control_state["agent_operator_active_candidate_id"],
                strategy_candidate_id,
            )
            self.assertEqual(
                updated_control_state["agent_operator_active_candidate_scenario"],
                "liquidity_crunch",
            )
            self.assertEqual(
                updated_control_state["agent_operator_candidate_previous_scenario"],
                "baseline",
            )
            self.assertEqual(
                updated_control_state["agent_operator_candidate_last_action"],
                "applied",
            )

            cycle_report = _read_json(root / "cycles" / "cycle_001.json")
            run_context = cycle_report["run_context"]
            self.assertEqual(run_context["agent_operator_mode"], "strategy")
            self.assertTrue(run_context["agent_operator_strategy_scenario_applied"])
            self.assertEqual(
                run_context["agent_operator_strategy_scenario_hint"],
                "liquidity_crunch",
            )
            self.assertEqual(
                run_context["agent_operator_strategy_candidate_id"],
                strategy_candidate_id,
            )
            self.assertEqual(
                (run_context["agent_operator_learning_recommendation"] or {}).get(
                    "recommendation_id"
                ),
                learning_recommendation.get("recommendation_id"),
            )
            self.assertEqual(
                (run_context["agent_operator_learning_candidate"] or {}).get(
                    "candidate_id"
                ),
                strategy_candidate_id,
            )
            self.assertEqual(
                (run_context["agent_operator_learning_outcome_attribution"] or {}).get(
                    "attributed_count"
                ),
                0,
            )

            learning_state = _read_json(root / "agent_operator_learning_state.json")
            self.assertEqual(learning_state["recommendation_sequence"], 1)
            self.assertEqual(learning_state["candidate_sequence"], 1)
            self.assertEqual(learning_state["active_candidate_id"], strategy_candidate_id)
            self.assertEqual(learning_state["recommendations"][-1]["status"], "pending_outcome")
            self.assertEqual(learning_state["candidates"][-1]["status"], "active")

    def test_strategy_mode_rejects_invalid_scenario_hint(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            control_state = {
                "schema_version": RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
                "updated_at": "2026-01-01T00:00:00Z",
                "control_version": 13,
                "paused": False,
                "restart_requested": False,
                "kill_switch_active": False,
                "cancel_all_requested": False,
                "selected_scenario": "baseline",
                "agent_operator_enabled": True,
                "agent_operator_mode": "strategy",
                "agent_operator_strategy_auto_apply": True,
                "last_annotation": "",
            }
            response_text = json.dumps(
                {
                    "summary": "Try unsupported scenario.",
                    "profitability_hypothesis": "N/A",
                    "risk_posture": "neutral",
                    "confidence": 0.4,
                    "recommended_actions": [],
                    "scenario_hint": "not_a_real_scenario",
                }
            )
            server, worker, endpoint = self._start_mock_claude_server(
                response_text=response_text
            )
            try:
                env = dict(os.environ)
                env["POLY_ROBOT_TEST_AGENT_KEY"] = "test-key"
                result, state_path, _, control_state_path, _ = self._run_supervisor(
                    temp_root=root,
                    control_state_payload=control_state,
                    cycles=1,
                    extra_args=[
                        "--agent-operator-api-key-env",
                        "POLY_ROBOT_TEST_AGENT_KEY",
                        "--agent-operator-endpoint-url",
                        endpoint,
                    ],
                    env=env,
                )
            finally:
                server.shutdown()
                server.server_close()
                worker.join(timeout=5)

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            state = _read_json(state_path)
            metadata = state["worker_results"][0]["last_metadata"]
            self.assertEqual(metadata["agent_operator_mode"], "strategy")
            self.assertFalse(metadata["agent_operator_strategy_scenario_applied"])
            self.assertEqual(
                metadata["agent_operator_strategy_scenario_hint"],
                "not_a_real_scenario",
            )
            self.assertEqual(
                metadata["agent_operator_strategy_scenario_rejected_reason"],
                "invalid_strategy_scenario_hint",
            )
            self.assertEqual(metadata.get("agent_operator_strategy_candidate_id"), "")
            learning_candidate = metadata.get("agent_operator_learning_candidate")
            self.assertIsInstance(learning_candidate, dict)
            self.assertEqual(
                learning_candidate.get("scenario_name"),
                "not_a_real_scenario",
            )
            updated_control_state = _read_json(control_state_path)
            self.assertEqual(updated_control_state["selected_scenario"], "baseline")
            self.assertEqual(
                str(updated_control_state.get("agent_operator_active_candidate_id", "")),
                "",
            )

            learning_state = _read_json(root / "agent_operator_learning_state.json")
            self.assertEqual(learning_state["recommendation_sequence"], 1)
            self.assertEqual(learning_state["candidate_sequence"], 1)
            self.assertEqual(learning_state["active_candidate_id"], "")
            self.assertEqual(learning_state["candidates"][-1]["status"], "pending")

    def test_strategy_mode_respects_strategy_auto_apply_disable_flag(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            control_state = {
                "schema_version": RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
                "updated_at": "2026-01-01T00:00:00Z",
                "control_version": 14,
                "paused": False,
                "restart_requested": False,
                "kill_switch_active": False,
                "cancel_all_requested": False,
                "selected_scenario": "baseline",
                "agent_operator_enabled": True,
                "agent_operator_mode": "strategy",
                "agent_operator_strategy_auto_apply": False,
                "last_annotation": "",
            }
            response_text = json.dumps(
                {
                    "summary": "Recommend stress scenario without auto-apply.",
                    "profitability_hypothesis": "Volatility likely to increase.",
                    "risk_posture": "neutral",
                    "confidence": 0.6,
                    "recommended_actions": [],
                    "scenario_hint": "liquidity_crunch",
                }
            )
            server, worker, endpoint = self._start_mock_claude_server(
                response_text=response_text
            )
            try:
                env = dict(os.environ)
                env["POLY_ROBOT_TEST_AGENT_KEY"] = "test-key"
                result, state_path, _, control_state_path, _ = self._run_supervisor(
                    temp_root=root,
                    control_state_payload=control_state,
                    cycles=1,
                    cycle_output=True,
                    extra_args=[
                        "--agent-operator-api-key-env",
                        "POLY_ROBOT_TEST_AGENT_KEY",
                        "--agent-operator-endpoint-url",
                        endpoint,
                    ],
                    env=env,
                )
            finally:
                server.shutdown()
                server.server_close()
                worker.join(timeout=5)

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            state = _read_json(state_path)
            metadata = state["worker_results"][0]["last_metadata"]
            self.assertEqual(metadata["agent_operator_mode"], "strategy")
            self.assertFalse(metadata["agent_operator_strategy_scenario_applied"])
            self.assertEqual(
                metadata["agent_operator_strategy_scenario_hint"],
                "liquidity_crunch",
            )
            self.assertEqual(
                metadata["agent_operator_strategy_scenario_rejected_reason"],
                "strategy_auto_apply_disabled",
            )
            self.assertEqual(metadata["agent_operator_strategy_candidate_id"], "")
            learning_candidate = metadata.get("agent_operator_learning_candidate")
            self.assertIsInstance(learning_candidate, dict)
            self.assertTrue(
                str(learning_candidate.get("candidate_id", "")).startswith("cand-")
            )
            self.assertEqual(metadata["selected_scenario"], "baseline")

            updated_control_state = _read_json(control_state_path)
            self.assertEqual(updated_control_state["selected_scenario"], "baseline")
            self.assertEqual(
                str(updated_control_state.get("agent_operator_active_candidate_id", "")),
                "",
            )
            self.assertFalse(updated_control_state["agent_operator_strategy_auto_apply"])

            cycle_report = _read_json(root / "cycles" / "cycle_001.json")
            run_context = cycle_report["run_context"]
            self.assertEqual(
                run_context["agent_operator_strategy_scenario_rejected_reason"],
                "strategy_auto_apply_disabled",
            )
            self.assertEqual(run_context["agent_operator_strategy_candidate_id"], "")
            self.assertIsInstance(
                run_context["agent_operator_learning_candidate"],
                dict,
            )

    def test_strategy_mode_attributes_delayed_learning_outcomes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            control_state = {
                "schema_version": RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
                "updated_at": "2026-01-01T00:00:00Z",
                "control_version": 15,
                "paused": False,
                "restart_requested": False,
                "kill_switch_active": False,
                "cancel_all_requested": False,
                "selected_scenario": "baseline",
                "agent_operator_enabled": True,
                "agent_operator_mode": "strategy",
                "agent_operator_strategy_auto_apply": True,
                "last_annotation": "",
            }
            response_text = json.dumps(
                {
                    "summary": "Sustain stress scenario for near-term risk.",
                    "profitability_hypothesis": "Near-term volatility opportunities.",
                    "risk_posture": "neutral",
                    "confidence": 0.7,
                    "recommended_actions": [],
                    "scenario_hint": "liquidity_crunch",
                }
            )
            server, worker, endpoint = self._start_mock_claude_server(
                response_text=response_text
            )
            try:
                env = dict(os.environ)
                env["POLY_ROBOT_TEST_AGENT_KEY"] = "test-key"
                result, _, _, _, _ = self._run_supervisor(
                    temp_root=root,
                    control_state_payload=control_state,
                    cycles=2,
                    cycle_output=True,
                    extra_args=[
                        "--agent-operator-api-key-env",
                        "POLY_ROBOT_TEST_AGENT_KEY",
                        "--agent-operator-endpoint-url",
                        endpoint,
                    ],
                    env=env,
                )
            finally:
                server.shutdown()
                server.server_close()
                worker.join(timeout=5)

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            cycle_one = _read_json(root / "cycles" / "cycle_001.json")
            cycle_two = _read_json(root / "cycles" / "cycle_002.json")
            cycle_one_outcomes = cycle_one["run_context"][
                "agent_operator_learning_outcome_attribution"
            ]
            cycle_two_outcomes = cycle_two["run_context"][
                "agent_operator_learning_outcome_attribution"
            ]
            self.assertEqual(cycle_one_outcomes["attributed_count"], 0)
            self.assertGreaterEqual(cycle_two_outcomes["attributed_count"], 1)
            self.assertIn(
                "rec-000001",
                cycle_two_outcomes.get("attributed_recommendation_ids", []),
            )

            learning_state = _read_json(root / "agent_operator_learning_state.json")
            self.assertGreaterEqual(learning_state["metrics"]["attributed_count"], 1)
            self.assertEqual(learning_state["recommendations"][0]["status"], "attributed")

    def test_supervisor_exits_non_zero_when_cycle_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            control_state = {
                "schema_version": RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
                "updated_at": "2026-01-01T00:00:00Z",
                "control_version": 1,
                "paused": False,
                "restart_requested": False,
                "kill_switch_active": False,
                "cancel_all_requested": False,
                "selected_scenario": "baseline",
                "last_annotation": "",
            }
            result, state_path, _, _, _ = self._run_supervisor(
                temp_root=root,
                control_state_payload=control_state,
                cycles=1,
                extra_args=["--heartbeat-timeout-seconds", "0.000000001"],
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("overall_status=FAILED", result.stdout)
            state = _read_json(state_path)
            self.assertEqual(state["status"], "FAILED")
            self.assertTrue(state["failed_workers"])

    def test_cancel_all_request_is_acknowledged_during_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            control_state = {
                "schema_version": RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
                "updated_at": "2026-01-01T00:00:00Z",
                "control_version": 2,
                "paused": False,
                "restart_requested": False,
                "kill_switch_active": False,
                "cancel_all_requested": True,
                "selected_scenario": "baseline",
                "last_annotation": "",
            }
            result, state_path, journal_path, control_state_path, audit_path = (
                self._run_supervisor(
                    temp_root=root,
                    control_state_payload=control_state,
                    cycles=1,
                )
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            state = _read_json(state_path)
            metadata = state["worker_results"][0]["last_metadata"]
            self.assertTrue(metadata["cancel_all_requested"])
            self.assertTrue(metadata["cancel_all_acknowledged"])
            updated_control_state = _read_json(control_state_path)
            self.assertFalse(updated_control_state["cancel_all_requested"])
            audit_events = _read_jsonl(audit_path)
            self.assertEqual(audit_events[-1]["action"], "cancel_all_acknowledged")
            heartbeat_stages = {
                (row.get("payload") or {}).get("stage")
                for row in _read_jsonl(journal_path)
                if row.get("event_type") == "worker_heartbeat"
            }
            self.assertIn("control_cancel_all_applied", heartbeat_stages)

    def test_kill_switch_active_emits_control_gate_heartbeat(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            control_state = {
                "schema_version": RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
                "updated_at": "2026-01-01T00:00:00Z",
                "control_version": 4,
                "paused": False,
                "restart_requested": False,
                "kill_switch_active": True,
                "cancel_all_requested": False,
                "selected_scenario": "baseline",
                "last_annotation": "",
            }
            result, state_path, journal_path, _, _ = self._run_supervisor(
                temp_root=root,
                control_state_payload=control_state,
                cycles=1,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            state = _read_json(state_path)
            metadata = state["worker_results"][0]["last_metadata"]
            self.assertTrue(metadata["kill_switch_active"])
            heartbeat_stages = {
                (row.get("payload") or {}).get("stage")
                for row in _read_jsonl(journal_path)
                if row.get("event_type") == "worker_heartbeat"
            }
            self.assertIn("control_kill_switch_gate", heartbeat_stages)

    def test_single_supervisor_lock_blocks_second_active_process(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            lock_path = root / "runtime_supervisor.lock.json"
            _write_json(
                lock_path,
                {
                    "schema_version": "runtime_supervisor_lock.v1",
                    "pid": os.getpid(),
                    "acquired_at": "2026-01-01T00:00:00Z",
                },
            )
            control_state = {
                "schema_version": RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
                "updated_at": "2026-01-01T00:00:00Z",
                "control_version": 16,
                "paused": False,
                "restart_requested": False,
                "kill_switch_active": False,
                "cancel_all_requested": False,
                "selected_scenario": "baseline",
                "last_annotation": "",
            }
            result, _, _, _, _ = self._run_supervisor(
                temp_root=root,
                control_state_payload=control_state,
                cycles=1,
                disable_single_supervisor_lock=False,
                extra_args=[
                    "--single-supervisor-lock-path",
                    str(lock_path),
                ],
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("single_supervisor_lock_active", result.stderr)


if __name__ == "__main__":
    unittest.main()
