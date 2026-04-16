# ADR 0001: Session architecture for Leroy Merlin access

## Status
Accepted

## Context
The project must interact with Leroy Merlin authenticated flows while minimizing bot-detection exposure and credential risk.

## Decision
Adopt a session-bootstrap architecture:
- User performs headed manual login once.
- System captures storage state and stores encrypted session artifacts outside the repository.
- Calculator services use session artifacts for API-call-first operations.
- Session renewal is explicit and triggered on auth failure signals.

## Consequences
- Positive: reduces dependence on persistent browser automation.
- Positive: aligns with secure credential/session handling guardrails.
- Negative: requires session lifecycle operational tooling and user refresh flows.
- Negative: API behavior may still enforce browser-coupled constraints.

## References
- `LeroyMerlin_Pilot_Research_Report_v1.0.md`
- `docs/evidence-status.md`

