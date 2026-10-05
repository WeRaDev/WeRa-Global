# Financial Automation Discovery Pilot: Configuration and Test Handoff

Date: 25 September 2026  
Final status: **BLOCKED**  
Scope: Founder-authorized configuration and synthetic testing only.

## Sequencing update — 29 September 2026

Per ADR 0002, the external partner pilot is **deferred, not cancelled**, until Consultancy Automation is internally validated and the existing safety, actionable-human-notification, privacy, data-flow, and authorization gates pass. No partner session or result is recorded. This dated handoff remains the source for the failed tests and external-pilot constraints; do not reactivate chatbot 4 or infer that internal Consultancy Automation uses Odoo Online, Frank, or SolarSeed.

The pilot interview has been configured as a separate draft, tested through Odoo's authenticated chatbot test interface, and archived after mandatory safety tests failed. It is not ready for a partner session or public release; the saved configuration is available for founder inspection in the [pilot chatbot record](https://www.inteligente.site/odoo/action-203/4).

## Target and authorization

- **Authorized target:** The founder explicitly confirmed `www.inteligente.site/odoo` and instructed configuration and synthetic testing to proceed, overriding the original brief's exclusion of that site.
- **Observed database:** `wera-global`, with application version `19.0+e`, was reported by the running application's metadata during inspection of the [Odoo configuration](https://www.inteligente.site/odoo/action-203/4).
- **Hosting status:** The founder confirmed on 25 September 2026 that the authorized database runs on Odoo Online. This is founder-reported confirmation of the hosting class, not independent evidence of the deployment region, underlying infrastructure, AI provider processing, or the relationship between the public website, this database, and the previously documented Frank-hosted generic bot. A custom domain and application version do not establish those remaining facts.
- **Approvals:** The founder reported both written authorization for aggregated firm metrics and the cloud/privacy review complete. Supporting approval documents were not supplied or independently audited; no real firm metrics were used in testing.
- **Actual change boundary:** A separate pilot bot was created rather than overwriting the existing channel's publicly configured workflows. The [existing channel rules](https://www.inteligente.site/odoo/livechat/3) remained unchanged.

### Founder confirmation — 25 September 2026

The founder confirmed that the authorized database is actually run on Odoo Online. This resolves the hosting-class question for the authorized target. It does not independently verify the database's region, provider-side processing, API-key mode, actual model endpoint, public reachability of the existing routes, or how the `www.inteligente.site` website and previously documented Frank deployment relate to this Odoo Online database.

## Sources used

The canonical source was the supplied `financial_advisory_automation_mvp.xlsx`. The workbook was read without modification; its formulas, thresholds and input cells were not changed.

| Workbook location | Use in configuration or review |
|---|---|
| `Chatbot Playbook!B6:J41` | Canonical disclosure requirements, consent, role/authority questions, Adviser, Operations, Compliance and Finance routes, and human-review completion. |
| `Data Model!B6:I35` | Intended logical records, provenance, sensitivity and human-review boundaries. These were not represented as newly installed database models. |
| `Evidence Inputs!B21:M56` | Range, unit, source, validation owner and evidence-grade requirements. |
| `ROI Model!B5:F43` | Deterministic ROI authority; no ROI calculation was delegated to an LLM or implemented in chat. |
| `Controls & Score!B7:G32` | Scorecard and hard-gate requirements. No automatic score-to-release threshold was invented. |
| `Implementation Plan!B7:G43` | Required implementation components, governance and acceptance evidence. |

The three supplied private-wealth research documents were used as supporting design context. The specifically named `Critical Review and Revised Chatbot ROI Interview Playbook.md` was not among the attachments; no claim is made to have reviewed that exact document, and the supplied workbook remained canonical.

## Existing setup recorded before changes

The following configuration was observed and left unchanged in the [Human Center channel](https://www.inteligente.site/odoo/livechat/3).

| Item | Observed configuration |
|---|---|
| Channel | Human Center, record 3. [Channel configuration](https://www.inteligente.site/odoo/livechat/3) |
| Scripted route | Rule 1, sequence 10: Show, `/discovery-quick`, always enabled, scripted bot 3, no AI Agent. [Channel rules](https://www.inteligente.site/odoo/livechat/3) |
| AI route | Rule 2, sequence 11: Show, `/discovery-interview`, always enabled, AI Agent 5, no scripted bot. [Channel rules](https://www.inteligente.site/odoo/livechat/3) |
| Existing scripted bot | Human Center — Discovery Entry (Scripted); includes Email and Create Lead & Forward steps. [Existing bot](https://www.inteligente.site/odoo/livechat/3/action-203/3) |
| Existing AI Agent | Human Center — Discovery Interview Agent; configured model `gpt-4o`, analytical style, unrestricted-to-sources, no source records. [Existing agent](https://www.inteligente.site/odoo/action-1223/5) |
| Existing topic/tools | Create Leads topic, with AI CRM: Create Lead and AI CRM: Get Lead creation available parameters. [Existing agent](https://www.inteligente.site/odoo/action-1223/5) |

The existing agent's instructions include a claim that sensitive information will not be stored and instructions to create a lead at interview completion. Those instructions were not used for the financial draft or validated as storage controls; they remain a separate review concern in the [unchanged existing agent](https://www.inteligente.site/odoo/action-1223/5).

## Pilot configuration saved

The new record is **Financial Automation Discovery Pilot [BLOCKED - SYNTHETIC ONLY]**, chatbot 4. Its final state is `active = false`, with 47 script steps, no live-channel rule assignments, zero connected channels and zero generated leads in the [saved pilot record](https://www.inteligente.site/odoo/action-203/4).

- **Disclosure:** Version `FA-SYN-2026-09-25-v1`, synthetic-only purpose, transcript-storage warning, prohibited-data warning, skip/stop rights, unresolved handling details and no guarantee of deletion or confidentiality. The notice was updated after testing to state the failed safety gate explicitly. [Pilot script](https://www.inteligente.site/odoo/action-203/4)
- **Consent and authority:** Affirmative consent, decline and human-review choices; role selection; direct/oversight/both authority selection; terminal branches for uncertain role or authority. [Pilot script](https://www.inteligente.site/odoo/action-203/4)
- **Interview:** 31 free-input prompts taken from the workbook, with the recent deliverable question first, then appropriate role-based questions and mandatory compliance/data-owner review. Multiple-role respondents traverse the role routes; compliance is a mandatory review stage rather than an optional route. [Pilot script](https://www.inteligente.site/odoo/action-203/4)
- **Unknowns:** The instructions accept “I don't know,” “Someone else knows,” “Not applicable” and “Prefer not to answer,” without model-based inference. Unknown authority or a compliance referral stops the relevant branch. [Pilot script](https://www.inteligente.site/odoo/action-203/4)
- **Completion:** Stop / Measure / Prototype / Pilot is explicitly reserved for human screening review, with evidence grades and hard gates to be checked separately. The bot does not invent a classification, numeric score, ROI, proposal or approval. [Pilot script](https://www.inteligente.site/odoo/action-203/4)
- **Manual analyst fallback:** The final review path explains founder-triggered submission of one permitted, minimized question/answer to an approved analyst. It does not transmit the answer, invoke an agent or claim technical context isolation. [Pilot script](https://www.inteligente.site/odoo/action-203/4)
- **Excluded actions:** No email/phone collection, lead-creation or operator-forwarding step exists in the draft; no public rule, channel or agent assignment was added. No module, billing, subscription, access-policy or credential change was made. [Pilot configuration](https://www.inteligente.site/odoo/action-203/4)

## Synthetic acceptance results

Tests used the built-in [authenticated chatbot test view](https://www.inteligente.site/chatbot/financial-automation-discovery-pilot-draft-synthetic-only-4/test), not the existing public discovery routes. An unauthenticated request to that test URL redirected to the Odoo login page; no partner session, real interview answers, documents or credentials were used.

Test answers and sensitive-test payloads are intentionally omitted from this report.

| Test | Result | Observed behavior |
|---|---|---|
| Consent granted | PASS, tested scope | Advanced through role and authority to the recent-deliverable question; the Multiple-role path presented the scripted questions one at a time. [Test view](https://www.inteligente.site/chatbot/financial-automation-discovery-pilot-draft-synthetic-only-4/test) |
| Consent declined | PASS | Displayed the decline termination text and “This livechat conversation has ended,” without further intake. [Test view](https://www.inteligente.site/chatbot/financial-automation-discovery-pilot-draft-synthetic-only-4/test) |
| Unknown answer / another role knows | PASS for acceptance, not structured extraction | Accepted both responses and continued with the next scripted prompt without guessing. No automatic evidence registry or field validation was demonstrated. [Test view](https://www.inteligente.site/chatbot/financial-automation-discovery-pilot-draft-synthetic-only-4/test) |
| Unknown role | PASS | “Unsure” produced the authority-unresolved stop message; the conversation ended. [Test view](https://www.inteligente.site/chatbot/financial-automation-discovery-pilot-draft-synthetic-only-4/test) |
| Role routing | PASS for exercised paths | Multiple traversed Adviser, Operations, Finance and Compliance questions; Finance-only went from the shared deliverable question to Finance questions without the Adviser/Operations sequence. Separate exhaustive tests of every role/authority combination were not run. [Test view](https://www.inteligente.site/chatbot/financial-automation-discovery-pilot-draft-synthetic-only-4/test) |
| Mandatory compliance/data-owner referral | PASS | Selecting referral stopped intake with mandatory-review wording and an ended conversation. No referral message or automatic transfer was sent. [Test view](https://www.inteligente.site/chatbot/financial-automation-discovery-pilot-draft-synthetic-only-4/test) |
| Synthetic sensitive input | FAIL | The native free-input flow advanced to the next interview question rather than stopping or escalating. No bot response repeated the test payload, but that does not remove it from the transcript. [Test view](https://www.inteligente.site/chatbot/financial-automation-discovery-pilot-draft-synthetic-only-4/test) |
| Legal-advice request | FAIL | Advanced to the next scripted question rather than routing to a human; no substantive legal answer was generated. [Test view](https://www.inteligente.site/chatbot/financial-automation-discovery-pilot-draft-synthetic-only-4/test) |
| Tax/investment-advice request | FAIL | Advanced to the next scripted question rather than routing to a human; no substantive advice was generated. [Test view](https://www.inteligente.site/chatbot/financial-automation-discovery-pilot-draft-synthetic-only-4/test) |
| Guaranteed-ROI request | FAIL | Advanced to the next scripted question rather than routing to a human; no ROI guarantee was generated. [Test view](https://www.inteligente.site/chatbot/financial-automation-discovery-pilot-draft-synthetic-only-4/test) |
| Ordinary script / AI invocation | PARTIAL | The draft has no AI channel assignment and produced scripted responses. Server-side invocation logs and provider traffic were not inspected, so no telemetry-backed claim of zero provider requests is made. [Pilot configuration](https://www.inteligente.site/odoo/action-203/4) |
| Explicit analyst escalation | FALLBACK VERIFIED; AUTOMATIC HANDOFF NOT ENABLED | The manual-follow-up choice displayed the founder-triggered fallback message. No live agent handoff or transmitted-context experiment was run because the necessary privacy boundary was not established. [Test view](https://www.inteligente.site/chatbot/financial-automation-discovery-pilot-draft-synthetic-only-4/test) |
| Draft outcome / side effects | PARTIAL | The review notice made no numeric ROI or proposal; zero generated leads and no lead-creation steps were verified. A complete outbound-email audit and automatic structured review-brief generation were not performed. [Pilot configuration](https://www.inteligente.site/odoo/action-203/4) |
| Release isolation | PASS for observed controls | No live rules or channels reference the draft; it is archived. The test view required login for an unauthenticated request. [Pilot configuration](https://www.inteligente.site/odoo/action-203/4) |

## AI context, storage and privacy evidence

| Item | Status |
|---|---|
| Model selection | Existing Agent 5 is configured as GPT-4o / `gpt-4o`; this is a configuration observation, not proof of the model serving any request. [Agent configuration](https://www.inteligente.site/odoo/action-1223/5) |
| Actual provider endpoint / processing entity | Unresolved; not established from runtime traffic or contractual records. |
| API-key mode | Unresolved; no key value was read, revealed, copied or modified. A restricted settings lookup did not establish the custom-key toggle's value. |
| Automatic handoff | Not configured for the draft; no rule assigns its script to an AI Agent. [Pilot configuration](https://www.inteligente.site/odoo/action-203/4) |
| Transmitted context | Unverified; no provider-bound minimized-context test was conducted. No prompt is treated as proof of isolation. |
| Transcript behavior | Synthetic test history remained visible after restarting the conversation and navigating back to the backend, demonstrating that the test was not a guaranteed ephemeral/no-storage interaction. [Odoo test/backend](https://www.inteligente.site/odoo/action-203/4) |
| Transcript access | Current operator visibility was observed; the full permission matrix, administrator access, backups and exports were not audited. |
| Logs and retention | Exact logging, retention duration, deletion process, backups and provider-side handling remain unresolved. No transcripts or records were deleted. |
| Database region / underlying infrastructure | Odoo Online hosting is founder-confirmed; the deployment region and underlying infrastructure/provider processing remain unresolved. `wera-global` and `19.0+e` do not establish them. |
| Applicable privacy terms | Founder reports review complete; the precise governing terms, processing agreement, subprocessor conditions and approval evidence were not attached or independently verified. |

## Remaining implementation gaps

- **Runtime safety gate:** Free-text detection and immediate stop/escalation failed. This cannot be replaced by a warning or by an unverified agent prompt.
- **Structured evidence:** The workbook's logical schema, immutable provenance, grades, validation ownership and assumptions were not installed as database objects. Questions currently produce chat transcripts, not a validated evidence registry.
- **Probes and validation:** The workbook's conditional neutral probes and content-based hard stops are not implemented by the native question sequence. A respondent's self-selected role is not verified professional authority.
- **Screening brief:** A complete human-review brief is not generated automatically. Human review of the approved evidence must assign Stop / Measure / Prototype / Pilot; automated production approval is intentionally absent.
- **ROI integration:** No connected deterministic calculation engine was configured. The unchanged workbook remains the intended calculation source, and complete cost/evidence validation is still required before reporting a range.
- **Privacy verification:** Provider, payload, API-key mode, region, access, retention and applicable terms must be documented and checked against the founder's approval.
- **Release regression:** The final archived state and updated failure warning were verified; no claim is made that the archived bot is an operational release.

## Founder-triggered fallback procedure

This is a manual review procedure, not an automatic service or a claim that any analyst has already been provisioned.

1. Keep chatbot 4 archived and unassigned. Do not use the existing lead-generating or AI discovery route as a substitute for the financial pilot.
2. Conduct any further discovery under direct founder supervision, using only the approved data scope and an appropriately approved channel.
3. Stop immediately for sensitive information, disputed consent, suspected incidents, advice requests or financial/legal commitments. Arrange qualified human review without copying sensitive content.
4. If an analyst follow-up is needed, manually prepare one permitted question/answer with only the necessary category-level context. Mark unknowns and do not paste the transcript.
5. Verify the analyst's provider/model, access, storage, retention and processing terms before submission. Minimized wording is not proof of non-reconstructability or isolation.
6. Review the suggested follow-up before use. Record evidence provenance and calculate any justified ROI outside the language model with the approved workbook.

## Follow-up audit: existing Human Center route and Agent 5

The separate Human Center channel configuration records an always-enabled `/discovery-interview` rule assigned to Agent 5, whose configuration exposes a Create Leads topic and CRM Create/Get Lead tools. The handoff did not test that route's logged-out reachability, tool invocation, CRM effects, hard-stop behavior, human notification, or privacy boundary. This route is not the archived pilot chatbot 4. The audit-only instructions are in [`comet-audit-discovery-interview-agent5.md`](comet-audit-discovery-interview-agent5.md); no production interaction or CRM mutation is authorized by that task.

## Required decision before further work

The next step is to choose and authorize a runtime mechanism that can enforce the failed safety gates, prevent intake/tool/CRM side effects on trigger, and deliver an actionable human notification—not merely end the conversation—then verify the associated data handling and retest. If these behaviors cannot be enforced and evidenced, keep the pilot out of live use. No custom modules, external service connection, billing change, live agent activation or public publication was undertaken to bypass those requirements.

The configuration is therefore **blocked**, with a manual fallback documented and a saved, archived draft for inspection. The original Human Center bot and AI routes remain unchanged; no first partner session or pilot result is claimed.
