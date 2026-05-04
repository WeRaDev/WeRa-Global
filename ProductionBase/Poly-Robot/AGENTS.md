# AGENTS.md
Provider-agnostic coding-agent instructions for `Poly-Robot`.

## Scope and precedence
- This file is the canonical agent instruction file for `Poly-Robot`.
- `WARP.md` defines governance/safety constraints and remains authoritative for high-impact operations.
- Use the most specific applicable instruction file near the edited path.

## Core delivery behavior
- Keep changes deterministic, auditable, and reversible.
- Plan before non-trivial implementation.
- Prioritize simulation/replay-first validation before hardware-adjacent changes.
- Do not include unrelated cleanup in the same change.

## Safety
- Never commit secrets, keys, tokens, or sensitive runtime data.
- Treat actuator-control, network-bridge, and autonomous command changes as high impact.
- Require explicit user confirmation before any high-impact execution path.

## Quality and validation
- Run project quality checks for touched scope:
  - `ruff check src/poly_robot tests scripts`
  - `python3 -m unittest`
  - `python3 scripts/validate_parameters.py --catalog config/parameters/catalog.v1.json --profile config/parameters/profiles/mvp_test_token.v1.json --baseline config/parameters/baselines/mvp_test_token.freeze.v1.json --calibration-policy config/calibration/llm_reliability.v1.json`
- For control-surface changes, include at least one reproducible security or operator-UX regression check.
