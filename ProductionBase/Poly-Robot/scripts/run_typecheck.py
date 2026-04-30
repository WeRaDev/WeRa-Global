#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DEV_REQUIREMENTS_PATH = ROOT_DIR / "requirements-dev.txt"
TYPECHECK_VENV_DIR = ROOT_DIR / ".venv" / "typecheck"


def _mypy_available() -> bool:
    return importlib.util.find_spec("mypy") is not None


def _venv_python_path() -> Path:
    if os.name == "nt":
        return TYPECHECK_VENV_DIR / "Scripts" / "python.exe"
    return TYPECHECK_VENV_DIR / "bin" / "python"


def _python_has_mypy(python_executable: Path) -> bool:
    probe_cmd = [
        str(python_executable),
        "-c",
        "import importlib.util,sys;sys.exit(0 if importlib.util.find_spec('mypy') else 1)",
    ]
    return subprocess.run(probe_cmd, cwd=ROOT_DIR, check=False).returncode == 0


def _install_dev_requirements(*, python_executable: Path) -> None:
    if not DEV_REQUIREMENTS_PATH.exists():
        raise RuntimeError(
            f"Missing dev requirements file at {DEV_REQUIREMENTS_PATH}"
        )
    upgrade_pip_cmd = [
        str(python_executable),
        "-m",
        "pip",
        "install",
        "--upgrade",
        "pip",
    ]
    print("[typecheck] ensuring pip in local typecheck venv", flush=True)
    upgraded = subprocess.run(upgrade_pip_cmd, cwd=ROOT_DIR, check=False)
    if upgraded.returncode != 0:
        raise RuntimeError("Failed to prepare local typecheck virtualenv.")

    install_cmd = [
        str(python_executable),
        "-m",
        "pip",
        "install",
        "-r",
        str(DEV_REQUIREMENTS_PATH),
    ]
    print(
        "[typecheck] mypy is not installed; bootstrapping dev requirements:",
        " ".join(install_cmd),
        flush=True,
    )
    completed = subprocess.run(install_cmd, cwd=ROOT_DIR, check=False)
    if completed.returncode != 0:
        raise RuntimeError(
            "Failed to install dev requirements required for typecheck."
        )


def _ensure_typecheck_venv() -> Path:
    venv_python = _venv_python_path()
    if not venv_python.exists():
        create_venv_cmd = [sys.executable, "-m", "venv", str(TYPECHECK_VENV_DIR)]
        print(
            "[typecheck] creating local typecheck virtualenv:",
            " ".join(create_venv_cmd),
            flush=True,
        )
        created = subprocess.run(create_venv_cmd, cwd=ROOT_DIR, check=False)
        if created.returncode != 0:
            raise RuntimeError("Failed to create local typecheck virtualenv.")
    if _python_has_mypy(venv_python):
        return venv_python

    _install_dev_requirements(python_executable=venv_python)
    return venv_python


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run Poly-Robot static type checks with automatic mypy bootstrap."
        )
    )
    parser.add_argument(
        "targets",
        nargs="*",
        default=["src/poly_robot"],
        help="mypy target paths or modules.",
    )
    parser.add_argument(
        "--pythonpath",
        default="src",
        help="Prefix to prepend to PYTHONPATH during typecheck.",
    )
    parser.add_argument(
        "--skip-bootstrap",
        action="store_true",
        help="Do not attempt to install mypy automatically if missing.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args, passthrough = parser.parse_known_args(argv)
    mypy_python = sys.executable

    if not _mypy_available():
        if args.skip_bootstrap:
            raise RuntimeError(
                "mypy is not installed and --skip-bootstrap was provided."
            )
        mypy_python = str(_ensure_typecheck_venv())

    env = os.environ.copy()
    if args.pythonpath:
        existing_pythonpath = env.get("PYTHONPATH")
        env["PYTHONPATH"] = (
            f"{args.pythonpath}{os.pathsep}{existing_pythonpath}"
            if existing_pythonpath
            else args.pythonpath
        )

    mypy_cmd = [mypy_python, "-m", "mypy", *args.targets, *passthrough]
    print("[typecheck] running:", " ".join(mypy_cmd), flush=True)
    return subprocess.call(mypy_cmd, cwd=ROOT_DIR, env=env)


if __name__ == "__main__":
    raise SystemExit(main())
