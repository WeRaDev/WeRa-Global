# ADR 0002: Anti-bot fallback policy

## Status
Accepted

## Context
Bot-detection controls may block standard automation. A deterministic fallback policy is needed to avoid ad hoc decisions.

## Decision
Use a two-tier policy:
1. Primary path: API-call-first flow with authenticated session artifacts.
2. Fallback path: Camoufox-based browser flow only when primary path fails and failure is evidenced.

Escalation requirements:
- Record failure evidence in `docs/evidence-status.md`.
- Document trigger condition and rollback strategy before enabling fallback path in runtime code.

## Consequences
- Positive: keeps architecture simple by default.
- Positive: enforces evidence-based activation of higher-complexity fallback.
- Negative: requires extra instrumentation to detect and classify failure causes.

## References
- `LeroyMerlin_Pilot_Research_Report_v1.0.md`
- `docs/evidence-status.md`