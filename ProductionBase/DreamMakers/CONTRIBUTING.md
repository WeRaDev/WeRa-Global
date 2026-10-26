# Contributing
## Governance and security preflight
- Read `WARP.md`, `AGENTS.md`, `SOUL.md` and `security/agents/manifest.yaml`.
- The project `SOUL.md` inherits the umbrella constitution. More-specific instructions cannot waive protected security floors.
- Use the isolated standalone validation commands in `README.md`; structure passing is not runtime admission or a visual-quality verdict.
- Keep manuscripts, outputs, generated reports, environments and credentials outside tracking. Preserve local originals and backups.
- Stage only an explicitly approved file list. Legacy document scripts and research require separate content/privacy review; ignore rules do not establish publication rights.
- Use the WARP Gitea account for any separately authorized commitments, never a personal owner identity.
- Native registration, CI activation, commits, pushes, publishing and marketing actions each retain their separate approval requirements.

## Prepared local quality gate
From the project root run `python3 -B -I ci/check_source.py --root . --tests`.
The standard-library-only command checks the new `ci/` and `tests/` sources and
executes only their synthetic test suite, failing if tests are absent or fail.
It does not import legacy conversion scripts or open manuscripts.
Optional local lint is `ruff check --no-cache ci tests` with the approved tool.
Run the standalone security validator separately using the README environment.
The umbrella root workflow explicitly routes this command to DreamMakers;
preparing its YAML does not activate remote CI or branch protection.
Do not restage Gate C changes, alter approved composition locks, or mark controls
verified merely because local checks pass. Gate B staged blobs remain unchanged
until a new staging decision is approved.

## Workflow
1. Capture task scope in `tasks/backlog.md`.
2. For non-trivial tasks, define a short implementation plan.
3. Implement in small commits with clear intent.
4. Validate changes and include command evidence in PR description.
5. Update related docs (`README.md`, ADRs, tasks) before merge.

## Branching and commits
- Branch naming: `feat/<scope>-<slug>`, `fix/<scope>-<slug>`, `chore/<scope>-<slug>`.
- Commit style: Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`).
- Keep commits atomic and reversible.

## Definition of Ready
A task is ready when it includes:
- problem statement
- scope/non-scope
- acceptance criteria
- dependencies
- validation plan

## Definition of Done
A task is done when:
- implementation is complete and reviewed
- relevant validation commands pass
- documentation is updated
- operational risk and rollback notes are documented when applicable

## PDF production evidence checklist (required for folio/text-layout fixes)
Include these artifacts in PR description or handoff notes:
- Input/output file paths and processed page list.
- `qpdf --check` output.
- `pdfinfo -box` output confirming unchanged trim/bleed intent.
- `pdffonts` summary after final normalization.
- Before/after rendered evidence (`pdftoppm`) for all changed pages.
- Pixel-metric summary for old-corner suppression and center-folio presence.
- Backup path for rollback (`*.pre-<fix>.pdf`).
- Keep actual client documents, full paths and visual evidence in approved restricted storage. Put only authorized, redacted evidence references in Git or PRs.
