# Comet Browser-Control Brief — Deferred: Financial Automation Live-Chat Bot

## Mission
This handoff is **deferred and non-actionable for now**. Do not configure, test, publish, activate, or run the external Financial Automation Discovery Pilot chatbot. The partner pilot is deferred, not cancelled, until internal Consultancy Automation is validated and the existing authorization, safety, actionable-human-notification, privacy, and data-flow gates pass. This brief is retained as future preparation only; work may resume only after those prerequisites pass and the founder re-authorizes it.

No external partner session or result is confirmed. This document does not authorize Odoo configuration or testing.

## Confirm the target before any future approved work
The target for any future approved work is the founder-designated Odoo Online pilot database for the Financial partner. Before editing:

1. Confirm the database name and URL with the founder and verify that the current browser session is in that database.
2. Confirm the founder has authorized configuration work there.
3. Check whether written authorization for the Financial partner's aggregated firm metrics and the cloud/privacy review are complete. If they are not, use synthetic test data only and leave the bot unpublished.
4. Record the current channel, chatbot, and AI Agent assignments before changing them.

**Do not confuse the target with the existing generic chatbot** at `www.inteligente.site`, which is hosted on Frank and performs generic live-chat/lead-routing/lead-creation only. Do not edit that bot, the Frank host, a customer database, or the SolarSeed TRL5 host as part of this task. If the target database cannot be confirmed, stop and ask the founder.

## Scope and safety boundaries
- The pilot may use only aggregated metrics from the Financial partner's own firm, and only after written authorization and cloud/privacy review.
- Never enter credentials, raw client records, personal data, third-party confidential data, or real customer documents. Use synthetic values for testing.
- Do not expose, copy, change, or store passwords, API keys, session tokens, or other secrets. If a secret is visible or a setting requires revealing one, stop and report the blocker.
- Do not change subscriptions, enable paid services, alter billing, create databases, install custom modules, delete records/transcripts, or change security/access policies.
- Do not send emails, create or distribute CRM leads containing interview answers, invite partners, or publish/share the chatbot.
- Do not promise compliance, guaranteed ROI, or a binding commercial proposal. The founder reviews any draft plan and ROI range before it is presented.
- Keep every consequential financial/legal decision subject to explicit human approval.

## Use the approved interview source
All repository paths below are relative to the project root, `ProductionBase/Inteligente/`.
Use `Resources/Documents/Research/Financial Automation/financial_advisory_automation_mvp.xlsx` as the canonical source for the question script, data model, controls, and scoring logic. The related research playbook is `Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md`.

If these sources are not available in the Comet session, do not invent detailed question wording, fields, thresholds, or formulas. Ask the founder to provide the approved source before completing the interview script.

The intended interview is deliverable-first: identify the completed output, its owner and recipient, frequency, quality criteria, effort, exceptions, review, and delivery. Ask one neutral question per turn, begin with a recent concrete example, allow “I don't know” or “someone else knows,” and do not suggest numeric ranges before the respondent gives an unaided answer. Route questions only to people who can reliably answer them.

The bot's outcome is a screening result: **Stop / Measure / Prototype / Pilot**. Record evidence grades and assumptions. ROI, if supported by the approved workbook, must be calculated deterministically as a range with sensitivity and full-cost assumptions; do not let the language model invent or guarantee an ROI. The output is a draft for founder review, not a proposal sent to the partner.

## Future scope after the deferral is lifted
In the designated pilot database:

1. Inspect the live-chat channel rules, assigned chatbot, script, AI Agent, topics/tools, model/provider selection, API-key mode, database region, transcript/log settings, and available privacy/retention terms. Record what is observable; never infer an unknown setting.
2. Configure the scripted interview from the approved source. Include a clear purpose/disclosure and an explicit consent gate. If consent is declined, end the interview without collecting answers.
3. Include a clear instruction not to enter sensitive information. If sensitive information appears, do not repeat it or incorporate it into a summary; stop the flow and report what happened without copying the sensitive content.
4. Keep the compliance/data-owner route mandatory for the financial-industry pilot. Legal, tax, or investment-advice requests; credentials; suspected breaches; disputed consent; and requests for guaranteed ROI must stop the automated interview and route to a human.
5. Use only synthetic test data. Do not run tests on the public website or with partner/customer data.

## Gate the AI Agent handoff
Odoo 19 documentation says an AI Agent assigned to a Live Chat channel rule takes priority over a scripted chatbot when both are assigned. The documentation does not establish that this setup can defer invocation until a particular script step, nor does it specify this database's exact prompt payload, transcript retention, or provider-side handling. Scripted-chatbot free-text answers are stored in chat transcripts. Odoo Online is cloud-hosted and does not support custom modules.

Therefore:

1. Do not assign the AI Agent to a live channel on the assumption that a prompt alone will keep it from seeing the full transcript.
2. In a safe test configuration, verify whether ordinary scripted questions run without invoking the AI Agent.
3. Trigger an explicit escalation using synthetic content. Verify the actual transmitted context, model/provider, storage, access, and retention—not just the displayed prompt or intended instructions.
4. Enable automatic handoff only if the test demonstrates both scripted-first behavior and the permitted minimized question/answer context, and the founder approves the observed data handling.
5. If either condition cannot be demonstrated, leave automatic invocation disabled. The approved pilot fallback is for the founder to manually submit one minimized, permitted question/answer to the analyst for a suggested follow-up.
6. GPT-4o is founder-reported, not confirmed. Verify the actual model/provider in this database. Do not change API keys or enable billing to make a model work; report any blocker.

Do not claim that prompts guarantee data isolation, prevent transcript access, or make an answer non-reconstructable.

## Acceptance tests
Run these with synthetic data in a non-public test flow, recording pass/fail and observed behavior:

- Consent granted: the approved scripted sequence proceeds one question at a time.
- Consent declined: the sequence stops without continuing intake.
- Unknown answer or referral to another role: the bot accepts the approved response and does not guess.
- Synthetic sensitive input: the bot stops/escalates without repeating the input in its response or summary.
- Legal/tax/investment-advice or guaranteed-ROI request: the bot routes to a human and makes no substantive commitment.
- Ordinary scripted path: confirm whether an AI Agent is invoked and inspect the actual context if it is.
- Explicit AI escalation: confirm whether only the approved minimized question/answer is sent. If this cannot be verified, leave the Agent disabled and document the founder-triggered fallback.
- Draft output: confirm that no automatic email, CRM lead creation/sharing containing interview answers, public proposal, or guaranteed ROI is generated.
- Confirm provider/model, API-key mode (without viewing the key), database region, transcript/log storage and retention, and applicable privacy terms—or clearly record each item as unresolved.

## Completion and handoff
The configuration is ready for founder review only when:

- The target Odoo Online database is confirmed and the existing Frank bot remains untouched.
- The approved script is configured and the synthetic acceptance tests are recorded.
- Automatic AI handoff is either demonstrated to meet the stated boundary and explicitly approved, or remains disabled with the founder-triggered fallback documented.
- Data scope, provider/model, region, transcript/log behavior, retention, and unresolved privacy items are reported accurately.
- The bot remains unpublished and unavailable to public visitors pending founder go-live approval and confirmation that written authorization and cloud/privacy review are complete.

Report back with the database identifier, channel/bot configuration changed, test results, observed AI context and data handling (or why these remain unverified), unresolved blockers, and the final status: **ready for founder review**, **fallback configured**, or **blocked**. Do not include secrets, interview answers, or sensitive test data in the report.

## Reference material
- Project decision: `docs/adr/0001-financial-automation-discovery-pilot.md`
- Pilot and Odoo constraints: `KnowledgeBase/kb-solution/docs/strategy/03-automation-center-solution.md`
- Financial-industry controls: `KnowledgeBase/kb-solution/docs/strategy/04-financial-automation-solution.md`
- Approved script and data model: `Resources/Documents/Research/Financial Automation/financial_advisory_automation_mvp.xlsx`
- [Odoo 19 AI live chat](https://www.odoo.com/documentation/19.0/applications/productivity/ai/live-chat.html)
- [Odoo 19 AI agents](https://www.odoo.com/documentation/19.0/applications/productivity/ai/agents.html)
- [Odoo 19 AI API keys](https://www.odoo.com/documentation/19.0/applications/productivity/ai/apikeys.html)
- [Odoo 19 scripted chatbots](https://www.odoo.com/documentation/19.0/applications/websites/livechat/chatbots.html)
- [Odoo Online](https://www.odoo.com/documentation/19.0/administration/odoo_online.html)
