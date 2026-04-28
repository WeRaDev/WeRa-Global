from __future__ import annotations
import importlib.util
import http.client

import json
import sys
import tempfile
import threading
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.runtime_web_gui import (  # noqa: E402
    OperatorControlManager,
    RuntimeDashboardService,
)
from poly_robot.schemas import (  # noqa: E402
    RUNTIME_OPERATOR_ACTION_SCHEMA_VERSION,
    RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
    RUNTIME_SUPERVISOR_DASHBOARD_SCHEMA_VERSION,
    RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION,
    RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION,
)


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True))
        handle.write("\n")


def _append_cycle_completed_event(
    path: Path,
    *,
    timestamp: str,
    cycle_index: int,
    events: int,
    risk_allowed_count: int,
    filled_trade_count: int,
    exit_candidate_count: int,
    confirmed_exit_count: int,
    total_execution_cost: float = 0.0,
    net_pnl: float = 0.0,
    attributed_trade_count: int = 0,
    expected_gross_edge_value: float = 0.0,
    expected_net_edge_value: float = 0.0,
    expected_net_edge_value_on_fills: float = 0.0,
    expected_value_after_execution_cost: float = 0.0,
    expected_edge_capture_ratio: float = 0.0,
    execution_cost_to_expected_net_ratio: float = 0.0,
    raw_probability_mean: float | None = None,
    calibrated_probability_mean: float | None = None,
    probability_drift_mean: float | None = None,
    probability_drift_abs_mean: float | None = None,
    probability_drift_max_abs: float | None = None,
    weighted_check_agreement_mean: float | None = None,
    calibration_applied_ratio: float | None = None,
    open_positions: int = 0,
    state_refresh_applied: bool = False,
    state_refresh_event_count: int = 0,
    state_refresh_max_streak: int = 0,
    stale_open_position_market_ids: list[str] | None = None,
    selected_scenario: str = "baseline",
    control_version: int = 1,
    result_hash_prefix: str = "hash",
) -> None:
    _append_jsonl(
        path,
        {
            "schema_version": RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION,
            "timestamp": timestamp,
            "event_type": "worker_heartbeat",
            "payload": {
                "worker_name": "test_token_loop",
                "stage": "cycle_completed",
                "cycle_index": cycle_index,
                "details": {
                    "cycle_index": cycle_index,
                    "selected_scenario": selected_scenario,
                    "control_version": control_version,
                    "events": events,
                    "risk_allowed_count": risk_allowed_count,
                    "filled_trade_count": filled_trade_count,
                    "exit_candidate_count": exit_candidate_count,
                    "confirmed_exit_count": confirmed_exit_count,
                    "total_execution_cost": total_execution_cost,
                    "net_pnl": net_pnl,
                    "attributed_trade_count": attributed_trade_count,
                    "expected_gross_edge_value": expected_gross_edge_value,
                    "expected_net_edge_value": expected_net_edge_value,
                    "expected_net_edge_value_on_fills": expected_net_edge_value_on_fills,
                    "expected_value_after_execution_cost": (
                        expected_value_after_execution_cost
                    ),
                    "expected_edge_capture_ratio": expected_edge_capture_ratio,
                    "execution_cost_to_expected_net_ratio": (
                        execution_cost_to_expected_net_ratio
                    ),
                    "raw_probability_mean": raw_probability_mean,
                    "calibrated_probability_mean": calibrated_probability_mean,
                    "probability_drift_mean": probability_drift_mean,
                    "probability_drift_abs_mean": probability_drift_abs_mean,
                    "probability_drift_max_abs": probability_drift_max_abs,
                    "weighted_check_agreement_mean": weighted_check_agreement_mean,
                    "calibration_applied_ratio": calibration_applied_ratio,
                    "open_positions": open_positions,
                    "state_refresh_applied": state_refresh_applied,
                    "state_refresh_event_count": state_refresh_event_count,
                    "state_refresh_max_streak": state_refresh_max_streak,
                    "stale_open_position_market_ids": (
                        list(stale_open_position_market_ids or [])
                    ),
                    "result_hash_prefix": result_hash_prefix,
                },
            },
        },
    )


def _load_runtime_gui_script_module():
    script_path = ROOT_DIR / "scripts" / "run_runtime_gui.py"
    module_spec = importlib.util.spec_from_file_location("run_runtime_gui", script_path)
    if module_spec is None or module_spec.loader is None:
        raise AssertionError("Unable to load run_runtime_gui.py module")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


class RuntimeWebGuiTests(unittest.TestCase):
    def test_control_post_forbidden_when_operator_token_not_configured(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_state.json"
            audit_path = root / "operator_audit.jsonl"

            _write_json(
                state_path,
                {
                    "schema_version": RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION,
                    "generated_at": "2026-01-01T00:00:00Z",
                    "cycle_index": 1,
                    "status": "SUCCESS",
                    "worker_count": 0,
                    "failed_workers": [],
                    "worker_results": [],
                },
            )
            control_manager = OperatorControlManager(
                control_state_path=control_state_path,
                audit_path=audit_path,
            )
            service = RuntimeDashboardService(
                state_path=state_path,
                journal_path=journal_path,
                control_manager=control_manager,
            )
            gui_module = _load_runtime_gui_script_module()
            handler_cls = gui_module._build_handler(
                dashboard_service=service,
                control_manager=control_manager,
                operator_token=None,
                recent_events_limit=10,
                recent_audit_limit=10,
            )
            server = gui_module.ThreadingHTTPServer(("127.0.0.1", 0), handler_cls)
            server_thread = threading.Thread(target=server.serve_forever, daemon=True)
            server_thread.start()

            try:
                host, port = server.server_address
                connection = http.client.HTTPConnection(host, port, timeout=5)
                connection.request(
                    "POST",
                    "/api/control/pause",
                    body=json.dumps({"actor": "alice", "reason": "maintenance"}),
                    headers={"Content-Type": "application/json"},
                )
                response = connection.getresponse()
                response_payload = json.loads(response.read().decode("utf-8"))
                connection.close()
                self.assertEqual(response.status, 403)
                self.assertEqual(
                    response_payload["error"], "operator_controls_disabled"
                )
            finally:
                server.shutdown()
                server.server_close()
                server_thread.join(timeout=5)

    def test_runtime_gui_dashboard_endpoint_applies_kpi_query_parameters(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_state.json"
            audit_path = root / "operator_audit.jsonl"

            _write_json(
                state_path,
                {
                    "schema_version": RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION,
                    "generated_at": "2026-01-01T00:00:00Z",
                    "cycle_index": 2,
                    "status": "SUCCESS",
                    "worker_count": 1,
                    "failed_workers": [],
                    "worker_results": [
                        {
                            "worker_name": "test_token_loop",
                            "status": "SUCCESS",
                            "attempts": [],
                            "attempt_count": 1,
                            "retry_count": 0,
                            "final_failure_reason": None,
                            "last_metadata": {
                                "events": 12,
                                "risk_allowed_count": 10,
                                "filled_trade_count": 3,
                                "partial_fill_count": 0,
                                "total_fees_paid": 0.05,
                                "total_slippage_cost": 0.08,
                                "total_execution_cost": 0.21,
                                "attributed_trade_count": 3,
                                "expected_gross_edge_value": 1.1,
                                "expected_net_edge_value": 0.7,
                                "expected_net_edge_value_on_fills": 0.6,
                                "expected_value_after_execution_cost": 0.05,
                                "average_expected_gross_edge_bps": 120.0,
                                "average_expected_net_edge_bps": 70.0,
                                "expected_edge_capture_ratio": 0.55,
                                "execution_cost_to_expected_net_ratio": 0.3,
                                "bankroll": 1000.0,
                                "day_start_equity": 1000.0,
                                "current_equity": 999.7,
                                "net_pnl": -0.3,
                                "open_notional": 40.0,
                                "open_positions": 1,
                                "total_exposure_fraction": 0.04,
                                "daily_drawdown_fraction": 0.003,
                                "result_hash": "kpi123",
                            },
                        }
                    ],
                },
            )
            _append_cycle_completed_event(
                journal_path,
                timestamp="2026-01-01T00:00:00Z",
                cycle_index=1,
                events=10,
                risk_allowed_count=9,
                filled_trade_count=3,
                exit_candidate_count=4,
                confirmed_exit_count=2,
                total_execution_cost=0.2,
                net_pnl=-0.1,
                attributed_trade_count=3,
                expected_gross_edge_value=1.0,
                expected_net_edge_value=0.8,
                expected_net_edge_value_on_fills=0.7,
                expected_value_after_execution_cost=0.1,
                expected_edge_capture_ratio=0.75,
                execution_cost_to_expected_net_ratio=0.25,
                result_hash_prefix="kpi-a",
            )
            _append_cycle_completed_event(
                journal_path,
                timestamp="2026-01-01T00:00:01Z",
                cycle_index=2,
                events=11,
                risk_allowed_count=10,
                filled_trade_count=3,
                exit_candidate_count=5,
                confirmed_exit_count=2,
                total_execution_cost=0.21,
                net_pnl=-0.3,
                attributed_trade_count=3,
                expected_gross_edge_value=1.1,
                expected_net_edge_value=0.7,
                expected_net_edge_value_on_fills=0.6,
                expected_value_after_execution_cost=0.05,
                expected_edge_capture_ratio=0.55,
                execution_cost_to_expected_net_ratio=0.3,
                result_hash_prefix="kpi-b",
            )

            control_manager = OperatorControlManager(
                control_state_path=control_state_path,
                audit_path=audit_path,
            )
            service = RuntimeDashboardService(
                state_path=state_path,
                journal_path=journal_path,
                control_manager=control_manager,
            )
            gui_module = _load_runtime_gui_script_module()
            handler_cls = gui_module._build_handler(
                dashboard_service=service,
                control_manager=control_manager,
                operator_token=None,
                recent_events_limit=10,
                recent_audit_limit=10,
            )
            server = gui_module.ThreadingHTTPServer(("127.0.0.1", 0), handler_cls)
            server_thread = threading.Thread(target=server.serve_forever, daemon=True)
            server_thread.start()

            try:
                host, port = server.server_address
                connection = http.client.HTTPConnection(host, port, timeout=5)
                connection.request(
                    "GET",
                    (
                        "/api/dashboard?"
                        "kpi_window=2&kpi_domain=risk_and_capital&kpi_status=warning"
                    ),
                )
                response = connection.getresponse()
                payload = json.loads(response.read().decode("utf-8"))
                connection.close()
                self.assertEqual(response.status, 200)
                self.assertEqual(payload["kpi_shadow"]["filters"]["window"], 2)
                self.assertEqual(
                    payload["kpi_shadow"]["filters"]["domain"], "risk_and_capital"
                )
                self.assertEqual(payload["kpi_shadow"]["filters"]["status"], "warning")
                self.assertEqual(
                    [item["kpi_id"] for item in payload["kpi_shadow"]["items"]],
                    ["net_pnl"],
                )
            finally:
                server.shutdown()
                server.server_close()
                server_thread.join(timeout=5)

    def test_dashboard_get_requires_token_when_read_api_mode_enabled(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_state.json"
            audit_path = root / "operator_audit.jsonl"

            _write_json(
                state_path,
                {
                    "schema_version": RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION,
                    "generated_at": "2026-01-01T00:00:00Z",
                    "cycle_index": 1,
                    "status": "SUCCESS",
                    "worker_count": 0,
                    "failed_workers": [],
                    "worker_results": [],
                },
            )
            control_manager = OperatorControlManager(
                control_state_path=control_state_path,
                audit_path=audit_path,
            )
            service = RuntimeDashboardService(
                state_path=state_path,
                journal_path=journal_path,
                control_manager=control_manager,
            )
            gui_module = _load_runtime_gui_script_module()
            handler_cls = gui_module._build_handler(
                dashboard_service=service,
                control_manager=control_manager,
                operator_token="secret-token",
                recent_events_limit=10,
                recent_audit_limit=10,
                read_api_token_required=True,
            )
            server = gui_module.ThreadingHTTPServer(("127.0.0.1", 0), handler_cls)
            server_thread = threading.Thread(target=server.serve_forever, daemon=True)
            server_thread.start()

            try:
                host, port = server.server_address
                connection = http.client.HTTPConnection(host, port, timeout=5)
                connection.request("GET", "/api/dashboard")
                response = connection.getresponse()
                response_payload = json.loads(response.read().decode("utf-8"))
                connection.close()
                self.assertEqual(response.status, 403)
                self.assertEqual(response_payload["error"], "invalid_operator_token")

                connection = http.client.HTTPConnection(host, port, timeout=5)
                connection.request(
                    "GET",
                    "/api/dashboard",
                    headers={"X-Operator-Token": "secret-token"},
                )
                response = connection.getresponse()
                response_payload = json.loads(response.read().decode("utf-8"))
                connection.close()
                self.assertEqual(response.status, 200)
                self.assertEqual(
                    response_payload["schema_version"],
                    RUNTIME_SUPERVISOR_DASHBOARD_SCHEMA_VERSION,
                )
            finally:
                server.shutdown()
                server.server_close()
                server_thread.join(timeout=5)

    def test_concurrent_operator_actions_keep_gap_free_action_sequence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manager = OperatorControlManager(
                control_state_path=root / "operator_state.json",
                audit_path=root / "operator_audit.jsonl",
            )

            action_count = 40
            start_gate = threading.Event()
            worker_errors: list[Exception] = []

            def annotate(index: int) -> None:
                try:
                    start_gate.wait(timeout=5)
                    manager.annotate(actor=f"worker-{index % 4}", note=f"note-{index}")
                except Exception as exc:
                    worker_errors.append(exc)

            workers = [
                threading.Thread(target=annotate, args=(idx,))
                for idx in range(action_count)
            ]
            for worker in workers:
                worker.start()
            start_gate.set()
            for worker in workers:
                worker.join(timeout=5)

            self.assertEqual(worker_errors, [])
            self.assertTrue(all(not worker.is_alive() for worker in workers))
            state = manager.load_control_state()
            self.assertEqual(state["control_version"], action_count)
            audit_events = manager.list_audit_events(limit=action_count)
            action_sequences = [int(event["action_sequence"]) for event in audit_events]
            control_state_versions = [
                int(event["control_state_version"]) for event in audit_events
            ]
            expected_sequence = list(range(1, action_count + 1))
            self.assertEqual(action_sequences, expected_sequence)
            self.assertEqual(control_state_versions, expected_sequence)

    def test_dashboard_payload_matches_runtime_state_and_journal(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_state.json"
            audit_path = root / "operator_audit.jsonl"

            _write_json(
                state_path,
                {
                    "schema_version": RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION,
                    "generated_at": "2026-01-01T00:00:00Z",
                    "cycle_index": 3,
                    "status": "SUCCESS",
                    "worker_count": 1,
                    "failed_workers": [],
                    "worker_results": [
                        {
                            "worker_name": "test_token_loop",
                            "status": "SUCCESS",
                            "attempts": [],
                            "attempt_count": 1,
                            "retry_count": 0,
                            "final_failure_reason": None,
                            "last_metadata": {
                                "events": 2,
                                "risk_allowed_count": 1,
                                "filled_trade_count": 1,
                                "partial_fill_count": 0,
                                "total_fees_paid": 0.125,
                                "total_slippage_cost": 0.22,
                                "total_execution_cost": 0.345,
                                "attributed_trade_count": 1,
                                "expected_gross_edge_value": 1.234,
                                "expected_net_edge_value": 0.789,
                                "expected_net_edge_value_on_fills": 0.5,
                                "expected_value_after_execution_cost": 0.155,
                                "average_expected_gross_edge_bps": 180.0,
                                "average_expected_net_edge_bps": 95.0,
                                "expected_edge_capture_ratio": 0.633713,
                                "execution_cost_to_expected_net_ratio": 0.69,
                                "bankroll": 1000.0,
                                "day_start_equity": 1000.0,
                                "current_equity": 999.655,
                                "net_pnl": -0.345,
                                "open_notional": 50.0,
                                "open_positions": 1,
                                "total_exposure_fraction": 0.05,
                                "daily_drawdown_fraction": 0.000345,
                                "result_hash": "abc123",
                            },
                        }
                    ],
                },
            )
            _append_jsonl(
                journal_path,
                {
                    "schema_version": RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION,
                    "timestamp": "2026-01-01T00:00:00Z",
                    "event_type": "worker_heartbeat",
                    "payload": {"worker_name": "test_token_loop", "cycle_index": 3},
                },
            )
            _append_jsonl(
                journal_path,
                {
                    "schema_version": RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION,
                    "timestamp": "2026-01-01T00:00:01Z",
                    "event_type": "worker_attempt_completed",
                    "payload": {
                        "worker_name": "test_token_loop",
                        "status": "SUCCESS",
                        "failure_reason": None,
                    },
                },
            )

            control_manager = OperatorControlManager(
                control_state_path=control_state_path,
                audit_path=audit_path,
            )
            service = RuntimeDashboardService(
                state_path=state_path,
                journal_path=journal_path,
                control_manager=control_manager,
            )
            payload = service.build_dashboard_payload(
                recent_events_limit=10, recent_audit_limit=10
            )

            self.assertEqual(
                payload["schema_version"], RUNTIME_SUPERVISOR_DASHBOARD_SCHEMA_VERSION
            )
            self.assertEqual(payload["supervisor_state"]["status"], "SUCCESS")
            self.assertEqual(payload["event_counts"]["worker_heartbeat"], 1)
            self.assertEqual(payload["event_counts"]["worker_attempt_completed"], 1)
            self.assertEqual(
                payload["worker_activity"]["test_token_loop"]["heartbeat_count"], 1
            )
            self.assertEqual(payload["loop_metrics"]["filled_trade_count"], 1)
            self.assertEqual(payload["loop_metrics"]["total_execution_cost"], 0.345)
            self.assertEqual(payload["loop_metrics"]["attributed_trade_count"], 1)
            self.assertEqual(
                payload["loop_metrics"]["expected_gross_edge_value"], 1.234
            )
            self.assertEqual(payload["loop_metrics"]["expected_net_edge_value"], 0.789)
            self.assertEqual(
                payload["loop_metrics"]["expected_net_edge_value_on_fills"], 0.5
            )
            self.assertEqual(
                payload["loop_metrics"]["expected_value_after_execution_cost"], 0.155
            )
            self.assertEqual(payload["financial_metrics"]["bankroll"], 1000.0)
            self.assertEqual(payload["financial_metrics"]["current_equity"], 999.655)
            self.assertEqual(payload["financial_metrics"]["net_pnl"], -0.345)
            self.assertEqual(payload["financial_metrics"]["open_positions"], 1)
            self.assertEqual(
                payload["financial_metrics"]["total_exposure_fraction"], 0.05
            )
            self.assertEqual(payload["financial_metrics"]["total_fees_paid"], 0.125)
            self.assertEqual(payload["financial_metrics"]["total_slippage_cost"], 0.22)
            self.assertEqual(
                payload["financial_metrics"]["average_execution_cost_per_fill"], 0.345
            )
            self.assertEqual(payload["financial_metrics"]["fill_rate"], 1.0)
            self.assertEqual(payload["financial_metrics"]["attributed_trade_count"], 1)
            self.assertEqual(
                payload["financial_metrics"]["expected_gross_edge_value"], 1.234
            )
            self.assertEqual(
                payload["financial_metrics"]["expected_net_edge_value"], 0.789
            )
            self.assertEqual(
                payload["financial_metrics"]["expected_net_edge_value_on_fills"], 0.5
            )
            self.assertEqual(
                payload["financial_metrics"]["expected_value_after_execution_cost"],
                0.155,
            )
            self.assertEqual(
                payload["financial_metrics"]["average_expected_gross_edge_bps"], 180.0
            )
            self.assertEqual(
                payload["financial_metrics"]["average_expected_net_edge_bps"], 95.0
            )
            self.assertEqual(
                payload["financial_metrics"]["expected_edge_capture_ratio"], 0.633713
            )
            self.assertEqual(
                payload["financial_metrics"]["execution_cost_to_expected_net_ratio"],
                0.69,
            )
            self.assertEqual(
                payload["control_state"]["schema_version"],
                RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
            )
            self.assertEqual(payload["recent_operator_actions"], [])
            self.assertEqual(payload["incident_feed"]["items"], [])
            self.assertEqual(payload["cycle_comparison"]["items"], [])

    def test_dashboard_payload_supports_track6_filters_incidents_and_comparison(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_state.json"
            audit_path = root / "operator_audit.jsonl"

            _write_json(
                state_path,
                {
                    "schema_version": RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION,
                    "generated_at": "2026-01-01T00:00:00Z",
                    "cycle_index": 2,
                    "status": "SUCCESS",
                    "worker_count": 1,
                    "failed_workers": [],
                    "worker_results": [],
                },
            )
            _append_cycle_completed_event(
                journal_path,
                timestamp="2026-01-01T00:00:00Z",
                cycle_index=1,
                events=10,
                risk_allowed_count=8,
                filled_trade_count=2,
                exit_candidate_count=4,
                confirmed_exit_count=1,
                total_execution_cost=0.6,
                net_pnl=0.3,
                attributed_trade_count=2,
                expected_gross_edge_value=1.5,
                expected_net_edge_value=0.9,
                expected_net_edge_value_on_fills=0.7,
                expected_value_after_execution_cost=0.1,
                expected_edge_capture_ratio=0.777778,
                execution_cost_to_expected_net_ratio=0.857143,
                result_hash_prefix="aaa",
            )
            _append_jsonl(
                journal_path,
                {
                    "schema_version": RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION,
                    "timestamp": "2026-01-01T00:00:01Z",
                    "event_type": "worker_retry_scheduled",
                    "payload": {
                        "worker_name": "test_token_loop",
                        "next_attempt_number": 2,
                    },
                },
            )
            _append_jsonl(
                journal_path,
                {
                    "schema_version": RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION,
                    "timestamp": "2026-01-01T00:00:02Z",
                    "event_type": "worker_attempt_completed",
                    "payload": {
                        "worker_name": "test_token_loop",
                        "status": "FAILED",
                        "failure_reason": "risk_guard_rejected",
                    },
                },
            )
            _append_cycle_completed_event(
                journal_path,
                timestamp="2026-01-01T00:00:03Z",
                cycle_index=2,
                events=12,
                risk_allowed_count=9,
                filled_trade_count=3,
                exit_candidate_count=5,
                confirmed_exit_count=2,
                total_execution_cost=0.8,
                net_pnl=0.55,
                attributed_trade_count=3,
                expected_gross_edge_value=1.9,
                expected_net_edge_value=1.2,
                expected_net_edge_value_on_fills=1.0,
                expected_value_after_execution_cost=0.2,
                expected_edge_capture_ratio=0.833333,
                execution_cost_to_expected_net_ratio=0.8,
                result_hash_prefix="bbb",
            )
            _append_jsonl(
                journal_path,
                {
                    "schema_version": RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION,
                    "timestamp": "2026-01-01T00:00:04Z",
                    "event_type": "control_invalid_scenario_fallback",
                    "payload": {
                        "requested_scenario": "unknown",
                        "fallback_scenario": "baseline",
                    },
                },
            )

            control_manager = OperatorControlManager(
                control_state_path=control_state_path,
                audit_path=audit_path,
            )
            control_manager.set_paused(paused=True, actor="alice", reason="maintenance")
            control_manager.set_scenario(actor="bob", scenario_name="liquidity_crunch")
            control_manager.annotate(actor="alice", note="monitoring")
            service = RuntimeDashboardService(
                state_path=state_path,
                journal_path=journal_path,
                control_manager=control_manager,
            )

            payload = service.build_dashboard_payload(
                recent_events_limit=20,
                recent_audit_limit=10,
                audit_actor="alice",
                incident_limit=2,
                comparison_window=2,
            )
            annotation_only_payload = service.build_dashboard_payload(
                recent_events_limit=20,
                recent_audit_limit=10,
                audit_actor="alice",
                audit_action="incident_annotation",
                incident_limit=2,
                comparison_window=2,
            )

            self.assertEqual(len(payload["recent_operator_actions"]), 2)
            self.assertTrue(
                all(
                    event["actor"] == "alice"
                    for event in payload["recent_operator_actions"]
                )
            )
            self.assertEqual(len(annotation_only_payload["recent_operator_actions"]), 1)
            self.assertEqual(
                annotation_only_payload["recent_operator_actions"][0]["action"],
                "incident_annotation",
            )
            self.assertEqual(payload["incident_feed"]["paging"]["total_incidents"], 3)
            self.assertEqual(payload["incident_feed"]["paging"]["next_cursor"], "1")
            self.assertEqual(len(payload["incident_feed"]["items"]), 2)
            self.assertEqual(
                payload["incident_feed"]["items"][0]["event_type"],
                "worker_attempt_completed",
            )
            self.assertEqual(
                payload["incident_feed"]["items"][1]["event_type"],
                "control_invalid_scenario_fallback",
            )
            self.assertEqual(payload["cycle_comparison"]["total_cycles"], 2)
            self.assertEqual(len(payload["cycle_comparison"]["items"]), 2)
            self.assertIsNone(payload["cycle_comparison"]["items"][0]["delta"])
            self.assertEqual(
                payload["cycle_comparison"]["items"][0]["expected_net_edge_value_on_fills"],
                0.7,
            )
            self.assertEqual(
                payload["cycle_comparison"]["items"][1]["expected_net_edge_value_on_fills"],
                1.0,
            )
            self.assertEqual(
                payload["cycle_comparison"]["items"][1]["delta"]["events"], 2
            )
            self.assertEqual(
                payload["cycle_comparison"]["items"][1]["delta"]["risk_allowed_count"],
                1,
            )
            self.assertEqual(
                payload["cycle_comparison"]["items"][1]["delta"]["filled_trade_count"],
                1,
            )
            self.assertEqual(
                payload["cycle_comparison"]["items"][1]["delta"][
                    "exit_candidate_count"
                ],
                1,
            )
            self.assertEqual(
                payload["cycle_comparison"]["items"][1]["delta"][
                    "confirmed_exit_count"
                ],
                1,
            )
            self.assertEqual(
                payload["cycle_comparison"]["items"][1]["delta"][
                    "attributed_trade_count"
                ],
                1,
            )
            self.assertAlmostEqual(
                payload["cycle_comparison"]["items"][1]["delta"][
                    "total_execution_cost"
                ],
                0.2,
                places=4,
            )
            self.assertAlmostEqual(
                payload["cycle_comparison"]["items"][1]["delta"]["net_pnl"],
                0.25,
                places=4,
            )
            self.assertAlmostEqual(
                payload["cycle_comparison"]["items"][1]["delta"][
                    "expected_gross_edge_value"
                ],
                0.4,
                places=4,
            )
            self.assertAlmostEqual(
                payload["cycle_comparison"]["items"][1]["delta"][
                    "expected_net_edge_value"
                ],
                0.3,
                places=4,
            )
            self.assertAlmostEqual(
                payload["cycle_comparison"]["items"][1]["delta"][
                    "expected_net_edge_value_on_fills"
                ],
                0.3,
                places=4,
            )
            self.assertAlmostEqual(
                payload["cycle_comparison"]["items"][1]["delta"][
                    "expected_value_after_execution_cost"
                ],
                0.1,
                places=4,
            )
            self.assertAlmostEqual(
                payload["cycle_comparison"]["items"][1]["delta"][
                    "expected_edge_capture_ratio"
                ],
                0.055555,
                places=6,
            )
            self.assertAlmostEqual(
                payload["cycle_comparison"]["items"][1]["delta"][
                    "execution_cost_to_expected_net_ratio"
                ],
                -0.057143,
                places=6,
            )

    def test_incident_feed_flags_profitability_drift_from_cycle_heartbeats(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            journal_path = root / "runtime_journal.jsonl"
            service = RuntimeDashboardService(
                state_path=root / "runtime_state.json",
                journal_path=journal_path,
                control_manager=OperatorControlManager(
                    control_state_path=root / "operator_state.json",
                    audit_path=root / "operator_audit.jsonl",
                ),
            )

            _append_cycle_completed_event(
                journal_path,
                timestamp="2026-01-01T00:00:00Z",
                cycle_index=1,
                events=10,
                risk_allowed_count=8,
                filled_trade_count=2,
                exit_candidate_count=4,
                confirmed_exit_count=1,
                expected_value_after_execution_cost=-0.12,
                execution_cost_to_expected_net_ratio=0.95,
            )
            _append_cycle_completed_event(
                journal_path,
                timestamp="2026-01-01T00:00:01Z",
                cycle_index=2,
                events=12,
                risk_allowed_count=9,
                filled_trade_count=3,
                exit_candidate_count=5,
                confirmed_exit_count=2,
                expected_value_after_execution_cost=0.18,
                execution_cost_to_expected_net_ratio=1.25,
            )

            feed = service.build_incident_feed(limit=10)

            self.assertEqual(feed["paging"]["total_incidents"], 2)
            self.assertEqual(len(feed["items"]), 2)
            self.assertEqual(feed["items"][0]["event_type"], "worker_heartbeat")
            self.assertEqual(feed["items"][1]["event_type"], "worker_heartbeat")
            self.assertEqual(feed["items"][0]["severity"], "warning")
            self.assertEqual(feed["items"][1]["severity"], "warning")
            self.assertIn(
                "Negative expected value after execution costs detected",
                feed["items"][0]["summary"],
            )
            self.assertIn(
                "Execution cost exceeded expected net edge",
                feed["items"][1]["summary"],
            )
    def test_incident_feed_escalates_stale_state_refresh_streak(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            journal_path = root / "runtime_journal.jsonl"
            service = RuntimeDashboardService(
                state_path=root / "runtime_state.json",
                journal_path=journal_path,
                control_manager=OperatorControlManager(
                    control_state_path=root / "operator_state.json",
                    audit_path=root / "operator_audit.jsonl",
                ),
            )

            _append_cycle_completed_event(
                journal_path,
                timestamp="2026-01-01T00:00:00Z",
                cycle_index=3,
                events=1,
                risk_allowed_count=0,
                filled_trade_count=0,
                exit_candidate_count=0,
                confirmed_exit_count=0,
                expected_value_after_execution_cost=0.0,
                execution_cost_to_expected_net_ratio=0.0,
                open_positions=2,
                state_refresh_applied=True,
                state_refresh_event_count=1,
                state_refresh_max_streak=4,
                stale_open_position_market_ids=["market-a", "market-b"],
            )

            feed = service.build_incident_feed(limit=10)

            self.assertEqual(feed["paging"]["total_incidents"], 1)
            self.assertEqual(len(feed["items"]), 1)
            self.assertEqual(feed["items"][0]["event_type"], "worker_heartbeat")
            self.assertEqual(feed["items"][0]["severity"], "error")
            self.assertIn(
                "State refresh replay has persisted across consecutive cycles",
                feed["items"][0]["summary"],
            )
            self.assertIn("max_streak=4", feed["items"][0]["summary"])

    def test_dashboard_payload_supports_kpi_shadow_filters(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_state.json"
            audit_path = root / "operator_audit.jsonl"

            _write_json(
                state_path,
                {
                    "schema_version": RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION,
                    "generated_at": "2026-01-01T00:00:00Z",
                    "cycle_index": 2,
                    "status": "SUCCESS",
                    "worker_count": 1,
                    "failed_workers": [],
                    "worker_results": [
                        {
                            "worker_name": "test_token_loop",
                            "status": "SUCCESS",
                            "attempts": [],
                            "attempt_count": 1,
                            "retry_count": 0,
                            "final_failure_reason": None,
                            "last_metadata": {
                                "events": 12,
                                "risk_allowed_count": 10,
                                "filled_trade_count": 3,
                                "partial_fill_count": 0,
                                "total_fees_paid": 0.05,
                                "total_slippage_cost": 0.08,
                                "total_execution_cost": 0.21,
                                "attributed_trade_count": 3,
                                "expected_gross_edge_value": 1.1,
                                "expected_net_edge_value": 0.7,
                                "expected_net_edge_value_on_fills": 0.6,
                                "expected_value_after_execution_cost": 0.05,
                                "average_expected_gross_edge_bps": 120.0,
                                "average_expected_net_edge_bps": 70.0,
                                "expected_edge_capture_ratio": 0.55,
                                "execution_cost_to_expected_net_ratio": 0.3,
                                "bankroll": 1000.0,
                                "day_start_equity": 1000.0,
                                "current_equity": 999.7,
                                "net_pnl": -0.3,
                                "open_notional": 40.0,
                                "open_positions": 1,
                                "total_exposure_fraction": 0.04,
                                "daily_drawdown_fraction": 0.003,
                                "result_hash": "kpi123",
                            },
                        }
                    ],
                },
            )
            _append_cycle_completed_event(
                journal_path,
                timestamp="2026-01-01T00:00:00Z",
                cycle_index=1,
                events=10,
                risk_allowed_count=9,
                filled_trade_count=3,
                exit_candidate_count=4,
                confirmed_exit_count=2,
                total_execution_cost=0.2,
                net_pnl=-0.1,
                attributed_trade_count=3,
                expected_gross_edge_value=1.0,
                expected_net_edge_value=0.8,
                expected_net_edge_value_on_fills=0.7,
                expected_value_after_execution_cost=0.1,
                expected_edge_capture_ratio=0.75,
                execution_cost_to_expected_net_ratio=0.25,
                result_hash_prefix="kpi-a",
            )
            _append_cycle_completed_event(
                journal_path,
                timestamp="2026-01-01T00:00:01Z",
                cycle_index=2,
                events=11,
                risk_allowed_count=10,
                filled_trade_count=3,
                exit_candidate_count=5,
                confirmed_exit_count=2,
                total_execution_cost=0.21,
                net_pnl=-0.3,
                attributed_trade_count=3,
                expected_gross_edge_value=1.1,
                expected_net_edge_value=0.7,
                expected_net_edge_value_on_fills=0.6,
                expected_value_after_execution_cost=0.05,
                expected_edge_capture_ratio=0.55,
                execution_cost_to_expected_net_ratio=0.3,
                result_hash_prefix="kpi-b",
            )

            control_manager = OperatorControlManager(
                control_state_path=control_state_path,
                audit_path=audit_path,
            )
            service = RuntimeDashboardService(
                state_path=state_path,
                journal_path=journal_path,
                control_manager=control_manager,
            )

            payload = service.build_dashboard_payload(
                kpi_window=2,
                kpi_domain="risk_and_capital",
                kpi_status="warning",
            )

            kpi_shadow = payload["kpi_shadow"]
            self.assertEqual(kpi_shadow["mode"], "shadow")
            self.assertEqual(
                kpi_shadow["policy"]["schema_version"],
                "kpi_shadow_policy.v1",
            )
            self.assertEqual(kpi_shadow["filters"]["window"], 2)
            self.assertEqual(kpi_shadow["filters"]["domain"], "risk_and_capital")
            self.assertEqual(kpi_shadow["filters"]["status"], "warning")
            self.assertIn("risk_and_capital", kpi_shadow["filters"]["available_domains"])
            self.assertEqual(
                [item["kpi_id"] for item in kpi_shadow["items"]],
                ["net_pnl"],
            )
            self.assertTrue(
                all(item["status"] == "warning" for item in kpi_shadow["items"])
            )
            self.assertEqual(kpi_shadow["summary"]["total_kpis"], 1)
            self.assertEqual(kpi_shadow["summary"]["status_counts"]["warning"], 1)
            self.assertEqual(
                kpi_shadow["items"][0]["status_reason"],
                "warning_below_threshold",
            )
    def test_dashboard_payload_populates_execution_kpis_when_no_fill_opportunity(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_state.json"
            audit_path = root / "operator_audit.jsonl"

            _write_json(
                state_path,
                {
                    "schema_version": RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION,
                    "generated_at": "2026-01-01T00:00:00Z",
                    "cycle_index": 2,
                    "status": "SUCCESS",
                    "worker_count": 1,
                    "failed_workers": [],
                    "worker_results": [
                        {
                            "worker_name": "test_token_loop",
                            "status": "SUCCESS",
                            "attempts": [],
                            "attempt_count": 1,
                            "retry_count": 0,
                            "final_failure_reason": None,
                            "last_metadata": {
                                "events": 0,
                                "risk_allowed_count": 0,
                                "filled_trade_count": 0,
                                "partial_fill_count": 0,
                                "total_execution_cost": 0.0,
                                "expected_net_edge_value": 0.0,
                                "expected_net_edge_value_on_fills": 0.0,
                                "expected_value_after_execution_cost": 0.0,
                                "expected_edge_capture_ratio": None,
                                "execution_cost_to_expected_net_ratio": None,
                                "bankroll": 1000.0,
                                "day_start_equity": 1000.0,
                                "current_equity": 1000.0,
                                "net_pnl": 0.0,
                                "open_notional": 0.0,
                                "open_positions": 0,
                                "total_exposure_fraction": 0.0,
                                "daily_drawdown_fraction": 0.0,
                                "result_hash": "no-fill-kpi",
                            },
                        }
                    ],
                },
            )

            for cycle_index in (1, 2):
                _append_jsonl(
                    journal_path,
                    {
                        "schema_version": (
                            RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION
                        ),
                        "timestamp": f"2026-01-01T00:00:0{cycle_index - 1}Z",
                        "event_type": "worker_heartbeat",
                        "payload": {
                            "worker_name": "test_token_loop",
                            "stage": "cycle_completed",
                            "cycle_index": cycle_index,
                            "details": {
                                "cycle_index": cycle_index,
                                "selected_scenario": "baseline",
                                "control_version": cycle_index,
                                "events": 0,
                                "risk_allowed_count": 0,
                                "filled_trade_count": 0,
                                "partial_fill_count": 0,
                                "exit_candidate_count": 0,
                                "confirmed_exit_count": 0,
                                "total_execution_cost": 0.0,
                                "net_pnl": 0.0,
                                "attributed_trade_count": 0,
                                "expected_gross_edge_value": 0.0,
                                "expected_net_edge_value": 0.0,
                                "expected_net_edge_value_on_fills": 0.0,
                                "expected_value_after_execution_cost": 0.0,
                                "expected_edge_capture_ratio": None,
                                "execution_cost_to_expected_net_ratio": None,
                                "open_positions": 0,
                                "result_hash_prefix": f"no-fill-{cycle_index}",
                            },
                        },
                    },
                )

            control_manager = OperatorControlManager(
                control_state_path=control_state_path,
                audit_path=audit_path,
            )
            service = RuntimeDashboardService(
                state_path=state_path,
                journal_path=journal_path,
                control_manager=control_manager,
            )

            payload = service.build_dashboard_payload(
                kpi_window=2,
                kpi_domain="execution_quality",
            )
            items_by_id = {
                str(item["kpi_id"]): item for item in payload["kpi_shadow"]["items"]
            }
            targeted_kpis = (
                "fill_rate",
                "partial_fill_rate",
                "average_execution_cost_per_fill",
                "expected_edge_capture_ratio",
                "execution_cost_to_expected_net_ratio",
            )
            for kpi_id in targeted_kpis:
                with self.subTest(kpi_id=kpi_id):
                    item = items_by_id[kpi_id]
                    self.assertEqual(item["latest_value"], 0.0)
                    self.assertNotEqual(item["status"], "insufficient_data")
                    self.assertNotEqual(
                        item["status_reason"],
                        "latest_value_missing",
                    )

    def test_dashboard_payload_rejects_invalid_kpi_status_filter(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            service = RuntimeDashboardService(
                state_path=root / "runtime_state.json",
                journal_path=root / "runtime_journal.jsonl",
                control_manager=OperatorControlManager(
                    control_state_path=root / "operator_state.json",
                    audit_path=root / "operator_audit.jsonl",
                ),
            )
            with self.assertRaises(ValueError):
                service.build_dashboard_payload(kpi_status="bad-status")

    def test_dashboard_payload_surfaces_calibration_reliability_kpis(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_state.json"
            audit_path = root / "operator_audit.jsonl"

            _write_json(
                state_path,
                {
                    "schema_version": RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION,
                    "generated_at": "2026-01-01T00:00:00Z",
                    "cycle_index": 2,
                    "status": "SUCCESS",
                    "worker_count": 1,
                    "failed_workers": [],
                    "worker_results": [
                        {
                            "worker_name": "test_token_loop",
                            "status": "SUCCESS",
                            "attempts": [],
                            "attempt_count": 1,
                            "retry_count": 0,
                            "final_failure_reason": None,
                            "last_metadata": {
                                "events": 12,
                                "risk_allowed_count": 10,
                                "filled_trade_count": 3,
                                "partial_fill_count": 0,
                                "total_execution_cost": 0.21,
                                "expected_net_edge_value": 0.7,
                                "expected_net_edge_value_on_fills": 0.6,
                                "expected_value_after_execution_cost": 0.05,
                                "expected_edge_capture_ratio": 0.55,
                                "execution_cost_to_expected_net_ratio": 0.3,
                                "raw_probability_mean": 0.66,
                                "calibrated_probability_mean": 0.6,
                                "probability_drift_mean": -0.06,
                                "probability_drift_abs_mean": 0.09,
                                "probability_drift_max_abs": 0.26,
                                "weighted_check_agreement_mean": 0.52,
                                "calibration_applied_ratio": 0.5,
                                "bankroll": 1000.0,
                                "day_start_equity": 1000.0,
                                "current_equity": 999.7,
                                "net_pnl": -0.3,
                                "open_notional": 40.0,
                                "open_positions": 1,
                                "total_exposure_fraction": 0.04,
                                "daily_drawdown_fraction": 0.003,
                                "result_hash": "calibration-kpi-hash",
                            },
                        }
                    ],
                },
            )
            _append_cycle_completed_event(
                journal_path,
                timestamp="2026-01-01T00:00:00Z",
                cycle_index=1,
                events=10,
                risk_allowed_count=9,
                filled_trade_count=3,
                exit_candidate_count=4,
                confirmed_exit_count=2,
                total_execution_cost=0.2,
                net_pnl=-0.1,
                expected_net_edge_value=0.8,
                expected_net_edge_value_on_fills=0.7,
                expected_value_after_execution_cost=0.1,
                expected_edge_capture_ratio=0.75,
                execution_cost_to_expected_net_ratio=0.25,
                raw_probability_mean=0.63,
                calibrated_probability_mean=0.60,
                probability_drift_mean=-0.03,
                probability_drift_abs_mean=0.03,
                probability_drift_max_abs=0.12,
                weighted_check_agreement_mean=0.58,
                calibration_applied_ratio=0.65,
                result_hash_prefix="calib-a",
            )
            _append_cycle_completed_event(
                journal_path,
                timestamp="2026-01-01T00:00:01Z",
                cycle_index=2,
                events=11,
                risk_allowed_count=10,
                filled_trade_count=3,
                exit_candidate_count=5,
                confirmed_exit_count=2,
                total_execution_cost=0.21,
                net_pnl=-0.3,
                expected_net_edge_value=0.7,
                expected_net_edge_value_on_fills=0.6,
                expected_value_after_execution_cost=0.05,
                expected_edge_capture_ratio=0.55,
                execution_cost_to_expected_net_ratio=0.3,
                raw_probability_mean=0.66,
                calibrated_probability_mean=0.60,
                probability_drift_mean=-0.06,
                probability_drift_abs_mean=0.09,
                probability_drift_max_abs=0.26,
                weighted_check_agreement_mean=0.52,
                calibration_applied_ratio=0.5,
                result_hash_prefix="calib-b",
            )

            control_manager = OperatorControlManager(
                control_state_path=control_state_path,
                audit_path=audit_path,
            )
            service = RuntimeDashboardService(
                state_path=state_path,
                journal_path=journal_path,
                control_manager=control_manager,
            )

            payload = service.build_dashboard_payload(
                kpi_window=2,
                kpi_domain="calibration_reliability",
            )

            kpi_shadow = payload["kpi_shadow"]
            items_by_id = {
                str(item["kpi_id"]): item for item in kpi_shadow["items"]
            }
            self.assertEqual(
                set(items_by_id),
                {
                    "calibration_applied_ratio",
                    "weighted_check_agreement_mean",
                    "probability_drift_abs_mean",
                    "probability_drift_max_abs",
                },
            )
            self.assertEqual(
                kpi_shadow["summary"]["status_counts"]["warning"],
                3,
            )
            self.assertEqual(
                kpi_shadow["summary"]["status_counts"]["critical"],
                1,
            )
            self.assertEqual(
                items_by_id["calibration_applied_ratio"]["status"],
                "warning",
            )
            self.assertEqual(
                items_by_id["weighted_check_agreement_mean"]["status"],
                "warning",
            )
            self.assertEqual(
                items_by_id["probability_drift_abs_mean"]["status"],
                "warning",
            )
            self.assertEqual(
                items_by_id["probability_drift_max_abs"]["status"],
                "critical",
            )
            self.assertAlmostEqual(
                payload["cycle_comparison"]["items"][1]["delta"][
                    "probability_drift_abs_mean"
                ],
                0.06,
                places=6,
            )

    def test_incident_feed_pagination_accepts_string_and_integer_cursor(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            journal_path = root / "runtime_journal.jsonl"
            control_manager = OperatorControlManager(
                control_state_path=root / "operator_state.json",
                audit_path=root / "operator_audit.jsonl",
            )
            service = RuntimeDashboardService(
                state_path=root / "runtime_state.json",
                journal_path=journal_path,
                control_manager=control_manager,
            )

            _append_jsonl(
                journal_path,
                {
                    "schema_version": RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION,
                    "timestamp": "2026-01-01T00:00:00Z",
                    "event_type": "worker_retry_scheduled",
                    "payload": {
                        "worker_name": "test_token_loop",
                        "next_attempt_number": 2,
                    },
                },
            )
            _append_jsonl(
                journal_path,
                {
                    "schema_version": RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION,
                    "timestamp": "2026-01-01T00:00:01Z",
                    "event_type": "worker_attempt_completed",
                    "payload": {
                        "worker_name": "test_token_loop",
                        "status": "FAILED",
                        "failure_reason": "runtime_error",
                    },
                },
            )
            _append_jsonl(
                journal_path,
                {
                    "schema_version": RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION,
                    "timestamp": "2026-01-01T00:00:02Z",
                    "event_type": "control_restart_acknowledged",
                    "payload": {"cycle_index": 7},
                },
            )
            _append_jsonl(
                journal_path,
                {
                    "schema_version": RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION,
                    "timestamp": "2026-01-01T00:00:03Z",
                    "event_type": "cycle_completed",
                    "payload": {"cycle_index": 8, "status": "FAILED"},
                },
            )

            newest_page = service.build_incident_feed(limit=2)
            self.assertEqual(newest_page["paging"]["total_incidents"], 4)
            self.assertEqual(newest_page["paging"]["cursor"], None)
            self.assertEqual(newest_page["paging"]["next_cursor"], "2")
            self.assertEqual(len(newest_page["items"]), 2)
            self.assertEqual(newest_page["items"][0]["incident_sequence"], 3)
            self.assertEqual(newest_page["items"][1]["incident_sequence"], 4)

            older_page = service.build_incident_feed(
                limit=2,
                cursor=newest_page["paging"]["next_cursor"],
            )
            self.assertEqual(older_page["paging"]["cursor"], "2")
            self.assertEqual(older_page["paging"]["next_cursor"], None)
            self.assertEqual(
                [item["incident_sequence"] for item in older_page["items"]], [1, 2]
            )

            first_only_page = service.build_incident_feed(limit=1, cursor=1)
            self.assertEqual(first_only_page["paging"]["cursor"], "1")
            self.assertEqual(
                [item["incident_sequence"] for item in first_only_page["items"]], [1]
            )

    def test_operator_actions_update_control_state_and_emit_audit_log(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            control_state_path = root / "operator_state.json"
            audit_path = root / "operator_audit.jsonl"
            manager = OperatorControlManager(
                control_state_path=control_state_path,
                audit_path=audit_path,
            )

            state = manager.set_paused(paused=True, actor="alice", reason="maintenance")
            self.assertTrue(state["paused"])
            state = manager.set_scenario(
                actor="alice", scenario_name="liquidity_crunch"
            )
            self.assertEqual(state["selected_scenario"], "liquidity_crunch")
            state = manager.annotate(actor="alice", note="watching retry spikes")
            self.assertEqual(state["last_annotation"], "watching retry spikes")
            state = manager.request_restart(actor="alice", reason="rolling update")
            self.assertTrue(state["restart_requested"])
            state = manager.acknowledge_restart(
                actor="runtime_supervisor", note="restart accepted"
            )
            self.assertFalse(state["restart_requested"])
            state = manager.set_paused(paused=False, actor="alice", reason="resume")
            self.assertFalse(state["paused"])

            self.assertEqual(
                state["schema_version"], RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION
            )
            self.assertEqual(state["control_version"], 6)
            events = manager.list_audit_events(limit=10)
            self.assertEqual(len(events), 6)
            self.assertEqual(
                events[0]["schema_version"], RUNTIME_OPERATOR_ACTION_SCHEMA_VERSION
            )
            self.assertEqual(events[0]["action_sequence"], 1)
            self.assertEqual(events[-2]["action"], "graceful_restart_acknowledged")
            self.assertEqual(events[-1]["action_sequence"], 6)
            self.assertEqual(events[-1]["action"], "resume")

    def test_kill_switch_and_cancel_all_actions_update_control_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manager = OperatorControlManager(
                control_state_path=root / "operator_state.json",
                audit_path=root / "operator_audit.jsonl",
            )

            state = manager.set_kill_switch(
                active=True,
                actor="alice",
                reason="emergency stop",
            )
            self.assertTrue(state["kill_switch_active"])
            self.assertTrue(state["cancel_all_requested"])
            state = manager.acknowledge_cancel_all(
                actor="runtime_supervisor",
                note="cancel-all applied",
            )
            self.assertFalse(state["cancel_all_requested"])
            state = manager.set_kill_switch(
                active=False,
                actor="alice",
                reason="resume validated",
            )
            self.assertFalse(state["kill_switch_active"])
            state = manager.request_cancel_all(actor="alice", reason="manual sweep")
            self.assertTrue(state["cancel_all_requested"])

            events = manager.list_audit_events(limit=10)
            self.assertEqual(
                [event["action"] for event in events[-4:]],
                [
                    "kill_switch_enabled",
                    "cancel_all_acknowledged",
                    "kill_switch_disabled",
                    "cancel_all_requested",
                ],
            )

    def test_runtime_gui_control_endpoints_include_kill_switch_and_cancel_all(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_state.json"
            audit_path = root / "operator_audit.jsonl"
            _write_json(
                state_path,
                {
                    "schema_version": RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION,
                    "generated_at": "2026-01-01T00:00:00Z",
                    "cycle_index": 1,
                    "status": "SUCCESS",
                    "worker_count": 0,
                    "failed_workers": [],
                    "worker_results": [],
                },
            )
            control_manager = OperatorControlManager(
                control_state_path=control_state_path,
                audit_path=audit_path,
            )
            service = RuntimeDashboardService(
                state_path=state_path,
                journal_path=journal_path,
                control_manager=control_manager,
            )
            gui_module = _load_runtime_gui_script_module()
            handler_cls = gui_module._build_handler(
                dashboard_service=service,
                control_manager=control_manager,
                operator_token="secret-token",
                recent_events_limit=10,
                recent_audit_limit=10,
            )
            server = gui_module.ThreadingHTTPServer(("127.0.0.1", 0), handler_cls)
            server_thread = threading.Thread(target=server.serve_forever, daemon=True)
            server_thread.start()

            try:
                host, port = server.server_address
                for path in (
                    "/api/control/kill-switch/on",
                    "/api/control/kill-switch/off",
                    "/api/control/cancel-all",
                ):
                    connection = http.client.HTTPConnection(host, port, timeout=5)
                    connection.request(
                        "POST",
                        path,
                        body=json.dumps({"actor": "alice", "reason": "test"}),
                        headers={
                            "Content-Type": "application/json",
                            "X-Operator-Token": "secret-token",
                        },
                    )
                    response = connection.getresponse()
                    payload = json.loads(response.read().decode("utf-8"))
                    connection.close()
                    self.assertEqual(response.status, 200)
                    self.assertEqual(payload["status"], "ok")
            finally:
                server.shutdown()
                server.server_close()
                server_thread.join(timeout=5)

    def test_invalid_control_arguments_raise_value_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manager = OperatorControlManager(
                control_state_path=root / "operator_state.json",
                audit_path=root / "operator_audit.jsonl",
            )
            with self.assertRaises(ValueError):
                manager.set_scenario(actor="alice", scenario_name=" ")
            with self.assertRaises(ValueError):
                manager.annotate(actor="alice", note=" ")
            with self.assertRaises(ValueError):
                manager.list_audit_events(limit=0)

    def test_invalid_incident_cursor_raises_value_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            journal_path = root / "runtime_journal.jsonl"
            _append_jsonl(
                journal_path,
                {
                    "schema_version": RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION,
                    "timestamp": "2026-01-01T00:00:00Z",
                    "event_type": "worker_retry_scheduled",
                    "payload": {
                        "worker_name": "test_token_loop",
                        "next_attempt_number": 2,
                    },
                },
            )
            service = RuntimeDashboardService(
                state_path=root / "runtime_state.json",
                journal_path=journal_path,
                control_manager=OperatorControlManager(
                    control_state_path=root / "operator_state.json",
                    audit_path=root / "operator_audit.jsonl",
                ),
            )
            with self.assertRaises(ValueError):
                service.build_dashboard_payload(incident_cursor="invalid-cursor")

    def test_runtime_gui_page_contains_track6_filter_controls(self) -> None:
        module = _load_runtime_gui_script_module()
        html = module._html_page()
        self.assertIn('id="auditActionFilter"', html)
        self.assertIn('id="auditActorFilter"', html)
        self.assertIn('id="incidentLimit"', html)
        self.assertIn('id="comparisonWindow"', html)
        self.assertIn('id="kpiWindow"', html)
        self.assertIn('id="kpiDomainFilter"', html)
        self.assertIn('id="kpiStatusFilter"', html)
        self.assertIn('onclick="loadNewerIncidents()"', html)
        self.assertIn('onclick="loadOlderIncidents()"', html)
        self.assertIn('onclick="clearKpiFilters()"', html)
        self.assertIn('id="financialPayload"', html)
        self.assertIn('id="kpiPayload"', html)
        self.assertIn('id="kpiSummary"', html)
        self.assertIn("How to Use and Control Poly-Robot", html)
        self.assertIn("Kill Switch ON", html)
        self.assertIn("Cancel All Orders", html)
        self.assertIn("KPI Shadow Mode", html)
        self.assertIn("KPI Workflow Help (default: collapsed)", html)
        for snippet in (
            'id="actor"',
            'id="token"',
            'id="reason"',
            'id="scenario"',
            'id="annotation"',
            'title="Audit identity recorded with every operator action."',
            'title="X-Operator-Token used for protected POST actions and optional read API mode."',
            'title="Operator reason persisted into control audit details."',
            'title="Scenario selected for subsequent test-token loop cycle context."',
            'title="Incident annotation text written to append-only operator action log."',
            'title="Pause new runtime progression while preserving state for safe maintenance."',
            'title="Resume runtime progression after pause conditions are cleared."',
            'title="Request a graceful restart acknowledged by the supervisor before next cycle execution."',
            'title="Immediately activate kill switch and force cancel-all intent for open orders."',
            'title="Disable kill switch after manual validation and formal resume decision."',
            'title="Request cancellation of all open orders through audited control channel."',
            'title="Persist selected scenario into control state for next cycle execution."',
            'title="Append incident annotation to operator audit history with actor and timestamp."',
            'title="Maximum number of recent journal events fetched in each dashboard request."',
            'title="Maximum number of recent operator actions included in dashboard payload."',
            'title="Optional exact action filter applied to operator audit events."',
            'title="Optional exact actor filter applied to operator audit events."',
            'title="Number of incident entries to include per feed page."',
            'title="Number of most recent completed cycles included in run-to-run comparison."',
            'title="Apply current filter and limit fields, then refresh dashboard data from newest incidents."',
            'title="Restore default limits, clear filters, and refresh dashboard from newest incidents."',
            'title="Navigate incident feed toward newer entries using cursor history."',
            'title="Navigate incident feed toward older entries when more pages are available."',
            'title="Expand for step-by-step KPI rollout instructions from shadow review through governance handoff."',
            'title="Number of most recent cycle samples used for KPI shadow series and trend deltas."',
            'title="Optional exact domain filter applied to KPI shadow items."',
            'title="Optional exact status filter for KPI shadow results."',
            'title="Apply dashboard and KPI filters together, then refresh from latest incidents and KPI payload."',
            'title="Clear KPI domain/status filters and reset KPI window to default shadow policy window."',
            "Use a stable operator name so incident timelines and approvals remain attributable.",
            "Filter changes affect dashboard payloads, incident feed pagination, and run-to-run comparison windows.",
            "KPI shadow mode evaluates benchmark policy bands without enforcing hard runtime gates.",
            "Returns KPI view to baseline all-domain mode for broad health checks.",
        ):
            self.assertIn(snippet, html)


if __name__ == "__main__":
    unittest.main()
