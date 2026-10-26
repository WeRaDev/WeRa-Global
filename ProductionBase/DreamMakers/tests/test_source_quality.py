"""Quality-gate mechanics only; fixtures are temporary, synthetic Python text."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "ci/check_source.py"
SPEC = importlib.util.spec_from_file_location("dreammakers_source_check", CHECKER)
quality = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(quality)


class SourceQualityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "synthetic-project"
        for name in quality.SOURCE_DIRECTORIES:
            directory = self.root / name
            directory.mkdir(parents=True)
            (directory / "fixture.py").write_text("value = 1\n", encoding="utf-8")

    def cli(self, *extra):
        return subprocess.run(
            [
                sys.executable,
                "-B",
                "-I",
                str(CHECKER),
                "--root",
                str(self.root),
                *extra,
            ],
            cwd=self.temp.name,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_valid_sources(self):
        self.assertEqual(
            quality.check_sources(self.root), ["ci/fixture.py", "tests/fixture.py"]
        )

    def test_nested_sources_checked(self):
        directory = self.root / "ci/nested"
        directory.mkdir()
        (directory / "broken.py").write_text("def broken(:\n", encoding="utf-8")
        with self.assertRaises(quality.SourceError):
            quality.check_sources(self.root)

    def test_source_is_not_executed(self):
        marker = Path(self.temp.name) / "must-not-exist"
        (self.root / "ci/fixture.py").write_text(
            f"from pathlib import Path\nPath({str(marker)!r}).write_text('unsafe')\n"
            "raise RuntimeError('must not execute')\n",
            encoding="utf-8",
        )
        quality.check_sources(self.root)
        self.assertFalse(marker.exists())

    def test_assets_and_legacy_scripts_are_not_parsed(self):
        for directory in ("Input", "Output", "Result", "scripts", ".venv"):
            parent = self.root / directory
            parent.mkdir()
            (parent / "private.py").write_bytes(b"\xffdef broken(:")
        self.assertEqual(len(quality.check_sources(self.root)), 2)

    def test_missing_source_directory_fails(self):
        (self.root / "ci/fixture.py").unlink()
        (self.root / "ci").rmdir()
        with self.assertRaises(quality.SourceError):
            quality.check_sources(self.root)

    def test_empty_source_directory_fails(self):
        (self.root / "tests/fixture.py").unlink()
        with self.assertRaises(quality.SourceError):
            quality.check_sources(self.root)

    def test_invalid_encoding_fails(self):
        (self.root / "ci/fixture.py").write_bytes(b"\xff")
        with self.assertRaises(quality.SourceError):
            quality.check_sources(self.root)

    def test_invalid_and_newer_syntax_fail(self):
        for source in ("def broken(:\n", "return 1\n", "type Alias = int\n"):
            with self.subTest(source=source):
                (self.root / "ci/fixture.py").write_text(source, encoding="utf-8")
                with self.assertRaises(quality.SourceError):
                    quality.check_sources(self.root)

    def test_oversized_source_fails(self):
        (self.root / "ci/fixture.py").write_bytes(b"#" * (quality.MAX_SOURCE_BYTES + 1))
        with self.assertRaises(quality.SourceError):
            quality.check_sources(self.root)

    def test_file_symlink_fails(self):
        outside = Path(self.temp.name) / "outside.py"
        outside.write_text("value = 2\n", encoding="utf-8")
        (self.root / "ci/link.py").symlink_to(outside)
        with self.assertRaises(quality.SourceError):
            quality.check_sources(self.root)

    def test_directory_symlink_fails(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (self.root / "ci/link").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(quality.SourceError):
            quality.check_sources(self.root)

    def test_root_source_directory_symlink_fails(self):
        (self.root / "ci/fixture.py").unlink()
        (self.root / "ci").rmdir()
        (self.root / "ci").symlink_to(self.root / "tests", target_is_directory=True)
        with self.assertRaises(quality.SourceError):
            quality.check_sources(self.root)

    def test_cli_success_from_unrelated_directory(self):
        self.assertEqual(self.cli().returncode, 0)

    def test_cli_failure_does_not_echo_source(self):
        marker = "SYNTHETIC_PRIVATE_PAYLOAD"
        (self.root / "ci/fixture.py").write_text(
            f"{marker} def broken(:\n", encoding="utf-8"
        )
        result = self.cli()
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(marker, result.stdout + result.stderr)

    def test_no_discovered_tests_is_failure(self):
        result = self.cli("--tests")
        self.assertEqual(result.returncode, 1)

    def write_test(self, body):
        (self.root / "tests/test_synthetic_case.py").write_text(
            "import unittest\nclass Fixture(unittest.TestCase):\n"
            f"    def test_case(self):\n        {body}\n",
            encoding="utf-8",
        )

    def test_successful_synthetic_suite_exits_zero(self):
        self.write_test("self.assertEqual(1, 1)")
        self.assertEqual(self.cli("--tests").returncode, 0)

    def test_failing_synthetic_suite_exits_nonzero(self):
        self.write_test("self.assertEqual(1, 2)")
        self.assertEqual(self.cli("--tests").returncode, 1)

    def test_skipped_synthetic_suite_exits_nonzero(self):
        self.write_test("self.skipTest('synthetic-only')")
        self.assertEqual(self.cli("--tests").returncode, 1)


if __name__ == "__main__":
    unittest.main()
