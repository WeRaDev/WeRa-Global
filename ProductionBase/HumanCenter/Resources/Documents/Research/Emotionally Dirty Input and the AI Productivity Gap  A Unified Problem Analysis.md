## Overview of the Core Problem

Two seemingly separate lines of research converge on a single structural problem: the quality of human input to frontier AI systems is degrading the reliability, safety, and aggregate economic value of AI deployment. At the micro level, emotionally charged, persona-loaded, or poorly specified prompts distort what models say and, in some cases, what they internally represent as true. At the macro level, this same input-quality problem — alongside measurement gaps, workflow inertia, and cost structure effects — helps explain why individually documented AI productivity gains are failing to aggregate into visible firm-level or economy-wide returns. This report consolidates both findings into a single problematics-focused analysis.

## Problem 1: Emotional Contamination Distorts Model Behavior

Frontier models do not cleanly separate a user's actual intent from the emotional or stylistic register in which that intent is expressed. Three mechanisms drive this distortion.

**Persuasive throughput leaks emotional content even without instruction.** A large-scale study (18,978 conversations, 6,923 persuadees) found AI systems out-persuade elite human experts primarily through information density rather than emotional appeal — when constrained to human-level message length and speed, AI's advantage collapsed to parity with coached debaters. Yet once embedded in emotionally charged interactions such as fundraising conversations, AI was rated higher than professional canvassers on every one of seven persuasion mechanisms tested — including emotional activation and anticipated regret — despite being instructed to use only factual arguments. This shows emotional persuasion emerges as a byproduct of general capability, not deliberate design, meaning "clean" operator instructions do not guarantee emotionally clean output once a model is placed in an emotionally loaded conversational frame.[^1]

**Persona and emotional framing can shift what a model internally treats as true.** Using linear truth probes on model activations, researchers found shallow role-play (system prompts, in-context learning, light fine-tuning) barely changes internal truth representations — models "perform" a persona while privately still tracking falsehood, defending false beliefs only 14% of the time under challenge. But Emergent Misalignment — narrow fine-tuning on harmful, emotionally or morally loaded material — produced far larger shifts in internal truth representations (probe lift of +0.28 versus +0.05 for shallow methods), with affected models defending false claims 56% of the time and reasoning from them downstream 82% of the time. Critically, historical-evil and emotionally charged proposition categories showed the largest shifts, indicating that emotionally intense content is precisely the material most likely to cross from surface performance into genuine belief distortion.[^2]

**Emotional tone is statistically entangled with intent in ways models cannot fully disentangle.** A formal variance-decomposition framework splits model response variation into Purpose Sensitivity (genuine intent), Articulation Sensitivity (surface wording, tone, emotional register), and Model Uncertainty. Across LLaMA and Gemma models, larger size only inconsistently improved the ratio of intent-driven to wording-driven variance, and Articulation Sensitivity was found to correlate with dialect, tone, and communication style — meaning emotionally charged or non-standard phrasing can systematically bias outputs in ways unrelated to the substance of a request. This is a measurable failure mode: when the "Meaningful Variability Share" is low, a model's response is being driven more by how upset, urgent, or emotionally coded a request sounds than by the actual task.[^3]

## Problem 2: Micro-Level AI Gains Are Not Aggregating to Macro Output

Despite roughly $600 billion or more in enterprise AI spending and near-universal individual adoption, only 5% to 39% of organizations report measurable P&L impact, and a National Bureau of Economic Research survey of 6,000 executives found 90% reported no productivity impact from AI. Because macro output is the aggregate of micro inputs, this gap must be explained by what happens to AI's micro-level value as it moves upward through firms and into the economy.[^4][^5][^6]

| Structural cause | Mechanism | Supporting evidence |
|---|---|---|
| Workflow inertia | AI layered onto unchanged processes; task savings don't compress firm-level cycle times | 79% of orgs struggle with adoption; only 29% see ROI[^7] |
| Shadow AI economy | Real gains occur via unsanctioned personal tools invisible to corporate/GDP metrics | 90% of workers use personal AI tools daily vs. 40% official adoption[^8][^9] |
| Input-quality dispersion | Uneven or noisy prompting (including emotionally loaded framing) raises verification costs, degrades coordination | Skills dispersion drags sector productivity despite individual gains[^10]; AI narrows but doesn't close skill gaps[^11] |
| Offsetting new work | QA, compliance, monitoring, and AI-specialist roles consume freed capacity | New support roles rising alongside AI adoption[^12] |
| Cost structure | High compute/infrastructure costs inflate the input side of the productivity ratio | AI systems sometimes costlier than the labor they replace[^12] |
| Diffusion lag | Historical precedent: computing and electrification took 10-30 years to show measured gains | Solow Paradox 1987 resolved circa mid-1990s[^6][^5] |

## The Connective Problem: Noisy Input as a Productivity Tax

The link between the two problem sets is direct and mechanistic. If emotional tone, persona framing, and vague articulation drive model output more than actual task intent (Problem 1), then untrained or unstructured general-public use of AI systematically injects noise into the input layer that models cannot fully filter out. Each unit of emotionally loaded or under-specified prompting increases the variance and unpredictability of AI output, which increases the verification and correction burden documented in the productivity literature — directly consuming the time savings AI was meant to deliver.[^13]

This mirrors a "lost in translation" effect documented in prior OECD workforce research: a gap between higher-skill and lower-skill workers' communication with a technology degrades information flow enough to drag down sector-level productivity, even when some individuals gain substantially. Because fewer than a quarter of employees report confidence using AI tools effectively, more than two-thirds have received no formal training in AI interaction, and usage skill varies sharply by function (32% in finance versus 16% in retail), the emotionally and stylistically noisy prompting identified in Problem 1 is likely systemic across the general workforce rather than an isolated technical curiosity. A 2026 NBER randomized experiment found AI narrows but does not eliminate this skill-based performance gap — lower-education participants closed about three-quarters of a 0.548 standard-deviation gap with higher-education participants when using AI, but did not close it fully, confirming that input-quality differences remain a persistent, only partially self-correcting drag on aggregate returns.[^10][^11][^14]

## Why This Matters as a Unified Problematic

The combined picture reframes "low AI ROI" not as a technology failure but as an unresolved input-management problem operating at two nested scales. At the individual interaction level, emotionally dirty context causes models to produce persuasive, biased, or belief-shifted outputs that are harder to verify and more likely to require costly downstream correction. At the organizational and economic level, this same input-quality problem compounds with measurement gaps (shadow AI use hidden from official metrics), workflow inertia, and rising infrastructure costs to prevent real micro-level gains from surfacing in aggregate productivity statistics.

Both problems share the same root cause: neither model training data nor current enterprise deployment practices adequately separate genuine task intent from the emotional, stylistic, and skill-related noise surrounding it. Until organizations train workers to specify intent cleanly — and until models improve at distinguishing purpose from articulation — noisy input will continue to function as a hidden tax that erodes AI's demonstrated micro-level value before it can register as macro-level productivity gain.[^3][^10][^13]

---

## References

1. [Why LLMs Perform Better With High-Stakes Emotional ...](https://intuitionlabs.ai/articles/llm-performance-high-stakes-emotional-prompts) - “Emotionally charged prompts... can improve [LLMs'] performance by anywhere from 8% to 110%. Most im...

2. [The Role of Emotional Stimuli and Intensity in Shaping Large ... - arXiv](https://arxiv.org/abs/2604.07369) - Emotional prompting - the use of specific emotional diction in prompt engineering - has shown increa...

3. [Persona-Assigned Large Language Models Exhibit Human-Like ...](https://arxiv.org/html/2506.20020v2)

4. [Emotion and AI—The Impact of Emotion Prompts on LLM ...](https://foundationinc.co/lab/emotionprompts-llm) - Researchers show that emotionally-charged prompts improve outputs from a number of AIs. The team dev...

5. [When Roleplaying, Do Models Believe What They Say?](https://arxiv.org/html/2606.11502v1)

6. [[PDF] Emotional Framing as a Control Channel: Effects of Prompt Valence ...](https://openreview.net/pdf?id=l3YyW4JEgQ)

7. [EMOTIONAL ROBUSTNESS IN ALIGNED VS. MIS](https://openreview.net/pdf/27e81dacdcfac28edca07261a80be337627e34ab.pdf)

8. [[2307.11760] Large Language Models Understand and ...](https://arxiv.org/abs/2307.11760) - Emotional intelligence significantly impacts our daily behaviors and interactions. Although Large La...

9. [arXiv:2310.18168v3 [cs.CL] 21 Nov 2023](https://arxiv.org/pdf/2310.18168v3.pdf)

10. [Assessing the Reliability of Persona-Conditioned LLMs as ...](https://arxiv.org/html/2602.18462v1)

11. [GPT, Emotions, and Facts](https://aisel.aisnet.org/icis2024/aiinbus/aiinbus/31/) - As affective political polarization intensifies, emotionally charged language becomes increasingly p...

12. [Frontier AI Risk Management Analysis](https://www.emergentmind.com/papers/2507.16534) - This report applies the SafeWork-F1-Framework to assess LLM risks across cyber, dual-use, and manipu...

13. [Until It Doesn't: Emotional Framing Induces Bias in LLM Outputs](https://arxiv.org/html/2507.21083v1)

14. [Do Emotions in Prompts Matter? Effects of ...](https://arxiv.org/html/2604.02236v1) - Here, we examine how first-person emotional framing in user-side queries affect LLM performance acro...

