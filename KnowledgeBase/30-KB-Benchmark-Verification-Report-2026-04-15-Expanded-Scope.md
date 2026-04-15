# 30 — KB Benchmark Verification Report (2026-04-15, Expanded Scope)

---

## Purpose
Document the expanded-scope benchmark evidence run that continues Q29 validation beyond the initial 20-question control check.

---

## Validation Scope
- ONNX security gate run in pinned container image
- Benchmark run via hardened Docker-only runner with pinned inputs and evidence artifacts
- Expanded sample size: 100 LongMemEval questions (`--limit 100`, raw/session mode)

---

## Hardened Controls Confirmed (Expanded Run)
1. **Container boundary enforced**
   - Execution via `KnowledgeBase/tools/run_mempalace_longmemeval_docker.sh`
2. **Pinned runtime image**
   - `python:3.12-slim@sha256:804ddf3251a60bbf9c92e73b7566c40428d54d0e79d3428194edf40da6521286`
3. **Pinned benchmark code**
   - MemPalace commit: `29bc868c899943c010c209f34f619c1ac4c544f8`
4. **Pinned dataset integrity**
   - `longmemeval_s_cleaned.json` SHA256: `d6f21ea9d60a0d56f34a05b609c79c88a451d2ae03597821ea3d5a9678c3a442`
5. **ONNX security gate**
   - ONNX floor check passed (`onnx==1.21.0`)
   - no `onnx.hub.load(..., silent=True)` usage detected
   - no `tarfile.extractall` usage detected
6. **Evidence artifact capture**
   - run metadata, pip freeze, benchmark stdout, benchmark JSONL output

---

## Evidence Artifacts
- Directory: `/tmp/mempalace-evidence/longmemeval_20260415T095109Z`
- Files:
  - `run_metadata.txt`
  - `pip_freeze.txt`
  - `benchmark_stdout.log`
  - `results_mempal_raw_session_20260415_0951.jsonl`

---

## Benchmark Output Summary (Limit=100)
- Runtime: 526.6s total (5.27s/question)
- Session-level:
  - Recall@1: 0.770
  - Recall@3: 0.900
  - Recall@5: 0.940
  - Recall@10: 0.980
  - Recall@30: 1.000
  - Recall@50: 1.000
  - NDCG@10: 0.874
- Turn-level: matched session-level metrics for this run
- Per-type (session recall_any@10):
  - multi-session: 1.000 (n=30)
  - single-session-user: 0.971 (n=70)

---

## Interpretation
- Hardened controls remain stable under expanded sample execution.
- Evidence confidence for the **method** is increased (20 → 100 sample scale).
- WeRa still does not treat external headline benchmark claims as fully verified baseline until full-scope reproducibility (larger/full dataset) is completed under the same controls.
