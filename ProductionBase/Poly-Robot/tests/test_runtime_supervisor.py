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

from poly_robot.runtime_supervisor import RuntimeSupervisor, WorkerSpec  # noqa: E402
from poly_robot.schemas import (  # noqa: E402
    RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION,
    RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION,
)


class RuntimeSupervisorTests(unittest.TestCase):
    def test_retries_failed_attempt_and_recovers(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            journal_path = root / "runtime_journal.jsonl"
            state_path = root / "runtime_state.json"
            attempts = {"count": 0}

            def worker(heartbeat):
                attempts["count"] += 1
                if attempts["count"] == 1:
                    raise RuntimeError("first attempt fails")
                heartbeat("worker_ready")
                return {"attempt": attempts["count"]}

            supervisor = RuntimeSupervisor(
                journal_path=journal_path,
                state_path=state_path,
                sleep_fn=lambda _: None,
            )
            summary = supervisor.run(
                [
                    WorkerSpec(
                        name="recovering_worker",
                        run=worker,
                        max_retries=2,
                        retry_backoff_seconds=0.0,
                        heartbeat_timeout_seconds=10.0,
                    )
                ]
            )

            self.assertEqual(summary["overall_status"], "SUCCESS")
            self.assertEqual(summary["cycles_completed"], 1)
            state_payload = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(
                state_payload["schema_version"], RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION
            )
            self.assertEqual(state_payload["status"], "SUCCESS")
            self.assertEqual(state_payload["worker_results"][0]["attempt_count"], 2)
            self.assertEqual(state_payload["worker_results"][0]["retry_count"], 1)
            self.assertEqual(
                state_payload["worker_results"][0]["last_metadata"]["attempt"], 2
            )

    def test_marks_failure_when_worker_emits_no_heartbeat(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            journal_path = root / "runtime_journal.jsonl"
            state_path = root / "runtime_state.json"

            def worker(_heartbeat):
                return {"state": "no-heartbeat"}

            supervisor = RuntimeSupervisor(
                journal_path=journal_path,
                state_path=state_path,
                sleep_fn=lambda _: None,
            )
            summary = supervisor.run(
                [
                    WorkerSpec(
                        name="silent_worker",
                        run=worker,
                        max_retries=1,
                        retry_backoff_seconds=0.0,
                        heartbeat_timeout_seconds=10.0,
                    )
                ],
                cycles=3,
                stop_on_failure=True,
            )

            self.assertEqual(summary["overall_status"], "FAILED")
            self.assertEqual(summary["cycles_completed"], 1)
            state_payload = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state_payload["status"], "FAILED")
            self.assertEqual(state_payload["failed_workers"], ["silent_worker"])
            self.assertEqual(
                state_payload["worker_results"][0]["final_failure_reason"],
                "missing_heartbeat",
            )

    def test_marks_failure_when_heartbeat_becomes_stale(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            journal_path = root / "runtime_journal.jsonl"
            state_path = root / "runtime_state.json"
            clock = {"value": 0.0}

            def monotonic() -> float:
                return clock["value"]

            def worker(heartbeat):
                heartbeat("started")
                clock["value"] = 5.0
                return {"state": "heartbeat-too-old"}

            supervisor = RuntimeSupervisor(
                journal_path=journal_path,
                state_path=state_path,
                sleep_fn=lambda _: None,
                monotonic_fn=monotonic,
            )
            summary = supervisor.run(
                [
                    WorkerSpec(
                        name="stale_worker",
                        run=worker,
                        max_retries=0,
                        retry_backoff_seconds=0.0,
                        heartbeat_timeout_seconds=1.0,
                    )
                ]
            )

            self.assertEqual(summary["overall_status"], "FAILED")
            state_payload = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state_payload["status"], "FAILED")
            self.assertTrue(
                state_payload["worker_results"][0]["final_failure_reason"].startswith(
                    "stale_heartbeat:"
                )
            )

    def test_journal_records_runtime_events(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            journal_path = root / "runtime_journal.jsonl"
            state_path = root / "runtime_state.json"

            def worker(heartbeat):
                heartbeat("step_one")
                heartbeat("step_two")
                return {"done": True}

            supervisor = RuntimeSupervisor(
                journal_path=journal_path,
                state_path=state_path,
                sleep_fn=lambda _: None,
            )
            supervisor.run([WorkerSpec(name="journal_worker", run=worker)])
            entries = [
                json.loads(line)
                for line in journal_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]

            self.assertGreaterEqual(len(entries), 5)
            self.assertTrue(
                all(
                    entry["schema_version"]
                    == RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION
                    for entry in entries
                )
            )
            self.assertIn("cycle_started", {entry["event_type"] for entry in entries})
            self.assertIn(
                "worker_heartbeat", {entry["event_type"] for entry in entries}
            )
            self.assertIn("cycle_completed", {entry["event_type"] for entry in entries})


if __name__ == "__main__":
    unittest.main()
