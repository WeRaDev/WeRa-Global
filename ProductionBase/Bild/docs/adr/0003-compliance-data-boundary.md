# ADR 0003: Compliance and data-boundary model

## Status
Accepted

## Context
Pilot execution uses client data and account authorization, requiring strong legal and data-boundary controls.

## Decision
Adopt compliance-first boundary rules:
- No account automation without signed authorization and DPA.
- No credentials/session artifacts stored in git.
- No unnecessary client PII in engineering artifacts; only minimum metadata required for execution.
- Evidence and legal status tracked as explicit readiness gates before operational scaling.

## Consequences
- Positive: reduces legal and security exposure early.
- Positive: aligns project operations with stated pilot legal model.
- Negative: onboarding may be slower due to legal and process prerequisites.

## References
- `LeroyMerlin_Pilot_Research_Report_v1.0.md`
- `tasks/execution-readiness.md`

