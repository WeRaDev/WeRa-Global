#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.runtime_web_gui import (  # noqa: E402
    OperatorControlManager,
    RuntimeDashboardService,
)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run Poly-Robot runtime web GUI for operator visibility into supervisor state, "
            "journal events, and audited control actions."
        )
    )
    parser.add_argument(
        "--state-path",
        type=Path,
        default=ROOT_DIR / "runtime" / "runtime_state.json",
        help="Path to runtime supervisor state snapshot JSON.",
    )
    parser.add_argument(
        "--journal-path",
        type=Path,
        default=ROOT_DIR / "runtime" / "runtime_journal.jsonl",
        help="Path to runtime supervisor JSONL journal.",
    )
    parser.add_argument(
        "--control-state-path",
        type=Path,
        default=ROOT_DIR / "runtime" / "operator_control_state.json",
        help="Path to persisted operator control state JSON.",
    )
    parser.add_argument(
        "--audit-path",
        type=Path,
        default=ROOT_DIR / "runtime" / "operator_action_audit.jsonl",
        help="Path to operator action audit JSONL log.",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host interface to bind.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="HTTP port for GUI server.",
    )
    parser.add_argument(
        "--operator-token",
        type=str,
        required=False,
        help=(
            "Operator token for POST control actions via X-Operator-Token header. "
            "When omitted, control endpoints run in read-only mode and POST actions are rejected."
        ),
    )
    parser.add_argument(
        "--recent-events-limit",
        type=int,
        default=200,
        help="Maximum number of recent journal events exposed by dashboard API.",
    )
    parser.add_argument(
        "--recent-audit-limit",
        type=int,
        default=100,
        help="Maximum number of recent operator actions exposed by dashboard API.",
    )
    return parser


def _html_page() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Poly-Robot Runtime Console</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif; margin: 24px; }
    .grid { display: grid; grid-template-columns: repeat(2, minmax(320px, 1fr)); gap: 16px; }
    .card { border: 1px solid #d0d7de; border-radius: 8px; padding: 12px; background: #fff; }
    h1, h2 { margin: 0 0 10px 0; }
    pre { margin: 0; max-height: 260px; overflow: auto; background: #f6f8fa; padding: 8px; border-radius: 6px; }
    button { margin-right: 8px; margin-bottom: 8px; }
    input { margin-right: 8px; margin-bottom: 8px; }
    .status-success { color: #1a7f37; font-weight: 600; }
    .status-failed { color: #cf222e; font-weight: 600; }
  </style>
</head>
<body>
  <h1>Poly-Robot Runtime Console</h1>
  <p id="summary">Loading...</p>
  <div class="card">
    <h2>Operator Controls</h2>
    <input id="actor" placeholder="actor" value="operator" />
    <input id="token" placeholder="operator token (if required)" />
    <input id="reason" placeholder="reason (optional)" />
    <button onclick="sendControl('/api/control/pause')">Pause</button>
    <button onclick="sendControl('/api/control/resume')">Resume</button>
    <button onclick="sendControl('/api/control/restart')">Graceful Restart</button>
    <br />
    <input id="scenario" placeholder="scenario name" value="baseline" />
    <button onclick="sendControl('/api/control/scenario')">Set Scenario</button>
    <br />
    <input id="annotation" placeholder="incident note" size="48" />
    <button onclick="sendControl('/api/control/annotate')">Annotate Incident</button>
    <div id="controlResult"></div>
  </div>
  <div class="card">
    <h2>Dashboard Views</h2>
    <input id="recentEventsLimit" placeholder="recent events limit" value="200" />
    <input id="recentAuditLimit" placeholder="recent audit limit" value="100" />
    <input id="auditActionFilter" placeholder="audit action filter" />
    <input id="auditActorFilter" placeholder="audit actor filter" />
    <br />
    <input id="incidentLimit" placeholder="incident page size" value="50" />
    <input id="comparisonWindow" placeholder="comparison window" value="10" />
    <button onclick="applyFilters()">Apply Filters</button>
    <button onclick="resetFilters()">Reset Filters</button>
    <button onclick="loadNewerIncidents()">Newer Incidents</button>
    <button onclick="loadOlderIncidents()">Older Incidents</button>
    <div id="filterResult"></div>
  </div>
  <div class="grid">
    <div class="card">
      <h2>State + Loop Metrics</h2>
      <pre id="statePayload"></pre>
    </div>
    <div class="card">
      <h2>Event Counts + Worker Activity</h2>
      <pre id="eventPayload"></pre>
    </div>
    <div class="card">
      <h2>Recent Operator Actions</h2>
      <pre id="auditPayload"></pre>
    </div>
    <div class="card">
      <h2>Recent Journal Events</h2>
      <pre id="journalPayload"></pre>
    </div>
    <div class="card">
      <h2>Incident Feed</h2>
      <pre id="incidentPayload"></pre>
    </div>
    <div class="card">
      <h2>Run-to-Run Comparison</h2>
      <pre id="comparisonPayload"></pre>
    </div>
  </div>
  <script>
    const defaultDashboardQuery = {
      recent_events_limit: 200,
      recent_audit_limit: 100,
      audit_action: '',
      audit_actor: '',
      incident_limit: 50,
      incident_cursor: null,
      comparison_window: 10
    };
    let dashboardQuery = { ...defaultDashboardQuery };
    let incidentCursorHistory = [];
    let lastDashboardPayload = null;

    function readPositiveInteger(inputId, fallbackValue) {
      const rawValue = document.getElementById(inputId).value;
      const parsed = parseInt(rawValue, 10);
      if (Number.isFinite(parsed) && parsed > 0) {
        return parsed;
      }
      return fallbackValue;
    }

    function syncQueryInputsFromState() {
      document.getElementById('recentEventsLimit').value = String(dashboardQuery.recent_events_limit);
      document.getElementById('recentAuditLimit').value = String(dashboardQuery.recent_audit_limit);
      document.getElementById('auditActionFilter').value = dashboardQuery.audit_action;
      document.getElementById('auditActorFilter').value = dashboardQuery.audit_actor;
      document.getElementById('incidentLimit').value = String(dashboardQuery.incident_limit);
      document.getElementById('comparisonWindow').value = String(dashboardQuery.comparison_window);
    }

    function applyQueryInputValues(resetIncidentCursor) {
      dashboardQuery.recent_events_limit = readPositiveInteger(
        'recentEventsLimit',
        defaultDashboardQuery.recent_events_limit
      );
      dashboardQuery.recent_audit_limit = readPositiveInteger(
        'recentAuditLimit',
        defaultDashboardQuery.recent_audit_limit
      );
      dashboardQuery.audit_action = (document.getElementById('auditActionFilter').value || '').trim();
      dashboardQuery.audit_actor = (document.getElementById('auditActorFilter').value || '').trim();
      dashboardQuery.incident_limit = readPositiveInteger(
        'incidentLimit',
        defaultDashboardQuery.incident_limit
      );
      dashboardQuery.comparison_window = readPositiveInteger(
        'comparisonWindow',
        defaultDashboardQuery.comparison_window
      );
      if (resetIncidentCursor) {
        dashboardQuery.incident_cursor = null;
        incidentCursorHistory = [];
      }
      syncQueryInputsFromState();
    }

    function dashboardUrl() {
      const params = new URLSearchParams();
      params.set('recent_events_limit', String(dashboardQuery.recent_events_limit));
      params.set('recent_audit_limit', String(dashboardQuery.recent_audit_limit));
      params.set('incident_limit', String(dashboardQuery.incident_limit));
      params.set('comparison_window', String(dashboardQuery.comparison_window));
      if (dashboardQuery.audit_action) {
        params.set('audit_action', dashboardQuery.audit_action);
      }
      if (dashboardQuery.audit_actor) {
        params.set('audit_actor', dashboardQuery.audit_actor);
      }
      if (dashboardQuery.incident_cursor !== null && dashboardQuery.incident_cursor !== undefined) {
        params.set('incident_cursor', String(dashboardQuery.incident_cursor));
      }
      return '/api/dashboard?' + params.toString();
    }
    async function fetchDashboard() {
      const response = await fetch(dashboardUrl());
      if (!response.ok) {
        document.getElementById('summary').textContent = 'Dashboard request failed: ' + response.status;
        return;
      }
      const payload = await response.json();
      lastDashboardPayload = payload;
      const state = payload.supervisor_state || {};
      const status = state.status || 'UNKNOWN';
      const statusClass = status === 'SUCCESS' ? 'status-success' : (status === 'FAILED' ? 'status-failed' : '');
      document.getElementById('summary').innerHTML =
        'Overall: <span class="' + statusClass + '">' + status + '</span> | cycle=' +
        (state.cycle_index ?? '-') + ' | failed_workers=' +
        ((state.failed_workers || []).length) + ' | generated_at=' + payload.generated_at;

      document.getElementById('statePayload').textContent = JSON.stringify({
        control_state: payload.control_state,
        loop_metrics: payload.loop_metrics,
        supervisor_state: payload.supervisor_state
      }, null, 2);
      document.getElementById('eventPayload').textContent = JSON.stringify({
        event_counts: payload.event_counts,
        worker_activity: payload.worker_activity
      }, null, 2);
      document.getElementById('auditPayload').textContent =
        JSON.stringify(payload.recent_operator_actions, null, 2);
      document.getElementById('journalPayload').textContent =
        JSON.stringify(payload.recent_journal_events, null, 2);
      document.getElementById('incidentPayload').textContent =
        JSON.stringify(payload.incident_feed, null, 2);
      document.getElementById('comparisonPayload').textContent =
        JSON.stringify(payload.cycle_comparison, null, 2);

      const incidentPaging = (payload.incident_feed || {}).paging || {};
      const cursorLabel = incidentPaging.cursor ?? 'latest';
      const olderCursor = incidentPaging.next_cursor ?? 'none';
      const totalIncidents = incidentPaging.total_incidents ?? 0;
      document.getElementById('filterResult').textContent =
        'Incident cursor=' + cursorLabel + ' | older_cursor=' + olderCursor + ' | total=' + totalIncidents;
    }

    function controlPayload() {
      return {
        actor: document.getElementById('actor').value || 'operator',
        reason: document.getElementById('reason').value || '',
        scenario_name: document.getElementById('scenario').value || '',
        note: document.getElementById('annotation').value || ''
      };
    }

    async function sendControl(path) {
      const token = document.getElementById('token').value || '';
      const response = await fetch(path, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Operator-Token': token
        },
        body: JSON.stringify(controlPayload())
      });
      const text = await response.text();
      document.getElementById('controlResult').textContent = 'Response (' + response.status + '): ' + text;
      await fetchDashboard();
    }
    async function applyFilters() {
      applyQueryInputValues(true);
      await fetchDashboard();
    }

    async function resetFilters() {
      dashboardQuery = { ...defaultDashboardQuery };
      incidentCursorHistory = [];
      syncQueryInputsFromState();
      await fetchDashboard();
    }

    async function loadOlderIncidents() {
      applyQueryInputValues(false);
      const incidentPaging = ((lastDashboardPayload || {}).incident_feed || {}).paging || {};
      const nextCursor = incidentPaging.next_cursor;
      if (!nextCursor) {
        document.getElementById('filterResult').textContent =
          'No older incidents available for this filter scope.';
        return;
      }
      if (dashboardQuery.incident_cursor !== null && dashboardQuery.incident_cursor !== undefined) {
        incidentCursorHistory.push(String(dashboardQuery.incident_cursor));
      }
      dashboardQuery.incident_cursor = nextCursor;
      await fetchDashboard();
    }

    async function loadNewerIncidents() {
      applyQueryInputValues(false);
      if (dashboardQuery.incident_cursor === null || dashboardQuery.incident_cursor === undefined) {
        document.getElementById('filterResult').textContent = 'Already viewing the newest incidents.';
        return;
      }
      if (incidentCursorHistory.length > 0) {
        dashboardQuery.incident_cursor = incidentCursorHistory.pop();
      } else {
        dashboardQuery.incident_cursor = null;
      }
      await fetchDashboard();
    }

    resetFilters();
    setInterval(fetchDashboard, 3000);
  </script>
</body>
</html>
"""


def _read_json_body(handler: BaseHTTPRequestHandler) -> dict:
    content_length = int(handler.headers.get("Content-Length", "0"))
    if content_length <= 0:
        return {}
    payload = handler.rfile.read(content_length).decode("utf-8")
    if not payload:
        return {}
    return json.loads(payload)


def _send_json(handler: BaseHTTPRequestHandler, *, status: int, payload: dict) -> None:
    body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _send_html(handler: BaseHTTPRequestHandler, *, status: int, payload: str) -> None:
    body = payload.encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _query_value(query: dict[str, list[str]], key: str) -> str | None:
    values = query.get(key)
    if not values:
        return None
    return values[0]


def _coerce_positive_int(value: str | None, *, field_name: str) -> int | None:
    if value is None or value == "":
        return None
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be an integer.") from exc
    if parsed <= 0:
        raise ValueError(f"{field_name} must be > 0.")
    return parsed


def _coerce_non_negative_int(value: str | None, *, field_name: str) -> int | None:
    if value is None or value == "":
        return None
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be an integer.") from exc
    if parsed < 0:
        raise ValueError(f"{field_name} must be >= 0.")
    return parsed


def _build_handler(
    *,
    dashboard_service: RuntimeDashboardService,
    control_manager: OperatorControlManager,
    operator_token: str | None,
    recent_events_limit: int,
    recent_audit_limit: int,
):
    class RuntimeGuiHandler(BaseHTTPRequestHandler):
        def _authorize_control_request(self) -> bool:
            if not operator_token:
                _send_json(
                    self,
                    status=403,
                    payload={"error": "operator_controls_disabled"},
                )
                return False
            request_token = self.headers.get("X-Operator-Token", "")
            if request_token == operator_token:
                return True
            _send_json(
                self,
                status=403,
                payload={"error": "invalid_operator_token"},
            )
            return False

        def _control_actor(self, payload: dict) -> str:
            actor = str(payload.get("actor", "operator")).strip()
            return actor or "operator"

        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            query = parse_qs(parsed.query)
            if parsed.path == "/":
                _send_html(self, status=200, payload=_html_page())
                return
            if parsed.path == "/healthz":
                _send_json(self, status=200, payload={"status": "ok"})
                return
            try:
                if parsed.path == "/api/dashboard":
                    events_limit = (
                        _coerce_positive_int(
                            _query_value(query, "recent_events_limit"),
                            field_name="recent_events_limit",
                        )
                        or recent_events_limit
                    )
                    audit_limit = (
                        _coerce_positive_int(
                            _query_value(query, "recent_audit_limit"),
                            field_name="recent_audit_limit",
                        )
                        or recent_audit_limit
                    )
                    incident_limit = (
                        _coerce_positive_int(
                            _query_value(query, "incident_limit"),
                            field_name="incident_limit",
                        )
                        or 50
                    )
                    incident_cursor = _coerce_non_negative_int(
                        _query_value(query, "incident_cursor"),
                        field_name="incident_cursor",
                    )
                    comparison_window = (
                        _coerce_positive_int(
                            _query_value(query, "comparison_window"),
                            field_name="comparison_window",
                        )
                        or 10
                    )
                    payload = dashboard_service.build_dashboard_payload(
                        recent_events_limit=events_limit,
                        recent_audit_limit=audit_limit,
                        audit_action=_query_value(query, "audit_action"),
                        audit_actor=_query_value(query, "audit_actor"),
                        incident_limit=incident_limit,
                        incident_cursor=incident_cursor,
                        comparison_window=comparison_window,
                    )
                    _send_json(self, status=200, payload=payload)
                    return
                if parsed.path == "/api/audit":
                    audit_limit = (
                        _coerce_positive_int(
                            _query_value(query, "limit"),
                            field_name="limit",
                        )
                        or recent_audit_limit
                    )
                    _send_json(
                        self,
                        status=200,
                        payload={
                            "events": control_manager.list_audit_events(
                                limit=audit_limit,
                                action=_query_value(query, "action"),
                                actor=_query_value(query, "actor"),
                            )
                        },
                    )
                    return
                if parsed.path == "/api/incidents":
                    incident_limit = (
                        _coerce_positive_int(
                            _query_value(query, "limit"),
                            field_name="limit",
                        )
                        or 50
                    )
                    incident_cursor = _coerce_non_negative_int(
                        _query_value(query, "cursor"),
                        field_name="cursor",
                    )
                    payload = dashboard_service.build_incident_feed(
                        limit=incident_limit,
                        cursor=incident_cursor,
                    )
                    _send_json(self, status=200, payload=payload)
                    return
                if parsed.path == "/api/comparison":
                    comparison_window = (
                        _coerce_positive_int(
                            _query_value(query, "window"),
                            field_name="window",
                        )
                        or 10
                    )
                    payload = dashboard_service.build_cycle_comparison(
                        window=comparison_window
                    )
                    _send_json(self, status=200, payload=payload)
                    return
            except ValueError as exc:
                _send_json(self, status=400, payload={"error": str(exc)})
                return
            _send_json(self, status=404, payload={"error": "not_found"})

        def do_POST(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            if not parsed.path.startswith("/api/control/"):
                _send_json(self, status=404, payload={"error": "not_found"})
                return
            if not self._authorize_control_request():
                return

            try:
                payload = _read_json_body(self)
            except json.JSONDecodeError:
                _send_json(self, status=400, payload={"error": "invalid_json"})
                return

            actor = self._control_actor(payload)
            reason = str(payload.get("reason", "")).strip()
            try:
                if parsed.path == "/api/control/pause":
                    state = control_manager.set_paused(
                        paused=True, actor=actor, reason=reason
                    )
                elif parsed.path == "/api/control/resume":
                    state = control_manager.set_paused(
                        paused=False, actor=actor, reason=reason
                    )
                elif parsed.path == "/api/control/restart":
                    state = control_manager.request_restart(actor=actor, reason=reason)
                elif parsed.path == "/api/control/scenario":
                    scenario_name = str(payload.get("scenario_name", "")).strip()
                    state = control_manager.set_scenario(
                        actor=actor, scenario_name=scenario_name
                    )
                elif parsed.path == "/api/control/annotate":
                    note = str(payload.get("note", "")).strip()
                    state = control_manager.annotate(actor=actor, note=note)
                else:
                    _send_json(self, status=404, payload={"error": "not_found"})
                    return
            except ValueError as exc:
                _send_json(self, status=400, payload={"error": str(exc)})
                return

            _send_json(
                self,
                status=200,
                payload={
                    "status": "ok",
                    "control_state": state,
                    "recent_operator_actions": control_manager.list_audit_events(
                        limit=recent_audit_limit
                    ),
                },
            )

        def log_message(self, format: str, *args) -> None:  # noqa: A003
            return

    return RuntimeGuiHandler


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    if args.recent_events_limit <= 0:
        raise ValueError("--recent-events-limit must be > 0")
    if args.recent_audit_limit <= 0:
        raise ValueError("--recent-audit-limit must be > 0")

    control_manager = OperatorControlManager(
        control_state_path=args.control_state_path,
        audit_path=args.audit_path,
    )
    dashboard_service = RuntimeDashboardService(
        state_path=args.state_path,
        journal_path=args.journal_path,
        control_manager=control_manager,
    )
    handler_cls = _build_handler(
        dashboard_service=dashboard_service,
        control_manager=control_manager,
        operator_token=args.operator_token,
        recent_events_limit=args.recent_events_limit,
        recent_audit_limit=args.recent_audit_limit,
    )
    server = ThreadingHTTPServer((args.host, args.port), handler_cls)
    print(
        "Runtime GUI listening: "
        f"http://{args.host}:{args.port} "
        f"control_mode={'token_required' if args.operator_token else 'read_only'} "
        f"state_path={args.state_path} "
        f"journal_path={args.journal_path} "
        f"control_state_path={args.control_state_path} "
        f"audit_path={args.audit_path}"
    )
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
