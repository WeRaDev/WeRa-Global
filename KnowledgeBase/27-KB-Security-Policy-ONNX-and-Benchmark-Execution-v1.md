# 27 — KB Security Policy: ONNX and Benchmark Execution v1

---

## Purpose
Define mandatory security controls for KB benchmark execution and model artifact handling, with explicit mitigation for known ONNX attack paths and supply-chain risks.

---

## Policy Scope
Applies to:
- Q29 benchmark reproducibility tasks
- Q32 CLI/MCP compatibility validation tasks
- Any benchmark, model download, or embedding workflow referenced in KB operations

---

## Mandatory Execution Boundary

1. **No direct benchmark tests on host machine**
- Benchmark runs are prohibited on host OS.
- Benchmark runs must execute inside Docker containers only.

2. **Approved execution path**
- Use `tools/run_mempalace_longmemeval_docker.sh` for LongMemEval dry-runs.
- Record command, image, dependency versions, and output in PR notes.
- Benchmark evidence is authoritative only when run metadata includes:
  - pinned container image digest
  - pinned benchmark code commit
  - pinned dataset SHA256

3. **Evidence label rule**
- If benchmark cannot complete, label claim as `unverified` and record blocker.
- Do not promote benchmark claims to `verified` without reproducible container logs.
- Any host-executed benchmark output is non-authoritative and cannot be used to promote `verified` status.

---

## ONNX Vulnerability Controls (Required)

### CVE-2024-7776 (path traversal in model archive extraction)
Risk:
- Malicious `.tar.gz` payload can write files outside intended directory, enabling overwrite and potential RCE.

Controls:
- Minimum version floor: `onnx >= 1.17.0` (superseded by stricter floor below).
- Block any unreviewed archive extraction paths.
- Require containerized execution and non-root runtime where possible.

### CVE-2026-34445 (ExternalDataInfo attribute injection, DoS/file bypass/object corruption)
Risk:
- Crafted ONNX model may abuse `setattr()` behavior to trigger memory abuse, offset bypass, or object corruption.

Controls:
- Minimum version floor: `onnx >= 1.21.0` (canonical policy floor).
- Reject lower versions during pre-run checks.
- Treat unknown model artifacts as untrusted until integrity checks pass.

### CVE-2026-28500 (`onnx.hub.load(..., silent=True)` trust bypass)
Risk:
- Trust verification bypass enables supply-chain attacks if model and manifest are replaced together.

Controls:
- Prohibit `onnx.hub.load(..., silent=True)` in project tooling.
- Validate SHA256 for downloaded model artifacts where available.
- Prefer pinned, reviewed artifact sources.

---

## Security Check Requirements

Before benchmark execution:
1. Run ONNX baseline checks:
   - `tools/security_checks_onnx.sh <target_dir>`
2. Confirm dependency floor:
   - ONNX version must be `>= 1.21.0`
3. Confirm container execution path:
   - benchmark command must run via Docker
4. Capture evidence:
   - command line, image digest/tag, pip package versions, benchmark output
   - benchmark code commit and dataset SHA256 verification output

If any check fails:
- stop run,
- classify claim as `unverified`,
- create/update item in `12-Open-Questions.md` with owner and remediation action.

---

## Incident Response Triggers
Trigger incident workflow when any of the following is detected:
- unexpected file writes outside intended cache/work directories
- integrity mismatch (hash mismatch, source drift)
- suspicious archive contents or traversal attempts
- unapproved ONNX version downgrade
- use of prohibited `silent=True` trust bypass

Response actions:
1. halt benchmark workflow
2. quarantine artifacts and container workspace
3. rotate affected credentials/tokens if exposure is plausible
4. file governance event and open-question entry with evidence
5. rerun only after remediation and review

---

## Operational Ownership
- **Security policy owner**: KB governance owner
- **Execution owner**: technical steward running benchmark workflows
- **Evidence reviewer**: KB steward (claim label authority)

---

## Compliance Status Labels
- `verified`: all required checks passed with reproducible container evidence
- `unverified`: evidence missing or check failure present
- `hypothesis`: conceptual claim not yet operationally tested
