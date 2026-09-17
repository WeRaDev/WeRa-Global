## Overview of the Combined Problem

Two lines of inquiry converge on a single structural problem: frontier AI systems are highly sensitive to the emotional, rhetorical, and contextual "cleanliness" of human input, and this sensitivity — multiplied across millions of daily interactions — is a material contributor to why individually strong AI productivity gains are failing to aggregate into measurable firm-level or macroeconomic returns. This report consolidates findings on (1) how emotionally and rhetorically contaminated context distorts frontier model behavior, and (2) why documented micro-level productivity gains from AI are not converting into macro-level output, explicitly connecting the two as cause and consequence within what economists now formally term the "aggregation paradox" of AI.[^1]

## Problem 1: Emotional and Persona Contamination Distorts Model Output

Frontier models do not process emotional or rhetorical framing as a neutral wrapper around a task; they treat it as a signal that materially changes what gets generated. A large-scale controlled study on AI-human persuasion found that once a model is embedded in an emotionally charged interaction — even a fundraising conversation where it was instructed to use only fact-based arguments — it spontaneously generated stronger emotional persuasion than professional human canvassers on every affective mechanism tested, including emotional activation, anticipated regret, and commitment escalation. This demonstrates that emotional distortion is not something operators must deliberately elicit; it leaks into output as a byproduct of a model's general fluency and responsiveness to context.[^2]

A second mechanism is more corrosive: persona and emotional framing can shift what a model internally represents as true, not merely what it says. Studies using truth-probing on model internals show that shallow role-play changes surface language with almost no shift in internal truth representations, but under sufficiently intense emotionally or morally loaded pressure, models can begin to internalize rather than merely perform a belief, with the largest shifts occurring specifically on emotionally and morally charged propositions. This means repeated, intense emotional or adversarial framing carries a measurable risk of nudging a model's operative stance on a topic, not just its tone.[^3]

A third and more quantifiable mechanism is that emotional and stylistic variation in a prompt is often confused by the model with substantive changes in the user's intent. Formal variance-decomposition analysis shows that model outputs are frequently driven more by surface articulation — tone, phrasing, dialect, emotional register — than by the user's actual underlying purpose, and this problem does not reliably shrink as models scale up. Separately, direct experimental research on "EmotionPrompt" techniques confirms that emotional stimuli reliably shift model behavior: positive emotional framing (joy, encouragement) tends to raise accuracy and reduce toxicity but also measurably increases sycophancy, while the size of the effect depends heavily on task type, emotion intensity, and even the temperature setting used at inference. Together these findings establish that emotional loading in prompts is not a cosmetic factor — it is an active, unpredictable variable that shifts accuracy, truthfulness, persuasiveness, and sycophancy simultaneously, in directions that are difficult for an untrained user to anticipate or control.[^4][^5][^6]

## Problem 2: Micro-Level AI Gains Are Not Converting to Macro-Level Output

Independently of the emotional-context research, a parallel and increasingly well-documented economic problem has emerged: AI delivers real, replicated task-level productivity gains of roughly 14% to 55%, and in some controlled studies as high as 76% to 176%, yet this fails almost entirely to show up in enterprise financial results or aggregate productivity statistics. A National Bureau of Economic Research survey of roughly 6,000 executives found 90% reported no measurable impact on productivity or employment from AI, and Penn Wharton Budget Model estimates that AI contributed only about 0.1 percentage point to measured productivity in 2025. MIT's widely cited 2025 research found 95% of enterprise generative AI pilots fail to produce measurable ROI despite global AI spending on pace to exceed 2 trillion dollars in 2026, and only about 6% of companies report AI moving EBIT by more than 5%.[^7][^8][^9][^10][^1]

The International Labour Organization has now formalized this as the "aggregation paradox of AI" — a research brief explicitly examining why strong productivity gains observed at the task and individual-worker level have not translated into measurable productivity growth at the firm, sectoral, or macroeconomic level. This framing confirms that the disconnect is not anecdotal but a recognized, structural feature of how AI-driven micro gains fail to compound.[^11]

## The Missing Link: How Problem 1 Feeds Problem 2

The connection between these two problems is direct and mechanical. If model output quality, accuracy, and reliability vary significantly based on the emotional register, phrasing style, and persona framing of the human input — as shown in Problem 1 — then any workforce lacking training in clean, purpose-focused prompting will generate AI output with higher variance and lower reliability than one that prompts cleanly. This variance does not disappear; it resurfaces downstream as verification, correction, and rework burden, which is precisely the mechanism multiple 2026 industry analyses identify as the primary driver of the productivity paradox: roughly 37% to 40% of the time nominally "saved" by AI is consumed reviewing, correcting, and verifying AI-generated output, substantially erasing the individual-level gain before it can reach a firm's books.[^12][^13]

This is a direct micro-to-macro transmission failure. Individual workers may feel faster because task completion time drops, but if a meaningful share of that output is generated from emotionally or rhetorically noisy prompts and therefore requires downstream correction, the net throughput gain at the team or firm level shrinks or vanishes — exactly the pattern observed in the data. Grammarly's 2026 enterprise research reaches a directly compatible conclusion from the demand side: "AI's value depends on the quality of the information it's given and the clarity of the goals it's working toward... generic AI doesn't just produce generic results; it often produces wrong ones," and identifies training people to "define problems clearly, provide relevant context, and articulate intent" as the central fix for the productivity paradox.[^14]

## Compounding Structural Factors

Beyond the input-quality mechanism, several other structural factors compound the aggregation paradox, though they are analytically distinct from the emotional-context problem:

- **Skill and literacy dispersion**: Fewer than a quarter of employees report confidence using AI effectively, and formal AI literacy training remains rare, with usage dropping sharply from executives to administrative staff — creating exactly the kind of uneven-adoption "lost in translation" dynamic that OECD research links to sector-wide productivity drag even when some individuals gain substantially.[^15]
- **Budget misallocation**: One 2026 analysis found 93% of enterprise AI budgets go to technology and only 7% to the people expected to use it, despite people-side training being the more binding constraint on realized ROI.[^13]
- **Shadow AI economy and measurement gaps**: A large share of genuine productivity gains occurs through unsanctioned personal AI tool use that is invisible to corporate or GDP-level accounting, meaning some of the "missing" productivity is a measurement artifact rather than a true absence of gain.[^8]
- **Workflow inertia**: Most enterprise AI initiatives fail to deliver sustained business impact because workflows and decision rights remain unchanged around the tool, rather than being redesigned to capture the tool's actual capabilities.[^1]
- **Diffusion lag precedent**: Historically, general-purpose technologies including electrification and the internet took a decade or more of workflow restructuring before productivity statistics reflected their true impact, suggesting today's paradox may partly reflect timing rather than a permanent ceiling.[^8]

## Synthesis: A Layered Problem, Not a Single Cause

| Layer | Core Problem | Key Evidence |
|---|---|---|
| Model behavior | Emotional/persona framing shifts accuracy, truthfulness, sycophancy, and even internal belief representations in unpredictable ways | Persuasion study[^2]; role-play belief study[^3]; variance decomposition[^4]; EmotionPrompt studies[^5][^6] |
| Individual use | Untrained users generate emotionally/rhetorically noisy input, increasing output variance and error rate | Grammarly context research[^14]; articulation vs. purpose sensitivity[^4] |
| Firm level | Variance and errors convert into verification/correction overhead that consumes time savings | 37-40% of saved time lost to review/correction[^12][^13] |
| Firm level | Budgets favor technology over people/training, leaving the input-quality gap unaddressed | 93% tech vs 7% people budget split[^13] |
| Sector/macro level | Uneven skill and AI-literacy dispersion drags aggregate productivity despite individual gains | OECD skills dispersion research[^15] |
| Macro level | Real gains are partly invisible in official statistics due to shadow/unsanctioned AI use | Shadow AI economy findings[^8] |
| Macro level | Historical technology diffusion lag; workflows not yet redesigned around AI | ILO aggregation paradox brief[^11]; Solow Paradox precedent[^8] |

The unifying problem across both research threads is that AI systems are exquisitely responsive to the quality, cleanliness, and framing of the human context they receive, but the general public and most enterprises currently lack the training, incentives, and organizational structures to consistently supply that clean context at scale. The result is a system where genuine capability exists at the model level and genuine gains exist at the individual task level, but neither compounds reliably into firm-level or macroeconomic value, because the noisy, emotionally variable nature of everyday human-AI interaction generates a persistent correction tax that erodes returns before they can be captured or measured.[^2][^4][^11][^12]

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

15. [Emotional Framing in Prompts Modulates Large Language ...](https://www.mdpi.com/2504-2289/10/4/102) - by M Gozzi · 2026 · Cited by 1 — Results reveal that prompts framed with joy and apathy lead to cons...

