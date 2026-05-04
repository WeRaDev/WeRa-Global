# name
python-systempy-lifecycle

# intent
Improve reliability of Python asyncio applications by standardizing component lifecycle management with `systemPY`, especially when multiple entrypoints or graceful shutdown requirements exist.

# trigger_conditions
- Project is Python + asyncio and has more than one entrypoint (worker, API, CLI, daemon, one-off scripts).
- Startup/shutdown logic is duplicated across scripts or services.
- Graceful reload/teardown behavior is inconsistent or fragile.

# required_inputs
- Python project layout and entrypoint list.
- Current init/startup/shutdown/reload code paths.
- Existing validation commands and runtime constraints.

# procedure
1. Identify atomic runtime components (DB, cache, logger, queue/worker, web server, telemetry).
2. Define one `Unit` per component and map responsibilities to lifecycle hooks:
   - `on_init`
   - `pre_startup`
   - `on_startup`
   - `on_shutdown`
   - `post_shutdown`
   - `on_exit`
3. Compose an application `App` from `Unit` mixins in explicit order.
4. Remove duplicated bootstrap/teardown logic from ad-hoc entrypoints.
5. Ensure lifecycle hooks do not call `super()` and rely on systemPY composition order.
6. Add or update tests/smoke checks for startup, graceful shutdown, and restart-safe behavior.

# validation
- Each critical runtime component has explicit startup and shutdown ownership.
- At least one deterministic smoke path validates startup and graceful stop.
- No duplicated init/shutdown orchestration remains across entrypoints.
- Failure handling and teardown are observable in logs/tests.

# expected_outputs
- Lifecycle map for project runtime components.
- Refactored entrypoint model using `systemPY` units.
- Verification evidence for startup/shutdown/reload behavior.

# failure_modes
- Over-adoption in projects where framework-native lifecycle already fully solves the problem.
- Incorrect mixin order causing hidden startup dependency bugs.
- Missing teardown checks leading to leaked connections/tasks.

# handoff_notes
- Use this skill selectively for Python asyncio lifecycle complexity, not as a mandatory baseline for non-Python projects.
- Keep adoption incremental: start with high-risk components first (DB, queues, background workers).
