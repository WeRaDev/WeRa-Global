# Bild execution readiness controls
This file operationalizes short-cycle readiness rules for Sprint 0–2.

## Stage gates
### Gate A: legal and data boundary
- Purchasing Agent Authorization Agreement template finalized.
- DPA template finalized.
- Explicit PII boundary documented (what cannot enter repository artifacts).

### Gate B: technical viability
- Session capture dry-run succeeds with no credential leakage.
- At least one authenticated read path to Leroy Merlin APIs is reproducible.
- API endpoint map is documented with status labels in `API_ENDPOINTS.md`.

### Gate C: controlled basket action
- End-to-end controlled basket creation works in pilot-safe environment.
- Failure modes and rollback/retry path documented.
- Evidence and risk labels updated in `docs/evidence-status.md`.

## Weekly cadence (KB-aligned)
- Track progress by object-level outcomes and blocked dependencies.
- Run weekly risk review against:
  - account suspension risk
  - session stability risk
  - endpoint drift risk
  - legal readiness risk
- Do not promote readiness claims without evidence-backed gate completion.

## Risk controls
- No production-like automation without signed legal package.
- No credential/session file storage in repository.
- No claim escalation from `hypothesis` to `verified` without reproducible artifacts.