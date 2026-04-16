# Bild evidence and claim-status register
This register enforces KB claim governance in project execution.

## Status labels
- `verified`: confirmed by reproducible evidence (logs, HAR files, tests, or official docs).
- `unverified`: plausible but not yet validated in Bild environment.
- `hypothesis`: speculative working assumption used for planning only.

## High-impact claims
1. Direct authenticated XHR/API calls can bypass browser-layer bot controls for steady-state basket operations.
   - status: `hypothesis`
   - source: `LeroyMerlin_Pilot_Research_Report_v1.0.md`
   - evidence required: successful authenticated end-to-end call sequence captured in Sprint 1.
2. DataDome blocks standard headless browser automation paths on Leroy Merlin infrastructure.
   - status: `unverified`
   - source: `LeroyMerlin_Pilot_Research_Report_v1.0.md`
   - evidence required: repeatable blocked run logs with response headers in Bild test harness.
3. Camoufox is a viable fallback when API-only flow fails.
   - status: `hypothesis`
   - source: pilot research report recommendations
   - evidence required: successful fallback run with documented reliability and failure modes.
4. Pilot legal model (authorized agent use with signed consent + DPA) is sufficient for pilot execution.
   - status: `unverified`
   - source: legal section in pilot research report
   - evidence required: signed legal package review and acceptance by project owner.

## Update protocol
- Update this file in every PR that changes assumptions, architecture, or legal/operational claims.
- Each status change must reference concrete evidence artifacts (file path, command output, or external legal memo ID).

