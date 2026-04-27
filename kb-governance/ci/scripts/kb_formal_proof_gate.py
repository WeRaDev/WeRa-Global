#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

VALID_VERIFICATION_STATUSES = {"verified", "true", "pass", "passed"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def normalize_scalar(raw_value: str) -> str:
    value = raw_value.split("#", 1)[0].strip()
    value = value.strip().strip("`'\"")
    value = value.rstrip(",.;")
    value = value.strip("`'\"")
    return value


def is_operational_kb_doc(rel: str) -> bool:
    if not rel.endswith(".md"):
        return False
    if rel.startswith("KnowledgeBase/templates/"):
        return False
    return rel.startswith("KnowledgeBase/kb-") and "/docs/" in rel


def git_command(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
    )


def git_ref_exists(root: Path, ref_name: str) -> bool:
    result = git_command(root, ["rev-parse", "--verify", "--quiet", ref_name])
    return result.returncode == 0


def detect_diff_range(root: Path, explicit_base_ref: str | None) -> str | None:
    if explicit_base_ref:
        if git_ref_exists(root, explicit_base_ref):
            return f"{explicit_base_ref}...HEAD"
        return None
    env_diff_range = os.getenv("KB_FORMAL_PROOF_DIFF_RANGE", "").strip()
    if env_diff_range:
        return env_diff_range

    if git_ref_exists(root, "HEAD~1"):
        return "HEAD~1..HEAD"

    if git_ref_exists(root, "origin/main"):
        return "origin/main...HEAD"

    return None


def changed_files_from_git(root: Path, diff_range: str) -> list[str]:
    result = git_command(root, ["diff", "--name-only", diff_range])
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def extract_formal_proof_mapping(text: str) -> dict[str, str] | None:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip().lower() != "formal_proof:":
            continue

        mapping: dict[str, str] = {}
        cursor = index + 1
        while cursor < len(lines):
            candidate = lines[cursor]
            if not candidate.strip():
                cursor += 1
                continue

            if not (candidate.startswith("  ") or candidate.startswith("\t")):
                break

            stripped = candidate.strip()
            if ":" in stripped:
                key, value = stripped.split(":", 1)
                mapping[key.strip().lower()] = normalize_scalar(value)
            cursor += 1
        return mapping
    return None


def is_within_root(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def validate_formal_proof_contract(root: Path, doc_path: Path, errors: list[str]) -> None:
    rel = doc_path.relative_to(root).as_posix()
    text = read_text(doc_path)
    mapping = extract_formal_proof_mapping(text)
    if mapping is None:
        errors.append(f"[formal-proof] missing formal_proof block in {rel}")
        return

    required_keys = ("engine", "trl_phase", "obligation_id", "proof_artifact", "verification_status")
    missing = [key for key in required_keys if not mapping.get(key)]
    if missing:
        errors.append(f"[formal-proof] missing required key(s) {missing} in {rel}")
        return

    engine = normalize_scalar(mapping["engine"]).lower()
    if engine != "ml-hilbert":
        errors.append(
            f"[formal-proof] invalid engine '{mapping['engine']}' in {rel}; expected 'ml-hilbert'"
        )

    trl_phase = normalize_scalar(mapping["trl_phase"]).lower()
    if trl_phase != "trl6":
        errors.append(
            f"[formal-proof] invalid trl_phase '{mapping['trl_phase']}' in {rel}; expected 'TRL6'"
        )

    verification_status = normalize_scalar(mapping["verification_status"]).lower()
    if verification_status not in VALID_VERIFICATION_STATUSES:
        errors.append(
            f"[formal-proof] invalid verification_status '{mapping['verification_status']}' in {rel}; expected one of {sorted(VALID_VERIFICATION_STATUSES)}"
        )

    obligation_id = mapping["obligation_id"]
    artifact_rel = mapping["proof_artifact"].strip()
    if artifact_rel.startswith("/"):
        errors.append(f"[formal-proof] proof_artifact must be repository-relative in {rel}: {artifact_rel}")
        return

    artifact_path = root / artifact_rel
    if not is_within_root(root, artifact_path):
        errors.append(f"[formal-proof] proof_artifact escapes repository root in {rel}: {artifact_rel}")
        return

    if not artifact_path.exists():
        errors.append(f"[formal-proof] proof_artifact missing for {rel}: {artifact_rel}")
        return

    if artifact_path.suffix != ".lean":
        errors.append(
            f"[formal-proof] proof_artifact must be a .lean file for {rel}: {artifact_rel}"
        )
        return

    artifact_text = read_text(artifact_path)
    if re.search(r"\bsorry\b", artifact_text):
        errors.append(f"[formal-proof] proof artifact contains 'sorry': {artifact_rel}")

    if not re.search(r"\b(theorem|lemma)\b", artifact_text):
        errors.append(f"[formal-proof] proof artifact missing theorem/lemma declaration: {artifact_rel}")

    if obligation_id not in artifact_text:
        errors.append(
            f"[formal-proof] obligation_id '{obligation_id}' not referenced in proof artifact {artifact_rel}"
        )

    if "proof_engine: ml-hilbert" not in artifact_text.lower():
        errors.append(
            f"[formal-proof] proof artifact must declare 'proof_engine: ml-hilbert': {artifact_rel}"
        )


def collect_operational_docs(
    root: Path,
    scan_all: bool,
    explicit_files: Iterable[str],
    base_ref: str | None,
    errors: list[str],
) -> list[Path]:
    if explicit_files:
        selected: list[Path] = []
        for item in explicit_files:
            candidate = Path(item)
            if not candidate.is_absolute():
                candidate = root / candidate
            if candidate.exists():
                selected.append(candidate)
        return sorted({path.resolve() for path in selected})

    if scan_all:
        kb_root = root / "KnowledgeBase"
        if not kb_root.exists():
            errors.append("[formal-proof] missing KnowledgeBase/ root")
            return []
        docs = [
            path
            for path in kb_root.rglob("*.md")
            if is_operational_kb_doc(path.relative_to(root).as_posix())
        ]
        return sorted(docs)

    diff_range = detect_diff_range(root, base_ref)
    if diff_range is None:
        errors.append(
            "[formal-proof] unable to determine git diff range; provide --base-ref or run with --scan-all"
        )
        return []

    changed_rel_paths = changed_files_from_git(root, diff_range)
    docs: list[Path] = []
    for rel in changed_rel_paths:
        if not is_operational_kb_doc(rel):
            continue
        candidate = root / rel
        if candidate.exists():
            docs.append(candidate)
    return sorted({path.resolve() for path in docs})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate TRL6 formal proof contracts for changed KB operational documents."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root path to validate (defaults to auto-detected repo root).",
    )
    parser.add_argument(
        "--scan-all",
        action="store_true",
        help="Validate all KB operational docs under KnowledgeBase/kb-*/docs.",
    )
    parser.add_argument(
        "--base-ref",
        default=None,
        help="Git base ref used for changed-file detection (for example: origin/main).",
    )
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        help="Explicit file path to validate (can be repeated).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve() if args.root is not None else repo_root()
    errors: list[str] = []

    docs = collect_operational_docs(
        root=root,
        scan_all=args.scan_all,
        explicit_files=args.file,
        base_ref=args.base_ref,
        errors=errors,
    )

    if not errors and not docs:
        print("kb_formal_proof_gate: PASSED (no operational KB docs selected)")
        return 0

    for path in docs:
        validate_formal_proof_contract(root, path, errors)

    if errors:
        print("kb_formal_proof_gate: FAILED")
        for item in errors:
            print(f"- {item}")
        return 1

    print("kb_formal_proof_gate: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
