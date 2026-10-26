# ADR 0001: DreamMakers source-only AgentBaseline preparation
Date: 2026-10-26.
Status: Accepted for local preparation only; registration, tracking and CI activation pending.
## Context
DreamMakers is a maintained WeRa self-publishing and marketing agency. Existing
implementation covers book production, not admitted marketing automation.
It currently has no independent Git repository or umbrella-tracked files.
The work area also contains manuscripts, outputs, environments, generated reports
and customer-specific scripts that must not be swept into a repository.
## Decision
Prepare governance under the DreamMakers name and explicitly inherit umbrella
constitutional and security requirements. Preserve all document-fidelity rules.
Use an allowlist-based `.gitignore` without moving or deleting local material.
Keep legacy scripts and research out of the initial tracking proposal until their
contents and rights have been separately reviewed; a pattern scan is not clearance.
Bootstrap `security/agents/` with the pinned `wera-agent-baseline-0.1` bundle.
Record `mika` in both owner roles, with review pending. All 35 controls and runtime
inventory remain unassessed; component approvals and admission remain pending.
Native umbrella registration is the proposed initial tracking model. Its
Git-index requirement means registration and an explicit selected-file staging
decision must be handled together in a later approval gate.
The nested baseline workflow is executable standalone scaffolding, not active
umbrella routing or proof of protected Gitea checks. No customer document pipeline
runs in CI. Root quality routing and synthetic document tests are a later gate.
## Alternatives considered
A separate Gitea repository/submodule requires a separately confirmed canonical
remote, delivery and history strategy. Do not invent one from inherited remotes.
Registry-only onboarding fails the existing Git-index-based contract; do not
weaken that contract to make an untracked project appear initialized.
## Consequences
Local source-only checks can run without touching manuscripts or live accounts.
Valid structure does not authenticate owners, certify controls or issue authority.
Live publishing, marketing, data transfers and purchases remain independently gated.
## Rollback
Revert only this preparation's governance, ignore and overlay changes after review.
Preserve originals, outputs, backups and QA evidence. No staging, commit, push,
remote configuration or production state is changed by this decision.
