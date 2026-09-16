# Interview Playbook: Financial-Advisory Automation Discovery

## Interview objective

The interviews should identify **one recurring, valuable and controllable use case** for a supervised automation pilot—not design an all-purpose AI assistant during the meeting. The output should be sufficient to estimate preliminary ROI, determine minimum data requirements, identify regulatory and operational constraints, and secure a concrete next step.

The three participants provide different evidence:

| Participant | Primary evidence | Risk if omitted |
|---|---|---|
| Adviser or owner | Value, customer work, professional judgement, willingness to buy | A technically sound solution may solve an unimportant problem |
| Operational colleague | Actual sequence, variants, exceptions, rework and system use | The business case may rely on an idealized process |
| Compliance or data owner | Permitted data, controls, retention, approval and deployment boundaries | The proposed pilot may be unusable or expose the firm to unacceptable risk |

For financial firms, AI use can implicate supervision, communications, recordkeeping and fair-dealing obligations; the relevant regime depends on jurisdiction and firm status. The interview must therefore establish jurisdiction and regulatory perimeter before assuming that any particular rule applies.[^1][^2]

## Desired decisions

By the end of discovery, the team should be able to answer:

1. What single output, decision or recurring case should be tested first?
2. Who uses it, who approves it and what happens because of it?
3. What is the current volume, effort, delay, correction burden and economic consequence?
4. Which parts are deterministic preparation and which require professional judgement?
5. What data are minimally necessary, legally and contractually accessible, and technically available?
6. What must not become worse?
7. How would released capacity produce hard savings, contribution margin or owner utility?
8. What pilot evidence would justify purchase or expansion?

## Preparation checklist

### Before scheduling

- Confirm the firm’s country, regulated status, service types and approximate size.
- Ask the sponsor to nominate an adviser, an operational user and the person responsible for compliance, privacy, security or data.
- Schedule separate interviews where hierarchy could suppress honest answers; conduct a short joint synthesis afterward.
- Request permission before recording or using an AI notetaker.
- Explain that no client-identifying or sensitive information is required in the first discussion.
- Ask for one sanitized example of a recurring report, communication or preparation package if policy permits.

### Bring to the meeting

- A one-page hypothesis sheet.
- A blank “last case” map: trigger, inputs, actions, decisions, output, approval and outcome.
- A preliminary ROI worksheet using ranges.
- A data inventory template.
- A risk and control checklist.
- A candidate-use-case scorecard.
- A written statement that findings are provisional until validated against records or a pilot.

### Initial hypotheses

Use these only as hypotheses to test:

- Routine client communication or report preparation consumes meaningful adviser time.
- The firm has accepted templates that can constrain AI-generated drafts.
- The adviser will retain approval for customer-facing or decision-influencing output.
- Released time could support customer acquisition, additional paid work or personal utility.
- A low-access pilot using approved documents is more feasible than autonomous access to bank accounts or client systems.
- Execution logs may later support operational optimization, but this is not the first pilot promise.

## Interview structure

Use three conversations of approximately 25–35 minutes. If only one joint meeting is possible, allocate 15 minutes to the adviser, 15 minutes to operations, 15 minutes to compliance/data and 10 minutes to alignment.

### Opening script

> “The purpose today is not to sell a predefined AI product or request broad access. The aim is to understand one recent piece of work, estimate whether improving it would create meaningful value, and identify the minimum evidence and controls needed for a small pilot. Rough ranges are sufficient where exact figures are unavailable. No client names, account numbers or confidential content are needed today.”

Ask permission to take notes and explain how the notes will be stored and used. If recording, obtain explicit agreement and confirm retention and deletion expectations.

## Adviser interview

### Goal

Understand customer value, professional judgement, desired outcomes, commercial economics, adoption and willingness to proceed.

### Core questions

Ask these in order and stop probing when enough evidence has been obtained.

1. **“Which recurring client output or decision takes more of your personal time than it should?”**
2. **“Please walk through the most recent example—from the moment it started until the client received or used it.”**
3. **“What parts required your judgement, and what parts followed a repeatable pattern or template?”**
4. **“Approximately how often does this occur, and how much of your active time does a typical case require?”**
5. **“What usually causes delays, corrections or rework?”**
6. **“What is the consequence of a late or incorrect result—for the client and for the firm?”**
7. **“How do you charge for this work: fixed fee, hourly, retainer, assets-based fee or part of a wider engagement?”**
8. **“If the system released five hours per week, what would you actually do with them?”**
9. **“Which outputs would you permit AI to draft, and which decisions must always remain yours?”**
10. **“What evidence would make you comfortable paying for or expanding a pilot?”**

### Optional probes

Use only when an answer remains unclear:

- “Can you show the template or checklist without client information?”
- “Does another person check it before it goes out?”
- “How much of the first draft normally survives into the final version?”
- “Do you currently turn work away or delay it because of capacity?”
- “Would released time reduce cost, generate additional work, or mainly improve personal quality of life?”
- “What happened the last time an error reached a client?”
- “What would make you stop using the system?”

### Adviser evidence to capture

| Field | Capture |
|---|---|
| Candidate unit | One email, report, review package, reconciliation or decision |
| Volume | Low/base/high cases per week or month |
| Time | Active adviser time, not just elapsed duration |
| Judgement boundary | Preparation versus professional decision |
| Quality | Material correction, traceability, completeness and timeliness |
| Value mechanism | Cost avoided, additional margin, retention, risk or owner utility |
| Commercial model | How work produces revenue |
| Adoption | Existing tools, preferred interaction and trust boundary |
| Commitment | Sample, colleague access, pilot budget or next meeting |

## Operational colleague interview

### Goal

Reconstruct the actual work, including invisible coordination, exceptions, duplicate entry and correction. Do not ask the colleague merely to confirm the adviser’s account.

### Core questions

1. **“Please show or describe the last completed case of this type.”**
2. **“What event starts the work, and how do you know it is complete?”**
3. **“Which inputs arrive, from whom, in what formats, and how often are they incomplete?”**
4. **“Which systems, spreadsheets, inboxes or portals do you use?”**
5. **“What do you copy, reconcile, calculate, format or chase manually?”**
6. **“Where do cases wait, return for correction or require escalation?”**
7. **“What are the common case variants and exceptions?”**
8. **“Who reviews each stage, and what do reviewers usually change?”**
9. **“Which templates, rules or examples define an acceptable result?”**
10. **“If one step were removed tomorrow, which would save the most effort without increasing risk?”**

### Observation prompts

If screen sharing is permitted, ask the colleague to demonstrate a sanitized or fabricated case while narrating actions. Record counts rather than impressions:

- Number of source systems.
- Number of handoffs.
- Number of manual transfers.
- Active minutes by role.
- Waiting time.
- First-pass acceptance.
- Corrections and reasons.
- Frequency of missing inputs.
- Percentage of standard versus exceptional cases.

Do not collect real credentials or customer data during discovery. Where evidence is needed, ask for redacted screenshots, field lists, blank templates or metadata first.

### Operational reality checks

Ask the same quantitative questions posed to the adviser without revealing the adviser’s estimates. Differences are useful evidence, not a problem to smooth over. Mark each disagreement for validation from system logs, timesheets, calendars or a short measurement exercise.

## Compliance/data interview

### Goal

Determine whether the proposed use is permissible, what controls are mandatory, who owns approval, and what minimum data architecture can support a pilot.

### Opening script

> “No assumption is being made that production client data or autonomous action is required. The objective is to define what can be tested safely, what evidence is needed, and which approvals apply.”

### Firm and jurisdiction

1. **“Which legal entities, jurisdictions and regulated activities would this use case touch?”**
2. **“Which regulator, professional code, contractual commitment or internal policy governs the output?”**
3. **“Is the output preparation, customer communication, advice, a recommendation, a record, or part of supervision?”**
4. **“Who has authority to approve this use case and production release?”**

Existing financial-services obligations generally remain applicable when AI is used rather than creating a broad technology exemption; FINRA, for example, specifically highlights supervision, communications, recordkeeping and fair dealing. This source is directly relevant only if the firm falls within the corresponding US regulatory perimeter.[^2]

### Data and authorization

5. **“What data categories are required, and which contain personal, financial, confidential or specially protected information?”**
6. **“Who is the controller or owner, and what legal, contractual or client authorization permits each use?”**
7. **“Can the pilot use synthetic, anonymized, pseudonymized, redacted or historical data instead?”**
8. **“Where may data be processed and stored, and are there location or transfer restrictions?”**
9. **“May vendors retain prompts or outputs, use them for model training, or involve subprocessors?”**
10. **“What retention and secure-deletion rules apply to inputs, outputs, prompts, logs and recordings?”**

Data minimization requires personal data to be adequate, relevant and limited to what is necessary for the stated purpose; the necessity assessment should also consider whether a less intrusive route can achieve the same purpose. Apply the client’s actual jurisdiction and counsel’s interpretation rather than assuming that EU rules apply universally.[^3][^4]

### Controls and accountability

11. **“Which outputs require human review, and what qualification must the reviewer hold?”**
12. **“Must AI-assisted communications or chat sessions be archived and supervised?”**
13. **“What source traceability, calculation evidence and audit trail are required?”**
14. **“What actions must the system never take without explicit approval?”**
15. **“How should incorrect output, unauthorized access or data leakage be escalated?”**
16. **“What testing and recurring review are required before and after deployment?”**
17. **“Which approved tools already exist, and which tools or personal accounts are prohibited?”**
18. **“What vendor due diligence, security assessment, contract or impact assessment is required?”**

NIST’s AI RMF calls for human-oversight processes to be defined, assessed and documented according to organizational policies. FINRA’s 2026 materials state that relevant firms should ensure AI-assisted customer communications meet applicable requirements and that certain business communications and chat sessions are retained and supervised.[^5][^1]

### Minimum viable data map

Complete this table during or immediately after the interview:

| Data element | Purpose | Source | Sensitivity | Permission | Storage | Retention | Human access | AI access |
|---|---|---|---|---|---|---|---|---|
| Example: transaction category | Draft report table | Approved export | Financial/personal | To confirm | Approved region | To confirm | Adviser | Read-only pilot |

If purpose, permission or owner is unknown, mark the element **blocked** rather than assuming access.

## Joint synthesis

Bring the three participants together for 20–30 minutes. Present findings as hypotheses and differences, not conclusions.

### Synthesis script

> “The current hypothesis is that [specific output] occurs [range] times per month, consumes [range] hours of active work, and creates [specific pain]. The proposed pilot would automate only [bounded preparation steps], retain [named human approvals], and exclude [prohibited actions]. Value would be measured through [metrics]. The main unknowns are [items]. Is this an accurate representation?”

### Resolve five points

- One pilot unit and eligible case type.
- Named business owner and human reviewer.
- Baseline measurement method.
- Minimum permitted data and environment.
- Success, guardrail and stop criteria.

Do not force consensus on uncertain numbers. Assign an owner and validation action to each unresolved assumption.

## Preliminary ROI capture

Use ranges during interviews rather than asking for accounting precision.

### Input sheet

| Input | Low | Base | High | Evidence type | Owner |
|---|---:|---:|---:|---|---|
| Eligible cases per month |  |  |  | Reported/logged/assumed |  |
| Current active hours per case |  |  |  |  |  |
| Future active hours per accepted case |  |  |  | Pilot assumption |  |
| Loaded cost by role |  |  |  |  |  |
| Material correction rate |  |  |  |  |  |
| Additional demand available |  |  |  |  |  |
| Capacity realization factor |  |  |  |  |  |
| Implementation cost |  |  |  | Provider estimate |  |
| Recurring and review cost |  |  |  |  |  |

### Value categories

- **Hard value:** contractor, overtime, payroll or planned-hire cost actually avoided.
- **Growth value:** attributable incremental contribution margin generated from released capacity.
- **Risk value:** measured change in expected loss, not maximum possible loss.
- **Owner utility:** discretionary time released; report separately from financial ROI.

The interview produces **potential ROI**, not proof. Each input should be labeled observed, reported, benchmarked or assumed and later replaced with measured pilot data.

## Use-case scorecard

Score each candidate from 1 to 5 and record the evidence behind the score.

| Criterion | Weight | Meaning |
|---|---:|---|
| Material customer/business value | 20% | Economic, risk or owner outcome matters |
| Frequency and volume | 10% | Repeats enough to justify setup |
| Standardization | 10% | Stable inputs, rules and accepted output |
| Data readiness | 15% | Accessible, lawful and sufficiently reliable |
| Reviewability | 10% | Human can efficiently verify output |
| Technical feasibility | 10% | Integrations and model capability are practical |
| Adoption probability | 10% | Users will incorporate it into work |
| Realization probability | 10% | Released capacity has a credible use |
| Risk manageability | 5% | Residual risk can be accepted and controlled |

A high total score does not override a compliance veto or an unacceptable failure consequence.

## Interview techniques

### Do

- Ask about the last real occurrence before asking for general opinions.
- Request ranges when exact figures are unavailable.
- Separate active touch time from waiting time.
- Ask what the client would stop, start or do more of if time were released.
- Repeat the same factual question across roles independently.
- Distinguish preparation from judgement and recommendation.
- Read back the hypothesis and invite correction.
- End with a small, concrete commitment.

### Avoid

- “Would an AI assistant be useful?”
- “How much time could AI save?”
- “Can access to all the data be provided?”
- “Which boring tasks should be automated?”
- “Would you pay for this?” without a defined use and price.
- Explaining the proposed solution before understanding the last case.
- Treating a desired future behavior as evidence of current demand.
- Collecting identifiable customer examples by email before approval.

## Red flags

Pause or narrow the engagement if:

- Nobody owns the outcome or approval.
- The use case depends on unrestricted access to bank credentials.
- No competent human can verify outputs.
- The firm expects autonomous investment or tax advice in the first release.
- Client data would enter an unapproved personal AI account.
- The economic case counts all released time at the billing rate despite no unmet demand.
- The process has very low volume or no stable output definition.
- The adviser and operator describe materially different processes but no records can validate them.
- The solution cannot produce required records, source lineage or review evidence.
- The client wants certainty before permitting any measurement.

## Closing script

> “The next step is not broad implementation. The team will summarize the current case, list assumptions and uncertainties, and propose the smallest test that can validate value without unnecessary data or autonomy. The summary will distinguish financial return from personal time value and will specify who reviews every client-facing output. Approval of that summary, one sanitized example and access to the named owners will be the decision point for a pilot proposal.”

## Post-interview deliverable

Within one working day, produce:

- Confirmed facts.
- Reported estimates and ranges.
- Assumptions requiring validation.
- Contradictions between interviewees.
- One recommended use case and one alternative.
- Data and control blockers.
- Preliminary low/base/high ROI logic.
- Pilot objective, Key Results and guardrails.
- Named owners and next actions.

Do not present a confident ROI percentage if its dominant inputs remain assumptions. Present the range, identify the two or three assumptions driving it, and make measurement of those assumptions the purpose of the pilot.

---

## References

1. [2026-annual-regulatory-oversight-report.pdf](https://www.finra.org/sites/default/files/2025-12/2026-annual-regulatory-oversight-report.pdf)

2. [GenAI: Continuing and Emerging Trends | FINRA.org](https://www.finra.org/rules-guidance/guidance/reports/2026-finra-annual-regulatory-oversight-report/gen-ai) - The GenAI topic of the 2026 FINRA Annual Regulatory Oversight Report informs member firms’ complianc...

3. [[PDF] Guidelines 03/2026 on web scraping in the context of generative AI](https://www.edpb.europa.eu/system/files/2026-07/edpb_guidelines_2020603_webscraping_v1_en_0.pdf)

4. [Opinion 28/2024 on certain data protection aspects related to ...](https://www.edpb.europa.eu/system/files/2024-12/edpb_opinion_202428_ai-models_en.pdf) - Purpose limitation and data minimisation principles (Article 5(1)(b) ... generation of personal data...

5. [Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf)

