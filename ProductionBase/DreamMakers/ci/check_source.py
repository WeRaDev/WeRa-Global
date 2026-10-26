#!/usr/bin/env python3
"""Check only ci/ and tests/; never load legacy pipelines or customer assets."""

from __future__ import annotations

import argparse
import ast
from pathlib import Path
import sys
import unittest

SOURCE_DIRECTORIES = ("ci", "tests")
MAX_SOURCE_BYTES = 2_000_000


class SourceError(ValueError):
    pass


def check_sources(root: Path) -> list[str]:
    """Parse and compile tooling sources without executing or importing them."""
    root = root.resolve()
    checked = []
    for directory in SOURCE_DIRECTORIES:
        parent = root / directory
        if parent.is_symlink() or not parent.is_dir():
            raise SourceError(f"{directory}: missing directory or symlink")
        sources = []
        pending = [parent]
        while pending:
            for path in sorted(pending.pop().iterdir()):
                relative = path.relative_to(root).as_posix()
                if path.is_symlink() or not path.resolve().is_relative_to(root):
                    raise SourceError(f"{relative}: symlinks are forbidden")
                if path.is_dir():
                    if path.name != "__pycache__":
                        pending.append(path)
                elif path.suffix == ".py":
                    if not path.is_file() or path.stat().st_size > MAX_SOURCE_BYTES:
                        raise SourceError(f"{relative}: invalid source or size limit")
                    sources.append(path)
        if not sources:
            raise SourceError(f"{directory}: no Python sources")
        for path in sorted(sources):
            relative = path.relative_to(root).as_posix()
            try:
                source = path.read_text(encoding="utf-8")
                tree = ast.parse(source, filename=relative, feature_version=(3, 11))
                compile(tree, relative, "exec", dont_inherit=True)
            except (SyntaxError, ValueError, UnicodeError, RecursionError) as exc:
                # Do not echo source lines or exception payloads into CI logs.
                raise SourceError(
                    f"{relative}: invalid Python 3.11-compatible source"
                ) from exc
            checked.append(relative)
    return checked


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument(
        "--tests",
        action="store_true",
        help="Also execute only the synthetic test_*.py suite in tests/.",
    )
    args = parser.parse_args(argv)
    try:
        checked = check_sources(args.root)
        print(
            f"PASS: {len(checked)} tooling/test sources compile; no conversion code executed."
        )
        if args.tests:
            suite = unittest.defaultTestLoader.discover(
                str(args.root.resolve() / "tests"), pattern="test_*.py"
            )
            if not suite.countTestCases():
                raise SourceError("no synthetic tests discovered")
            result = unittest.TextTestRunner(verbosity=2).run(suite)
            if not result.wasSuccessful() or result.skipped:
                return 1
        return 0
    except SourceError as exc:
        print(f"dreammakers-quality: FAILED: {exc}", file=sys.stderr)
        return 1
    except (OSError, ImportError):
        print(
            "dreammakers-quality: FAILED; missing, unreadable or invalid tooling/test sources, "
            "or unreadable synthetic tests.",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
