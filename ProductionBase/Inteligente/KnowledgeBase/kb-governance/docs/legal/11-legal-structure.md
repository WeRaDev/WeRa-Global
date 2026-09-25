---
metadata:
  primary_domain: governance
  secondary_domains: [value-proposition]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-09-25
  next_review_due: 2026-12-25
  provenance:
    actor: agent-warp
    source: "Inteligente/Resources/Documents/Research/Human Center — Product 1  Shrinking AI  Desk Research, Heuristic Evaluation &amp; Competitive Analysis.md; founder-approved Discovery Pilot decision; Odoo 19.0 AI and Live Chat documentation"
    confidence: high
    review_status: draft
---

# Legal Structure

## Purpose
Record Inteligente's legal-entity and compliance posture.

## Scope
- In scope: legal-entity identification and baseline compliance posture (DPA, data residency).
- Out of scope: full legal/tax structuring advice.

## Current State
- **Legal entity confirmed**: Inteligente (`www.inteligente.site`) is a consultancy business operated by **Inteligente Razão — Unipessoal LDA** (HQ Lisboa, Portugal), stated directly in the Shrinking AI research document's project description.
- **VAT/NIF confirmed (Sept 2026)**: **PT514477580**. This may now be used in contracts, invoices, and the DPA template's signature block.
- Baseline compliance posture (candidate, not yet formalized): EU-hosted data storage, signed DPA per client, no client data used to train public models, audit logging for consequential actions — consistent with `../../../../SOUL.md` and comparable-vendor practice noted in pricing research.
- **DPA template (not yet built)**: Inteligente acts as a data **processor** for any client engagement touching client-owned personal data (e.g. email content processed by Shrinking AI/Automation Center, financial/client records processed by Financial Automation); the client remains the **controller**. A GDPR Art. 28(3)-compliant DPA template must cover: subject matter, duration, nature and purpose of processing; the categories of personal data and data subjects involved; the controller's rights and the processor's obligations; instructions-only processing; staff confidentiality; Art. 32 security measures; sub-processor authorization and flow-down (naming the actual sub-processors used — the LLM API provider(s), n8n/Make/Zapier, hosting/EU cloud provider); assistance with data-subject rights requests; assistance with the controller's Art. 32-36 obligations (security, breach notification, DPIAs); deletion or return of data at engagement end; and audit/inspection rights. Building it requires first finalizing the actual sub-processor stack (see Open Actions).
- **Heightened considerations for Financial Automation** (Automation Center's finance-industry service): Financial Automation's target audience explicitly includes financial-advisory firms and investment-fund-adjacent solo consultants (see `../../../kb-customers/docs/gtm/05-financial-automation-segments.md`). Existing sector-specific obligations (e.g. supervision, communications and recordkeeping duties in relevant US-regulated firms) can remain applicable to AI-assisted activity and must be established per client and jurisdiction, never assumed. The compliance/data-owner discovery route (see `../../../kb-solution/docs/strategy/04-financial-automation-solution.md`) is the mechanism for this and must complete before any pilot proceeds for a regulated or confidential-data client.
- **Partner Discovery Pilot privacy boundary (Sept 2026):** stage 1 is on Odoo Online, which is Odoo-managed cloud hosting, not local processing. The pilot may use aggregated metrics from the Financial partner's own firm only after written authorization and cloud/privacy review; credentials, raw client records, and third-party confidential data are excluded. Odoo's chatbot documentation says free-input answers are stored in chat transcripts. Odoo's AI documentation supports ChatGPT/OpenAI provider configuration but does not specify this agent's exact prompt payload, transcript/log retention, selected hosting region, or all provider-side processing. Verify the pilot database, agent/channel rules, provider/API-key mode, privacy terms, data location, access, and retention before collecting even the permitted pilot metrics. Do not claim that no private information leaves the machine during this cloud stage. The later Frank local-model MVP is a separate stage requiring its own verification that the local model and supporting services make no unintended external calls.

## Decisions / Rules
- The entity name and VAT/NIF (PT514477580) may now both be used in external-facing material, contracts, and invoices as confirmed.
- Any client engagement handling confidential/financial data requires a signed DPA before work begins — no DPA template exists yet (see Open Actions), so no such engagement should be signed until one does.
- Before the partner pilot, obtain written authorization and complete the cloud/privacy review for the Financial partner's own aggregated metrics; document the permitted fields, excluded data, Odoo database region, provider mode, transcript/log handling, and retention. Odoo Online is not local-only.
- Do not send personal data or third-party confidential data to GPT-4o or another provider unless the applicable controller/processor terms, DPA, data-transfer basis, and provider retention/training settings have been reviewed and approved.
- Financial Automation engagements with financial-advisory or otherwise regulated clients require jurisdiction and regulatory-perimeter confirmation via the compliance/data-owner discovery route; findings must be recorded as confirmed, unresolved, or requiring specialist review — never treated as "compliant" merely because a respondent believes it is.

## Evidence
- `../../../../Resources/Documents/Research/Human Center — Product 1  Shrinking AI  Desk Research, Heuristic Evaluation &amp; Competitive Analysis.md` — verified, states the entity name directly in the project description.
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — verified, describes the compliance posture comparable vendors advertise (EU servers, GDPR, DPA, no training on client data), now Automation Center's own reference.
- `../../../../Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md` — verified, evidences that existing financial-services obligations (supervision, communications, recordkeeping) can remain applicable to AI-assisted activity.
- [Odoo 19 AI API keys](https://www.odoo.com/documentation/19.0/applications/productivity/ai/apikeys.html) — confirms Odoo AI supports OpenAI and Gemini provider configurations, including own API keys.
- [Odoo 19 scripted chatbots](https://www.odoo.com/documentation/19.0/applications/websites/livechat/chatbots.html) — states that free-input answers are stored in chat transcripts.

## Cross-Domain Links
- Related domains: `kb-value-proposition`, `kb-customers`, `kb-solution`
- Related documents: `../../../kb-value-proposition/docs/company/01-company-overview.md`, `../../../kb-customers/docs/gtm/05-financial-automation-segments.md`, `../../../kb-solution/docs/strategy/04-financial-automation-solution.md`

## Open Actions
- Before the Odoo Online pilot, verify database region, account/provider/API-key mode, actual agent context, transcript/log access and retention, applicable Odoo/OpenAI terms, and written partner authorization; record what is unknown rather than asserting local processing, owner: Founder/Consultant.
- Build the GDPR-compliant DPA template (Art. 28(3) clause checklist above): (1) finalize the actual sub-processor list (which LLM API provider(s), which of n8n/Make/Zapier, which EU-region hosting/storage provider) so the Annex is accurate; (2) adapt a reputable DPA template (e.g. a Portuguese law firm's standard template, or a GDPR.eu/IAPP reference template) to that sub-processor list and to Inteligente Razão — Unipessoal LDA / PT514477580; (3) have it reviewed by counsel before first use, owner: Founder/Consultant, due: see `../../../../tasks/backlog.md` HC-004.
- Before onboarding any financial-advisory or otherwise regulated Financial Automation client, confirm the applicable regulatory perimeter and required controls with counsel or a qualified compliance reviewer, owner: Founder/Consultant.
