# name
repo-orientation

# intent
Establish a reliable understanding of repository boundaries, architecture, workflows, constraints, and safe edit surfaces before implementation begins.

# trigger_conditions
- A new task starts in an unfamiliar repository or subproject.
- The request touches multiple modules or unclear ownership boundaries.
- Build/test/lint commands are unknown.

# required_inputs
- Repository root path.
- Relevant `README.md`, `WARP.md`, `CONTRIBUTING.md`, and project docs.
- Current task request and intended change scope.

# procedure
1. Identify repository scope and active project boundaries.
2. Read the highest-precedence rule files for the target paths.
3. Locate and record canonical build, test, lint, and run commands.
4. Map editable zones, stable zones, and generated artifact paths.
5. Identify key dependencies, interfaces, and quality/security constraints.
6. Produce a concise orientation summary tied to the requested task.

# validation
- Required documentation files were read or explicitly noted as missing.
- At least one executable validation path is identified (tests/lint/typecheck/smoke).
- Proposed edit targets are aligned with rule precedence and ownership.

# expected_outputs
- Repository context snapshot for the task.
- Candidate files/modules to inspect or edit.
- Confirmed verification command set.
- Risks and assumptions list.

# failure_modes
- Missing or stale documentation creates incorrect assumptions.
- Incorrect rule precedence causes invalid edits.
- Hidden generated files are edited directly by mistake.

# handoff_notes
- If orientation is incomplete, block implementation and request missing context.
- Preserve the orientation summary for planning and review stages.
