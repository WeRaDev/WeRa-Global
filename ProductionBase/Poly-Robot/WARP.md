# WARP.md
This file defines project-specific operating rules for the `Poly-Robot` sub-project.

## Project intent
Poly-Robot develops modular robotics capabilities with a simulation-first and safety-first approach.

## Delivery standards
- Keep changes small, auditable, and reversible.
- Propose a concise implementation plan before non-trivial code changes.
- Document architecture decisions in `docs/adr/` as the project evolves.
- Keep sprint-ready tasks in `tasks/`.

## Safety and engineering guardrails
- Prioritize simulation and replayable tests before touching hardware integration paths.
- Never commit credentials, tokens, private keys, or environment-specific secrets.
- Treat actuator-control, network-bridge, and autonomous command changes as high-impact; require explicit user confirmation before execution.
- Prefer deterministic scripts and reproducible test fixtures over manual steps.

## Quality baseline
- Establish lint, typecheck, and test commands before feature growth.
- Require at least one reproducible validation path for each critical control workflow.

## Mandatory Gitea commitment identity (WARP-only)
- For every Gitea commit/push in this repository, use only the `WARP` account.
- Before commit, set repo-local identity to WARP:
  - `git config user.name "WARP"`
  - `git config user.email "<primary email of the WARP Gitea account>"`
- Before commit/push, verify `git config --get user.name`, `git config --get user.email`, and `git remote get-url origin` target the WeRa Global Gitea namespace.
