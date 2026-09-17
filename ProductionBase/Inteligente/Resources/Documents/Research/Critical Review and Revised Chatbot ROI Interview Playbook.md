# Critical Review and Revised Chatbot ROI Interview Playbook

## Executive judgment

The proposed chatbot playbook is directionally sound but is still too broad to produce a **realistic ROI estimate from interviews alone**. It can produce an **opportunity-screening estimate**—a provisional range used to decide whether evidence collection and a pilot are justified—but it cannot produce an investment-grade ROI until interview claims are checked against records and observed performance.

The simplest reliable approach is not to ask respondents to estimate an entire future automation. It is to reconstruct one recent, concrete instance of one recurring deliverable, establish how often comparable instances occur, identify what expenditure or output could actually change, and ask permission to verify the few inputs that dominate the result. Short recall periods and time diaries are more reliable than broad “usual hours” questions; prolonged recall reduces data quality, and stylised working-time estimates can diverge from diary evidence.[^1][^2][^3]

The revised design therefore separates two decisions:

1. **Screening decision:** Is this use case worth measuring and piloting?
2. **Investment decision:** Did measured pilot performance, adoption, quality, and realized economic value justify deployment?

The chatbot should make the first decision possible. It must not pretend to settle the second.

## Critical findings

### The interview asks too much

A chatbot cannot reliably obtain complete workflow economics, technical feasibility, compliance requirements, adoption forecasts, and implementation cost from one conversational sequence. The more concepts packed into an interview, the greater the respondent burden and the higher the risk of vague, internally inconsistent answers. Sound questionnaire design calls for clear, specific questions that respondents can answer, one concept at a time, in a logical order.[^4][^5]

The playbook should therefore stop trying to build a complete business case during discovery. Its output should be a **bounded hypothesis with an evidence plan**, not a precise ROI promise.

### Abstract questions weaken recall

Questions such as “How many hours does this process usually take?” or “How much could automation save?” require respondents to average variable experiences and forecast an unfamiliar future state. Self-reported working time is vulnerable to recall error, while recent-day or diary-based measurement generally performs better than longer recall and single-item estimates.[^6][^2][^7]

A more reliable opening is:

> “Think of the most recent normal example that was completed. What was the final item delivered?”

The chatbot can then reconstruct that instance. Only afterward should it ask whether the example was typical and how the difficult cases differ.

### Time saved is misclassified

The previous approach risks treating released labour hours as financial benefit. Time saved is initially **capacity**, not cash. It becomes financial value only if it reduces paid overtime, contractor invoices, planned recruitment, or headcount; enables additional contribution margin; or creates another approved and measurable operational outcome.[^8][^9][^10]

This distinction is particularly important in professional services. If work is billed hourly, reducing billable effort may reduce revenue unless the firm redeploys the released capacity or changes the pricing model.[^11]

The chatbot must classify each claimed benefit as one of the following:

| Benefit class | What it means | May enter financial ROI? |
|---|---|---|
| Cash-releasing saving | Existing expenditure will stop | Yes, when an accountable owner confirms the action |
| Cost avoidance | A planned future expense will not occur | Yes, when the plan and timing are evidenced |
| Incremental margin | Extra profitable work can be delivered | Yes, using contribution margin and credible demand |
| Released capacity | Staff time becomes available | No; report separately until its use is approved |
| Quality or service benefit | Fewer errors, faster response, better consistency | Only if linked to a measurable economic consequence |
| Risk reduction | Lower probability or impact of a loss | Separately unless frequency, impact and attribution are defensible |

### The wrong people may be asked

The adviser can identify customer value and describe the visible work, but may not know complete operational effort, loaded labour cost, data availability, or the budget consequence of released capacity. The operational colleague can validate effort and exceptions but may not know margins or commercial demand. The compliance or data owner can decide whether a pilot is permissible and what evidence may be accessed, but should not be treated as the source of ROI assumptions.

The chatbot must route questions according to knowledge ownership:

| Respondent | Reliable contribution | Should not be relied on for |
|---|---|---|
| Adviser or business owner | Deliverable, customer outcome, fee model, demand, recent example | Detailed processing effort unless personally performed |
| Operational colleague | Active time, handoffs, rework, exceptions, volume source | Loaded cost, sales conversion, compliance approval |
| Compliance/data owner | Data location, permissions, retention, controls, prohibited uses | Productivity saving or commercial value |
| Finance or budget owner, if needed | Loaded rates, avoidable spend, contribution margin, realization | Detailed operational sequence |

Three interviews are not always necessary. If the first conversation reveals no recurring unit, no material volume, no plausible value-capture mechanism, or no permitted evidence route, the chatbot should stop rather than burden additional respondents.

### Numeric prompts can anchor answers

Giving examples such as “5–10 hours” before asking for a respondent’s estimate can anchor the answer. The chatbot should first elicit the respondent’s unaided number, then ask how it was derived, and only then offer ranges if the respondent cannot answer. Question wording and order can change responses; clear, neutral questions and small, non-overlapping response sets improve interpretability.[^12][^5]

### Low, base, and high are insufficient

Three scenarios create an appearance of rigor if all three are arbitrary percentages around the same weak assumptions. Credible estimates require documented assumptions, ranges grounded in available evidence, cross-checks, and sensitivity analysis that identifies which inputs most affect the conclusion.[^13][^14][^15]

The revised model should calculate:

- **Evidence-backed case:** uses only confirmed expenditure changes or observed unit economics.
- **Expected case:** includes plausible capacity conversion and expected adoption, visibly labelled as assumptions.
- **Break-even case:** shows the minimum eligible volume, net time reduction, or adoption needed for the investment to pay back.

The chatbot should also identify the two or three variables that control the result. Early appraisal is systematically vulnerable to optimism bias, with benefits overstated and costs or duration understated; estimates should therefore be stress-tested and revised as evidence improves.[^16][^17][^18]

### Automation cost is under-specified

A licence or model-usage price is not the full cost. The estimate must account for discovery, design, integration, data preparation, security and privacy work, testing, training, human review, exception handling, monitoring, support, maintenance, and internal staff time. If implementation cost is not yet known, the chatbot should calculate a **maximum affordable cost** or break-even envelope rather than inventing a vendor estimate.

### Quality is not merely expectation versus delivery

Managing expectations can affect perceived satisfaction, but it does not establish objective quality. For automation, quality must include acceptance criteria such as factual correctness, completeness, compliance, consistency, timeliness, and safe handling of exceptions. “Set an easy target and overachieve” creates perverse incentives; the proper target is the minimum outcome that makes the investment worthwhile while meeting non-negotiable quality and risk thresholds.

For AI-enabled systems, performance and controls should be tested under conditions similar to deployment, human oversight should be documented, and errors, overrides, complaints, escalations, and go/no-go decisions should be monitored.[^19][^20]

## Revised measurement logic

### Minimum viable estimate

The interview needs only enough information to populate this chain:

`Recurring unit × eligible volume × observed net improvement × adoption × value-capture rate − full cost`

Where:

- **Recurring unit** is one clearly bounded case or deliverable with a defined start and accepted end.
- **Eligible volume** is the number of comparable units that fit the proposed automation, excluding out-of-scope exceptions.
- **Observed net improvement** is the baseline active effort minus assisted active effort, including review, correction, fallback, and exception handling.
- **Adoption** is the proportion of eligible units actually processed through the solution.
- **Value-capture rate** is the proportion of released capacity that creates an approved economic consequence.
- **Full cost** includes one-time and recurring internal and external costs.

At interview stage, observed net improvement is unavailable. The chatbot should therefore collect the **baseline**, identify a testable automation boundary, and calculate break-even requirements. It should not ask the client to predict a precise percentage reduction.

### Financial formulas

The pre-pilot screen should separate capacity from financial value:

\[
\text{Released capacity} = V \times E \times (T_b-T_a) \times A
\]

where:

- \(V\) = total recurring volume,
- \(E\) = eligible share,
- \(T_b\) = baseline net active time per unit,
- \(T_a\) = assisted net active time per unit,
- \(A\) = sustained adoption.

Cash and margin benefits should then be calculated independently:

\[
\text{Financial benefit} = C_s + C_a + M_i + Q_v
\]

where:

- \(C_s\) = confirmed cash-releasing savings,
- \(C_a\) = evidenced cost avoidance,
- \(M_i\) = incremental contribution margin,
- \(Q_v\) = monetized quality or risk benefit supported by evidence.

\[
\text{ROI} = \frac{\text{Financial benefit}-\text{full automation cost}}{\text{full automation cost}} \times 100
\]

Released capacity should not be inserted into financial benefit unless a named owner confirms how and when it will be converted. Estimates should show ranges and sensitivity because an early point estimate conceals uncertainty; appraisal guidance recommends documenting the evidence base, assumptions, risks, and boundary conditions.[^21][^22]

## Revised chatbot interview

### Design principles

The chatbot should:

- Ask one short question per turn.
- Use the respondent’s terminology rather than impose automation jargon.
- Begin with a recent concrete example.
- Ask for a number without suggesting a range.
- Always allow “I don’t know,” “not applicable,” and “someone else knows.”
- Ask for the source behind every material number.
- Distinguish active work time from waiting or calendar duration.
- Record normal work, review, correction, and exceptions separately.
- Show a short summary for correction at the end of each topic.
- Stop once the screening decision can be made.

These principles reflect established questionnaire guidance to use concrete language, one concept per question, logical sequencing, answerable response options, and pretesting.[^23][^24][^5][^25]

### Opening and consent

> “This conversation will assess whether one recurring piece of work is worth measuring for automation. It will not produce a guaranteed ROI. Please do not include client names, account details, personal data, confidential case facts, passwords, or credentials. Answers will be summarized for the project team. May the interview begin?”

If consent is not provided, stop. If restricted information appears, warn the respondent, do not repeat it in the summary, and route the incident according to the client’s data-handling procedure.

### Route A: adviser

The adviser route should take approximately 8–12 minutes.

**A1 — Concrete unit**

> “Think of the most recent normal piece of recurring work that you would like made easier. What final item did you deliver?”

Reject broad answers such as “client service” or “administration.” Probe once:

> “What specific item was complete at the end—for example, a reviewed message, report, file, calculation, or meeting pack?”

**A2 — Recipient and decision**

> “Who used that item, and what did it allow them to do?”

This tests whether the deliverable has a real user and outcome.

**A3 — Frequency**

> “In the last full month, approximately how many similar items were completed?”

Follow with:

> “Is that number recorded somewhere, estimated from your calendar, or recalled from memory?”

Do not first ask for annual volume; shorter reference periods reduce recall burden. If the month was unusual, request the most recent normal month.

**A4 — Commercial mechanism**

> “How does this work affect the business financially?”

Offer options only after an unaided response:

- Included in a fixed fee.
- Charged by time.
- Supports a retainer.
- Internal overhead.
- Reduces risk or meets an obligation.
- Unsure.

**A5 — Consequence of faster work**

> “If this work required less staff time, what would actually change during the next 12 months?”

Accept only a specific consequence: reduce external spend, avoid planned hiring, serve evidenced demand, clear a measured backlog, improve a service target, or release capacity with no current financial commitment.

**A6 — Evidence owner**

> “Who can confirm the monthly volume, commercial model, and intended use of any released capacity?”

**A7 — Value summary**

The chatbot displays:

> “The proposed unit is [unit]. It is used by [recipient] for [decision]. Estimated monthly volume is [volume], sourced from [source]. The possible value mechanism is [mechanism]. Is any part incorrect?”

### Route B: operational colleague

This route should take approximately 10–15 minutes and focus on one recent instance of the same unit.

**B1 — Instance selection**

> “Please use the most recent normal example of [unit]. Was it normal, unusually easy, or unusually difficult?”

If not normal, continue but tag it and request another representative example later.

**B2 — Start and finish**

> “What event started the work?”

> “What event meant the item was accepted as complete?”

These two questions define the measurement boundary.

**B3 — Contributors**

> “Which roles spent active working time on this example?”

Ask about roles, not employee names.

**B4 — Active time by role**

For each role:

> “About how much active working time did that role spend on this example, excluding waiting time?”

Then ask:

> “What did you use to estimate that—time record, timestamps, calendar, file history, or memory?”

**B5 — Review and correction**

> “After the first version, how much additional active time was spent reviewing or correcting it?”

Do not combine creation and review; automation often moves effort into verification rather than eliminating it.

**B6 — Exceptions**

> “Out of the last ten similar items, about how many needed materially different handling?”

If the respondent cannot estimate, record “unknown” rather than selecting a range.

**B7 — Failure consequence**

> “What is the most important thing that must not become worse?”

Follow with one measurable acceptance question:

> “How is that checked today?”

**B8 — Verification request**

> “Which existing record could verify volume, active effort, review, or rework with the least effort?”

Examples should be offered only if needed: timestamps, task-system records, time sheets, version history, queue reports, or a short prospective diary.

**B9 — Operational summary**

The chatbot displays the defined unit, boundaries, roles, baseline effort, review, exceptions, quality guardrail, and evidence sources for correction.

### Route C: compliance or data owner

This route is a feasibility gate, not an ROI interview. It should take approximately 6–10 minutes.

**C1 — Data categories**

> “To produce [unit], what categories of information are used?”

Ask for categories, not examples containing live client data.

**C2 — Systems of record**

> “Which approved systems hold those categories?”

**C3 — Permitted test data**

> “What is the least sensitive data that may be used for a pilot: synthetic data, redacted historic cases, anonymized data, or controlled live data?”

**C4 — Prohibited action**

> “What must the automation never access, generate, decide, or send?”

**C5 — Human accountability**

> “Which role must approve the output before it is used or sent?”

**C6 — Evidence requirements**

> “What logs, explanations, retention, testing, or review records are required?”

**C7 — Approval route**

> “Who can authorize a limited pilot, and what evidence do they need?”

NIST guidance supports documenting human oversight, overrides, errors, complaints, escalations, and accountable go/no-go decisions rather than relying on a generic statement that a human remains “in the loop.”[^26][^19]

### Optional Route D: finance owner

Trigger this route only when a financial ROI will be presented.

**D1 — Labour basis**

> “For each relevant role, which approved loaded hourly cost should be used?”

If finance does not use hourly loaded costs, accept its standard costing basis.

**D2 — Spend consequence**

> “Which current or planned expenditure would change if the pilot succeeds?”

**D3 — Capacity conversion**

> “Is there approved demand or backlog that can absorb released capacity?”

**D4 — Margin basis**

> “Which contribution-margin measure should be applied to additional work?”

**D5 — Appraisal rule**

> “What time horizon, payback threshold, and discounting convention should the business case use?”

Without finance validation, the output must be labelled **operational value estimate**, not confirmed financial ROI.

## Chatbot branching rules

### Continue when

Continue to evidence collection if all of the following are present:

- A recurring unit has a clear start and accepted finish.
- A user and outcome are identifiable.
- Volume is material enough to measure.
- At least one plausible value mechanism exists.
- Quality can be tested.
- A permitted evidence path exists.

### Stop or redirect when

Stop the ROI path when any of the following applies:

- The work is genuinely one-off.
- No one uses the output or changes a decision because of it.
- The sole benefit is unspecified “time saved.”
- No record or prospective measurement can verify the baseline.
- The data owner rejects every feasible pilot-data option.
- The required activity is legally or contractually prohibited.
- The output cannot be evaluated against an acceptance standard.

Redirect a low-data opportunity to a **measurement sprint**: sample five to ten normal cases, record active time and exceptions close to performance, and return to the estimate. Real-time or short-recall diaries can reduce error compared with broad retrospective questions.[^27][^2][^28]

## Evidence grading

Every input should carry a grade:

| Grade | Evidence | Permitted use |
|---|---|---|
| A | System record, invoice, ledger, approved finance figure | Evidence-backed case |
| B | Recent sample, timestamps, diary, file history | Evidence-backed case with stated limitations |
| C | Reconciled estimates from two knowledgeable respondents | Expected case only |
| D | Single respondent’s unsupported recollection | Screening and sensitivity only |
| E | Automation team or chatbot assumption | Never presented as client evidence |

The chatbot must preserve provenance: respondent role, reference period, source type, confidence, and whether another owner confirmed the input. A reliable estimate should be comprehensive, documented, accurate, and credible, with uncertainties, key assumptions, cross-checks, and sensitivity analysis visible.[^14][^29]

## Screening output

The chatbot should not output “Expected ROI: 147%.” It should generate a one-page decision record:

### Opportunity statement

- Recurring unit and recipient.
- Business outcome enabled.
- In-scope and excluded cases.
- Current volume and evidence grade.

### Baseline

- Active effort by role.
- Review and rework effort.
- Exception frequency.
- Current elapsed time, if service speed matters.
- Current quality measure.

### Value route

- Cash-releasing saving.
- Cost avoidance.
- Incremental contribution margin.
- Released capacity reported separately.
- Quality and risk benefits reported separately unless monetization is evidenced.

### Feasibility

- Permitted pilot data.
- Required human approval.
- Prohibited actions.
- Logging, retention, security, and test requirements.

### Uncertainty

- Evidence grade for each material input.
- Missing finance inputs.
- Two or three most sensitive assumptions.
- Break-even condition.

### Recommendation

Choose one:

- **Stop:** no material or permissible opportunity.
- **Measure:** insufficient baseline evidence; conduct a short measurement sprint.
- **Prototype:** value route exists and a low-risk technical test is justified.
- **Pilot:** baseline, controls, owner, and success thresholds are ready.

## Pilot replaces prediction

The final ROI should be built from matched pre/post evidence, not optimism expressed during interviews. Define the same eligible unit before and after; include production, verification, correction, fallback, and exceptions; measure actual adoption; and apply the client-approved value-conversion rule.

The pilot should monitor:

- Eligible and excluded volume.
- Successful completion and fallback.
- Active human time.
- Review and correction time.
- Errors and severity.
- Human overrides and reasons.
- Adoption and abandonment.
- Cycle time and backlog, where relevant.
- Actual expenditure or revenue consequence.
- Full implementation and operating cost.

AI performance, oversight, and controls should be measured in deployment-like conditions and reassessed in production rather than assumed from a demonstration.[^20][^19]

## Final verdict

The earlier questions were **not yet the simplest and most reliable way to estimate client ROI**. They were useful for broad discovery but asked respondents to supply estimates they were not well placed to know and risked converting remembered hours directly into monetary value.

The revised playbook is simpler because it asks each person only for facts within that person’s knowledge, anchored to one recent example. It is more reliable because it separates active time from waiting, baseline from future-state assumptions, capacity from cash, and screening from verified ROI. It also treats “unknown” as a valid result and converts missing information into a targeted evidence request rather than a guessed input.

The defensible proposition is:

> **The chatbot does not calculate a promised ROI from conversation. It identifies a bounded use case, reconstructs its baseline, locates the economic value route, grades the evidence, and specifies the smallest measurement or pilot needed to establish ROI.**

---

## References

1. [Data Quality and Recall Bias in Time-Diary Research: The Effects of Prolonged Recall Periods in Self-Administered Online Time-Use Surveys - Petrus te Braak, Theun Pieter van Tienoven, Joeri Minnen, Ignace Glorieux, 2023](https://journals.sagepub.com/doi/10.1177/00811750221126499) - Previous research has shown that a prolonged recall period is associated with lower data quality in ...

2. [Data Quality and Recall Bias in Time-Diary Research The ...](https://cris.vub.be/ws/portalfiles/portal/108088123/88383252.pdf)

3. [Improving Stylised Working Time Estimates with Time Diary ...](https://pmc.ncbi.nlm.nih.gov/articles/PMC6609582/) - Accurate working time estimates represent an important component of the statistical toolbox used for...

4. [Methods 101: Survey Question Wording](https://www.pewresearch.org/methods/2018/03/21/methods-101-video-question-wording/) - The second video in Pew Research Center's Methods 101 series helps explain question wording – a conc...

5. [Writing Survey Questions - Pew Research Center](https://www.pewresearch.org/writing-survey-questions/) - Perhaps the most important part of the survey process is the creation of questions that accurately m...

6. [A comparison of self-reported and device measured sedentary ... - NIH](https://pmc.ncbi.nlm.nih.gov/articles/PMC7055033/) - Sedentary behaviour (SB) is a risk factor for chronic disease and premature mortality. While many in...

7. [Assessing Physicians' Recall Bias of Work Hours With a ...](https://www.jmir.org/2021/12/e26763) - Background: Previous studies have shown inconsistencies in the accuracy of self-reported work hours....

8. [[PDF] AI ROI realization executive playbook](https://www.devry.edu/content/dam/devry_edu/devryworks/d/AI-ROI-Realization-Executive-Playbook.pdf)

9. [Analyst Workflow Automation ROI](https://gsconsultingllc.com/insights/analyst-workflow-automation-roi) - Time saved alone is not ROI. A credible business case follows one case population from arrival throu...

10. [AI Value Realization: From Deployment to Business Impact | Midgentic](https://midgentic.com/learn/ai-value-realization) - Deployment, adoption, usage, productivity, impact, ROI, and value realization are not the same thing...

11. [AI Automation ROI for Mid-Market Professional Services Firms](https://www.kursol.io/blog/ai-automation-roi-professional-services) - Automation that saves billable hours can cut revenue unless capacity is redeployed. The honest ROI m...

12. [Anchoring Bias in Research: How the First Number Skews ...](https://www.koji.so/docs/anchoring-bias-research) - Anchoring bias makes the first number a respondent sees pull every later answer toward it — distorti...

13. [Cost Estimating and Assessment Guide](https://www.gao.gov/assets/gao-20-195g.pdf) - ... Sensitivity, and Risk Analysis. 76. Survey of Step 5. 79. Chapter 9. Step 6 ... 2 Without this a...

14. [GAO-20-195G, Accessible Version, Cost Estimating and Assessment Guide: Best Practice by Developing and Managing Program Cost](https://www.gao.gov/assets/710/706933.pdf)

15. [INFORMATION](https://www.gao.gov/assets/gao-17-281.pdf)

16. [Supplementary Green Book Guidance – Optimism Bias](https://assets.publishing.service.gov.uk/media/5a74dae740f0b65f61322c72/Optimism_bias.pdf) - If the adjustment for optimism is shown as a separate piece of analysis, sensitivity analysis should...

17. [Green Book supplementary guidance: optimism bias](https://www.gov.uk/government/publications/green-book-supplementary-guidance-optimism-bias) - Supplementary guidance to the Green Book on estimates for a project's costs, benefits and duration i...

18. [The Green Book (2026)](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government/the-green-book-2026) - Practitioners should explicitly adjust their appraisals for optimism bias. This is the proven tenden...

19. [Measure - AIRC](https://airc.nist.gov/airmf-resources/playbook/measure/) - Access proven measurement techniques and metrics for assessing AI risks and system performance, ensu...

20. [Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf)

21. [GAO-09-3SP, GAO Cost Estimating and Assessment Guide: Best Practices for Developing and Managing Capital Program Costs](https://www.gao.gov/assets/a77186.html)

22. [Cost Estimating Guidance - GOV.UK](https://www.gov.uk/government/publications/cost-estimating-guidance/cost-estimating-guidance)

23. [Questionnaire Design](https://qataruniversity-prd.qu.edu.qa/siteimages/static_file/qu/research/sesri/documents/workshops/2013/3rd/questionnaire%20desig%20-%20english.pdf)

24. [Designing the future of ONS surveys - National Statistical](https://blog.ons.gov.uk/2019/01/10/designing-future-surveys/) - Looking at how a respondent thinks, and how they conceptualise a topic, in order to construct the qu...

25. [Question and questionnaire development overview for Census 2021](https://www.ons.gov.uk/census/censustransformationprogramme/questiondevelopment/questionandquestionnairedevelopmentoverviewforcensus2021) - How we developed and tested the overall look of the Census 2021 questions and questionnaires.

26. [AI RMF PLAYBOOK](https://airc.nist.gov/docs/AI_RMF_Playbook.pdf)

27. [World Bank Document](https://documents1.worldbank.org/curated/en/099814102072416574/pdf/IDU195d006a6196d314cc21a96310b5efaaff3cd.pdf)

28. [LET'S TALK DATA | Recording the time divide: A comparative study ...](https://www.worldbank.org/en/events/2023/12/14/let-s-talk-data-recording-the-time-divide-a-comparative-study-of-smartphone-and-recall-based-approaches-to-time-use-meas) - In this

29. [1.33.9 Cost Estimating Guidelines - IRM](https://www.irs.gov/irm/part1/irm_01-033-009)

