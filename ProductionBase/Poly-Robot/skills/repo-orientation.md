# name
repo-orientation

# intent
Establish a reliable understanding of Poly-Robot repository boundaries, architecture, workflows, constraints, and safe edit surfaces before implementation begins.

# trigger_conditions
- A new task starts in Poly-Robot or a related integration surface.
- The request touches multiple modules (e.g. strategy + risk + execution + GUI).
- Build/test/lint commands or config layout is unknown.
- Working with Polymarket integration adapters, canary lifecycle, or TRL4 host deployment.

# required_inputs
- Repository root path (`ProductionBase/Poly-Robot/`).
- `README.md`, `WARP.md`, `AGENTS.md`, `SOUL.md`, `CONTRIBUTING.md`.
- `docs/adr/` for accepted architecture decisions.
- Current task request and intended change scope.

# procedure
1. Read `WARP.md` for project safety guardrails and Gitea identity policy.
2. Read `AGENTS.md` for agent behavioral constraints and quality commands.
3. Read `CONTRIBUTING.md` for baseline check commands and DoR/DoD.
4. Read `README.md` for project structure map, CLI commands, and Docker workflows.
5. Read `POLY_ROBOT_ECONOMY_UNIFIED_SPEC.md` for economic logic and parameter definitions.
6. Map editable zones:
   - `src/poly_robot/`: core modules (strategy, risk, execution, exit, governance, runtime, integration, canary lifecycle).
   - `scripts/`: CLI runner entrypoints.
   - `tests/`: unit and regression tests.
   - `config/`: parameters, calibration, certification, replay, integration configs.
7. Map stable/generated zones:
   - `runtime/`: generated artifacts (state, journal, cycle reports, certification reports). Never commit.
   - `.mypy_cache/`, `.ruff_cache/`, `.venv*/`, `__pycache__/`: generated tooling artifacts.
   - `contracts.py`, `schemas.py`: stable interface layer -- changes here affect all consumers.
8. Identify verification commands:
   - Lint: `ruff check src/poly_robot tests scripts`
   - Tests: `PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*.py"`
   - Governance: `python3 scripts/validate_parameters.py --catalog config/parameters/catalog.v1.json --profile config/parameters/profiles/mvp_test_token.v1.json --baseline config/parameters/baselines/mvp_test_token.freeze.v1.json --calibration-policy config/calibration/llm_reliability.v1.json`
   - Security: `bandit -q -r src/poly_robot scripts -s B404,B603,B310,B105`
   - Type check: `python3 scripts/run_typecheck.py`
9. Produce orientation summary for the task.

# validation
- All governance docs read and project-specific constraints identified.
- At least one executable validation path confirmed runnable.
- Proposed edit targets align with WARP.md safety rules and module ownership.
- High-impact changes (actuator-control, network-bridge, autonomous commands, live trading) flagged for explicit confirmation.

# expected_outputs
- Repository context snapshot for the task.
- Candidate files/modules to inspect or edit.
- Confirmed verification command set.
- Risks and assumptions list.

# failure_modes
- Editing `contracts.py`/`schemas.py` without checking downstream consumers.
- Running live-mode commands without credential preflight validation.
- Missing the Polymarket-trading/ dead-weight zone (no tests, no lifecycle awareness).
- Skipping canary lifecycle gate checks after integration adapter changes.

# handoff_notes
- If orientation is incomplete, block implementation and request missing context.
- Preserve the orientation summary for planning and review stages.
- For TRL4 host operations, always verify SSH + Tailscale connectivity first.
