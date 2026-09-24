# AGENTS.md
Provider-agnostic coding/knowledge-agent instructions for `Inteligente`.

## Scope and precedence
- This file is the canonical agent instruction file for `Inteligente`.
- `WARP.md` is the governance/safety/process source of truth.
- If guidance conflicts, follow the most specific rule in this order:
  1. Files under touched subdirectories
  2. This `AGENTS.md`
  3. `WARP.md`
  4. Umbrella-level rules from the parent (`WeRa Global`) repository

## Core delivery behavior
- Keep changes small, reviewable, and task-scoped.
- Propose a concise plan before non-trivial implementation or business-model changes.
- Prefer explicit verification (evidence, sources) over assumptions, especially in `KnowledgeBase/` documents.
- Do not refactor or rewrite unrelated content unless explicitly requested.

## Knowledgebase authoring rules
- Every `KnowledgeBase/kb-*/docs/**` document must use the metadata/provenance block from `KnowledgeBase/templates/KB-Domain-Document-Template-v1.md`.
- Mark claims `evidence_status: unverified` or `hypothesis` unless backed by a cited source (e.g. a file under `Resources/Documents/Research/`).
- Update `last_reviewed_at` / `next_review_due` when materially editing a domain document.

## Quality and validation
- Baseline structure check: all required files/folders listed in `README.md` exist (`.gitea/workflows/ci.yml` `baseline-check` job).
- Knowledgebase structure check: every `KnowledgeBase/kb-*` folder has a `README.md` (`kb-structure-check` job).
- Once automation delivery code is added, extend this section with the applicable lint/typecheck/test commands.

## Security and legal guardrails
- Never commit credentials, session files, tokens, or client documents.
- Do not run real client-account automation without signed authorization and a DPA.
- Treat any anti-bot bypass or unauthorized-access approach as out of scope.
