---
metadata:
  primary_domain: solution
  secondary_domains: [key-activities, key-resources, governance, metrics]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: hypothesis
  last_reviewed_at: 2026-10-05
  next_review_due: 2027-01-05
  provenance:
    actor: agent-warp
    source: "This session's LinkedIn Post-Sharing Tool implementation plan and architect-review critique (2026-10-05); ADR 0002 Consultancy Automation internal-first decision (2026-09-29); founder-approved LinkedIn accessibility-automation scope decision (prior session)"
    confidence: medium
    review_status: draft
---
# Consultancy Automation — Internal Automation Methodology

## Purpose
Describe the **process** Inteligente follows when designing, reviewing, and validating an internal automation tool under **Consultancy Automation** (Automation Center's internal-first use case, ADR 0002). This is a methodology document, not a record of a completed or selected internal workflow: it distills the process actually followed while planning the LinkedIn Post-Sharing Tool into reusable stages for future internal-automation work.

## Scope
- In scope: the staged process for scoping, architecting, critiquing, and validating an internal automation tool before and during its implementation.
- Out of scope: Automation Center's client-facing discovery-and-ROI methodology for external engagements (`03-automation-center-solution.md`); any specific tool's implementation detail (lives in that tool's own directory/README/ADR, e.g. `automations/linkedin-post-share/`); selection of the specific bounded workflow, baseline, or host required by ADR 0002 and backlog item HC-021 — those remain open decisions, not fixed by this document.

## Current State
No internal Consultancy Automation workflow has been run or validated yet. This methodology emerged from a single planning exercise (the LinkedIn Post-Sharing Tool, a candidate automation of part of Inteligente's own consultancy operations — founder-controlled content distribution) and is therefore a **hypothesis**, not a proven internal standard. It is offered as the current default process for the next internal-automation planning effort, to be revised once a real workflow has been run end-to-end and HC-021's validation record exists.

### Observed stages (from the LinkedIn Post-Sharing Tool planning session)
1. **Policy/eligibility verification before design.** Before any architecture work, verify the current, authoritative constraints of any external system being automated against (e.g., which API product/scope an app can actually self-serve access, versus which requires a separate vetted product), rather than assuming the most prominent documentation page applies. Treat deprecation notices and access-tier boundaries as scoped, not blanket.
2. **Explicit scope-exclusion declaration before design.** Write down what will **not** be built or automated (carried over from an earlier, separate safety decision for this case: no scraping, no messaging, no feed/profile scanning, no browser automation) before any design work starts, so later work cannot silently expand scope.
3. **Architecture-decision plan with recorded trade-off reasoning.** For each non-trivial choice (e.g., API endpoint, auth flow, identity resolution, dependency footprint), record the choice and why rejected alternatives were rejected, in a plan and/or ADR, so the rationale is auditable later — mirroring the ADR discipline already used for client-facing decisions (ADR 0001, ADR 0002).
4. **Human-approval invariant built into the tool, not left to process discipline.** For any action with an external, hard-to-reverse effect (e.g., publishing content), the tool itself enforces an explicit confirmation step (e.g., typed confirmation) before executing that action; the plan may add supporting guardrails such as pre-flight content validation and an append-only action log once risk review (stage 6) identifies the need.
5. **Minimal-dependency, mock-only build posture.** Default to no new runtime dependencies for small internal tools, and test exclusively against mocks/fakes — never the live external system — until a narrowly-scoped validation step (stage 7) is deliberately run.
6. **Independent architect-style critique pass before implementation.** After a plan exists, run a dedicated review pass covering at minimum: unvalidated technical assumptions, audit/traceability of consequential actions, idempotency/retry safety, pre-flight input validation, credential/secret handling, and single-point-of-failure/vendor risk. Fold accepted findings back into the plan before writing code.
7. **Narrow validation spike before full build.** Cheaply test the riskiest unverified assumptions identified in stage 6 (e.g., one manual OAuth round-trip, one manual identity-lookup call) before investing in the full implementation, so a wrong assumption is caught while it is still cheap to fix.
8. **Baseline-and-measure discipline, carried over from the external methodology.** Even for an internal tool, define what "before" looks like and what will be measured as "after," so the eventual go/no-go decision (HC-021) has comparable, evidence-graded evidence — consistent with the evidence-grading culture already used in Automation Center's client-facing methodology (`03-automation-center-solution.md`).

Stage 8 has not yet been exercised: the LinkedIn Post-Sharing Tool exists only as a plan plus a critique pass (stages 1-6 observed, stage 7 recommended but not yet run, stage 8 not yet applicable since no implementation or baseline exists).

## Decisions / Rules
- No internal automation tool proceeds to implementation without a written scope-exclusion list (stage 2).
- Any internal tool that performs an external, consequential action (e.g., publishing content on the founder's behalf) must enforce an explicit, non-bypassable human-confirmation step before that action executes.
- Non-trivial architecture decisions for internal tools are recorded (plan and/or ADR) before implementation, on the same evidentiary standard as client-facing methodology decisions.
- A dedicated critique/review pass is performed on every non-trivial internal-automation plan before implementation begins; its accepted findings are folded into the plan, not deferred indefinitely.
- The riskiest unverified technical assumption(s) in a plan are validated with a minimal manual spike before full implementation, rather than discovered mid-build.
- Internal tools default to minimal/no new runtime dependencies and mock-only automated tests; calls to the real external system are limited to the explicit validation spike and later real usage, never to routine automated tests.
- This methodology does not select or assume a specific bounded workflow, baseline, measurement, or host for Consultancy Automation; ADR 0002 and HC-021 govern that selection separately, and this document must not be read as having made that selection.

## Evidence
- This session's LinkedIn Post-Sharing Tool implementation plan (2026-10-05) — hypothesis-grade (E, per the Automation Center evidence-grading scale in `03-automation-center-solution.md`): a single planning artifact, not yet implemented or run.
- This session's architect-style critique of that plan (2026-10-05) — same single-session origin; identified the gaps reflected in stage 6 above (validation spike, audit trail, idempotency, pre-flight validation, secret-handling specificity, vendor-dependency risk).
- `docs/adr/0002-consultancy-automation-internal-first.md` — founder decision establishing Consultancy Automation as internal-first; does not select a workflow, baseline, or host.
- `03-automation-center-solution.md` — source of the evidence-grading and Stop/Measure/Prototype/Pilot framing this document borrows (stage 8) for internal use.

## Cross-Domain Links
- Related domains: `kb-key-activities`, `kb-key-resources`, `kb-governance`, `kb-metrics`
- Related documents: `./03-automation-center-solution.md`, `../../../kb-key-activities/docs/execution/05-automation-center-key-activities.md`, `../../../../docs/adr/0002-consultancy-automation-internal-first.md`, `../../../../tasks/backlog.md` (HC-021)

## Open Actions
- Select the bounded internal workflow, data boundary, baseline, and measures required by ADR 0002/HC-021; decide separately whether the LinkedIn Post-Sharing Tool is that workflow or a different candidate, owner: Founder/Consultant.
- Run the stage-7 validation spike (manual OAuth round-trip and identity lookup) for the LinkedIn Post-Sharing Tool plan before full implementation, owner: Founder/Consultant.
- Fold the stage-6 critique findings (audit log, idempotency guard, pre-flight length validation, OS-keychain secret storage, token-expiry warning, vendor-dependency risk note) into the LinkedIn Post-Sharing Tool plan before implementation.
- After the first internal workflow is implemented and run, revisit this methodology against real results and update `evidence_status` from `hypothesis` toward `verified` or revise the stages, owner: Founder/Consultant.
