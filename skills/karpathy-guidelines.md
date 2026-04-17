# name
karpathy-guidelines

# intent
Improve development quality, clarity, and efficiency by reducing common LLM coding mistakes: silent assumptions, overengineering, broad/unrelated edits, and weak verification.

# trigger_conditions
- Any coding, refactoring, or bug-fix task.
- Ambiguous user requests that can be interpreted in multiple ways.
- Tasks at risk of overcomplication or broad diffs.
- Work that needs explicit and testable success criteria.

# required_inputs
- Task objective and acceptance context.
- Relevant code/documentation scope.
- Existing project rules from `WARP.md` and applicable subproject rules.

# procedure
1. Think Before Coding
   - State assumptions explicitly.
   - Surface ambiguity and alternatives.
   - Ask for clarification when uncertainty affects correctness.
2. Simplicity First
   - Implement the minimum sufficient solution.
   - Avoid speculative abstractions and unrequested configurability.
3. Surgical Changes
   - Edit only lines directly required by the task.
   - Preserve unrelated style and behavior.
   - Remove only artifacts made obsolete by your own change.
4. Goal-Driven Execution
   - Define concrete success criteria before implementation.
   - Use verifiable checks (tests/lint/type/smoke) to confirm completion.
   - For multi-step tasks: each step must include an explicit verification action.

# validation
- Assumptions are documented or resolved before major edits.
- Final implementation is minimal relative to requested scope.
- Diff contains no unrelated refactors or drive-by formatting changes.
- Completion includes explicit verification evidence.

# expected_outputs
- Cleaner scoped diffs.
- Fewer revision cycles caused by overengineering.
- Earlier clarification of ambiguous requirements.
- More reliable delivery through measurable verification.

# failure_modes
- Treating assumptions as facts and implementing the wrong interpretation.
- Adding unnecessary architecture for hypothetical future needs.
- Expanding change scope beyond the request.
- Declaring completion without concrete verification.

# handoff_notes
- Use this skill as a behavioral overlay with all implementation-oriented skills.
- Pair with `task-intake` and `quality-gate` by default.
- If tradeoffs exist, document them explicitly for reviewer/user decision.
