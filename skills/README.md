# WeRa Global Skills Framework
This directory contains reusable skills for consistent, high-quality project execution across WeRa Global.

## Purpose
The skills system standardizes how tasks are scoped, implemented, verified, and improved.
It combines:
- Process skills (orientation, intake, planning, quality, release, retro)
- Behavioral skill (`karpathy-guidelines`) to reduce common coding mistakes

## Canonical index
- `registry.yaml` is the source of truth for available skills and default execution profiles.

## Recommended usage flow
For most non-trivial work:
1. `repo-orientation`
2. `task-intake`
3. `karpathy-guidelines`
4. `implementation-plan` (when complexity/risk requires)
5. `quality-gate`
6. `release-readiness` (release-impacting work)
7. `retro-capture`

For pull-request audit and review quality:
1. `repo-orientation`
2. `revisor-pr-audit`
3. `quality-gate`
4. `release-readiness`

For small low-risk fixes:
1. `task-intake`
2. `karpathy-guidelines`
3. `quality-gate`

## Creating new skills
1. Copy `SKILL_TEMPLATE.md` to a new file in `skills/`.
2. Fill all required sections (`name`, `intent`, `trigger_conditions`, `required_inputs`, `procedure`, `validation`, `expected_outputs`, `failure_modes`, `handoff_notes`).
3. Register the new skill in `registry.yaml`.
4. Add at least one representative prompt to `skills/evals/evals.json`.
5. Validate the skill on realistic project prompts before broad adoption.

## Quality review baseline
- `skills/evals/evals.json` stores baseline prompts used to test skill behavior over time.
- Review prompts should include ambiguity handling, simplicity pressure, surgical diff pressure, and verification requirements.
- PR-review prompts should also verify severity discipline, actionable findings, and mentorship-quality tone.
