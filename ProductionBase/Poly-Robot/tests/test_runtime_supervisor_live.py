from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT_DIR / "scripts" / "run_runtime_supervisor.py"


class _LiveFeedHandler(BaseHTTPRequestHandler):
    payload: list[dict] = []

    def do_GET(self) -> None:  # noqa: N802
        body = json.dumps(self.payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003
        del format, args
        return


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class RuntimeSupervisorLiveIngestionIntegrationTests(unittest.TestCase):
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
