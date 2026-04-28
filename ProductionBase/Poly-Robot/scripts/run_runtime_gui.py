#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
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
        "--kpi-shadow-policy-path",
        type=Path,
        default=ROOT_DIR / "config" / "integration" / "kpi_shadow_policy.v1.json",
        help="Path to KPI shadow policy JSON consumed by dashboard shadow-mode payloads.",
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
            "Operator token for control actions via X-Operator-Token header. "
            "When omitted, token is read from --operator-token-env; if still unset, "
            "control endpoints run in read-only mode and POST actions are rejected."
        ),
    )
    parser.add_argument(
        "--operator-token-env",
        type=str,
        default="POLY_ROBOT_OPERATOR_TOKEN",
        help=(
            "Environment variable name used to load operator token at runtime. "
            "If set and present, this value takes precedence over --operator-token."
        ),
    )
    parser.add_argument(
        "--token-required-read-api",
        action="store_true",
        help=(
            "Require X-Operator-Token for /api/* GET endpoints in addition to "
            "POST control actions."
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
    button { margin: 0; }
    input { margin: 0; }
    .status-success { color: #1a7f37; font-weight: 600; }
    .status-failed { color: #cf222e; font-weight: 600; }
    .guide-list { margin: 0; padding-left: 20px; line-height: 1.45; }
    .section-help { margin: 0 0 10px 0; color: #57606a; line-height: 1.45; }
    .field-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 10px 12px; margin-bottom: 10px; }
    .field-group { display: flex; flex-direction: column; gap: 4px; }
    .field-label { font-weight: 600; font-size: 13px; }
    .field-hint { margin: 0; font-size: 12px; color: #57606a; line-height: 1.4; }
    .button-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 8px 10px; margin-bottom: 10px; }
    .button-group { display: flex; flex-direction: column; gap: 4px; }
    .help-panel { border: 1px solid #d8dee4; border-radius: 6px; padding: 8px 10px; background: #f6f8fa; margin-bottom: 10px; }
    .help-panel summary { font-weight: 600; cursor: pointer; }
    .status-pill { display: inline-block; border-radius: 999px; padding: 2px 8px; font-size: 11px; font-weight: 600; }
    .status-pill.ok { background: #dafbe1; color: #1a7f37; }
    .status-pill.warning { background: #fff8c5; color: #9a6700; }
    .status-pill.critical { background: #ffebe9; color: #cf222e; }
    .status-pill.insufficient_data { background: #ddf4ff; color: #0969da; }
  </style>
</head>
<body>
  <h1>Poly-Robot Runtime Console</h1>
  <p id="summary">Loading...</p>
  <div class="card">
    <h2>How to Use and Control Poly-Robot</h2>
    <ol class="guide-list">
      <li>Start the runtime supervisor first so state/journal files are updated continuously.</li>
      <li>Use Dashboard Views filters to focus on incidents, action history, and cycle comparisons.</li>
      <li>Review the Financial Dashboard for equity, PnL, exposure, and execution-cost metrics.</li>
      <li>Use Pause before maintenance, Resume to continue runtime, and Graceful Restart for controlled restarts.</li>
      <li>Use Kill Switch ON to halt submissions immediately (and request cancel-all); use Kill Switch OFF after manual verification.</li>
      <li>Use Cancel All Orders to request deterministic cancellation of all currently open orders.</li>
      <li>Set Scenario to steer the next cycle input profile and use incident annotations for auditability.</li>
      <li>If no operator token was configured at startup, control POST actions are disabled (read-only mode).</li>
      <li>When read-api token mode is enabled, include a valid token to load dashboard API data.</li>
    </ol>
  </div>
  <div class="card">
    <h2>Operator Controls</h2>
    <p class="section-help">
      Fill identity fields first, then use action buttons in order of safety impact. Every submitted action is written to append-only operator audit logs.
    </p>
    <div class="field-grid">
      <div class="field-group">
        <label class="field-label" for="actor">Actor</label>
        <input id="actor" placeholder="operator" value="operator" title="Audit identity recorded with every operator action." />
        <p class="field-hint">Use a stable operator name so incident timelines and approvals remain attributable.</p>
      </div>
      <div class="field-group">
        <label class="field-label" for="token">Operator Token</label>
        <input id="token" placeholder="operator token (if required)" title="X-Operator-Token used for protected POST actions and optional read API mode." />
        <p class="field-hint">Required when token protection is active; leave blank only in explicitly configured read-only mode.</p>
      </div>
      <div class="field-group">
        <label class="field-label" for="reason">Reason</label>
        <input id="reason" placeholder="maintenance window, drill, rollback, etc." title="Operator reason persisted into control audit details." />
        <p class="field-hint">Provide a concise operational reason to improve post-incident and post-release traceability.</p>
      </div>
    </div>
    <div class="button-grid">
      <div class="button-group">
        <button onclick="sendControl('/api/control/pause')" title="Pause new runtime progression while preserving state for safe maintenance.">Pause</button>
        <p class="field-hint">Use before maintenance or investigation to stop new cycle actions safely.</p>
      </div>
      <div class="button-group">
        <button onclick="sendControl('/api/control/resume')" title="Resume runtime progression after pause conditions are cleared.">Resume</button>
        <p class="field-hint">Use after confirming controls, data inputs, and incident status are healthy.</p>
      </div>
      <div class="button-group">
        <button onclick="sendControl('/api/control/restart')" title="Request a graceful restart acknowledged by the supervisor before next cycle execution.">Graceful Restart</button>
        <p class="field-hint">Triggers deterministic restart intent instead of abrupt process interruption.</p>
      </div>
      <div class="button-group">
        <button onclick="sendControl('/api/control/kill-switch/on')" title="Immediately activate kill switch and force cancel-all intent for open orders.">Kill Switch ON</button>
        <p class="field-hint">Emergency path: stop submissions now and move to incident response workflow.</p>
      </div>
      <div class="button-group">
        <button onclick="sendControl('/api/control/kill-switch/off')" title="Disable kill switch after manual validation and formal resume decision.">Kill Switch OFF</button>
        <p class="field-hint">Only use after incident commander and runtime operator confirm safe recovery.</p>
      </div>
      <div class="button-group">
        <button onclick="sendControl('/api/control/cancel-all')" title="Request cancellation of all open orders through audited control channel.">Cancel All Orders</button>
        <p class="field-hint">Use for manual risk reduction or reconciliation cleanup during abnormal behavior.</p>
      </div>
    </div>
    <div class="field-grid">
      <div class="field-group">
        <label class="field-label" for="scenario">Scenario Name</label>
        <input id="scenario" placeholder="baseline" value="baseline" title="Scenario selected for subsequent test-token loop cycle context." />
        <p class="field-hint">Set to a known scenario profile name to steer next-cycle stress behavior.</p>
      </div>
      <div class="button-group">
        <button onclick="sendControl('/api/control/scenario')" title="Persist selected scenario into control state for next cycle execution.">Set Scenario</button>
        <p class="field-hint">Applies scenario choice and bumps control version for deterministic replayability.</p>
      </div>
      <div class="field-group">
        <label class="field-label" for="annotation">Incident Note</label>
        <input id="annotation" placeholder="incident detail, remediation step, or handoff note" size="48" title="Incident annotation text written to append-only operator action log." />
        <p class="field-hint">Capture findings, hypotheses, and handoff checkpoints as structured operational evidence.</p>
      </div>
      <div class="button-group">
        <button onclick="sendControl('/api/control/annotate')" title="Append incident annotation to operator audit history with actor and timestamp.">Annotate Incident</button>
        <p class="field-hint">Use after every key decision so responders can reconstruct timeline quickly.</p>
      </div>
    </div>
    <div id="controlResult"></div>
  </div>
  <div class="card">
    <h2>Dashboard Views</h2>
    <p class="section-help">
      Tune view limits and filters to reduce noise during investigations. Filter changes affect dashboard payloads, incident feed pagination, and run-to-run comparison windows.
    </p>
    <div class="field-grid">
      <div class="field-group">
        <label class="field-label" for="recentEventsLimit">Recent Events Limit</label>
        <input id="recentEventsLimit" placeholder="200" value="200" title="Maximum number of recent journal events fetched in each dashboard request." />
        <p class="field-hint">Lower values improve focus and response speed; higher values broaden event context.</p>
      </div>
      <div class="field-group">
        <label class="field-label" for="recentAuditLimit">Recent Audit Limit</label>
        <input id="recentAuditLimit" placeholder="100" value="100" title="Maximum number of recent operator actions included in dashboard payload." />
        <p class="field-hint">Increase when reviewing long operator sessions; decrease for fast incident triage.</p>
      </div>
      <div class="field-group">
        <label class="field-label" for="auditActionFilter">Audit Action Filter</label>
        <input id="auditActionFilter" placeholder="incident_annotation, pause, resume..." title="Optional exact action filter applied to operator audit events." />
        <p class="field-hint">Use to isolate a single action class such as pause/resume or incident annotations.</p>
      </div>
      <div class="field-group">
        <label class="field-label" for="auditActorFilter">Audit Actor Filter</label>
        <input id="auditActorFilter" placeholder="release_manager, runtime_operator_on_call..." title="Optional exact actor filter applied to operator audit events." />
        <p class="field-hint">Use to isolate who initiated actions during a deployment or incident window.</p>
      </div>
      <div class="field-group">
        <label class="field-label" for="incidentLimit">Incident Page Size</label>
        <input id="incidentLimit" placeholder="50" value="50" title="Number of incident entries to include per feed page." />
        <p class="field-hint">Smaller pages are easier to scan; larger pages support broad retrospective review.</p>
      </div>
      <div class="field-group">
        <label class="field-label" for="comparisonWindow">Comparison Window</label>
        <input id="comparisonWindow" placeholder="10" value="10" title="Number of most recent completed cycles included in run-to-run comparison." />
        <p class="field-hint">Increase window for trend detection; reduce window to focus on immediate regressions.</p>
      </div>
    </div>
    <div class="button-grid">
      <div class="button-group">
        <button onclick="applyFilters()" title="Apply current filter and limit fields, then refresh dashboard data from newest incidents.">Apply Filters</button>
        <p class="field-hint">Commits field values and resets incident cursor so you start from the latest page.</p>
      </div>
      <div class="button-group">
        <button onclick="resetFilters()" title="Restore default limits, clear filters, and refresh dashboard from newest incidents.">Reset Filters</button>
        <p class="field-hint">Use when troubleshooting to return to canonical default dashboard scope.</p>
      </div>
      <div class="button-group">
        <button onclick="loadNewerIncidents()" title="Navigate incident feed toward newer entries using cursor history.">Newer Incidents</button>
        <p class="field-hint">Moves one page toward present time; shows latest incidents when cursor reaches newest.</p>
      </div>
      <div class="button-group">
        <button onclick="loadOlderIncidents()" title="Navigate incident feed toward older entries when more pages are available.">Older Incidents</button>
        <p class="field-hint">Moves one page deeper into incident history for forensic timeline reconstruction.</p>
      </div>
    </div>
    <div id="filterResult"></div>
  </div>
  <div class="card">
    <h2>KPI Shadow Mode</h2>
    <p class="section-help">
      KPI shadow mode evaluates benchmark policy bands without enforcing hard runtime gates. Use these controls to inspect KPI status by domain, severity, and cycle window before promoting thresholds into canary enforcement.
    </p>
    <details class="help-panel" id="kpiWorkflowHelp">
      <summary title="Expand for step-by-step KPI rollout instructions from shadow review through governance handoff.">KPI Workflow Help (default: collapsed)</summary>
      <ol class="guide-list">
        <li>Start in broad scope (empty domain/status) and confirm all KPI items render with valid latest values.</li>
        <li>Set KPI Window to inspect short-term drift versus medium-horizon behavior before threshold changes.</li>
        <li>Filter by Domain to isolate execution quality, forecast quality, risk/capital, or operational reliability concerns.</li>
        <li>Filter by Status to focus on warning/critical candidates requiring investigation and policy tuning.</li>
        <li>Review each KPI series, status reason, and threshold band prior to any rollback-policy promotion.</li>
      </ol>
    </details>
    <div class="field-grid">
      <div class="field-group">
        <label class="field-label" for="kpiWindow">KPI Window</label>
        <input id="kpiWindow" placeholder="10" value="10" title="Number of most recent cycle samples used for KPI shadow series and trend deltas." />
        <p class="field-hint">Use smaller windows for rapid incident triage and larger windows for policy calibration analysis.</p>
      </div>
      <div class="field-group">
        <label class="field-label" for="kpiDomainFilter">KPI Domain Filter</label>
        <input id="kpiDomainFilter" placeholder="execution_quality, risk_and_capital..." title="Optional exact domain filter applied to KPI shadow items." />
        <p class="field-hint">Leave blank for all domains, or enter a domain key to inspect a focused KPI slice.</p>
      </div>
      <div class="field-group">
        <label class="field-label" for="kpiStatusFilter">KPI Status Filter</label>
        <input id="kpiStatusFilter" placeholder="ok, warning, critical, insufficient_data" title="Optional exact status filter for KPI shadow results." />
        <p class="field-hint">Use warning/critical during incident response, or insufficient_data during instrumentation validation.</p>
      </div>
    </div>
    <div class="button-grid">
      <div class="button-group">
        <button onclick="applyFilters()" title="Apply dashboard and KPI filters together, then refresh from latest incidents and KPI payload.">Apply KPI Filters</button>
        <p class="field-hint">Uses current KPI window/domain/status values with the same refresh path as dashboard filters.</p>
      </div>
      <div class="button-group">
        <button onclick="clearKpiFilters()" title="Clear KPI domain/status filters and reset KPI window to default shadow policy window.">Clear KPI Filters</button>
        <p class="field-hint">Returns KPI view to baseline all-domain mode for broad health checks.</p>
      </div>
    </div>
    <div id="kpiSummary"></div>
  </div>
  <div class="grid">
    <div class="card">
      <h2>State + Loop Metrics</h2>
      <pre id="statePayload"></pre>
    </div>
    <div class="card">
      <h2>Financial Dashboard</h2>
      <pre id="financialPayload"></pre>
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
    <div class="card">
      <h2>KPI Shadow Payload</h2>
      <pre id="kpiPayload"></pre>
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
      comparison_window: 10,
      kpi_window: 10,
      kpi_domain: '',
      kpi_status: ''
    };
    let dashboardQuery = { ...defaultDashboardQuery };
    let incidentCursorHistory = [];
    let lastDashboardPayload = null;
    function operatorTokenHeaders() {
      const token = document.getElementById('token').value || '';
      if (!token) {
        return {};
      }
      return {
        'X-Operator-Token': token
      };
    }
    function hasNumericValue(value) {
      return value !== null && value !== undefined && Number.isFinite(Number(value));
    }

    function formatNumber(value, digits) {
      const numeric = Number(value);
      if (!Number.isFinite(numeric)) {
        return '-';
      }
      return numeric.toFixed(digits);
    }

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
      document.getElementById('kpiWindow').value = String(dashboardQuery.kpi_window);
      document.getElementById('kpiDomainFilter').value = dashboardQuery.kpi_domain;
      document.getElementById('kpiStatusFilter').value = dashboardQuery.kpi_status;
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
      dashboardQuery.kpi_window = readPositiveInteger(
        'kpiWindow',
        defaultDashboardQuery.kpi_window
      );
      dashboardQuery.kpi_domain = (document.getElementById('kpiDomainFilter').value || '').trim();
      dashboardQuery.kpi_status = (document.getElementById('kpiStatusFilter').value || '').trim();
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
      params.set('kpi_window', String(dashboardQuery.kpi_window));
      if (dashboardQuery.audit_action) {
        params.set('audit_action', dashboardQuery.audit_action);
      }
      if (dashboardQuery.audit_actor) {
        params.set('audit_actor', dashboardQuery.audit_actor);
      }
      if (dashboardQuery.kpi_domain) {
        params.set('kpi_domain', dashboardQuery.kpi_domain);
      }
      if (dashboardQuery.kpi_status) {
        params.set('kpi_status', dashboardQuery.kpi_status);
      }
      if (dashboardQuery.incident_cursor !== null && dashboardQuery.incident_cursor !== undefined) {
        params.set('incident_cursor', String(dashboardQuery.incident_cursor));
      }
      return '/api/dashboard?' + params.toString();
    }
    async function fetchDashboard() {
      const response = await fetch(dashboardUrl(), {
        headers: operatorTokenHeaders()
      });
      if (!response.ok) {
        const errorText = await response.text();
        document.getElementById('summary').textContent =
          'Dashboard request failed: ' + response.status + (errorText ? ' ' + errorText : '');
        return;
      }
      const payload = await response.json();
      lastDashboardPayload = payload;
      const state = payload.supervisor_state || {};
      const financial = payload.financial_metrics || {};
      const status = state.status || 'UNKNOWN';
      const statusClass = status === 'SUCCESS' ? 'status-success' : (status === 'FAILED' ? 'status-failed' : '');
      const equitySummary = hasNumericValue(financial.current_equity)
        ? ' | equity=' + formatNumber(financial.current_equity, 2)
        : '';
      const netPnlSummary = hasNumericValue(financial.net_pnl)
        ? ' | net_pnl=' + (Number(financial.net_pnl) >= 0 ? '+' : '') + formatNumber(financial.net_pnl, 2)
        : '';
      document.getElementById('summary').innerHTML =
        'Overall: <span class="' + statusClass + '">' + status + '</span> | cycle=' +
        (state.cycle_index ?? '-') + ' | failed_workers=' +
        ((state.failed_workers || []).length) +
        equitySummary +
        netPnlSummary +
        ' | generated_at=' + payload.generated_at;

      document.getElementById('statePayload').textContent = JSON.stringify({
        control_state: payload.control_state,
        loop_metrics: payload.loop_metrics,
        financial_metrics: payload.financial_metrics,
        supervisor_state: payload.supervisor_state
      }, null, 2);
      document.getElementById('financialPayload').textContent =
        JSON.stringify(payload.financial_metrics, null, 2);
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
      const kpiShadow = payload.kpi_shadow || {};
      const kpiSummary = kpiShadow.summary || {};
      const kpiStatusCounts = kpiSummary.status_counts || {};
      const kpiFilters = kpiShadow.filters || {};
      const statusOrder = ['ok', 'warning', 'critical', 'insufficient_data'];
      const statusPills = statusOrder.map((statusName) => {
        const count = kpiStatusCounts[statusName] ?? 0;
        return '<span class="status-pill ' + statusName + '">' + statusName + ': ' + count + '</span>';
      }).join(' ');
      document.getElementById('kpiPayload').textContent =
        JSON.stringify(kpiShadow, null, 2);
      document.getElementById('kpiSummary').innerHTML =
        'KPI items=' + (kpiSummary.total_kpis ?? 0) +
        ' | window=' + (kpiFilters.window ?? '-') +
        ' | domain=' + (kpiFilters.domain ?? 'all') +
        ' | status=' + (kpiFilters.status ?? 'all') +
        ' | ' + statusPills;

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
      const response = await fetch(path, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...operatorTokenHeaders()
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
    async function clearKpiFilters() {
      dashboardQuery.kpi_window = defaultDashboardQuery.kpi_window;
      dashboardQuery.kpi_domain = '';
      dashboardQuery.kpi_status = '';
      dashboardQuery.incident_cursor = null;
      incidentCursorHistory = [];
      syncQueryInputsFromState();
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


def _resolve_operator_token(
    *,
    operator_token: str | None,
    operator_token_env: str,
) -> str | None:
    env_name = operator_token_env.strip()
    if env_name:
        env_token = os.environ.get(env_name, "").strip()
        if env_token:
            return env_token
    cli_token = (operator_token or "").strip()
    return cli_token or None


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
    read_api_token_required: bool = False,
):
    class RuntimeGuiHandler(BaseHTTPRequestHandler):
        def _request_token_matches(self) -> bool:
            if not operator_token:
                return False
            request_token = self.headers.get("X-Operator-Token", "")
            return request_token == operator_token

        def _authorize_read_request(self) -> bool:
            if not read_api_token_required:
                return True
            if self._request_token_matches():
                return True
            _send_json(
                self,
                status=403,
                payload={"error": "invalid_operator_token"},
            )
            return False

        def _authorize_control_request(self) -> bool:
            if not operator_token:
                _send_json(
                    self,
                    status=403,
                    payload={"error": "operator_controls_disabled"},
                )
                return False
            if self._request_token_matches():
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
            if parsed.path.startswith("/api/") and not self._authorize_read_request():
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
                    kpi_window = _coerce_positive_int(
                        _query_value(query, "kpi_window"),
                        field_name="kpi_window",
                    )
                    payload = dashboard_service.build_dashboard_payload(
                        recent_events_limit=events_limit,
                        recent_audit_limit=audit_limit,
                        audit_action=_query_value(query, "audit_action"),
                        audit_actor=_query_value(query, "audit_actor"),
                        incident_limit=incident_limit,
                        incident_cursor=incident_cursor,
                        comparison_window=comparison_window,
                        kpi_window=kpi_window,
                        kpi_domain=_query_value(query, "kpi_domain"),
                        kpi_status=_query_value(query, "kpi_status"),
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
                elif parsed.path == "/api/control/kill-switch/on":
                    state = control_manager.set_kill_switch(
                        active=True, actor=actor, reason=reason
                    )
                elif parsed.path == "/api/control/kill-switch/off":
                    state = control_manager.set_kill_switch(
                        active=False, actor=actor, reason=reason
                    )
                elif parsed.path == "/api/control/cancel-all":
                    state = control_manager.request_cancel_all(
                        actor=actor, reason=reason
                    )
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
    resolved_operator_token = _resolve_operator_token(
        operator_token=args.operator_token,
        operator_token_env=args.operator_token_env,
    )
    if args.token_required_read_api and not resolved_operator_token:
        raise ValueError(
            "--token-required-read-api requires an operator token via "
            "--operator-token or --operator-token-env."
        )

    control_manager = OperatorControlManager(
        control_state_path=args.control_state_path,
        audit_path=args.audit_path,
    )
    dashboard_service = RuntimeDashboardService(
        state_path=args.state_path,
        journal_path=args.journal_path,
        control_manager=control_manager,
        kpi_shadow_policy_path=args.kpi_shadow_policy_path,
    )
    handler_cls = _build_handler(
        dashboard_service=dashboard_service,
        control_manager=control_manager,
        operator_token=resolved_operator_token,
        recent_events_limit=args.recent_events_limit,
        recent_audit_limit=args.recent_audit_limit,
        read_api_token_required=args.token_required_read_api,
    )
    server = ThreadingHTTPServer((args.host, args.port), handler_cls)
    control_mode = "token_required" if resolved_operator_token else "read_only"
    api_read_mode = "token_required" if args.token_required_read_api else "open"
    print(
        "Runtime GUI listening: "
        f"http://{args.host}:{args.port} "
        f"control_mode={control_mode} "
        f"api_read_mode={api_read_mode} "
        f"state_path={args.state_path} "
        f"journal_path={args.journal_path} "
        f"control_state_path={args.control_state_path} "
        f"audit_path={args.audit_path} "
        f"kpi_shadow_policy_path={args.kpi_shadow_policy_path}"
    )
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
