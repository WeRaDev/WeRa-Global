# DreamMakers
DreamMakers is a maintained WeRa self-publishing and marketing agency. Its current
implementation provides reproducible, open-source PDF/EPUB book production
workflows (font substitution, page-number normalization, print-ready bleed
management and reflowable EPUB conversion). It is not a desktop publishing
replacement, does not redesign source layouts by default, and does not yet
establish an approved live marketing or publishing automation service.

## Quick start: source-only baseline validation
From the umbrella checkout root, use Python 3.11 or newer:
```bash
cd ProductionBase/DreamMakers
python3 -m venv .agent-baseline-ci
.agent-baseline-ci/bin/python -m pip install -r security/agents/bundle/requirements.txt
.agent-baseline-ci/bin/python security/agents/bundle/validate.py --root .
```
In a standalone checkout start at the project root and omit the `cd` command.
Dependency installation needs an approved package source or pre-provisioned wheel
cache; validation itself is offline. Expected result: valid structure and denied
admission, with all 35 controls unassessed. This does not run conversions or open
manuscripts. `--admission` deliberately exits nonzero while approvals are pending.
The legacy conversion scripts use additional third-party libraries and document
tools; a reproducible pipeline dependency/test contract is a separate gated task.

## Project structure
- `README.md`: project purpose, usage, and constraints.
- `WARP.md`: project-level operational and governance rules.
- `AGENTS.md`: canonical coding-agent operating instructions for this repository.
- `SOUL.md`: constitutional safety and service principles for agent behavior.
- `CONTRIBUTING.md`: contribution workflow and quality requirements.
- `docs/adr/`: architecture decision records.
- `tasks/`: sprint-ready work tracking documents.
- `skills/`: project-specific reusable skill playbooks.
- `security/agents/`: pending manifest, assessments and hash-locked standalone policy bundle.
- `.gitea/workflows/`: standalone CI scaffolding; not active umbrella CI routing.
- `scripts/`: existing document-specific workflows; review and sanitize before tracking or reuse.
- `ci/`, `tests/`: standard-library-only quality-gate tooling and temporary synthetic Python fixtures; no document conversions.
- Local manuscripts, outputs, reports, research and environments are not automatically approved for Git tracking. `.gitignore` allows only named governance files and source/security directories; staging still requires an explicit reviewed file list.

## Core workflows
- Research and define change scope in `tasks/backlog.md`.
- Record major technical decisions under `docs/adr/`.
- Implement small, reviewable changes with validation evidence.
- Run the standalone security validator after governance/composition changes. Do not regenerate hashes merely to make it pass.
- Run the local quality command below for changes to `ci/` and `tests/`. Do not run document-specific scripts as a generic build/test command: some have hardcoded inputs/outputs, and the existing EPUB verifier reports diagnostics without enforcing every failure via its exit status.
- Verify output PDFs with reproducible checks (font embedding, page boxes, visual QA).
- For EPUB3 production, use semantic reflowable XHTML for selectable text, separate the cover and front matter, omit a visible source TOC when a clean nav is requested, preserve original images inline, and validate in Apple Books before release.
- If both DOCX and PDF are available, use DOCX as the semantic conversion source and PDF as the visual/reference baseline.
- For folio hotfixes, use a page-scoped workflow: detect corner folios, patch only affected pages, then run structural and pixel-based before/after QA on the exact modified regions.

## Constraints and known limits
- Preserve text geometry whenever a task requires zero reflow.
- Avoid destructive rewrites of PDF content streams unless explicitly required.
- Keep tooling open-source and scriptable.
- Use Gitea-based review and traceability for production changes.
- Avoid broad bottom-corner masks; allow only minimal folio-area cleanup masks that are proven not to overlap body text.
- Never run CI against client manuscripts or use CI to contact author, publishing or marketing accounts.
- DreamMakers is registered as a native/incubation umbrella project; this directory has no independent repository identity. Only the separately approved Gate B files are staged.
- Root CI routing is prepared locally in `../../.gitea/workflows/dreammakers-quality.yml`; the existing root AgentBaseline workflow covers this native overlay. The nested workflow remains a standalone scaffold. Delivery, remote execution and required-check enforcement are not yet verified or activated.

## Local quality checks (synthetic-only)
From the project root, no package installation is needed for the new quality gate:

    python3 -B -I ci/check_source.py --root . --tests

The command checks Python 3.11-compatible syntax in `ci/` and `tests/`, without
executing the checked sources during compilation, then explicitly runs the
synthetic `test_*.py` suite from `tests/`. It fails for missing/empty source
directories, invalid encoding/syntax, symlinks, no discovered tests or failing/skipped
tests. Fixtures are generated in temporary directories; no real documents,
conversion scripts, environments, credentials or network services are accessed
by this suite. `-B -I` avoids bytecode writes and ambient Python import paths.
These flags are not a security sandbox for arbitrary or subsequently changed tests.
For local lint, when the approved Ruff tool is available, run
`ruff check --no-cache ci tests`; Ruff is not a dependency of the CI command.
The gate verifies its own source/test mechanics only. It does not validate PDF
layout, EPUB packages, document fidelity, publication rights or business outcomes.
Fail-on-error document verification and manual Apple Books/rendered-output QA
remain separate requirements before any document delivery.

## Folio-fix quality gate (mandatory)
1. Structural checks:
- `qpdf --check <output.pdf>`
- `pdfinfo -box <output.pdf>` (verify page size/trim/bleed unchanged)
2. Font checks:
- `pdffonts <output.pdf>` and normalize unexpected `Helvetica` artifacts after overlay merges.
3. Page-scoped folio verification:
- Audit target pages with `pdftotext -bbox-layout` to find bottom numeric candidates.
- Confirm centered folio exists on each target page.
- If a page has `/Rotate 180`, verify folio placement in visual coordinates (rendered page), not only stream-space coordinates.
4. Visual regression checks for modified pages:
- Render before/after PNGs via `pdftoppm`.
- Compute pixel diff statistics for old corner-folio zones; corner darkness must reduce to near-zero.
- Confirm center-folio zone gains expected dark pixels.
- For overlay fallback, verify that difference bounding boxes are limited to folio regions and do not clip adjacent body text.
5. Safety check:
- Ensure diff bounding boxes stay in folio regions (no body-text clipping).
6. Rollback and traceability:
- Keep a pre-fix backup of every promoted PDF (e.g. `*.pre-<fix>.pdf`).
- Persist a machine-readable report for the exact page list processed and per-page status.

## Session-derived production notes
- `pdftotext -bbox-layout` can still report corner folio text after visual masking; acceptance must be based on rendered output + diff metrics, not bbox extraction alone.
- On pages with complex stream structure, direct instruction deletion may miss visual folios; use validated fallback overlay only for the unresolved pages.
- Run a post-overlay font-name normalization pass and re-check `pdffonts` to remove incidental `Helvetica` artifacts introduced by overlay generators.

## Contribution path and ownership
- Open work items in `tasks/backlog.md` and promote to active sprint scope as needed.
- Submit changes through pull requests with clear validation output.
- Business and technical/security owner: Gitea account `mika`, aligned with WeRa umbrella standards. Review status remains pending; owner assignment grants no runtime authority.
- Gitea commitment identity remains `WARP`. No staging, commits, pushes or account/configuration changes without separate authorization.
