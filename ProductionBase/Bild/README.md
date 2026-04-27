# Bild
Bild is an AI procurement agent project for Leroy Merlin PRO pilot operations: it converts structured renovation/construction context into a ready-to-pay Leroy Merlin basket while keeping legal authorization, client data sovereignty, and credential security as hard constraints. Non-goals for the pilot are direct payment automation, unauthorized account use, and unsupported marketplace/seller-side workflows.

## Quick start
```bash
cd ProductionBase/Bild
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
If dependency installation fails, fix the reported error before continuing.

## Project structure
- `LeroyMerlin_Pilot_Research_Report_v1.0.md`: canonical pilot research baseline.
- `docs/adr/`: architecture decision records for high-impact choices (session strategy, anti-bot fallback, legal controls).
- `tasks/`: sprint-ready work items and operating task templates.
- `skills/`: project-specific agent skills for repeatable delivery workflows.
- `.gitea/workflows/`: CI pipelines for lint/test/security validation.
- `WARP.md`: project execution and safety policy for contributors and agents.

## Core workflows
- Build: `python -m pip install -r requirements.txt`
- Test: `python -m pytest -q`
- Lint/typecheck: `ruff check . && ruff format --check . && mypy src session_test.py har_extract.py`
- Run (Sprint 1 scaffold validation): `python session_test.py --dry-run`
- Run (HAR endpoint extraction): `python har_extract.py --har-file /path/to/capture.har --output-markdown observed_endpoints.md`

## Constraints and known limits
- Primary technical risk: DataDome + Cloudflare bot defenses may block standard headless automation.
- Baseline approach: direct authenticated API-call layer from exported real-browser session state.
- Fallback approach: Camoufox when API-only calls are insufficient.
- Legal requirement: signed purchasing-agent authorization and DPA before any client credential usage.
- Data governance: EU-hosted Nextcloud workspace and encrypted credential/session storage only.

## Evidence and claim status
- Evidence register: `docs/evidence-status.md`
- API discovery log: `API_ENDPOINTS.md`
- Rule: non-trivial claims must be tagged as `verified`, `unverified`, or `hypothesis` with source notes.

## Contribution and ownership
- Product owner: Fransis Team / Mike Ananyin.
- Architecture and legal constraints derive from `LeroyMerlin_Pilot_Research_Report_v1.0.md`.
- Delivery model: weekly sprint cadence; pull-request based review for all non-trivial changes.
