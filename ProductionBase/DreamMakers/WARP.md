# DreamMakers WARP configuration
This file extends the umbrella `WARP.md` for `ProductionBase/DreamMakers`.

## Scope
- Project mission: a maintained WeRa self-publishing and marketing agency.
- Current implementation: reproducible PDF/EPUB book production, including non-destructive font substitution, page-number normalization, and print-ready box validation.
- Marketing automation is not established by the current source or baseline overlay.

## Rule precedence
1. Personal/global Warp rules
2. Umbrella `WARP.md`
3. This project `WARP.md`
4. Subdirectory-level rules (if created later)

The most specific rule takes precedence.
Project instructions may strengthen, but never waive, umbrella security floors.
`AGENTS.md` is the canonical agent instruction file; it and this file must remain
consistent with the project `SOUL.md`, which inherits the umbrella constitution.

## AgentBaseline pilot
- `mika` is the business and technical/security owner recorded in `security/agents/manifest.yaml`; ownership review remains pending.
- Run the locked standalone validator for composition changes. Structural success does not authenticate owners, approve controls, or grant runtime authority.
- The initial profile is `dev-sandbox`, with all 35 controls unassessed and runtime inventory unassessed. An empty agent list is not evidence of no deployed agents.
- Use synthetic document fixtures for development checks. Do not use manuscripts, author/customer records, campaign audiences or real service accounts in CI.
- Preserve originals and keep client assets, generated outputs, local environments and credentials out of source control.
- Publishing, marketing sends, purchases, client-data transfers and live account changes require separately approved scope and independent authority. This pilot enables none of them.
- Native umbrella registration, selected staging and CI activation remain separate approval gates. A nested workflow does not execute automatically in umbrella CI.
- Use the WARP Gitea account for commitments, not the owner account. Never stage, commit or push without explicit permission.

## Required project baseline
This repository must maintain:
- `README.md`
- `WARP.md`
- `AGENTS.md`
- `SOUL.md`
- `CONTRIBUTING.md`
- `.gitea/workflows/`
- `docs/adr/`
- `tasks/`
- `skills/`

## Delivery standards
- Plan before non-trivial changes.
- Keep changes atomic and reversible.
- Validate with explicit commands and attach evidence.
- Update documentation in the same delivery cycle as behavior changes.
- For EPUB production, treat the source PDF page 1 as a dedicated cover when it is image-only, omit a visible source TOC page when a clean EPUB navigation document is requested, and keep front matter separate from body chapters.
- For the confirmed Apple Books target, prefer semantic reflowable EPUB3 with selectable text, inline images, and original image assets; do not use PDF-sized fixed pixel canvases unless explicitly requested.
- When both DOCX and PDF sources are supplied, use DOCX as the primary semantic source for paragraphs, headings, images, and hyperlinks; use PDF as visual/reference evidence and fallback only.
- EPUB acceptance requires both automated package/TOC/link/image checks and manual reader verification; structural checks alone are not a visual pass.

## Quality and safety
- Do not commit secrets or sensitive data.
- Prefer deterministic scripts over manual click-path workflows.
- Preserve source fidelity for images and layout unless redesign is the explicit task.
- Document rollback expectations for format-changing operations.
- Preserve original embedded JPG/PNG assets without recompression whenever possible; use responsive CSS (`max-width: 100%`) rather than fixed page geometry for reflowable output.
- Verify cover separation, front-matter ordering, selectable text, inline image order, metadata, and clickable `nav.xhtml` targets in an Apple Books-oriented QA pass.
- Treat folio fixes as page-scoped operations first; avoid whole-document rewrites when validator provides an explicit page subset.
- For rotated pages (`/Rotate 180`) and non-zero page origins (`MediaBox` with non-zero lower-left), compute placement in visual coordinates and validate rendered output, not only raw stream coordinates.
- When overlay fallback is required, masks must be minimal and constrained to validated folio ROI; broad corner masks are not allowed.
