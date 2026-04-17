# name
implementation-plan

# intent
Design a safe, reviewable implementation approach for non-trivial changes with clear sequencing and validation checkpoints.

# trigger_conditions
- Task impacts multiple modules or repositories.
- Architectural or high-risk changes are requested.
- User explicitly asks for a plan.

# required_inputs
- Output from `task-intake`.
- Orientation summary from `repo-orientation`.
- Existing architecture and constraints documentation.

# procedure
1. Confirm current-state architecture relevant to the change.
2. Break target outcome into minimal, reversible increments.
3. Define file-level change strategy and dependency order.
4. Attach validation checkpoints per increment.
5. Define rollback and risk-mitigation approach for stateful or high-impact steps.
6. Produce an implementation plan for approval when required.

# validation
- Plan steps are executable in order and avoid circular dependencies.
- Each step has corresponding verification criteria.
- High-impact operations include rollback and safety checks.

# expected_outputs
- Concise implementation plan.
- Sequenced execution stages.
- Validation and rollback strategy.
- Open questions requiring stakeholder confirmation.

# failure_modes
- Planning based on assumptions not validated in code/docs.
- Oversized steps that are hard to review or revert.
- Missing rollback strategy for high-impact changes.

# handoff_notes
- Execution begins only after required approvals.
- Update plan when new findings materially change the approach.
