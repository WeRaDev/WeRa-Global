from pathlib import Path


def test_required_scaffold_files_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    required = [
        root / "README.md",
        root / "WARP.md",
        root / "CONTRIBUTING.md",
        root / "requirements.txt",
        root / "API_ENDPOINTS.md",
        root / "session_test.py",
        root / "har_extract.py",
        root / "src" / "bild" / "session_state.py",
        root / "src" / "bild" / "har_endpoints.py",
        root / "docs" / "evidence-status.md",
        root / "tasks" / "execution-readiness.md",
        root / "docs" / "adr" / "0001-session-architecture.md",
        root / "docs" / "adr" / "0002-anti-bot-fallback-policy.md",
        root / "docs" / "adr" / "0003-compliance-data-boundary.md",
    ]
    for path in required:
        assert path.exists(), f"Missing expected scaffold file: {path}"
