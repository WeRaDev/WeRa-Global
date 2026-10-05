---
title: "WeRa Cloud / Inteligenta — Internal BaaS Pilot Charter"
date: "2026-09-28"
type: "internal-pilot-charter"
status: "founder-directed"
owner: "Inteligente Razão LDA"
related_docs:
  - "2026-05-18-concept-note-wera-cloud-rnd.md"
  - "../../../../../../../ProductionBase/SolarCity/tasks/backlog.md"
---

# WeRa Cloud / Inteligenta — Internal BaaS Pilot Charter

## Purpose
Prove that WeRa Cloud can host and support a consultancy as a Business-as-a-Software (BaaS) tenant. Inteligenta is the first internal technical pilot, operated by Inteligente Razão LDA, the solo-founder company incubating WeRa Global.

## Operating model and ownership
- **WeRa Cloud** provides the hosting and platform layer.
- **Inteligenta** provides the first consultancy business context and operating workflows.
- **Owner:** Inteligente Razão LDA owns the platform and Inteligenta processes, including technical operations and approval of outputs.
- **Decision rights:** consequential decisions remain with a human. Agents may assist or propose, but do not replace human approval.

## Scope
- Internal consultancy business automation only.
- Limit process scope to Human Center customer work.
- The system is used internally; this charter does not authorize customer-facing access or a finished-product claim.
- Use synthetic data for the technical smoke test. This charter does not authorize connecting a customer's account or using live customer data.

## Exclusions and legal timing
- Tokenization and Tokenized Service-Financing are out of scope.
- No claim that WeRa Cloud or the BaaS implementation is a finished product.
- The separate Financial Automation pilot is not part of this BaaS pilot.
- Per founder direction, customer-facing legal prerequisites are deferred until onboarding a real external WeRa Cloud customer. Revisit them before that onboarding.

## Timebox and budget
- **Duration:** one week, 2026-09-28 through 2026-10-05.
- **Host:** existing Frank machine (SolarSeed TRL4).
- **Cash budget:** €0. Do not incur paid hosting, API, license, hardware, or other spend. Stop and request a human decision if a paid dependency appears necessary.

## Technical completion gate
The delayed design-thinking session may begin only after the SolarCity framework is shown to work technically on Frank. This is a technical smoke-readiness gate, not completion of the 72-hour Phase 6 experiment, external customer validation, or product-market validation.

Evidence required for a human to mark the gate complete:
- The deployed SolarCity source revision is identified and traceable; do not deploy from an uncommitted or unverified working tree.
- Storage backing and backup/restore readiness are verified before using or growing City container storage.
- The City deployment does not disrupt the existing FilantropiaSolar services; in particular, port 8069 ownership is resolved without displacing Filantropia Odoo.
- Required framework services report healthy, and the operator UI/gateway and Spirit health checks succeed.
- A synthetic end-to-end smoke test demonstrates the human approval path. No customer data or paid external inference is used.
- The repository-native SolarCity tests and compose validation pass. GPU/local-inference status is explicitly evidenced; a CPU-only or inference-disabled fallback requires human acceptance and must not be described as full inference readiness.
- Results and any accepted limitations are recorded in the SolarCity operational report.

## Current evidence and status
The SolarCity reports from 2026-09-25 marked the Frank gate blocked. A live, read-only SSH recheck on 2026-09-28 confirmed:
- `/data-bulk` resolves to `/dev/sda7[/data-bulk]`, the root filesystem; `/dev/sdb1` is listed as an unmapped `crypto_LUKS` partition. The separate `/data` mount is on `/dev/mapper/data_crypt`.
- `/etc/crypttab` declares the `data_bulk` mapping, but it is not active. `/etc/fstab` includes both a mapper mount and a same-path bind entry for `/data-bulk`; this configuration has not been changed or validated for recovery.
- Eight systemd units are failed: the four NVIDIA/module-load units and `user@0`, `user@1000`, `user@110`, and `user@996`. `nvidia-smi` cannot communicate with the NVIDIA driver.
- Docker uses `/data-bulk/docker`. Five Filantropia containers are running; no City containers or City Docker network are present.
- `filantropia-odoo` is stopped (reported as exited 27 hours earlier), and no process was listening on port 8069 during this check. The earlier 8069 conflict is not currently active, but the existing Odoo service and data must be preserved.
- `/home/wera/SolarCity` has no Git metadata, and the deployed `scripts/preflight.sh` is absent. Backup directory metadata includes files through 2026-08-30; no restore test was performed.
- The inspected local `scripts/preflight.sh` was streamed to Frank for read-only execution, not copied there. Root space and memory passed; systemd, GPU, OpenFang, and llama.cpp checks failed, yielding exit status 1.

## Human-directed pause
On 2026-09-28, the founder directed that `/data-bulk` remain untouched while a human handles storage restoration offline. GPU restoration is also in progress; wait for the founder’s report before further Frank action or choosing a CPU-only/inference-disabled fallback. The technical gate remains **BLOCKED** during this pause.

Detailed host recovery actions remain in `ProductionBase/SolarCity/tasks/backlog.md`. Storage, Docker, systemd, port, and deployed-data changes require an explicit human review of the exact operation and rollback before execution.

## Gate decision
The gate owner is the human decision-maker for Inteligente Razão LDA. No host services or files were modified. The design-thinking session remains deferred until the technical evidence above is reviewed and accepted.
