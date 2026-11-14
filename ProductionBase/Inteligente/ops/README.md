# Inteligente operations

Operational evidence for WeRa Hosting and Inteligente-related Odoo/edge workloads.

## Purpose

This folder holds **read-only discovery artifacts**, baseline alignment notes, and runbooks.

**Architecture baseline (current):**
`Resources/Documents/Research/WeRa_Hosting_Shared_Odoo_Platform_v3.md`
— shared multi-company / multi-website Odoo platform; confidentiality mandatory; shared lifecycle accepted.

**Historical (superseded as default):**
`Resources/Documents/Research/WeRa_Hosting_Final_Research_and_Architecture.md`
— separate client-stack recommendation (v2).

No document here authorizes production restructuring by itself. State-changing work needs explicit owner approval.

## Contents

| Document | Role |
|----------|------|
| `v3-shared-platform-baseline-g1-delta-2026-11-14.md` | **Active ops baseline** — v3 decisions, G1 delta, wave plan, InCity exception recommendation |
| `g1-inventory-frank-odoo-2026-11-13.md` | **G1 Inventory** — domain → host → runtime → DB → filestore map |
| `owner-decisions-wave1-2026-11-14.md` | **Phase 0** — owner confirmations (draft defaults) |
| `delta-discovery-access-recovery-2026-11-14.md` | **Phase 1** — users/ACL/sharing/mail/backup signals |
| `wave1-design-package-2026-11-14.md` | **Phase 2** — matrices, tests, backup/edge design, change checklist |
| `service-limitations-shared-platform-wave1.md` | Internal/commercial limits one-pager (draft) |
| `incity/` | **InCity on Frank** — community Odoo 19 shim, compose template, backup evidence |

**Execution hold:** Phase 3 (edge/ACL prod) and Phase 4 (copy/restore drills) need explicit owner approval per change.

## Rules

- Never commit secrets, tunnel credentials, DB passwords, or admin passwd values.
- Prefer tenant IDs over hostnames as durable keys.
- Label facts as **observed**, decisions as **decided**/**proposed**, and completed work as **done**.
- Do not reintroduce v2 per-client split work unless a v3 §6.4 exception is explicitly approved.
- Re-run inventory after material host changes; keep dated filenames or update `last_verified_at`.

## Related

- Current research baseline: `../Resources/Documents/Research/WeRa_Hosting_Shared_Odoo_Platform_v3.md`
- Historical v2 research: `../Resources/Documents/Research/WeRa_Hosting_Final_Research_and_Architecture.md`
- SolarSeed TRL ops: `../../SolarSeed-v3/WARP.md` (Frank = `wera-ss-pt-sn-1`)
- Odoo multi-site restore skill (agent): odoo-trl4-restore-operations
