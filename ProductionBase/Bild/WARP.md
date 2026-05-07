# WARP.md
This file defines project-specific operating rules for the `Bild` sub-project.

## Project intent
Bild builds an AI purchasing-agent workflow for Leroy Merlin PRO pilot clients:
- Intake customer project context (text/audio/files) into structured JSON.
- Generate bill-of-material suggestions with AI under explicit constraints.
- Build and validate a basket on Leroy Merlin using authorized client sessions.

## Current maturity
- Stage: pre-development / pilot initialization.
- Source baseline: `LeroyMerlin_Pilot_Research_Report_v1.0.md`.
- Priority: Sprint 1 portal recon and authenticated API endpoint mapping.

## Delivery standards
- Keep changes small and reviewable.
- For non-trivial implementation, propose a plan before coding.
- Document architecture changes in `docs/adr/`.
- Keep sprint-ready work in `tasks/`.

## Security and legal guardrails
- Never commit credentials, session states, tokens, or client documents.
- Session files (`auth_<client_id>.json`) must remain in encrypted vault storage, never repository storage.
- Do not run real account automation without signed client authorization and DPA.
- Use EU-hosted storage for pilot client data.

## Technical guardrails
- Default strategy is API endpoint mapping + authenticated `httpx` flow from real-browser bootstrapped sessions.
- Treat DataDome and Cloudflare behavior as high-risk constraints; validate assumptions with evidence.
- If API-only flow fails, use Camoufox fallback with clear documentation of why fallback is required.

## Quality baseline
- Establish and enforce lint, typecheck, and tests as part of Sprint 1 setup.
- All critical flows must include at least one reproducible smoke test path.

## Mandatory Gitea commitment identity (WARP-only)
- For every Gitea commit/push in this repository, use only the `WARP` account.
- Before commit, set repo-local identity to WARP:
  - `git config user.name "WARP"`
  - `git config user.email "<primary email of the WARP Gitea account>"`
- Before commit/push, verify `git config --get user.name`, `git config --get user.email`, and `git remote get-url origin` target the WeRa Global Gitea namespace.

## DevOps Architect baseline (Archon-SE Enhanced)
- This repository adopts the enhanced DevOps Architect profile defined in `AGENTS.md`.
- Prioritize smallest viable changes, explicit verification, and rollback notes for infra-impacting updates.
- Gate irreversible operations (data drops, force-push, destructive infra actions, production deploys) behind explicit user confirmation.
- Prefer evidence-backed diagnostics over assumptions; include observable success/failure checks for each non-trivial change.
