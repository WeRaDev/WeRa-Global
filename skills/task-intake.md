# name
task-intake

# intent
Translate a user request into a constrained execution scope with acceptance criteria, non-goals, and validation strategy.

# trigger_conditions
- Any new implementation request.
- Ambiguous tasks that may be interpreted in multiple ways.
- Requests with potential cross-repository impact.

# required_inputs
- User request text.
- Current repository and project context.
- Applicable rules and constraints from `WARP.md` files.

# procedure
1. Extract the core objective and classify it (fix, feature, refactor, docs, ops).
2. Define in-scope outcomes and explicit non-scope boundaries.
3. Convert intent into concrete acceptance criteria.
4. Identify dependencies, risks, and required sequencing.
5. Choose execution mode: direct small change vs planned medium/large change.
6. Confirm validation commands and success signals.

# validation
- Acceptance criteria are testable and tied to observable outcomes.
- Scope excludes unrelated cleanup unless explicitly requested.
- Dependencies and risks are documented before edits.

# expected_outputs
- Structured task definition.
- Scope/non-scope statement.
- Acceptance criteria and verification plan.
- Recommended execution path (direct implementation or plan-first).

# failure_modes
- Vague objectives lead to over-implementation.
- Missing non-scope boundaries cause scope creep.
- Validation omitted, resulting in unverifiable delivery.

# handoff_notes
- Feed outputs into the implementation-plan skill when complexity is medium/high.
- Re-run intake if requirements change during execution.
