#!/usr/bin/env bash
set -euo pipefail

# Docker-only runner for MemPalace LongMemEval dry-runs.
# Benchmark execution is performed inside a container by policy.

WORK_DIR="${WORK_DIR:-/tmp/mempalace-bench}"
DATA_DIR="${DATA_DIR:-/tmp/longmemeval-data}"
EVIDENCE_DIR="${EVIDENCE_DIR:-/tmp/mempalace-evidence}"
LIMIT="${LIMIT:-20}"
PY_IMAGE="${PY_IMAGE:-python:3.12-slim@sha256:804ddf3251a60bbf9c92e73b7566c40428d54d0e79d3428194edf40da6521286}"
MEMPALACE_REPO="${MEMPALACE_REPO:-https://github.com/MemPalace/mempalace}"
MEMPALACE_COMMIT="${MEMPALACE_COMMIT:-29bc868c899943c010c209f34f619c1ac4c544f8}"
DATASET_NAME="${DATASET_NAME:-longmemeval_s_cleaned.json}"
DATASET_URL="${DATASET_URL:-https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned/resolve/main/longmemeval_s_cleaned.json}"
DATASET_SHA256="${DATASET_SHA256:-d6f21ea9d60a0d56f34a05b609c79c88a451d2ae03597821ea3d5a9678c3a442}"

mkdir -p "${WORK_DIR}" "${DATA_DIR}" "${EVIDENCE_DIR}"
RUN_TS="$(date -u +"%Y%m%dT%H%M%SZ")"
RUN_EVIDENCE_DIR="${EVIDENCE_DIR}/longmemeval_${RUN_TS}"
mkdir -p "${RUN_EVIDENCE_DIR}"

if [[ ! -d "${WORK_DIR}/.git" ]]; then
  git clone "${MEMPALACE_REPO}" "${WORK_DIR}"
else
  git -C "${WORK_DIR}" remote set-url origin "${MEMPALACE_REPO}"
fi
git -C "${WORK_DIR}" fetch --all --tags --prune
git -C "${WORK_DIR}" fetch origin "${MEMPALACE_COMMIT}" --depth 1 || true
git -C "${WORK_DIR}" checkout -f "${MEMPALACE_COMMIT}"

if [[ ! -f "${DATA_DIR}/${DATASET_NAME}" ]]; then
  curl -fsSL \
    -o "${DATA_DIR}/${DATASET_NAME}" \
    "${DATASET_URL}"
fi
ACTUAL_DATASET_SHA256="$(shasum -a 256 "${DATA_DIR}/${DATASET_NAME}" | awk '{print $1}')"
if [[ "${ACTUAL_DATASET_SHA256}" != "${DATASET_SHA256}" ]]; then
  echo "Dataset SHA256 mismatch for ${DATASET_NAME}" >&2
  echo "Expected: ${DATASET_SHA256}" >&2
  echo "Actual:   ${ACTUAL_DATASET_SHA256}" >&2
  exit 1
fi

cat > "${RUN_EVIDENCE_DIR}/run_metadata.txt" <<EOF
runner_script=KnowledgeBase/tools/run_mempalace_longmemeval_docker.sh
timestamp_utc=${RUN_TS}
docker_image=${PY_IMAGE}
mempalace_repo=${MEMPALACE_REPO}
mempalace_commit=${MEMPALACE_COMMIT}
dataset_name=${DATASET_NAME}
dataset_url=${DATASET_URL}
dataset_sha256=${DATASET_SHA256}
limit=${LIMIT}
EOF

docker run --rm \
  -v "${WORK_DIR}:/workspace" \
  -v "${DATA_DIR}:/data" \
  -v "${RUN_EVIDENCE_DIR}:/evidence" \
  -w /workspace \
  "${PY_IMAGE}" \
  bash -lc "
    set -euo pipefail
    python -m pip install --no-cache-dir --upgrade pip
    python -m pip install --no-cache-dir chromadb pyyaml 'onnx>=1.21.0'
    python -m pip freeze > /evidence/pip_freeze.txt
    python benchmarks/longmemeval_bench.py /data/${DATASET_NAME} --limit ${LIMIT} | tee /evidence/benchmark_stdout.log
    cp benchmarks/results_mempal_raw_session_*.jsonl /evidence/ 2>/dev/null || true
  "

echo "Evidence captured at: ${RUN_EVIDENCE_DIR}"
