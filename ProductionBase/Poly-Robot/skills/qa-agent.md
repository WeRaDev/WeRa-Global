# name
qa-agent

# intent
Run a repeatable Poly-Robot QA audit that combines code-quality review, security validation, and operator UX regression checks before delivery.

# trigger_conditions
- Any pull request that changes `src/poly_robot/`, `scripts/`, `tests/`, or runtime configuration.
- Any change touching operator controls, runtime web GUI, integration adapters, or policy/risk logic.
- Any request for QA sign-off, readiness check, or release confidence.

# required_inputs
- Changed file set and pull request diff.
- Risk classification for changed scope (low/medium/high impact).
- Current CI command set from `.gitea/workflows/ci.yml`.
- Acceptance criteria from task or PR description.

# procedure
1. Classify changed files into QA scopes: core logic, security boundaries, and operator UX surfaces.
2. Run baseline checks:
   - `ruff check src/poly_robot tests scripts`
   - `PYTHONPATH=src python3 -m mypy src/poly_robot`
   - `PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*.py"`
3. Run security regression checks:
   - `PYTHONPATH=src python3 -m unittest tests.test_integration_adapters tests.test_llm_policy tests.test_parameter_governance`
4. Run security static analysis:
   - `bandit -q -r src/poly_robot scripts -s B404,B603,B310,B105`
5. Run UX regression checks:
   - `PYTHONPATH=src python3 -m unittest tests.test_runtime_web_gui tests.test_runtime_supervisor_controls tests.test_runtime_supervisor_live`
6. Review changed code for maintainability and correctness (error handling, logging clarity, bounded retries/timeouts, deterministic behavior).
7. Produce QA verdict with severity-ranked findings and concrete remediation actions.

# validation
- Baseline, security, and UX check categories are all executed or explicitly documented as blocked.
- QA findings include reproducible command output and impacted file paths.
- Final verdict is one of: `pass`, `pass_with_risk`, `changes_required`.

# expected_outputs
- QA report containing:
  - command matrix and pass/fail status,
  - security findings with severity,
  - UX findings with user impact,
  - code-quality findings with remediation.
- Final merge recommendation.

# failure_modes
- Skipping UX tests when operator-facing code changed.
- Treating suppressed static-analysis findings as resolved instead of tracked debt.
- Running only full-suite tests without targeted security/UX subsets.
- Reporting “pass” without residual risk disclosure.

# handoff_notes
- If security checks are suppressed (for example Bandit IDs), record the exact suppressed IDs and a follow-up hardening task.
- If CI and local outputs differ, attach exact command lines and environment assumptions to the QA report.
