# 29 — KB Benchmark Verification Report (2026-04-15)

---

## Purpose
Document execution evidence for the hardened benchmark workflow introduced for Q29/Q32 validation.

---

## Validation Scope
- Security gate run in pinned container image
- Benchmark run via hardened Docker-only runner with pinned inputs and evidence artifacts
- Sample size: 20 LongMemEval questions (`--limit 20`, raw/session mode)

---

## Hardened Controls Verified
1. **Container boundary enforced**
   - Benchmark executed via `KnowledgeBase/tools/run_mempalace_longmemeval_docker.sh`
2. **Pinned runtime image**
   - `python:3.12-slim@sha256:804ddf3251a60bbf9c92e73b7566c40428d54d0e79d3428194edf40da6521286`
3. **Pinned benchmark code**
   - MemPalace commit: `29bc868c899943c010c209f34f619c1ac4c544f8`
4. **Pinned dataset integrity**
   - `longmemeval_s_cleaned.json` SHA256: `d6f21ea9d60a0d56f34a05b609c79c88a451d2ae03597821ea3d5a9678c3a442`
5. **ONNX security gate**
   - `onnx>=1.21.0` floor satisfied
   - no `onnx.hub.load(..., silent=True)` usage detected
   - no `tarfile.extractall` usage detected in scanned target
6. **Evidence artifact capture**
   - run metadata, pip freeze, benchmark stdout, benchmark JSONL output

---

## Evidence Artifacts
- Directory: `/tmp/mempalace-evidence/longmemeval_20260415T091741Z`
- Files:
  - `run_metadata.txt`
  - `pip_freeze.txt`
  - `benchmark_stdout.log`
  - `results_mempal_raw_session_20260415_0918.jsonl`

---

## Benchmark Output Summary (Limit=20)
- Runtime: 117.1s total (5.85s/question)
- Session-level:
  - Recall@1: 0.650
  - Recall@3: 0.750
  - Recall@5: 0.800
  - Recall@10: 0.950
  - Recall@30: 1.000
  - Recall@50: 1.000
  - NDCG@10: 0.778
- Turn-level: matched session-level metrics for this run

---

## Interpretation
- The **hardening controls are operationally verified** (containerization, pinning, integrity checks, and evidence capture).
- This run is sufficient to validate the hardened method and governance gate behavior.
- This run is **not** sufficient to promote broad benchmark headline claims to fully verified WeRa baseline; full-scope reproducibility (larger benchmark coverage) remains a separate step.
