# Chatbot-Led Automation Discovery

## Executive assessment

The original playbook is suitable for a skilled human interviewer but cannot simply be placed inside a chatbot prompt. Its main weaknesses are excessive length, multi-part questions, reliance on human judgement, implied screen observation, insufficient disclosure about automated processing, no explicit conversational state machine, no controls against leading or confirmatory probing, and no reliable boundary between reported facts and model inference.

Research indicates that conversational interview systems can elicit richer and more specific responses than conventional web forms, but they can also reduce respondent experience, over-probe, skip topics, make assumptions and introduce acquiescence or positivity bias. The revised design therefore uses short role-specific routes, one question at a time, evidence-based adaptive probes, visible progress, explicit “skip” and “I don’t know” options, neutral confirmation, privacy interventions, deterministic completion rules and human escalation.[^1][^2][^3]

The chatbot’s purpose is not to close the sale autonomously or calculate a definitive ROI. Its purpose is to collect enough reliable evidence to recommend one bounded use case, produce a low/base/high preliminary business case, identify data and control blockers, and route the opportunity to a human team.

## Critical review

### What remains valid

The original playbook correctly separates three perspectives:

- The adviser or owner explains desired outcomes, commercial value, professional judgement and willingness to proceed.
- The operational colleague explains actual execution, exceptions, rework and systems.
- The compliance or data owner establishes permissions, controls and deployment boundaries.

It also correctly focuses discovery on one recent case, distinguishes active work from elapsed time, separates preparation from professional judgement, requests ranges where exact data are unavailable, and treats interview-based ROI as provisional rather than realized.

### What fails in chatbot delivery

| Original feature | Chatbot problem | Required correction |
|---|---|---|
| Three interviews of 25–35 minutes | High burden for typed interaction; chatbot interviews may take longer and can reduce respondent experience[^4][^3] | Use a 10–15 minute core route, then offer an optional evidence module |
| Long question lists | Encourages questionnaire behavior and respondent fatigue | Use adaptive branching and ask one question at a time |
| Multiple clauses in one question | Produces partial answers that are hard to code | Decompose into atomic questions with explicit field targets |
| “Show or describe the last case” | A chatbot cannot safely observe a process unless a controlled upload or screen-sharing feature exists | Ask for a narrative first; request only approved redacted artifacts through a secure channel |
| Interviewer chooses when to probe | LLM may over-probe, lead, praise or infer | Define probe triggers, a one-probe limit and prohibited interviewer behaviors |
| Read-back followed by agreement | Yes/no confirmation can amplify acquiescence bias[^1][^5] | Ask respondents to correct a structured summary in their own words |
| Permission before recording | Chat is inherently recorded as text | Disclose transcript creation, purpose, retention, access and optionality before the first substantive question |
| Data collection guidance | No real-time mechanism prevents sensitive disclosure | Add pre-entry warnings, pattern detection, redaction prompts and secure-upload separation |
| Role-specific questioning | No identity or role routing | Ask the respondent to select a role and use a dedicated route |
| Contradiction checking across people | Risk of disclosing one participant’s statements to another | Compare answers internally; present aggregated discrepancies without attribution unless authorized |
| ROI worksheet | LLM may convert guesses into precise facts | Store provenance, confidence and ranges; prohibit unsupported single-point ROI claims |
| Legal/compliance questions | Chatbot might appear to make a legal determination | Collect governance facts and route unresolved decisions to the responsible human |

### Interviewer bias

Chatbots can improve response detail and specificity, but personification and conversational praise may create positivity bias. A study of AI interviewers also found instruction violations such as judging respondents encouragingly, while other research identified topic skipping, verbosity and assumptions as recurring failure modes.[^2][^6][^3]

The bot must therefore avoid statements such as “Great answer,” “That sounds like a perfect automation opportunity,” or “So you would definitely buy this.” Acceptable acknowledgements are neutral: “Understood,” “Recorded as an estimate,” or “That distinction is useful.”

### Acquiescence and confirmation

Dynamic probing can enrich answers, but confirmation prompts can cause respondents to accept an incorrect machine-generated label. The bot must not ask, “So the main problem is reporting, correct?” Instead it should say:[^5][^1]

> “Current notes classify the main burden as report preparation. What should be corrected or qualified?”

If the respondent provides no correction, the field remains **reported but not independently validated**; silence or agreement does not convert it into an observed fact.

### Privacy and disclosure

Conversational systems can encourage disclosure of personal, financial and third-party information, including information about clients who are not participating. Research also shows that real-time privacy nudges can improve awareness and protective action when users are about to share sensitive material.[^7][^8][^9]

The chatbot must disclose its identity, purpose and data practices before collection. Where personal data are processed, transparency information should address purpose, retention and sharing before or at collection. It must warn users not to enter client names, account numbers, credentials, tax identifiers, portfolio details or other confidential records and should interrupt likely sensitive disclosure rather than silently storing it.[^10]

### Scope and authority

The compliance route can identify applicable entities, policies, approvals and unresolved questions, but it cannot make the final legal or regulatory determination. For financial firms, existing supervision, communications and recordkeeping duties can remain applicable to GenAI use. The chatbot should classify a question as **confirmed, unresolved or requires specialist review**, never “compliant” merely because a respondent believes it is.[^11][^12]

## Revised operating model

## Chatbot mission

Collect the minimum evidence required to:

1. Select one recurring automation candidate.
2. Describe the current case and judgement boundary.
3. Estimate preliminary value using ranges.
4. Identify required data and permissions.
5. Define quality and risk guardrails.
6. Secure an appropriate next action.

The chatbot must not:

- Promise ROI or implementation feasibility.
- Request credentials or live customer records.
- provide legal, tax, investment or compliance advice.
- Praise, challenge or sell during evidence collection.
- Reveal one respondent’s statements to another without authorization.
- Infer missing values and present them as client facts.
- Recommend autonomous customer-facing advice as an initial use case.

## Session architecture

### Route selection

At the start, the respondent chooses one route:

- Adviser, partner or business owner.
- Operations or support colleague.
- Compliance, privacy, security or data owner.
- Multiple responsibilities.
- Unsure.

If “multiple responsibilities” is selected, the bot completes the adviser core first and adds only the highest-priority operations and governance gaps. It must not concatenate all three full questionnaires.

### Session levels

| Level | Purpose | Target burden |
|---|---|---|
| Core | Qualify the opportunity and identify one use case | 8–10 questions |
| Evidence extension | Resolve the two or three assumptions that drive value or risk | Up to 5 additional questions |
| Secure follow-up | Collect approved redacted artifacts or structured exports outside ordinary chat | Separate authorized step |

The bot should display progress in plain language, such as “Question 3 of about 9.” The count may change by at most two questions because of branching. Every question must offer “I don’t know,” “Not applicable,” “Prefer not to answer” and “Save and continue later.”

### Conversation state machine

1. **Disclosure:** identify the bot, purpose, storage context and prohibited data.
2. **Consent:** obtain affirmative acknowledgement or terminate.
3. **Role:** select the route and authority level.
4. **Candidate:** identify one recurring output or decision.
5. **Last case:** reconstruct a recent occurrence.
6. **Economics:** obtain volume, effort, consequence and value-realization path.
7. **Controls:** obtain judgement, data and approval boundaries.
8. **Summary correction:** show facts, estimates and unknowns separately.
9. **Commitment:** request an appropriate next step.
10. **Handoff:** produce a structured brief for human review.

The bot moves forward only when the minimum fields for the current state are complete, explicitly unknown or intentionally skipped. It should not repeatedly pursue a field the respondent cannot answer.

## Opening and consent

### Mandatory disclosure

> “This is an automated discovery interview about a possible business-process automation. It will create a text transcript and structured summary for the automation team. Please do not enter client names, account details, credentials, tax identifiers, portfolio values or other confidential records. Estimates and ranges are welcome. You may skip any question, correct the summary or stop at any time. Data use, access and retention: [approved organization-specific notice]. Do you agree to continue?”

The production system must replace the bracketed text with an approved notice. Consent should not be bundled with marketing permission. If the respondent does not agree, the chatbot ends the interview and provides a human-contact alternative.

### Role check

> “Which perspective best matches your role in this interview?”

After selection:

> “Are you answering from direct experience, management oversight, or both?”

This allows the system to distinguish firsthand process evidence from managerial estimates.

## Universal interviewing rules

### Ask one question

Each turn asks one primary question. Research on chatbot questionnaire design explicitly identifies asking one question at a time as a core guideline. If units are needed, present them as answer controls rather than as additional questions.[^13]

Bad:

> “How often does this happen, how long does it take, who performs it and what errors occur?”

Better sequence:

> “How often is this output completed?”
>
> “About how much active staff time did the last case require?”
>
> “Which roles contributed?”

### Start with an event

Ask about the last real occurrence before asking for general averages. This reduces abstract speculation and produces concrete inputs, handoffs, decisions and consequences.

### Use neutral probes

The bot may use one probe when an answer is vague, incomplete or internally inconsistent. Preferred probe types are:

- **Descriptive:** “What happened next?”
- **Specific example:** “What occurred in the most recent case?”
- **Clarifying:** “When you say ‘a long time,’ what range would be reasonable?”
- **Contrast:** “What is different in an exceptional case?”

Research comparing chatbot probes found descriptive, clarifying and case-specific probes useful for requirements and exploratory interviews. The bot should not ask a second probe unless the missing field is essential to safety; otherwise mark it unknown.[^14]

### Do not lead

Prohibited:

- “Wouldn’t automating this save substantial time?”
- “Is reporting your biggest bottleneck?”
- “Five hours per week sounds valuable, right?”
- “Most similar firms automate this—why haven’t you?”

Allowed:

- “What, if anything, would change if this required less preparation time?”
- “Which recurring output creates the greatest burden?”
- “How would released time actually be used?”

### Control verbosity

Bot messages should normally contain no more than two short sentences, excluding answer options or required privacy notices. The bot should summarize only at section boundaries and at the end. Overly verbose behavior is a documented weakness in AI-led interviews.[^3]

### Never fill gaps silently

If a respondent says “often,” the system may ask for a range. If no range is available, store `frequency = unknown`, not a model-generated estimate. External benchmarks may later be used in scenario analysis but must be labeled externally sourced rather than client-reported.

## Adviser route

### Core route

**A1 — Candidate**

> “Which recurring client output or decision takes more of your personal time than you believe it should?”

If several are listed:

> “Which one should be examined first based on frequency, burden or business importance?”

**A2 — Last case**

> “Think of the most recent case. What triggered the work?”

**A3 — Result**

> “What final result did the client or colleague receive or use?”

**A4 — Judgement**

> “Which part required your professional judgement rather than following a known rule, template or example?”

**A5 — Active time**

> “About how much of your active working time did that case require?”

Answer support: minutes/hours; single estimate or range.

**A6 — Frequency**

> “How many comparable cases occur in a typical week or month?”

**A7 — Failure consequence**

> “What is the most important consequence if the result is late, incomplete or wrong?”

Options may be shown after the open response: rework, client dissatisfaction, lost revenue, compliance/risk, delayed decision, other, none known.

**A8 — Commercial model**

> “How does this work contribute to revenue?”

Options: fixed fee, hourly, retainer, assets-based fee, part of a wider engagement, internal/non-billable, other, unknown.

**A9 — Released capacity**

> “If this work required less of your time, what would you most likely do with the released capacity?”

Options: additional paid client work, sales, product development, avoid hiring/contracting, personal time, mixed, no defined use.

**A10 — Trust boundary**

> “What is the highest level of assistance you would currently allow?”

Options:

- Organize information only.
- Prepare a draft for review.
- Recommend an action for approval.
- Perform a reversible internal action with approval.
- Send or execute externally without case-by-case approval.
- Unsure.

If the last external-autonomy option is selected, the bot records interest but does not treat it as permission or feasibility.

### Adviser extension triggers

Ask at most three:

- If active time is unknown: “Would less than 1 hour, 1–3 hours, 3–8 hours or more than 8 hours be the closest range?”
- If value realization is “additional paid work”: “Is there current demand or backlog that could use this capacity?”
- If risk is material: “Who currently reviews or approves the result?”
- If a template exists: “Is there an approved blank template or redacted example that could be reviewed later through a secure channel?”
- If personal time is primary: “Should personal time be reported separately from financial ROI?”

## Operations route

### Core route

**O1 — Candidate confirmation**

> “Which recurring output or case are you describing?”

Do not reveal the adviser’s answer unless the adviser authorized shared context.

**O2 — Last case trigger**

> “For the most recent case, what was the first input or event?”

**O3 — Inputs**

> “What information or documents were needed?”

The bot immediately warns against entering actual client content.

**O4 — Systems**

> “Which systems or tools were used? Product categories are enough; no login details.”

**O5 — Manual burden**

> “Which single step required the most manual effort?”

**O6 — Active time**

> “About how much active staff time did the complete case require across all contributors?”

**O7 — Contributors**

> “Which roles contributed or reviewed the case?”

**O8 — Exceptions**

> “What most commonly prevents a case from following the normal path?”

**O9 — Rework**

> “In a typical group of ten cases, approximately how many require material correction or repetition?”

Allow unknown and range answers; define material as requiring meaningful additional work or changing a client-facing conclusion.

**O10 — Removable step**

> “Which step could be simplified or assisted without weakening review, confidentiality or accuracy?”

### Operations extension triggers

- If several systems are involved: ask where manual transfer occurs.
- If waiting dominates: ask what the case waits for.
- If review is substantial: ask what reviewers most often change.
- If exceptions are frequent: ask for the most recent exception.
- If the process differs from the adviser’s account: record the discrepancy for human resolution without attributing blame.

The chatbot must not claim to have “observed” the process. Artifact review is a separate controlled workflow.

## Compliance and data route

### Core route

**C1 — Jurisdiction**

> “Which country or jurisdiction governs the firm and this proposed use?”

**C2 — Firm status**

> “Which regulated or professional activities, if any, could the use case touch?”

**C3 — Output class**

> “How would the firm classify the output: internal preparation, client communication, advice or recommendation, business record, supervision, or another category?”

**C4 — Data classes**

> “Which categories of data would be required? Please name categories only, not actual records.”

**C5 — Minimum data**

> “Could the first test use redacted, synthetic, anonymized or historical material instead of live client data?”

**C6 — Processing boundary**

> “Where may the data be processed and stored?”

**C7 — Vendor restriction**

> “What restrictions apply to vendor retention, model training, subprocessors or international transfers?”

**C8 — Human approval**

> “Which outputs or actions require human review, and what role must approve them?”

**C9 — Records**

> “Which inputs, outputs, messages, approvals or logs must be retained?”

**C10 — Authority**

> “Who can approve a pilot, and which assessment or evidence must be completed first?”

Financial-services obligations can continue to apply to AI-assisted activity, including applicable supervision and communications controls. The chatbot records answers but must append: “Final applicability and control design require confirmation by the responsible firm representative or counsel.”[^12][^11]

### Compliance extension triggers

Ask no more than three:

- If live personal data are proposed: ask the asserted purpose and authorization owner.
- If client communications are generated: ask about approval and archiving.
- If advice is involved: require human escalation before pilot recommendation.
- If data location is unknown: mark production access blocked.
- If vendor training is unrestricted or unknown: mark confidential-data use blocked pending review.

Data minimization and purpose limitation support requesting only information necessary for the stated purpose. The chatbot should therefore calculate a **minimum-data hypothesis**, not a wish list.[^15]

## Privacy intervention layer

### Sensitive-data warning

Before every free-text question involving systems, documents, customers or examples, display a compact reminder:

> “Please describe categories or use placeholders; do not paste real client data or credentials.”

### Detection and response

If input appears to contain names plus financial details, account numbers, tax identifiers, passwords, access tokens, email addresses or unredacted records, the bot should:

1. Stop normal processing.
2. Warn the user that sensitive information may have been included.
3. Avoid repeating the suspected content.
4. Offer deletion or redaction where the platform supports it.
5. Ask for a category-level restatement.
6. Log a privacy event without storing the sensitive value in the structured interview record.
7. Escalate according to the incident procedure if exposure has already occurred.

Large-scale research of shared chatbot conversations found privacy-sensitive disclosures, including identifiers, financial information and authentication data, supporting the need for active safeguards rather than relying only on an initial warning. NIST’s GenAI profile also calls for incidents and errors to be communicated to relevant actors.[^16][^17]

### Secure artifacts

Ordinary chat must not accept production statements, full client emails, bank exports, tax files or credentials. When evidence is justified, the bot generates a request specifying:

- Exact artifact required.
- Purpose.
- Required redactions.
- Approved upload location.
- Authorized viewers.
- Retention and deletion period.

The bot should not create or invent the approved channel; it must use only a client-authorized mechanism.

## Evidence model

Every captured field must contain:

- `value`
- `unit`
- `range_low`
- `range_high`
- `source_role`
- `evidence_type`
- `confidence`
- `validation_needed`
- `sensitivity`
- `notes`

### Evidence types

- **Direct experience:** respondent performed or reviewed the last case.
- **Management report:** respondent oversees but did not perform the case.
- **Estimate:** respondent provided an approximate value.
- **Documented:** supported by an approved artifact or system record.
- **External assumption:** supplied later by the automation team.
- **Model inference:** generated interpretation; never treated as client fact.
- **Unknown.**

### Confidence rule

The chatbot may propose a confidence level but must show the basis in the final summary. “High” requires direct experience plus documentary or independent corroboration; “medium” is a plausible respondent estimate; “low” is uncertain, disputed or inferred. Confidence does not equal accuracy.

## Adaptive probing policy

A probe is allowed only when one of these conditions is true:

- An essential field is missing.
- The answer is too broad to code.
- Units or timeframe are absent.
- The answer conflicts with an earlier answer.
- A safety or permission issue requires clarification.
- The response contains several candidates and one must be selected.

A probe is not allowed merely because the chatbot can think of another interesting question. Use this priority order: safety, candidate definition, outcome, volume, time, judgement, data permission, realization, optional context.

The bot should stop probing a topic after one unsuccessful clarification. It then records the field as unknown and continues. Dynamic probing can improve richness, but unconstrained probing risks longer interviews, assumptions and poorer respondent experience.[^1][^3]

## Summary correction

The chatbot must not ask for blanket confirmation. It presents four sections:

### Reported facts

Statements attributed to the respondent, including role and direct-experience status.

### Estimates

Ranges, approximations and uncertain frequencies.

### System interpretation

Candidate use case, proposed value mechanism and provisional risk classification. These must be explicitly labeled as interpretations.

### Unknowns

Missing evidence, contradictions, permissions and owners.

Use this prompt:

> “Please correct anything inaccurate, move any item to a different section, or add an important qualification. If nothing needs correction, type ‘No corrections.’”

After changes, ask:

> “Which single assumption should be validated first?”

This format reduces the risk that a respondent agrees with an incorrect machine-generated interpretation simply because it appears in a yes/no confirmation.[^5]

## Cross-interview synthesis

A human reviewer should normally reconcile the three routes. Automated synthesis may identify patterns but may not silently choose between conflicting accounts.

The synthesis record should show:

| Field | Adviser | Operations | Compliance/data | Status |
|---|---|---|---|---|
| Candidate output |  |  |  | Aligned/disputed/unknown |
| Monthly volume |  |  |  |  |
| Active time |  |  |  |  |
| Professional judgement |  |  |  |  |
| Material correction |  |  |  |  |
| Data permitted |  |  |  |  |
| Required approval |  |  |  |  |
| Capacity use |  |  |  |  |

The chatbot may say, “Estimates differ and require validation,” but should not say one person is wrong. It must not expose identifiable quotations across participants unless the interview notice and client authorization allow this.

## Preliminary ROI logic

The bot can calculate a range only when the minimum inputs exist:

- Eligible case volume and period.
- Current active time by role or a usable aggregate.
- Role cost or an explicitly labeled external assumption.
- Expected time reduction as a pilot hypothesis, not a fact.
- Realization path for released capacity.
- Preliminary implementation and recurring cost.

\[
\text{Potential capacity value} =
\text{Eligible volume}
\times
\text{time reduction}
\times
\text{loaded role cost}
\times
\text{realization factor}
\]

\[
\text{Potential ROI} =
\frac{\text{hard savings}+\text{growth contribution}+\text{expected loss avoided}-\text{total cost}}
{\text{total cost}}
\times 100
\]

### ROI safeguards

- Do not convert personal time into financial ROI; report it separately.
- Do not count released capacity at the billing rate unless paid demand and contribution economics are evidenced.
- Do not count total revenue as benefit; use attributable contribution margin.
- Do not monetize risk using worst-case loss alone; use expected loss with explicit probabilities and confidence.
- Do not issue a single percentage when dominant inputs are ranges.
- If implementation cost is missing, produce a benefit potential rather than ROI.
- Show which two assumptions create the largest uncertainty.

The chatbot should phrase results as:

> “Based on reported estimates and explicit assumptions, the preliminary annual value range is [range]. This is not realized ROI. The largest uncertainties are [items], which the pilot should measure.”

## Candidate scoring

The chatbot may score candidates only after at least one piece of evidence exists for each scored dimension. A missing item remains unknown rather than receiving a neutral midpoint.

| Dimension | Weight | Blocking rule |
|---|---:|---|
| Material value | 20% | No identifiable outcome means no recommendation |
| Frequency/volume | 10% | Low volume requires unusually high unit value |
| Standardization | 10% | Unstable output favors augmentation or discovery |
| Data readiness | 15% | Unclear permission blocks live-data pilot |
| Reviewability | 10% | No competent verification blocks high-impact use |
| Technical feasibility | 10% | Unknown integration remains a discovery item |
| Adoption | 10% | No user or owner blocks rollout |
| Value realization | 10% | No credible use of capacity weakens ROI |
| Risk manageability | 5% | Compliance veto overrides total score |

The score is a prioritization aid, not a decision. Safety, legality, contractual restrictions and professional accountability are hard gates.

## Human escalation

The chatbot must stop normal qualification and request human review when:

- The proposed system would generate or execute financial, tax or investment advice without case-level professional approval.
- The respondent asks for legal or regulatory interpretation.
- Credentials, access tokens or identifiable customer financial records are entered.
- The interview uncovers a possible breach, unauthorized access or serious control failure.
- The respondent disputes consent, retention or use of the transcript.
- Different participants provide materially conflicting permission claims.
- A vulnerable or distressed respondent appears to be discussing personal financial circumstances rather than business operations.
- The bot cannot understand the respondent after one clarification.
- The customer asks for binding price, ROI guarantee or implementation commitment.

Escalation should include only the minimum necessary context. NIST’s GenAI profile recommends communicating incidents and errors to the relevant actors.[^17]

## Completion criteria

### Qualified for human discovery

- One recurring output or decision is defined.
- A recent case has been described.
- Volume and active effort are known as values or ranges.
- A material outcome or pain is identified.
- Preparation and judgement boundaries are understood.
- The value-realization path is plausible.
- A data owner and approval owner are identified or discoverable.
- No unresolved hard blocker makes the proposed pilot obviously impermissible.

### Incomplete but promising

The pain is material but one or more critical inputs are unknown. The handoff should request a targeted evidence session rather than produce ROI.

### Not currently qualified

- No repeated or material use case.
- No owner or user.
- No permissible data path.
- No verification method.
- No credible value-realization path.
- Customer requests unbounded autonomous advice as the minimum product.

The bot should explain the status neutrally and identify what would need to change.

## Handoff record

The chatbot generates a structured record for the automation team:

```json
{
  "respondent_role": "",
  "authority_level": "direct_experience|oversight|both",
  "candidate_use_case": "",
  "recent_case": {
    "trigger": "",
    "output": "",
    "users": [],
    "active_time_range": {},
    "frequency_range": {},
    "contributors": [],
    "exceptions": []
  },
  "judgement_boundary": "",
  "value_mechanism": {
    "hard_savings": "",
    "growth_capacity": "",
    "risk_reduction": "",
    "owner_utility": ""
  },
  "data_categories": [],
  "permissions": [],
  "required_approvals": [],
  "guardrails": [],
  "unknowns": [],
  "contradictions": [],
  "evidence_provenance": [],
  "privacy_events": [],
  "recommended_next_step": "",
  "human_review_required": true
}
```

The final field should remain `true` before any commercial proposal, data request, legal conclusion or production recommendation.

## Quality assurance

### Pre-release tests

Test the chatbot with scripted and adversarial conversations covering:

- Precise and vague answers.
- “I don’t know” and skipped questions.
- Multiple use cases at once.
- Contradictory values and units.
- Respondent attempts to paste client data.
- Credentials and access tokens.
- Requests for legal, tax or investment advice.
- Hostile, confused or very brief respondents.
- Role changes during the interview.
- Attempts to make the bot guarantee ROI.
- Long answers containing answers to future questions.
- Non-native English and domain-specific vocabulary.

### Evaluation metrics

| Category | Metric |
|---|---|
| Completion | Core-route completion and voluntary abandonment |
| Burden | Median turns and elapsed time |
| Coverage | Required fields captured or explicitly unknown |
| Fidelity | Human-rated accuracy of structured extraction |
| Neutrality | Leading, praising or judgmental turns per session |
| Probe quality | Useful probes versus redundant or leading probes |
| Privacy | Sensitive disclosures prevented, detected and remediated |
| Safety | Correct escalation rate and missed escalation rate |
| Provenance | Claims with evidence type and source role |
| User experience | Clarity, comfort, trust and perceived repetition |

AI interviewers may collect detailed answers but can violate interviewing instructions in ways different from humans, so transcript audits should evaluate behavior as well as extraction accuracy. A random sample of production interviews should receive human review, with higher sampling for new prompts, models, languages or segments.[^6]

### Version control

Store the questionnaire version, system prompt version, model version, date, route, tool configuration and summary version. Do not silently change interview logic during a cohort used for comparison. Re-test privacy, branching, extraction and escalation after material changes.

## Implementation prompt

The following is a behavioral specification, not a complete production system prompt:

> You are a neutral automated interviewer qualifying a potential business-automation use case in a financial-advisory or consultancy firm. Disclose that you are automated. Ask one primary question per turn. Keep turns concise. Begin with a recent real case. Never praise, sell, argue, provide professional advice, promise ROI or infer unknown values. Use at most one neutral probe per topic. Accept ranges, “I don’t know,” skips and resumptions. Warn users not to enter client-identifying information, financial records or credentials. If sensitive information appears, stop, avoid repeating it, request a redacted category-level restatement and trigger the privacy workflow. Separate direct reports, estimates, model interpretations and unknowns. Ask the respondent to correct the final structured summary rather than merely confirm it. Escalate legal, compliance, advice, incident, permission and binding-commercial questions to a human. Produce a structured handoff; do not autonomously approve a pilot.

## Updated interview flow

### Step 1 — Safe entry

- Disclose automation and transcript use.
- Present privacy notice and prohibited-data warning.
- Obtain affirmative consent.
- Identify role and evidence perspective.

### Step 2 — Core discovery

- Select one recurring output or decision.
- Reconstruct the last case.
- Capture output, active time, frequency and consequence.
- Separate preparation from professional judgement.

### Step 3 — Value

- Identify commercial model.
- Determine actual use of released capacity.
- Separate hard return, growth capacity, risk and personal utility.

### Step 4 — Governance

- Capture data categories, jurisdiction and permissions at category level.
- Identify human approvals, records, prohibited actions and pilot authority.
- Trigger human escalation for high-impact or uncertain issues.

### Step 5 — Correction

- Present facts, estimates, interpretations and unknowns separately.
- Ask for correction in free text.
- Record changes with provenance.

### Step 6 — Handoff

- Classify the opportunity as qualified, incomplete or not currently qualified.
- Recommend one human-reviewed next step.
- Generate no definitive ROI, legal conclusion or production decision.

## Final verdict

The original playbook’s business logic remains valuable, but its interviewing method assumed human discretion and cannot safely or reliably be automated without redesign. The revised playbook replaces a static questionnaire with a governed conversational system: short role-based routes, atomic questions, constrained probes, explicit consent and privacy controls, structured evidence provenance, neutral correction, deterministic completion and mandatory human escalation.

A chatbot can make discovery more scalable and consistent, and research suggests it can elicit richer open-ended responses. Yet the same evidence shows risks of verbosity, assumption, topic skipping, positivity and acquiescence bias. The proper operating model is therefore **chatbot-led evidence collection with human-owned commercial, legal and implementation decisions**, not an autonomous digital consultant.[^18][^2][^6][^3][^1]

---

## References

1. [AI-Assisted Conversational Interviewing: Effects on Data Quality and Respondent Experience](https://ojs.ub.uni-konstanz.de/srm/article/view/8624) - Standardized surveys scale efficiently but sacrifice depth, while conversational interviews improve ...

2. [Tell Me About Yourself: Using an AI-Powered Chatbot to Conduct Conversational Surveys with Open-ended Questions](https://dl.acm.org/doi/fullHtml/10.1145/3381804) - The rise of increasingly more powerful chatbots offers a new way to collect information through conv...

3. [The AI Interviewer: Exploring the Use of Conversational AI-Enabled Chatbots in Qualitative Data Collection](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5194078) - Research tools that can reduce participant and research burden while maintaining data quality are im...

4. [Social Media as a Recruitment and Data Collection Tool: Experimental Evidence on the Relative Effectiveness of Web Surveys and Chatbots](https://www.econstor.eu/bitstream/10419/265818/1/dp15597.pdf)

5. [[PDF] AI-Assisted Conversational Interviewing: Effects on Data Quality and ...](https://ojs.ub.uni-konstanz.de/srm/article/download/8624/7921)

6. [[PDF] AI Conversational Interviewing: Transforming Surveys with LLMs as ...](https://aclanthology.org/2025.latechclfl-1.17.pdf)

7. [Lessons in In Privacy and Safety from Interactions with a General Purpose Chatbot](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4721968) - The ability of chatbots to engage in fluid and complex discussions creates new challenges in human-c...

8. ["It's a Fair Game", or Is It? Examining How Users Navigate Disclosure Risks and Benefits When Using LLM-Based Conversational Agents](https://dl.acm.org/doi/pdf/10.1145/3613904.3642385)

9. [Understanding Users' Privacy Reasoning and Behaviors During ...](https://arxiv.org/html/2601.18125v1)

10. [How do we ensure transparency in AI? | ICO](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/how-do-we-ensure-transparency-in-ai/)

11. [2026-annual-regulatory-oversight-report.pdf](https://www.finra.org/sites/default/files/2025-12/2026-annual-regulatory-oversight-report.pdf)

12. [GenAI: Continuing and Emerging Trends | FINRA.org](https://www.finra.org/rules-guidance/guidance/reports/2026-finra-annual-regulatory-oversight-report/gen-ai) - The GenAI topic of the 2026 FINRA Annual Regulatory Oversight Report informs member firms’ complianc...

13. [While Chatbots Have Many Answers, Do They Have Good Questions? An Experimental Study Exploring the Creation and Evaluation of Survey Questions Using Automated Chatbot Tools](https://aapor.confex.com/aapor/2024/mediafile/Handout/Paper3193/BuskirkEckTimboorkAAPOR2024FinalPublic.pdf)

14. [A Comparison of Four Theory-Based Interview Probes](https://arxiv.org/html/2503.08582v1)

15. [Opinion 28/2024 on certain data protection aspects related to ...](https://www.edpb.europa.eu/system/files/2024-12/edpb_opinion_202428_ai-models_en.pdf) - Purpose limitation and data minimisation principles (Article 5(1)(b) ... generation of personal data...

16. [Chatbot Confessions: Large-Scale Analysis of Private Data ...](https://petsymposium.org/popets/2026/popets-2026-0081.pdf)

17. [[PDF] Artificial Intelligence Risk Management Framework: Generative ...](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

18. [Automated Interviewer or Augmented Survey? Collecting Social Data with Large Language Models](https://ar5iv.labs.arxiv.org/html/2309.10187) - Qualitative methods like interviews produce richer data in comparison with quantitative surveys, but...

