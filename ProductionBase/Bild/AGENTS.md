# AGENTS.md
Provider-agnostic coding-agent instructions for `Bild`.

## Scope and precedence
- This file is the canonical agent instruction file for `Bild`.
- `WARP.md` is the governance/safety/process source of truth.
- If guidance conflicts, follow the most specific rule in this order:
  1. Files under touched subdirectories
  2. This `AGENTS.md`
  3. `WARP.md`
  4. Umbrella-level rules from the parent repository

## Core delivery behavior
- Keep changes small, reviewable, and task-scoped.
- Propose a concise plan before non-trivial implementation.
- Prefer explicit verification over assumptions.
- Do not refactor unrelated code unless explicitly requested.

## Quality and validation
- Use repository-native checks for touched scope:
  - `python -m pytest -q`
  - `ruff check .`
  - `ruff format --check .`
  - `mypy src session_test.py har_extract.py`
- For changed behavior, add or update at least one reproducible test/smoke path.

## Security and legal guardrails
- Never commit credentials, session files, tokens, or client documents.
- Do not run real account automation without signed authorization and DPA.
- Treat anti-bot bypass assumptions as unverified until backed by evidence.
