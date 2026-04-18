# name
quality-gate

# intent
Ensure changes satisfy repository-native quality expectations through deterministic verification and transparent failure reporting.

# trigger_conditions
- Any code or configuration change intended for delivery.
- Before opening or updating a pull request.
- After resolving review feedback.

# required_inputs
- Changed file set.
- Project-native validation commands (tests, lint, typecheck, build, smoke checks).
- Target acceptance criteria.

# procedure
1. Run format/lint checks using repository-native tooling.
2. Run unit/integration/smoke tests appropriate to changed scope.
3. Run type or static analysis checks where configured.
4. Capture failures with exact command, error summary, and impacted files.
5. Apply focused fixes and re-run failed checks.
6. Produce a final pass/fail validation report.

# validation
- All required checks pass, or explicit blockers are documented.
- Failures are reproducible via reported commands.
- Verification coverage matches changed scope.

# expected_outputs
- Validation report with command results.
- Pass/fail status by check category.
- Residual risk notes for any deferred failures.

# failure_modes
- Running non-standard checks that differ from CI.
- Partial re-runs that miss regressions in adjacent scope.
- Silent failures due to missing environment prerequisites.

# handoff_notes
- If checks cannot run, provide concrete remediation steps and environment gaps.
- Never mark task complete without transparent quality status.
