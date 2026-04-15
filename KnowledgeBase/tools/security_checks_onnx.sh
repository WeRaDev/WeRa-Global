#!/usr/bin/env bash
set -euo pipefail

# Security checks for ONNX-related risk controls used by KB benchmark workflows.
# Intended to run inside CI/containerized environments.

TARGET_DIR="${1:-.}"

python3 - <<'PY'
import sys
try:
    import onnx  # type: ignore
except Exception as exc:
    print(f"[FAIL] onnx import failed: {exc}")
    sys.exit(1)

version = tuple(int(x) for x in onnx.__version__.split(".")[:3])
required = (1, 21, 0)
if version < required:
    print(f"[FAIL] onnx version {onnx.__version__} < 1.21.0")
    sys.exit(1)
print(f"[OK] onnx version {onnx.__version__} meets minimum 1.21.0")
PY

MATCH_FOUND=0
while IFS= read -r -d '' file; do
  if grep -nE "onnx\.hub\.load\(.*silent\s*=\s*True" "$file"; then
    MATCH_FOUND=1
  fi
done < <(
  find "${TARGET_DIR}" -type f \
    \( -name "*.py" -o -name "*.sh" -o -name "*.yaml" -o -name "*.yml" \) \
    ! -name "security_checks_onnx.sh" \
    ! -path "*/.git/*" \
    ! -path "*/.venv/*" -print0
)
if [[ "${MATCH_FOUND}" -eq 1 ]]; then
  echo "[FAIL] detected onnx.hub.load(..., silent=True) usage"
  exit 1
fi
echo "[OK] no onnx.hub.load(..., silent=True) usage found"
TAR_WARN=0
while IFS= read -r -d '' file; do
  if grep -nE "tarfile\.extractall" "$file"; then
    TAR_WARN=1
  fi
done < <(
  find "${TARGET_DIR}" -type f \
    \( -name "*.py" -o -name "*.sh" \) \
    ! -name "security_checks_onnx.sh" \
    ! -path "*/.git/*" \
    ! -path "*/.venv/*" -print0
)
if [[ "${TAR_WARN}" -eq 1 ]]; then
if [[ -n "${CODE_FILES}" ]] && grep -nE "tarfile\.extractall" ${CODE_FILES}; then
  echo "[WARN] tarfile.extractall found; review for path traversal protections"
else
  echo "[OK] no tarfile.extractall usage found in target tree"
fi
