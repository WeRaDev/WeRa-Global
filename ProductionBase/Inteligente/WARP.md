# WARP.md
This file defines project-specific operating rules for the `Inteligente` sub-project.

## Project intent
Inteligente (`Inteligente Razao - Unipessoal LDA`, `www.inteligente.site`) is an AI-automation consultancy running two product lines:
- **Human Center**: human-facilitated AI-adoption services. Service **Shrinking AI** discovers and scopes a client's actual workflow bottleneck (Design Thinking / Theory of Constraints framing) via a paid diagnostic session. Service **Empowering Human** (hypothesis-stage) helps individuals and businesses discover the most suitable AI applications for their needs.
- **Automation Center**: builds automations (n8n/Make/Zapier + LLM orchestration, OCR/document extraction) for bounded, high-trust use cases: email triage/drafting/follow-up, document/receipt processing, bookkeeping handoff. Service **Financial Automation** specializes this for the financial industry.
- Keep every consequential (financial/legal) action subject to explicit human approval.

## Current maturity
- Stage: the partner-led Financial Automation Discovery Pilot was formally initiated in Sept 2026; no first session or result is yet confirmed. Stages are Odoo Online pilot → local MVP on Frank (TRL4, `wera-ss-pt-sn-1`) → first paying customer on the SolarSeed TRL5 host (`wera-ss-pt-tv-1`), subject to readiness and isolation checks.
- Source baseline: `Resources/Documents/Research/` (desk research, pricing benchmarks, problem framing).
- Priority: validate the deliverable-first interview, evidence-graded ROI output, and commercial buying decision with the partner pilot. Empowering Human has no commissioned research yet.

## Delivery standards
- Keep changes small and reviewable.
- For non-trivial implementation or business-model changes, propose a plan before executing.
- Document architecture and business-model decisions in `docs/adr/`.
- Keep sprint-ready work in `tasks/`.
- Keep the `KnowledgeBase/` business-model-canvas domains current as the business model evolves; tag unverified claims with `evidence_status: unverified` per the KB document template.

## Security and legal guardrails
- Never commit client credentials, session state, tokens, or client documents.
- Do not run automation against a real client account without signed authorization and a Data Processing Agreement (DPA).
- Use EU-hosted storage for client data where required; do not use client data to train public models.
- Require human approval for any financially or legally consequential automated action.

## Quality baseline
- Baseline documentation/structure is validated by `.gitea/workflows/ci.yml`.
- Once automation delivery code exists, establish and enforce lint, typecheck, and tests in the same sprint that introduces the tooling.

## Mandatory Gitea commitment identity (WARP-only)
- For every Gitea commit/push in this repository, use only the `WARP` account.
- Before commit, set repo-local identity to WARP:
  - `git config user.name "WARP"`
  - `git config user.email "<primary email of the WARP Gitea account>"`
- Before commit/push, verify `git config --get user.name`, `git config --get user.email`, and `git remote get-url origin` target the WeRa Global Gitea namespace.
