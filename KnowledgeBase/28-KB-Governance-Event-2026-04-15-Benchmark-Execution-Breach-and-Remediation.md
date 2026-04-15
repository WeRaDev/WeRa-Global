# 28 — Governance Event: Benchmark Execution Breach and Remediation (2026-04-15)

---

## Event Type
`governance/security/process-breach`

---

## Summary
A benchmark command was executed directly on host before the Docker-only execution policy and security gate were fully enforced for Q29/Q32 validation.

This event records the breach, impact, and corrective controls now in place.

---

## What Happened
- Host-level benchmark execution occurred during early Q29 evidence gathering.
- The run attempted model artifact retrieval outside the later-approved containerized workflow.
- Execution did not satisfy the final governance requirement: benchmark evidence must originate from Docker-only runs.

---

## Impact Assessment
- **Policy compliance impact**: medium (process violation)
- **Security exposure impact**: limited but non-zero (host touched model download path before hardening gate)
- **Evidence validity impact**: host-run evidence downgraded; excluded from `verified` basis

---

## Corrective Actions Implemented
1. Docker-only benchmark runner hardened with pinned inputs:
   - pinned Docker image digest
   - pinned MemPalace commit
   - pinned dataset SHA256 verification
2. ONNX security checks hardened for reliable source scanning and version floor enforcement.
3. Governance workflow gate updated to require containerized evidence and security checks.
4. Security policy formalized with CVE-specific controls and incident triggers.
5. Q29/Q32 evidence policy updated: host-run outputs are non-authoritative.

---

## Preventive Controls (Going Forward)
- No benchmark commands executed directly on host.
- Only `tools/run_mempalace_longmemeval_docker.sh` evidence accepted for Q29 benchmark claims.
- ONNX security check (`tools/security_checks_onnx.sh`) required prior to benchmark claim promotion.
- Any violation triggers governance event entry and `12-Open-Questions.md` update.

---

## Ownership
- **Event owner**: KB governance owner
- **Remediation owner**: technical steward
- **Evidence reviewer**: KB steward

---

## Closure Criteria
- Containerized benchmark evidence archived with pinned metadata.
- Security checks pass under policy floor.
- Q29/Q32 status notes reflect stricter evidence bar and breach handling.
