from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT_DIR / "scripts" / "run_runtime_supervisor.py"


class _LiveFeedHandler(BaseHTTPRequestHandler):
    payload: list[dict] = []
    payload_sequence: list[list[dict]] | None = None
    request_count: int = 0

    @classmethod
    def reset(cls) -> None:
        cls.payload = []
        cls.payload_sequence = None
        cls.request_count = 0

    def do_GET(self) -> None:  # noqa: N802
        handler_cls = type(self)
        payload = handler_cls.payload
        if handler_cls.payload_sequence:
            sequence_index = min(
                handler_cls.request_count,
                len(handler_cls.payload_sequence) - 1,
            )
            payload = handler_cls.payload_sequence[sequence_index]
        handler_cls.request_count += 1
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003
        del format, args
        return


class _PreflightAuthHandler(BaseHTTPRequestHandler):
    time_status: int = 200
    time_payload: object = {"timestamp": "2026-01-01T00:00:00Z"}
    auth_status: int = 200
    auth_payload: object = [{"apiKey": "test-key"}]
    geoblock_status: int = 200
    geoblock_payload: object = {"blocked": False}
    request_paths: list[str] = []

    @classmethod
    def reset(cls) -> None:
        cls.time_status = 200
        cls.time_payload = {"timestamp": "2026-01-01T00:00:00Z"}
        cls.auth_status = 200
        cls.auth_payload = [{"apiKey": "test-key"}]
        cls.geoblock_status = 200
        cls.geoblock_payload = {"blocked": False}
        cls.request_paths = []

    def _write_json_response(self, status_code: int, payload: object) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        handler_cls = type(self)
        request_path = self.path.split("?", 1)[0]
        handler_cls.request_paths.append(request_path)
        if request_path == "/time":
            self._write_json_response(handler_cls.time_status, handler_cls.time_payload)
            return
        if request_path == "/auth/api-keys":
            self._write_json_response(handler_cls.auth_status, handler_cls.auth_payload)
            return
        if request_path == "/geoblock":
            self._write_json_response(
                handler_cls.geoblock_status,
                handler_cls.geoblock_payload,
            )
            return
        self._write_json_response(404, {"error": "not_found", "path": request_path})

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003
        del format, args
        return


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def _write_live_rollout_preflight_config(
    path: Path,
    *,
    max_secret_age_days: int,
    enforce_auth_healthcheck: bool = False,
    disable_live_trading_on_auth_failure: bool = False,
    enable_geoblock_check: bool = False,
    geoblock_url: str | None = None,
) -> None:
    rollout_stage: dict[str, object] = {
        "stage": "canary_live",
        "enabled": True,
        "real_order_submission": True,
        "max_order_notional_usd": 50,
        "max_daily_notional_usd": 500,
        "max_open_orders": 3,
    }
    if enforce_auth_healthcheck:
        rollout_stage["enforce_auth_healthcheck"] = True
    if enable_geoblock_check:
        rollout_stage["enable_geoblock_check"] = True
    if geoblock_url:
        rollout_stage["geoblock_url"] = geoblock_url
    payload: dict[str, object] = {
        "config_name": "poly_robot_live_trade_rollout_controls_test",
        "config_version": "1.0.0",
        "default_execution_mode": "paper",
        "secrets_policy": {
            "allow_plaintext_secrets": False,
            "required_env_vars": ["POLYMARKET_API_KEY"],
            "preferred_secret_sources": ["vault"],
            "max_secret_age_days": max_secret_age_days,
        },
        "rollout_stages": [rollout_stage],
    }
    if disable_live_trading_on_auth_failure:
        payload["global_guards"] = {
            "disable_live_trading_on_auth_failure": True
        }
    _write_json(
        path,
        payload,
    )


def _write_polymarket_clob_config(path: Path, *, clob_base_url: str) -> None:
    _write_json(
        path,
        {
            "config_name": "polymarket_clob_live_test",
            "config_version": "1.0.0",
            "endpoints": {
                "clob_rest_base_url": clob_base_url,
            },
            "order_rules": {
                "required_market_metadata": [],
            },
        },
    )


class RuntimeSupervisorLiveIngestionIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        _LiveFeedHandler.reset()
        _PreflightAuthHandler.reset()
    @staticmethod
    def _build_live_clob_preflight_command(
        *,
        state_path: Path,
        journal_path: Path,
        control_state_path: Path,
        control_audit_path: Path,
        cycle_output_dir: Path,
        rollout_config_path: Path,
        clob_config_path: Path | None = None,
    ) -> list[str]:
        command = [
            sys.executable,
            str(SCRIPT_PATH),
            "--events",
            str(ROOT_DIR / "tests" / "fixtures" / "replay_events.jsonl"),
            "--execution-mode",
            "live_polymarket_clob",
            "--live-rollout-stage",
            "canary_live",
            "--live-rollout-config",
            str(rollout_config_path),
            "--allow-real-trading",
            "--cycles",
            "1",
            "--max-retries",
            "0",
            "--retry-backoff-seconds",
            "0",
            "--ingestion-max-retries",
            "0",
            "--ingestion-retry-backoff-seconds",
            "0",
            "--execution-gateway-max-retries",
            "0",
            "--execution-gateway-retry-backoff-seconds",
            "0",
            "--state-path",
            str(state_path),
            "--journal-path",
            str(journal_path),
            "--control-state-path",
            str(control_state_path),
            "--control-audit-path",
            str(control_audit_path),
            "--cycle-output-dir",
            str(cycle_output_dir),
        ]
        if clob_config_path is not None:
            command.extend(
                [
                    "--polymarket-clob-config",
                    str(clob_config_path),
                ]
            )
        return command

    @staticmethod
    def _build_valid_preflight_env() -> dict[str, str]:
        env = dict(os.environ)
        env["POLYMARKET_API_KEY"] = "test-key"
        env["POLYMARKET_API_KEY_SOURCE"] = "vault"
        env["POLYMARKET_API_KEY_LAST_ROTATED_AT"] = "2099-01-01T00:00:00Z"
        return env

    def test_live_polymarket_mode_runs_without_replay_events_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_control_state.json"
            control_audit_path = root / "operator_action_audit.jsonl"
            cycle_output_dir = root / "cycles"

            _LiveFeedHandler.payload = [
                {
                    "id": "live-market-1",
                    "question": "Will test coverage remain green?",
                    "updatedAt": "2026-04-26T15:00:00Z",
                    "endDate": "2026-05-01T00:00:00Z",
                    "outcomePrices": "[\"0.61\", \"0.39\"]",
                    "liquidity": "64000.0",
                    "volume24hr": 2200.0,
                    "oneWeekPriceChange": 0.08,
                }
            ]
            server = ThreadingHTTPServer(("127.0.0.1", 0), _LiveFeedHandler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                live_source_url = f"http://127.0.0.1:{server.server_port}/markets"
                command = [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--ingestion-mode",
                    "live_polymarket",
                    "--live-source-url",
                    live_source_url,
                    "--cycles",
                    "1",
                    "--max-retries",
                    "0",
                    "--retry-backoff-seconds",
                    "0",
                    "--ingestion-max-retries",
                    "0",
                    "--ingestion-retry-backoff-seconds",
                    "0",
                    "--execution-gateway-max-retries",
                    "0",
                    "--execution-gateway-retry-backoff-seconds",
                    "0",
                    "--state-path",
                    str(state_path),
                    "--journal-path",
                    str(journal_path),
                    "--control-state-path",
                    str(control_state_path),
                    "--control-audit-path",
                    str(control_audit_path),
                    "--cycle-output-dir",
                    str(cycle_output_dir),
                ]
                result = subprocess.run(
                    command, capture_output=True, text=True, check=False
                )

                self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
                self.assertIn("ingestion_mode=live_polymarket", result.stdout)

                state = _read_json(state_path)
                metadata = state["worker_results"][0]["last_metadata"]
                self.assertEqual(metadata["cycle_status"], "EXECUTED")
                self.assertEqual(metadata["selected_scenario"], "live_polymarket")
                self.assertGreaterEqual(metadata["events"], 1)

                cycle_report = _read_json(cycle_output_dir / "cycle_001.json")
                run_context = cycle_report["run_context"]
                self.assertEqual(run_context["ingestion_mode"], "live_polymarket")
                self.assertEqual(
                    run_context["ingestion_source"]["source_url"], live_source_url
                )
                self.assertIsNone(run_context["input_events_path"])
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=1.0)

    def test_live_polymarket_clob_execution_mode_is_wired_and_gated(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_control_state.json"
            control_audit_path = root / "operator_action_audit.jsonl"
            cycle_output_dir = root / "cycles"

            _LiveFeedHandler.payload = [
                {
                    "id": "live-market-clob",
                    "question": "Will CLOB mode stay gated before implementation?",
                    "updatedAt": "2026-04-26T15:00:00Z",
                    "endDate": "2026-05-01T00:00:00Z",
                    "outcomePrices": "[\"0.61\", \"0.39\"]",
                    "liquidity": "64000.0",
                    "volume24hr": 2200.0,
                    "oneWeekPriceChange": 0.08,
                }
            ]
            server = ThreadingHTTPServer(("127.0.0.1", 0), _LiveFeedHandler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                live_source_url = f"http://127.0.0.1:{server.server_port}/markets"
                command = [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--ingestion-mode",
                    "live_polymarket",
                    "--live-source-url",
                    live_source_url,
                    "--execution-mode",
                    "live_polymarket_clob",
                    "--live-rollout-stage",
                    "canary_live",
                    "--cycles",
                    "1",
                    "--max-retries",
                    "0",
                    "--retry-backoff-seconds",
                    "0",
                    "--ingestion-max-retries",
                    "0",
                    "--ingestion-retry-backoff-seconds",
                    "0",
                    "--execution-gateway-max-retries",
                    "0",
                    "--execution-gateway-retry-backoff-seconds",
                    "0",
                    "--state-path",
                    str(state_path),
                    "--journal-path",
                    str(journal_path),
                    "--control-state-path",
                    str(control_state_path),
                    "--control-audit-path",
                    str(control_audit_path),
                    "--cycle-output-dir",
                    str(cycle_output_dir),
                ]
                result = subprocess.run(
                    command, capture_output=True, text=True, check=False
                )

                self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
                self.assertIn("execution_mode=live_polymarket_clob", result.stdout)

                cycle_report = _read_json(cycle_output_dir / "cycle_001.json")
                execution_context = cycle_report["run_context"]["execution"]
                self.assertEqual(execution_context["mode"], "live_polymarket_clob")
                self.assertEqual(execution_context["rollout_stage"], "canary_live")
                self.assertFalse(execution_context["credential_preflight"]["required"])
                self.assertEqual(
                    execution_context["credential_preflight"]["status"],
                    "skipped",
                )
                self.assertEqual(cycle_report["filled_trade_count"], 0)
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=1.0)

    def test_live_clob_preflight_fails_when_secret_metadata_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_control_state.json"
            control_audit_path = root / "operator_action_audit.jsonl"
            cycle_output_dir = root / "cycles"
            rollout_config_path = root / "rollout_preflight.json"
            _write_live_rollout_preflight_config(
                rollout_config_path,
                max_secret_age_days=30,
            )
            command = self._build_live_clob_preflight_command(
                state_path=state_path,
                journal_path=journal_path,
                control_state_path=control_state_path,
                control_audit_path=control_audit_path,
                cycle_output_dir=cycle_output_dir,
                rollout_config_path=rollout_config_path,
            )
            env = dict(os.environ)
            env["POLYMARKET_API_KEY"] = "test-key"
            env.pop("POLYMARKET_API_KEY_SOURCE", None)
            env.pop("POLYMARKET_API_KEY_LAST_ROTATED_AT", None)

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )

            self.assertNotEqual(result.returncode, 0)
            output = f"{result.stdout}\n{result.stderr}"
            self.assertIn("Live credential preflight failed", output)
            self.assertIn("secret_source_metadata_missing", output)
            self.assertIn("secret_rotation_metadata_missing", output)

    def test_live_clob_preflight_fails_when_secret_rotation_is_stale(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_control_state.json"
            control_audit_path = root / "operator_action_audit.jsonl"
            cycle_output_dir = root / "cycles"
            rollout_config_path = root / "rollout_preflight.json"
            _write_live_rollout_preflight_config(
                rollout_config_path,
                max_secret_age_days=1,
            )
            command = self._build_live_clob_preflight_command(
                state_path=state_path,
                journal_path=journal_path,
                control_state_path=control_state_path,
                control_audit_path=control_audit_path,
                cycle_output_dir=cycle_output_dir,
                rollout_config_path=rollout_config_path,
            )
            env = dict(os.environ)
            env["POLYMARKET_API_KEY"] = "test-key"
            env["POLYMARKET_API_KEY_SOURCE"] = "vault"
            env["POLYMARKET_API_KEY_LAST_ROTATED_AT"] = "2000-01-01T00:00:00Z"

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )

            self.assertNotEqual(result.returncode, 0)
            output = f"{result.stdout}\n{result.stderr}"
            self.assertIn("Live credential preflight failed", output)
            self.assertIn("secret_rotation_stale", output)
            self.assertIn("stale_secrets", output)

    def test_live_clob_preflight_passes_with_valid_secret_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_control_state.json"
            control_audit_path = root / "operator_action_audit.jsonl"
            cycle_output_dir = root / "cycles"
            rollout_config_path = root / "rollout_preflight.json"
            _write_live_rollout_preflight_config(
                rollout_config_path,
                max_secret_age_days=30,
            )
            command = self._build_live_clob_preflight_command(
                state_path=state_path,
                journal_path=journal_path,
                control_state_path=control_state_path,
                control_audit_path=control_audit_path,
                cycle_output_dir=cycle_output_dir,
                rollout_config_path=rollout_config_path,
            )
            env = self._build_valid_preflight_env()

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            cycle_report = _read_json(cycle_output_dir / "cycle_001.json")
            execution_context = cycle_report["run_context"]["execution"]
            self.assertTrue(execution_context["credential_preflight"]["required"])
            self.assertEqual(
                execution_context["credential_preflight"]["status"],
                "passed",
            )

    def test_live_clob_preflight_rejects_l1_auth_when_actor_is_not_operator(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_control_state.json"
            control_audit_path = root / "operator_action_audit.jsonl"
            cycle_output_dir = root / "cycles"
            rollout_config_path = root / "rollout_preflight.json"
            _write_live_rollout_preflight_config(
                rollout_config_path,
                max_secret_age_days=30,
            )
            command = self._build_live_clob_preflight_command(
                state_path=state_path,
                journal_path=journal_path,
                control_state_path=control_state_path,
                control_audit_path=control_audit_path,
                cycle_output_dir=cycle_output_dir,
                rollout_config_path=rollout_config_path,
            )
            command.extend(
                [
                    "--l1-auth-operation",
                    "derive_api_key",
                    "--l1-auth-context",
                    "startup",
                ]
            )
            env = self._build_valid_preflight_env()

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )

            self.assertNotEqual(result.returncode, 0)
            output = f"{result.stdout}\n{result.stderr}"
            self.assertIn("L1 auth operation denied by runtime policy", output)
            self.assertIn("l1_auth_operator_actor_not_authorized", output)

    def test_live_clob_preflight_rejects_l1_auth_restart_without_control_signal(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_control_state.json"
            control_audit_path = root / "operator_action_audit.jsonl"
            cycle_output_dir = root / "cycles"
            rollout_config_path = root / "rollout_preflight.json"
            _write_live_rollout_preflight_config(
                rollout_config_path,
                max_secret_age_days=30,
            )
            command = self._build_live_clob_preflight_command(
                state_path=state_path,
                journal_path=journal_path,
                control_state_path=control_state_path,
                control_audit_path=control_audit_path,
                cycle_output_dir=cycle_output_dir,
                rollout_config_path=rollout_config_path,
            )
            command.extend(
                [
                    "--operator-control-actor",
                    "operator",
                    "--l1-auth-operation",
                    "derive_api_key",
                    "--l1-auth-context",
                    "restart",
                ]
            )
            env = self._build_valid_preflight_env()

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )

            self.assertNotEqual(result.returncode, 0)
            output = f"{result.stdout}\n{result.stderr}"
            self.assertIn("L1 auth operation denied by runtime policy", output)
            self.assertIn("l1_auth_control_state_unavailable", output)

    def test_live_clob_preflight_allows_l1_auth_startup_for_operator(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_control_state.json"
            control_audit_path = root / "operator_action_audit.jsonl"
            cycle_output_dir = root / "cycles"
            rollout_config_path = root / "rollout_preflight.json"
            _write_live_rollout_preflight_config(
                rollout_config_path,
                max_secret_age_days=30,
            )
            command = self._build_live_clob_preflight_command(
                state_path=state_path,
                journal_path=journal_path,
                control_state_path=control_state_path,
                control_audit_path=control_audit_path,
                cycle_output_dir=cycle_output_dir,
                rollout_config_path=rollout_config_path,
            )
            command.extend(
                [
                    "--operator-control-actor",
                    "operator",
                    "--l1-auth-operation",
                    "derive_api_key",
                    "--l1-auth-context",
                    "startup",
                ]
            )
            env = self._build_valid_preflight_env()

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            cycle_report = _read_json(cycle_output_dir / "cycle_001.json")
            execution_context = cycle_report["run_context"]["execution"]
            self.assertTrue(execution_context["l1_auth_guard"]["allowed"])
            self.assertEqual(
                execution_context["l1_auth_guard"]["context"],
                "startup",
            )
            self.assertEqual(
                execution_context["credential_preflight"]["status"],
                "passed",
            )

    def test_live_clob_preflight_allows_l1_auth_restart_when_control_requested(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_control_state.json"
            control_audit_path = root / "operator_action_audit.jsonl"
            cycle_output_dir = root / "cycles"
            rollout_config_path = root / "rollout_preflight.json"
            _write_live_rollout_preflight_config(
                rollout_config_path,
                max_secret_age_days=30,
            )
            _write_json(
                control_state_path,
                {
                    "schema_version": "runtime_operator_control_state.v1",
                    "restart_requested": True,
                },
            )
            command = self._build_live_clob_preflight_command(
                state_path=state_path,
                journal_path=journal_path,
                control_state_path=control_state_path,
                control_audit_path=control_audit_path,
                cycle_output_dir=cycle_output_dir,
                rollout_config_path=rollout_config_path,
            )
            command.extend(
                [
                    "--operator-control-actor",
                    "operator",
                    "--l1-auth-operation",
                    "derive_api_key",
                    "--l1-auth-context",
                    "restart",
                ]
            )
            env = self._build_valid_preflight_env()

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            output = f"{result.stdout}\n{result.stderr}"
            self.assertNotIn("L1 auth operation denied by runtime policy", output)
            state = _read_json(state_path)
            metadata = state["worker_results"][0]["last_metadata"]
            self.assertEqual(metadata["cycle_status"], "RESTART_REQUESTED")

    def test_live_clob_preflight_fails_when_global_auth_guard_healthcheck_fails(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_control_state.json"
            control_audit_path = root / "operator_action_audit.jsonl"
            cycle_output_dir = root / "cycles"
            rollout_config_path = root / "rollout_preflight_auth.json"
            clob_config_path = root / "polymarket_clob_test.json"
            _write_live_rollout_preflight_config(
                rollout_config_path,
                max_secret_age_days=30,
                disable_live_trading_on_auth_failure=True,
            )

            server = ThreadingHTTPServer(("127.0.0.1", 0), _PreflightAuthHandler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                clob_base_url = f"http://127.0.0.1:{server.server_port}"
                _write_polymarket_clob_config(
                    clob_config_path,
                    clob_base_url=clob_base_url,
                )
                _PreflightAuthHandler.time_status = 200
                _PreflightAuthHandler.time_payload = {
                    "timestamp": time.time()
                }
                _PreflightAuthHandler.auth_status = 401
                _PreflightAuthHandler.auth_payload = {"error": "unauthorized"}

                command = self._build_live_clob_preflight_command(
                    state_path=state_path,
                    journal_path=journal_path,
                    control_state_path=control_state_path,
                    control_audit_path=control_audit_path,
                    cycle_output_dir=cycle_output_dir,
                    rollout_config_path=rollout_config_path,
                    clob_config_path=clob_config_path,
                )
                env = dict(os.environ)
                env["POLYMARKET_API_KEY"] = "test-key"
                env["POLYMARKET_API_KEY_SOURCE"] = "vault"
                env["POLYMARKET_API_KEY_LAST_ROTATED_AT"] = "2099-01-01T00:00:00Z"
                env["POLYMARKET_API_SECRET"] = "c2VjcmV0"
                env["POLYMARKET_API_PASSPHRASE"] = "test-passphrase"
                env["POLYMARKET_ADDRESS"] = "0x1234567890"

                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    check=False,
                    env=env,
                )

                self.assertNotEqual(result.returncode, 0)
                output = f"{result.stdout}\n{result.stderr}"
                self.assertIn("auth_healthcheck_failed", output)
                self.assertIn("clob_l2_auth_request_failed", output)
                self.assertIn("/time", _PreflightAuthHandler.request_paths)
                self.assertIn("/auth/api-keys", _PreflightAuthHandler.request_paths)
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=1.0)

    def test_live_clob_preflight_passes_when_global_auth_guard_healthcheck_passes(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_control_state.json"
            control_audit_path = root / "operator_action_audit.jsonl"
            cycle_output_dir = root / "cycles"
            rollout_config_path = root / "rollout_preflight_auth.json"
            clob_config_path = root / "polymarket_clob_test.json"
            _write_live_rollout_preflight_config(
                rollout_config_path,
                max_secret_age_days=30,
                disable_live_trading_on_auth_failure=True,
            )

            server = ThreadingHTTPServer(("127.0.0.1", 0), _PreflightAuthHandler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                clob_base_url = f"http://127.0.0.1:{server.server_port}"
                _write_polymarket_clob_config(
                    clob_config_path,
                    clob_base_url=clob_base_url,
                )
                _PreflightAuthHandler.time_status = 200
                _PreflightAuthHandler.time_payload = {
                    "timestamp": time.time()
                }
                _PreflightAuthHandler.auth_status = 200
                _PreflightAuthHandler.auth_payload = [{"apiKey": "test-key"}]

                command = self._build_live_clob_preflight_command(
                    state_path=state_path,
                    journal_path=journal_path,
                    control_state_path=control_state_path,
                    control_audit_path=control_audit_path,
                    cycle_output_dir=cycle_output_dir,
                    rollout_config_path=rollout_config_path,
                    clob_config_path=clob_config_path,
                )
                env = dict(os.environ)
                env["POLYMARKET_API_KEY"] = "test-key"
                env["POLYMARKET_API_KEY_SOURCE"] = "vault"
                env["POLYMARKET_API_KEY_LAST_ROTATED_AT"] = "2099-01-01T00:00:00Z"
                env["POLYMARKET_API_SECRET"] = "c2VjcmV0"
                env["POLYMARKET_API_PASSPHRASE"] = "test-passphrase"
                env["POLYMARKET_ADDRESS"] = "0x1234567890"

                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    check=False,
                    env=env,
                )

                self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
                cycle_report = _read_json(cycle_output_dir / "cycle_001.json")
                execution_context = cycle_report["run_context"]["execution"]
                credential_preflight = execution_context["credential_preflight"]
                self.assertEqual(credential_preflight["status"], "passed")
                self.assertTrue(execution_context["enforce_auth_healthcheck"])
                self.assertEqual(
                    credential_preflight["auth_healthcheck"]["status"],
                    "passed",
                )
                self.assertEqual(
                    credential_preflight["auth_healthcheck"]["l2_auth_status_code"],
                    200,
                )
                self.assertIn("/time", _PreflightAuthHandler.request_paths)
                self.assertIn("/auth/api-keys", _PreflightAuthHandler.request_paths)
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=1.0)

    def test_live_mode_uses_wallet_convergence_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_control_state.json"
            control_audit_path = root / "operator_action_audit.jsonl"
            cycle_output_dir = root / "cycles"
            wallet_convergence_path = root / "wallet_convergence.json"
            wallet_convergence_path.write_text(
                json.dumps({"live-market-wallet": 4.0}),
                encoding="utf-8",
            )

            _LiveFeedHandler.payload = [
                {
                    "id": "live-market-wallet",
                    "question": "Will wallet convergence improve this setup?",
                    "updatedAt": "2026-04-26T15:05:00Z",
                    "endDate": "2026-05-01T00:00:00Z",
                    "outcomePrices": "[\"0.45\", \"0.55\"]",
                    "liquidity": "1200.0",
                    "volume24hr": 420.0,
                    "oneWeekPriceChange": 0.02,
                }
            ]
            server = ThreadingHTTPServer(("127.0.0.1", 0), _LiveFeedHandler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                live_source_url = f"http://127.0.0.1:{server.server_port}/markets"
                command = [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--ingestion-mode",
                    "live_polymarket",
                    "--live-source-url",
                    live_source_url,
                    "--live-wallet-convergence-path",
                    str(wallet_convergence_path),
                    "--live-wallet-convergence-threshold",
                    "3",
                    "--cycles",
                    "1",
                    "--max-retries",
                    "0",
                    "--retry-backoff-seconds",
                    "0",
                    "--ingestion-max-retries",
                    "0",
                    "--ingestion-retry-backoff-seconds",
                    "0",
                    "--execution-gateway-max-retries",
                    "0",
                    "--execution-gateway-retry-backoff-seconds",
                    "0",
                    "--state-path",
                    str(state_path),
                    "--journal-path",
                    str(journal_path),
                    "--control-state-path",
                    str(control_state_path),
                    "--control-audit-path",
                    str(control_audit_path),
                    "--cycle-output-dir",
                    str(cycle_output_dir),
                ]
                result = subprocess.run(
                    command, capture_output=True, text=True, check=False
                )

                self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
                cycle_report = _read_json(cycle_output_dir / "cycle_001.json")
                run_context = cycle_report["run_context"]
                self.assertEqual(
                    run_context["ingestion_source"]["wallet_convergence_path"],
                    str(wallet_convergence_path),
                )
                self.assertEqual(
                    run_context["ingestion_source"]["wallet_convergence_threshold"],
                    3.0,
                )
                self.assertEqual(
                    run_context["ingestion_metadata"]["wallet_signal_markets"],
                    1,
                )
                self.assertTrue(
                    run_context["ingestion_metadata"]["wallet_signal_enabled"]
                )
                self.assertNotIn(
                    "wallet_signal_unavailable", run_context["ingestion_reasons"]
                )
                self.assertEqual(len(cycle_report["records"]), 1)
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=1.0)

    def test_live_mode_applies_state_refresh_when_events_repeat_and_open_positions_exist(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_control_state.json"
            control_audit_path = root / "operator_action_audit.jsonl"
            cycle_output_dir = root / "cycles"

            _LiveFeedHandler.payload = [
                {
                    "id": "live-market-sticky",
                    "question": "Will sticky live payload be de-duplicated?",
                    "updatedAt": "2026-04-26T15:03:00Z",
                    "endDate": "2026-05-01T00:00:00Z",
                    "outcomePrices": "[\"0.61\", \"0.39\"]",
                    "liquidity": "64000.0",
                    "volume24hr": 2200.0,
                    "oneWeekPriceChange": 0.08,
                }
            ]
            server = ThreadingHTTPServer(("127.0.0.1", 0), _LiveFeedHandler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                live_source_url = f"http://127.0.0.1:{server.server_port}/markets"
                command = [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--ingestion-mode",
                    "live_polymarket",
                    "--live-source-url",
                    live_source_url,
                    "--cycles",
                    "2",
                    "--cycle-interval-seconds",
                    "0",
                    "--max-retries",
                    "0",
                    "--retry-backoff-seconds",
                    "0",
                    "--ingestion-max-retries",
                    "0",
                    "--ingestion-retry-backoff-seconds",
                    "0",
                    "--execution-gateway-max-retries",
                    "0",
                    "--execution-gateway-retry-backoff-seconds",
                    "0",
                    "--state-path",
                    str(state_path),
                    "--journal-path",
                    str(journal_path),
                    "--control-state-path",
                    str(control_state_path),
                    "--control-audit-path",
                    str(control_audit_path),
                    "--cycle-output-dir",
                    str(cycle_output_dir),
                ]
                result = subprocess.run(
                    command, capture_output=True, text=True, check=False
                )

                self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
                state = _read_json(state_path)
                metadata = state["worker_results"][0]["last_metadata"]
                self.assertEqual(metadata["cycle_status"], "EXECUTED")
                self.assertEqual(metadata["events"], 1)
                self.assertEqual(metadata["open_positions"], 1)
                self.assertTrue(metadata["state_refresh_applied"])
                self.assertEqual(metadata["state_refresh_event_count"], 1)
                self.assertEqual(metadata["state_refresh_market_ids"], ["live-market-sticky"])
                self.assertEqual(metadata["state_refresh_max_streak"], 1)
                self.assertEqual(metadata["stale_open_position_market_ids"], [])
                self.assertIn(
                    "state_refresh_from_seen_events",
                    metadata["ingestion_reasons"],
                )

                cycle_one = _read_json(cycle_output_dir / "cycle_001.json")
                cycle_two = _read_json(cycle_output_dir / "cycle_002.json")
                self.assertEqual(cycle_one["filled_trade_count"], 1)
                self.assertEqual(cycle_two["filled_trade_count"], 0)
                self.assertEqual(len(cycle_two["records"]), 1)
                refreshed = cycle_two["records"][0]
                self.assertEqual(refreshed["market_id"], "live-market-sticky")
                refreshed_risk = refreshed["replay_record"]["risk_decision"]
                self.assertIn(
                    "entry_suppressed_for_state_refresh",
                    refreshed_risk["reasons"],
                )
                self.assertTrue(
                    refreshed_risk["metadata"]["state_refresh_event"]
                )
                self.assertIn(
                    "no_new_events_since_last_cycle",
                    cycle_two["run_context"]["ingestion_reasons"],
                )
                self.assertIn(
                    "state_refresh_from_seen_events",
                    cycle_two["run_context"]["ingestion_reasons"],
                )
                self.assertEqual(
                    cycle_two["run_context"]["stateful_cycle"]["starting_open_positions"],
                    1,
                )
                self.assertTrue(
                    cycle_two["run_context"]["ingestion_metadata"]["state_refresh_applied"]
                )
                self.assertEqual(
                    cycle_two["run_context"]["ingestion_metadata"][
                        "state_refresh_event_count"
                    ],
                    1,
                )
                self.assertEqual(
                    cycle_two["run_context"]["ingestion_metadata"][
                        "state_refresh_market_ids"
                    ],
                    ["live-market-sticky"],
                )
                self.assertEqual(
                    cycle_two["run_context"]["ingestion_metadata"][
                        "state_refresh_max_streak"
                    ],
                    1,
                )
                self.assertEqual(
                    cycle_two["run_context"]["ingestion_metadata"][
                        "stale_open_position_market_ids"
                    ],
                    [],
                )
                self.assertEqual(
                    cycle_two["run_context"]["ingestion_metadata"][
                        "state_refresh_stale_threshold_cycles"
                    ],
                    6,
                )
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=1.0)
    def test_live_mode_suppresses_entries_after_consecutive_degraded_cycles(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_control_state.json"
            control_audit_path = root / "operator_action_audit.jsonl"
            cycle_output_dir = root / "cycles"

            _LiveFeedHandler.payload_sequence = [
                [
                    {
                        "id": "live-market-degraded-a",
                        "question": "Will degraded streak protection activate?",
                        "updatedAt": "2026-04-26T15:10:00Z",
                        "endDate": "2026-05-01T00:00:00Z",
                        "outcomePrices": "[\"0.62\", \"0.38\"]",
                        "liquidity": "64000.0",
                        "volume24hr": 2400.0,
                        "oneWeekPriceChange": 0.06,
                    },
                    {
                        "id": "live-market-degraded-a",
                        "question": "Will degraded streak protection activate?",
                        "updatedAt": "2026-04-26T15:10:00Z",
                        "endDate": "2026-05-01T00:00:00Z",
                        "outcomePrices": "[\"0.62\", \"0.38\"]",
                        "liquidity": "64000.0",
                        "volume24hr": 2400.0,
                        "oneWeekPriceChange": 0.06,
                    },
                ],
                [
                    {
                        "id": "live-market-degraded-b",
                        "question": "Will ingestion suppression block new entries?",
                        "updatedAt": "2026-04-26T15:11:00Z",
                        "endDate": "2026-05-01T00:00:00Z",
                        "outcomePrices": "[\"0.57\", \"0.43\"]",
                        "liquidity": "65000.0",
                        "volume24hr": 2600.0,
                        "oneWeekPriceChange": 0.04,
                    },
                    {
                        "id": "live-market-degraded-b",
                        "question": "Will ingestion suppression block new entries?",
                        "updatedAt": "2026-04-26T15:11:00Z",
                        "endDate": "2026-05-01T00:00:00Z",
                        "outcomePrices": "[\"0.57\", \"0.43\"]",
                        "liquidity": "65000.0",
                        "volume24hr": 2600.0,
                        "oneWeekPriceChange": 0.04,
                    },
                ],
            ]
            server = ThreadingHTTPServer(("127.0.0.1", 0), _LiveFeedHandler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                live_source_url = f"http://127.0.0.1:{server.server_port}/markets"
                command = [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--ingestion-mode",
                    "live_polymarket",
                    "--live-source-url",
                    live_source_url,
                    "--cycles",
                    "2",
                    "--cycle-interval-seconds",
                    "0",
                    "--ingestion-degraded-entry-suppress-threshold-cycles",
                    "2",
                    "--max-retries",
                    "0",
                    "--retry-backoff-seconds",
                    "0",
                    "--ingestion-max-retries",
                    "0",
                    "--ingestion-retry-backoff-seconds",
                    "0",
                    "--execution-gateway-max-retries",
                    "0",
                    "--execution-gateway-retry-backoff-seconds",
                    "0",
                    "--state-path",
                    str(state_path),
                    "--journal-path",
                    str(journal_path),
                    "--control-state-path",
                    str(control_state_path),
                    "--control-audit-path",
                    str(control_audit_path),
                    "--cycle-output-dir",
                    str(cycle_output_dir),
                ]
                result = subprocess.run(
                    command, capture_output=True, text=True, check=False
                )

                self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
                state = _read_json(state_path)
                metadata = state["worker_results"][0]["last_metadata"]
                self.assertEqual(metadata["cycle_status"], "EXECUTED")
                self.assertEqual(metadata["ingestion_status"], "DEGRADED")
                self.assertEqual(metadata["ingestion_degraded_streak"], 2)
                self.assertTrue(metadata["ingestion_degraded_entry_suppressed"])
                self.assertIn(
                    "entry_suppressed_due_consecutive_ingestion_degraded",
                    metadata["ingestion_reasons"],
                )

                cycle_two = _read_json(cycle_output_dir / "cycle_002.json")
                self.assertEqual(cycle_two["run_context"]["ingestion_status"], "DEGRADED")
                self.assertEqual(
                    cycle_two["run_context"]["ingestion_metadata"][
                        "ingestion_degraded_streak"
                    ],
                    2,
                )
                self.assertTrue(
                    cycle_two["run_context"]["ingestion_metadata"][
                        "ingestion_degraded_entry_suppressed"
                    ]
                )
                self.assertIn(
                    "entry_suppressed_due_consecutive_ingestion_degraded",
                    cycle_two["run_context"]["ingestion_reasons"],
                )
                self.assertEqual(len(cycle_two["records"]), 1)
                cycle_two_risk = cycle_two["records"][0]["replay_record"]["risk_decision"]
                self.assertIn(
                    "entry_suppressed_for_ingestion_degradation",
                    cycle_two_risk["reasons"],
                )
                self.assertFalse(cycle_two_risk["metadata"]["state_refresh_event"])
                self.assertTrue(
                    cycle_two_risk["metadata"]["ingestion_degraded_entry_suppressed"]
                )
                self.assertEqual(
                    cycle_two_risk["metadata"]["ingestion_degraded_streak"],
                    2,
                )
            finally:
                _LiveFeedHandler.reset()
                server.shutdown()
                server.server_close()
                thread.join(timeout=1.0)

    def test_live_mode_flags_stale_open_positions_after_state_refresh_streak(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_control_state.json"
            control_audit_path = root / "operator_action_audit.jsonl"
            cycle_output_dir = root / "cycles"

            _LiveFeedHandler.payload = [
                {
                    "id": "live-market-sticky",
                    "question": "Will repeated state refresh be marked stale?",
                    "updatedAt": "2026-04-26T15:03:00Z",
                    "endDate": "2026-05-01T00:00:00Z",
                    "outcomePrices": "[\"0.61\", \"0.39\"]",
                    "liquidity": "64000.0",
                    "volume24hr": 2200.0,
                    "oneWeekPriceChange": 0.08,
                }
            ]
            server = ThreadingHTTPServer(("127.0.0.1", 0), _LiveFeedHandler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                live_source_url = f"http://127.0.0.1:{server.server_port}/markets"
                command = [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--ingestion-mode",
                    "live_polymarket",
                    "--live-source-url",
                    live_source_url,
                    "--state-refresh-stale-threshold-cycles",
                    "2",
                    "--cycles",
                    "3",
                    "--cycle-interval-seconds",
                    "0",
                    "--max-retries",
                    "0",
                    "--retry-backoff-seconds",
                    "0",
                    "--ingestion-max-retries",
                    "0",
                    "--ingestion-retry-backoff-seconds",
                    "0",
                    "--execution-gateway-max-retries",
                    "0",
                    "--execution-gateway-retry-backoff-seconds",
                    "0",
                    "--state-path",
                    str(state_path),
                    "--journal-path",
                    str(journal_path),
                    "--control-state-path",
                    str(control_state_path),
                    "--control-audit-path",
                    str(control_audit_path),
                    "--cycle-output-dir",
                    str(cycle_output_dir),
                ]
                result = subprocess.run(
                    command, capture_output=True, text=True, check=False
                )

                self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
                state = _read_json(state_path)
                metadata = state["worker_results"][0]["last_metadata"]
                self.assertEqual(metadata["cycle_status"], "EXECUTED")
                self.assertTrue(metadata["state_refresh_applied"])
                self.assertEqual(metadata["state_refresh_max_streak"], 2)
                self.assertEqual(
                    metadata["stale_open_position_market_ids"],
                    ["live-market-sticky"],
                )
                self.assertIn(
                    "stale_open_positions_under_state_refresh",
                    metadata["ingestion_reasons"],
                )

                cycle_three = _read_json(cycle_output_dir / "cycle_003.json")
                self.assertIn(
                    "stale_open_positions_under_state_refresh",
                    cycle_three["run_context"]["ingestion_reasons"],
                )
                self.assertEqual(
                    cycle_three["run_context"]["ingestion_metadata"][
                        "state_refresh_max_streak"
                    ],
                    2,
                )
                self.assertEqual(
                    cycle_three["run_context"]["ingestion_metadata"][
                        "stale_open_position_market_ids"
                    ],
                    ["live-market-sticky"],
                )
                self.assertEqual(
                    cycle_three["run_context"]["ingestion_metadata"][
                        "state_refresh_stale_threshold_cycles"
                    ],
                    2,
                )
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=1.0)

    def test_live_mode_ignores_invalid_scenario_pack_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_control_state.json"
            control_audit_path = root / "operator_action_audit.jsonl"
            cycle_output_dir = root / "cycles"

            _LiveFeedHandler.payload = [
                {
                    "id": "live-market-2",
                    "question": "Can live mode run without replay config?",
                    "updatedAt": "2026-04-26T15:01:00Z",
                    "endDate": "2026-05-01T00:00:00Z",
                    "outcomePrices": "[\"0.59\", \"0.41\"]",
                    "liquidity": "51000.0",
                    "volume24hr": 900.0,
                    "oneWeekPriceChange": 0.03,
                }
            ]
            server = ThreadingHTTPServer(("127.0.0.1", 0), _LiveFeedHandler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                live_source_url = f"http://127.0.0.1:{server.server_port}/markets"
                command = [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--ingestion-mode",
                    "live_polymarket",
                    "--live-source-url",
                    live_source_url,
                    "--scenario-pack",
                    str(root / "does_not_exist.json"),
                    "--cycles",
                    "1",
                    "--max-retries",
                    "0",
                    "--retry-backoff-seconds",
                    "0",
                    "--ingestion-max-retries",
                    "0",
                    "--ingestion-retry-backoff-seconds",
                    "0",
                    "--execution-gateway-max-retries",
                    "0",
                    "--execution-gateway-retry-backoff-seconds",
                    "0",
                    "--state-path",
                    str(state_path),
                    "--journal-path",
                    str(journal_path),
                    "--control-state-path",
                    str(control_state_path),
                    "--control-audit-path",
                    str(control_audit_path),
                    "--cycle-output-dir",
                    str(cycle_output_dir),
                ]
                result = subprocess.run(
                    command, capture_output=True, text=True, check=False
                )

                self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
                state = _read_json(state_path)
                metadata = state["worker_results"][0]["last_metadata"]
                self.assertEqual(metadata["cycle_status"], "EXECUTED")
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=1.0)

    def test_live_mode_allows_zero_event_cycle_when_filtered(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_control_state.json"
            control_audit_path = root / "operator_action_audit.jsonl"
            cycle_output_dir = root / "cycles"

            _LiveFeedHandler.payload = [
                {
                    "id": "live-market-3",
                    "question": "Will this market be filtered?",
                    "updatedAt": "2026-04-26T15:02:00Z",
                    "endDate": "2026-05-01T00:00:00Z",
                    "outcomePrices": "[\"0.51\", \"0.49\"]",
                    "liquidity": "1200.0",
                    "volume24hr": 10.0,
                    "oneWeekPriceChange": 0.01,
                }
            ]
            server = ThreadingHTTPServer(("127.0.0.1", 0), _LiveFeedHandler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                live_source_url = f"http://127.0.0.1:{server.server_port}/markets"
                command = [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--ingestion-mode",
                    "live_polymarket",
                    "--live-source-url",
                    live_source_url,
                    "--live-min-volume-24h",
                    "100",
                    "--cycles",
                    "1",
                    "--max-retries",
                    "0",
                    "--retry-backoff-seconds",
                    "0",
                    "--ingestion-max-retries",
                    "0",
                    "--ingestion-retry-backoff-seconds",
                    "0",
                    "--execution-gateway-max-retries",
                    "0",
                    "--execution-gateway-retry-backoff-seconds",
                    "0",
                    "--state-path",
                    str(state_path),
                    "--journal-path",
                    str(journal_path),
                    "--control-state-path",
                    str(control_state_path),
                    "--control-audit-path",
                    str(control_audit_path),
                    "--cycle-output-dir",
                    str(cycle_output_dir),
                ]
                result = subprocess.run(
                    command, capture_output=True, text=True, check=False
                )

                self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
                state = _read_json(state_path)
                metadata = state["worker_results"][0]["last_metadata"]
                self.assertEqual(metadata["cycle_status"], "EXECUTED")
                self.assertEqual(metadata["events"], 0)

                cycle_report = _read_json(cycle_output_dir / "cycle_001.json")
                self.assertEqual(cycle_report["run_context"]["ingestion_status"], "DEGRADED")
                self.assertIn(
                    "no_markets_after_filters",
                    cycle_report["run_context"]["ingestion_reasons"],
                )
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=1.0)


if __name__ == "__main__":
    unittest.main()
