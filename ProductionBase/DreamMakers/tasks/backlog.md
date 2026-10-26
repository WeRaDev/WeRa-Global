# Backlog

## Template
- **Title**:
- **Problem statement**:
- **Scope**:
- **Non-scope**:
- **Acceptance criteria**:
- **Dependencies**:
- **Validation plan**:
- **Status**: Backlog | Ready | In Progress | Review | Validated | Done

## Items
- **Title**: Automate folio visual validator for corner-to-center migrations
- **Problem statement**: Manual validation repeatedly finds residual corner folios and occasional clipping side effects after post-processing overlays.
- **Scope**: Build a reproducible checker that audits target pages for corner folios, centered folio presence, and body-text clipping risk in modified low-band regions.
- **Non-scope**: Full OCR-based proofreading or semantic content QA.
- **Acceptance criteria**:
  - Detect bottom-corner numeric folios on explicit page lists.
  - Emit pass/fail for center presence and corner suppression (pixel metrics).
  - Integrate with existing scripts and output machine-readable JSON.
- **Dependencies**: poppler (`pdftotext`, `pdftoppm`), Python image analysis stack.
- **Validation plan**:
  - Run checker on known-good and known-bad samples from this session.
  - Compare checker verdicts with human validator outcomes.
- **Status**: Ready
