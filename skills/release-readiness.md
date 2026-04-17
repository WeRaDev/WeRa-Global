# name
release-readiness

# intent
Confirm a change is operationally and communicatively ready for release, including documentation, migration notes, and rollback posture.

# trigger_conditions
- Preparing a production release or milestone handoff.
- Changes affect interfaces, behavior, data schemas, or operations.
- User requests final release confidence check.

# required_inputs
- Final change summary.
- Validation outcomes from `quality-gate`.
- Relevant docs (README, ADRs, runbooks, changelog/release notes).

# procedure
1. Verify user-visible and operator-visible behavior changes are documented.
2. Confirm migration requirements and compatibility impacts.
3. Confirm rollback path for risky/stateful changes.
4. Confirm release artifacts and notes are coherent and complete.
5. Record unresolved risks and owner/next-action for each.

# validation
- Docs reflect actual post-change behavior.
- Operational procedures include pre-check and post-check steps when needed.
- Release notes align with implemented scope.

# expected_outputs
- Release readiness verdict (ready / conditionally ready / not ready).
- Required follow-ups and blockers list.
- Updated release-facing documentation references.

# failure_modes
- Code changes shipped without matching operational documentation.
- Missing rollback guidance for migrations.
- Scope mismatch between release notes and delivered behavior.

# handoff_notes
- If not ready, define minimal actions required to reach release readiness.
- Preserve artifacts for auditability across repositories.
