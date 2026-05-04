#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REQUIRED_BASELINE_PATHS = (
    "README.md",
    "WARP.md",
    "AGENTS.md",
    "SOUL.md",
    "CONTRIBUTING.md",
    ".gitea/workflows",
    "docs/adr",
    "tasks",
    "skills",
)
REQUIRED_REPO_FIELDS = (
    "id",
    "path",
    "default_branch",
    "status",
    "vcs_mode",
    "baseline_policy",
)
VALID_VCS_MODES = {"submodule", "native"}
VALID_BASELINE_POLICIES = {"delegated", "enforced"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def normalize_scalar(raw_value: str) -> str:
    value = raw_value.strip()
    if " #" in value:
        value = value.split(" #", 1)[0].strip()
    value = value.strip().strip("'\"")
    return value


def parse_repos_yaml(path: Path) -> list[dict[str, str]]:
    repos: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_repos = False

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped == "repos:":
            in_repos = True
            continue
        if not in_repos:
            continue
        if not stripped:
            continue
        if stripped.startswith("- id:"):
            if current is not None:
                repos.append(current)
            current = {"id": normalize_scalar(stripped.split(":", 1)[1])}
            continue
        if current is None:
            continue
        if ":" not in stripped:
            continue
        key, raw_value = stripped.split(":", 1)
        current[key.strip()] = normalize_scalar(raw_value)

    if current is not None:
        repos.append(current)
    return repos


def parse_gitmodules_paths(path: Path) -> set[str]:
    if not path.exists():
        return set()
    paths: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("path = "):
            continue
        paths.add(normalize_scalar(stripped.split("=", 1)[1]))
    return paths


def run_git_lines(root: Path, args: list[str]) -> tuple[int, list[str], str]:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
    )
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    return result.returncode, lines, result.stderr.strip()


def tracked_production_projects(root: Path, errors: list[str]) -> set[str]:
    code, lines, stderr = run_git_lines(root, ["ls-files"])
    if code != 0:
        errors.append(f"[git] unable to list tracked files: {stderr or 'unknown git error'}")
        return set()
    projects: set[str] = set()
    for line in lines:
        if not line.startswith("ProductionBase/"):
            continue
        parts = line.split("/")
        if len(parts) < 2 or not parts[1]:
            continue
        candidate = root / "ProductionBase" / parts[1]
        if candidate.is_dir():
            projects.add(parts[1])
    return projects


def tracked_gitlinks(root: Path, errors: list[str]) -> set[str]:
    code, lines, stderr = run_git_lines(root, ["ls-files", "--stage"])
    if code != 0:
        errors.append(f"[git] unable to list gitlinks: {stderr or 'unknown git error'}")
        return set()

    gitlinks: set[str] = set()
    for line in lines:
        if "\t" not in line:
            continue
        metadata, rel_path = line.split("\t", 1)
        parts = metadata.split()
        if not parts:
            continue
        if parts[0] == "160000":
            gitlinks.add(rel_path)
    return gitlinks


def project_name_from_path(path_value: str) -> str | None:
    path = Path(path_value)
    parts = path.parts
    if len(parts) < 2:
        return None
    if parts[0] != "ProductionBase":
        return None
    return parts[1]


def validate_registry(root: Path) -> list[str]:
    errors: list[str] = []
    registry_path = root / "ProductionBase" / "repos.yaml"
    if not registry_path.exists():
        return ["[registry] missing ProductionBase/repos.yaml"]

    repos = parse_repos_yaml(registry_path)
    if not repos:
        return ["[registry] no repositories parsed from ProductionBase/repos.yaml"]

    module_paths = parse_gitmodules_paths(root / ".gitmodules")
    gitlinks = tracked_gitlinks(root, errors)
    tracked_projects = tracked_production_projects(root, errors)

    ids_seen: set[str] = set()
    paths_seen: set[str] = set()
    registered_projects: set[str] = set()
    submodule_registry_paths: set[str] = set()

    for repo in repos:
        repo_id = repo.get("id", "")
        if not repo_id:
            errors.append("[registry] repository entry missing id")
        elif repo_id in ids_seen:
            errors.append(f"[registry] duplicate repository id '{repo_id}'")
        else:
            ids_seen.add(repo_id)

        for field in REQUIRED_REPO_FIELDS:
            if not repo.get(field):
                errors.append(f"[registry] repository '{repo_id or '<unknown>'}' missing field '{field}'")

        path_value = repo.get("path", "")
        if path_value in paths_seen:
            errors.append(f"[registry] duplicate repository path '{path_value}'")
        paths_seen.add(path_value)

        project_name = project_name_from_path(path_value)
        if project_name is None:
            errors.append(
                f"[registry] repository '{repo_id or '<unknown>'}' has invalid path '{path_value}' (must start with ProductionBase/)"
            )
            continue
        registered_projects.add(project_name)

        vcs_mode = repo.get("vcs_mode", "")
        baseline_policy = repo.get("baseline_policy", "")

        if vcs_mode not in VALID_VCS_MODES:
            errors.append(
                f"[registry] repository '{repo_id}' has invalid vcs_mode '{vcs_mode}' (expected one of {sorted(VALID_VCS_MODES)})"
            )
        if baseline_policy not in VALID_BASELINE_POLICIES:
            errors.append(
                f"[registry] repository '{repo_id}' has invalid baseline_policy '{baseline_policy}' (expected one of {sorted(VALID_BASELINE_POLICIES)})"
            )

        project_path = root / path_value
        if vcs_mode == "native":
            if not project_path.exists():
                errors.append(f"[registry] native repository '{repo_id}' path does not exist: {path_value}")
            if path_value in module_paths:
                errors.append(
                    f"[registry] native repository '{repo_id}' path appears in .gitmodules and should be submodule mode: {path_value}"
                )
            if baseline_policy == "enforced":
                for required in REQUIRED_BASELINE_PATHS:
                    if not (project_path / required).exists():
                        errors.append(
                            f"[baseline] native repository '{repo_id}' missing required baseline path: {path_value}/{required}"
                        )

        if vcs_mode == "submodule":
            submodule_registry_paths.add(path_value)
            if path_value not in module_paths:
                errors.append(
                    f"[submodule] repository '{repo_id}' marked submodule but missing from .gitmodules: {path_value}"
                )
            if path_value not in gitlinks:
                errors.append(
                    f"[submodule] repository '{repo_id}' marked submodule but path is not tracked as gitlink: {path_value}"
                )
            if baseline_policy != "delegated":
                errors.append(
                    f"[baseline] submodule repository '{repo_id}' must use delegated baseline_policy (found '{baseline_policy}')"
                )

    missing_registration = sorted(tracked_projects - registered_projects)
    if missing_registration:
        errors.append(
            f"[registry] tracked ProductionBase projects missing from registry: {', '.join(missing_registration)}"
        )

    stale_registration = sorted(registered_projects - tracked_projects)
    if stale_registration:
        errors.append(
            f"[registry] registry contains non-tracked ProductionBase projects: {', '.join(stale_registration)}"
        )

    extra_modules = sorted(module_paths - submodule_registry_paths)
    if extra_modules:
        errors.append(
            f"[submodule] .gitmodules contains paths not declared as submodule repos in registry: {', '.join(extra_modules)}"
        )

    orphan_gitlinks = sorted(path for path in gitlinks if path not in module_paths)
    if orphan_gitlinks:
        errors.append(
            f"[submodule] orphan gitlinks tracked without .gitmodules mapping: {', '.join(orphan_gitlinks)}"
        )

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate ProductionBase repository registry, baseline policy, and submodule structure."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root path to validate (defaults to auto-detected repo root).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve() if args.root is not None else repo_root()
    errors = validate_registry(root)

    if errors:
        print("productionbase_registry_validate: FAILED")
        for item in errors:
            print(f"- {item}")
        return 1

    print("productionbase_registry_validate: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
