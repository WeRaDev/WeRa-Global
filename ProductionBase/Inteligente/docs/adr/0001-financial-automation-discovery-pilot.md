# ADR 0001: Financial Automation Discovery Pilot and Staged Delivery

## Status
Accepted — 2026-09-25

## Context
Automation Center’s governed discovery and ROI method has been designed, but no partner pilot session or result is yet confirmed. The Financial partner will act as the pilot customer using only authorized, aggregated metrics from their own firm; the Operations partner will validate the interview method. This is also a commercial pilot: its output should help the customer make a documented buying decision, not merely test the technology.

The existing Odoo Live Chat deployment on Frank has generic lead-capture behavior, not the governed interview. Odoo 19 documentation describes an AI Agent attached to a Live Chat channel rule as taking priority over a scripted chatbot when both are assigned. It does not establish that the scripted interview can invoke the agent only at a later escalation step, nor specify the exact conversation payload, transcript retention, or all provider-side handling. Odoo Online is hosted by Odoo and does not support custom modules.

## Decision
Deliver the work in three gated stages:

1. **Discovery Pilot — Odoo Online.** Use a structured, deliverable-first interview and the Odoo AI Agent stack (GPT-4o is the founder-reported model and must be verified in the pilot database). The Financial partner is the customer; the Operations partner validates the method. The analyst is intended to receive only a minimized, schema-allowed question/answer context after explicit escalation and to suggest a targeted follow-up. Before enabling automatic handoff, test that the supported Odoo configuration preserves the scripted-chatbot-first sequence and verify the context sent, storage/processing locations, and transcript/log retention. If that boundary cannot be verified, the founder will manually invoke the analyst on the single permitted question/answer during this partner pilot. Prompts and instructions alone are not proof of data isolation.
2. **Local MVP — Frank (`wera-ss-pt-sn-1`, TRL4).** After the pilot validates the method, host Odoo and live chat on Frank and use a local AI model. Proceed only after capacity, ingress, tenancy, access-control, backup, and isolation checks.
3. **First paying customer — SolarSeed TRL5 (`wera-ss-pt-tv-1`).** After the customer signs, deploy that customer’s account and agent on the intended TRL5 host, subject to readiness and customer-isolation checks. The long-term direction is a dedicated machine per customer, within Inteligente’s network or on the customer’s premises.

The interview starts from deliverables, not a copy of the customer’s existing workflow: identify the output, owner, recipient, frequency, quality criteria, effort, exceptions, review, and delivery. The analyst can propose clarifying questions for one answer at a time. ROI is calculated deterministically, with evidence grades, assumptions, sensitivity, and a range; the output is a draft automation plan and estimated ROI for founder review before it is presented as a proposal. Non-reconstructability is a design goal, not a guarantee, unless supported by testing.

For the Odoo Online pilot, allow only aggregated metrics from the Financial partner’s own firm after written authorization and cloud/privacy review. Do not collect credentials, raw client records, or third-party confidential data. This is a cloud-hosted pilot, not local-only processing. Pilot success requires a validated interview/ROI workflow plus a documented buying decision or qualified paid-pilot offer; payment is a separate milestone.

Use current market benchmarks and a modest case-by-case undercut; do not set a fixed discount or use internal costs as a cost-plus revenue formula. Internal costs remain viability guardrails. Partner compensation is only a proposal: both participants would share revenue from financial-industry customers during each customer’s active maintenance period, with an additional customer-attributed share of one-time automation fees for the introducer. Shares would be calculated from collected revenue after agreed direct delivery costs. Percentages, allocation, caps, duration, employer/conflict approvals, and legal/tax review remain open. Resolve the conflict between the existing free-discovery decision and a proposed share of a one-time discovery fee before promising or pricing either.

## Consequences
- The pilot can validate method and commercial interest without claiming local-only processing or completed privacy guarantees.
- Odoo’s native Live Chat behavior is a setup gate. If escalation-only invocation cannot be demonstrated, the founder-triggered analyst step is the pilot fallback; automated handoff remains gated.
- A successful partner pilot does not itself mean a paid client engagement has been signed or paid.
- The workbook remains at `Resources/Documents/Research/Financial Automation/financial_advisory_automation_mvp.xlsx`; its uncommitted move is user-owned and must not be staged or reverted.

## References
- `KnowledgeBase/kb-solution/docs/strategy/03-automation-center-solution.md`
- `KnowledgeBase/kb-solution/docs/strategy/04-financial-automation-solution.md`
- `KnowledgeBase/kb-key-resources/docs/architecture/06-automation-center-key-resources.md`
- `tasks/backlog.md`
- [Odoo 19 AI live chat](https://www.odoo.com/documentation/19.0/applications/productivity/ai/live-chat.html)
- [Odoo 19 AI agents](https://www.odoo.com/documentation/19.0/applications/productivity/ai/agents.html)
- [Odoo 19 AI API keys](https://www.odoo.com/documentation/19.0/applications/productivity/ai/apikeys.html)
- [Odoo 19 scripted chatbots](https://www.odoo.com/documentation/19.0/applications/websites/livechat/chatbots.html)
- [Odoo 19 Odoo Online](https://www.odoo.com/documentation/19.0/administration/odoo_online.html)
