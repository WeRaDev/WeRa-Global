# Bild
Bild is an AI procurement agent project for Leroy Merlin PRO pilot operations: it converts structured renovation/construction context into a ready-to-pay Leroy Merlin basket while keeping legal authorization, client data sovereignty, and credential security as hard constraints. Non-goals for the pilot are direct payment automation, unauthorized account use, and unsupported marketplace/seller-side workflows.

## Quick start
```bash
cd /Users/mikhailananyin/Documents/WeRa\ Global/ProductionBase/Bild
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt || true
```
If `requirements.txt` does not exist yet, create it as part of Sprint 1 when service modules are added.

## Project structure
- `LeroyMerlin_Pilot_Research_Report_v1.0.md`: canonical pilot research baseline.
- `docs/adr/`: architecture decision records for high-impact choices (session strategy, anti-bot fallback, legal controls).
- `tasks/`: sprint-ready work items and operating task templates.
- `skills/`: project-specific agent skills for repeatable delivery workflows.
- `.gitea/workflows/`: CI pipelines for lint/test/security validation.
- `WARP.md`: project execution and safety policy for contributors and agents.

## Core workflows
- Build: TBD in Sprint 1 after module scaffold (`calculator/`, `agent/`, `api/`) is created.
- Test: TBD in Sprint 1; minimum path should cover session capture, endpoint mapping, and basket creation smoke tests.
- Lint/typecheck: TBD in Sprint 1 (recommended baseline: `ruff`, `mypy`, `pytest`).
- Run: TBD in Sprint 2 after first Calculator MVP implementation.

## Constraints and known limits
- Primary technical risk: DataDome + Cloudflare bot defenses may block standard headless automation.
- Baseline approach: direct authenticated API-call layer from exported real-browser session state.
- Fallback approach: Camoufox when API-only calls are insufficient.
- Legal requirement: signed purchasing-agent authorization and DPA before any client credential usage.
- Data governance: EU-hosted Nextcloud workspace and encrypted credential/session storage only.

## Contribution and ownership
- Product owner: Fransis Team / Mike Ananyin.
- Architecture and legal constraints derive from `LeroyMerlin_Pilot_Research_Report_v1.0.md`.
- Delivery model: weekly sprint cadence; pull-request based review for all non-trivial changes.
