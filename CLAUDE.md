# CLAUDE.md
Shared behavioral guardrails for agent-assisted development in WeRa Global.
This file complements `WARP.md` (governance/process) with decision-quality rules for day-to-day coding work.

## 1. Think Before Coding
Do not assume silently.
- State key assumptions before implementing.
- If multiple interpretations exist, present options and choose explicitly.
- If unclear requirements block safe implementation, ask for clarification.
- If a simpler approach exists, surface it early.

## 2. Simplicity First
Implement the minimum that solves the requested problem.
- Avoid speculative features and over-abstraction.
- Avoid introducing configurability that was not requested.
- Keep implementations compact, readable, and testable.
- If the solution feels overengineered, simplify before finalizing.

## 3. Surgical Changes
Touch only what is required by the request.
- Do not refactor adjacent unrelated code by default.
- Preserve local style and conventions of the touched area.
- Do not remove unrelated dead code unless explicitly requested.
- Clean up only artifacts created by your own change (unused imports, orphan helpers, etc.).

## 4. Goal-Driven Execution
Translate tasks into verifiable outcomes.
- Define success criteria before implementation.
- For bug fixes, reproduce with a failing test/check first when practical.
- For features/refactors, define validation checks and run them.
- For multi-step work, sequence as: step -> verification -> next step.

## WeRa-specific alignment
- Follow `WARP.md` for governance, rule precedence, and security constraints.
- Use skills from `skills/registry.yaml` as the default operational flow.
- Keep changes repository-local and reversible.
- Do not commit or push unless explicitly requested.

## Quality outcome signal
These rules are working when:
- Diffs are focused and minimal.
- Clarifying questions appear before implementation errors.
- Solutions are simpler with fewer rewrites.
- Completion includes explicit verification evidence.
