---
governance_event:
  date: 2026-04-19
  workflow: cross-domain
  temporal_scope: mixed
  documents:
    - .gitea/workflows/kb-canonical-validate.yml
    - .gitea/workflows/kb-governance-routing.yml
    - kb-governance/tasks/sprints/2026-20.md
  decisions:
    - FOLLOW19-01 infrastructure hardening is accepted with container-mode pilot evidence.
    - Workflow-level checkout URL override to `host.docker.internal` is the validated control point for containerized jobs.
    - Runner-level `GITHUB_SERVER_URL` alone is insufficient to change `actions/checkout` clone behavior in this setup.
  open_actions:
    - Track post-checkout submodule warning cleanup as non-blocking CI noise reduction.
    - Reassess server-side clone URL/root URL strategy only after container-mode remains stable across additional cycles.
  owner: governance council delegate
  status: closed
---

# Governance Event — FOLLOW19-01 Container Checkout Pilot Review
## Trigger
Sprint `2026-20` execution of carry-over `FOLLOW19-01`, focused on durable container-mode checkout networking for KB governance workflows.

## Validation performed
- Confirmed initial container-mode pilot failure signature (pre-remediation):
  - checkout attempted `http://127.0.0.1:3000/wera-global/WeRa-Global/` and failed with `Connection refused` in runs tied to `run ids 31 and 32`.
- Implemented workflow-level checkout override in both KB workflows:
  - `github-server-url: http://host.docker.internal:3000`.
- Re-dispatched both workflows on branch `feat/kb-roadmap-verification-phase18`; observed successful completions:
  - `http://127.0.0.1:3000/wera-global/WeRa-Global/actions/runs/29`
  - `http://127.0.0.1:3000/wera-global/WeRa-Global/actions/runs/30`
- Verified checkout log evidence in successful jobs:
  - `git remote add origin http://host.docker.internal:3000/wera-global/WeRa-Global`
  - fetch from `http://host.docker.internal:3000/...` completed successfully.
- Verified workflows advanced beyond checkout into policy scripts:
  - `kb_canonical_validate: PASSED`
  - `kb_quality_gate_fixtures: PASSED`
  - `kb_governance_routing_check: PASSED`

## Findings
- The blocker was not container DNS reachability itself; it was checkout URL selection.
- Runner env override did not affect checkout target, while workflow-level override did.
- Container-mode runner operation is now viable for this pipeline with explicit checkout server URL control.

## Decisions
- Close `FOLLOW19-01` as validated in sprint `2026-20`.
- Keep workflow-level `github-server-url` override in both workflows as the current durable baseline.
- Keep rollback-ready runner backup and retain host-mode fallback as operational safety until multi-cycle stability is demonstrated.

## Rollback conditions
- Immediate rollback if any container-mode run reverts checkout target to `127.0.0.1:3000`.
- Immediate rollback if checkout can no longer fetch from `host.docker.internal` or if regression blocks validator execution.
- Rollback procedure:
  - revert checkout override changes in `.gitea/workflows/kb-canonical-validate.yml` and `.gitea/workflows/kb-governance-routing.yml`,
  - restore prior runner configuration from `/Users/mikhailananyin/.act_runner_wera_global/config.yaml.bak.sprint202620.20260419182434`,
  - re-run host-mode verification workflows before further infra changes.

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.governance.events_2026_04_19_follow19_01_container_checkout_pilot_review
  proof_artifact: kb-governance/formal-proofs/governance-events-2026-04-19-follow19-01-container-checkout-pilot-review.lean
  verification_status: verified
