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
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True))
        handle.write("\n")


class RuntimeWebGuiTests(unittest.TestCase):
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
                                "total_execution_cost": 0.345,
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
            payload = service.build_dashboard_payload(recent_events_limit=10, recent_audit_limit=10)

            self.assertEqual(payload["schema_version"], RUNTIME_SUPERVISOR_DASHBOARD_SCHEMA_VERSION)
            self.assertEqual(payload["supervisor_state"]["status"], "SUCCESS")
            self.assertEqual(payload["event_counts"]["worker_heartbeat"], 1)
            self.assertEqual(payload["event_counts"]["worker_attempt_completed"], 1)
            self.assertEqual(payload["worker_activity"]["test_token_loop"]["heartbeat_count"], 1)
            self.assertEqual(payload["loop_metrics"]["filled_trade_count"], 1)
            self.assertEqual(payload["loop_metrics"]["total_execution_cost"], 0.345)
            self.assertEqual(payload["control_state"]["schema_version"], RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION)
            self.assertEqual(payload["recent_operator_actions"], [])

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
            state = manager.set_scenario(actor="alice", scenario_name="liquidity_crunch")
            self.assertEqual(state["selected_scenario"], "liquidity_crunch")
            state = manager.annotate(actor="alice", note="watching retry spikes")
            self.assertEqual(state["last_annotation"], "watching retry spikes")
            state = manager.request_restart(actor="alice", reason="rolling update")
            self.assertTrue(state["restart_requested"])
            state = manager.acknowledge_restart(actor="runtime_supervisor", note="restart accepted")
            self.assertFalse(state["restart_requested"])
            state = manager.set_paused(paused=False, actor="alice", reason="resume")
            self.assertFalse(state["paused"])

            self.assertEqual(state["schema_version"], RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION)
            self.assertEqual(state["control_version"], 6)
            events = manager.list_audit_events(limit=10)
            self.assertEqual(len(events), 6)
            self.assertEqual(events[0]["schema_version"], RUNTIME_OPERATOR_ACTION_SCHEMA_VERSION)
            self.assertEqual(events[0]["action_sequence"], 1)
            self.assertEqual(events[-2]["action"], "graceful_restart_acknowledged")
            self.assertEqual(events[-1]["action_sequence"], 6)
            self.assertEqual(events[-1]["action"], "resume")

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


if __name__ == "__main__":
    unittest.main()
