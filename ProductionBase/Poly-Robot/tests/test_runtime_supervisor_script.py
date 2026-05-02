from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def _load_runtime_supervisor_script_module():
    script_path = ROOT_DIR / "scripts" / "run_runtime_supervisor.py"
    module_spec = importlib.util.spec_from_file_location(
        "run_runtime_supervisor", script_path
    )
    if module_spec is None or module_spec.loader is None:
        raise AssertionError("Unable to load run_runtime_supervisor.py module")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


class RuntimeSupervisorScriptTests(unittest.TestCase):
    def test_secret_max_age_seconds_conversion_uses_ceiling_days(self) -> None:
        module = _load_runtime_supervisor_script_module()
        self.assertEqual(module._secret_max_age_days_from_seconds(1.0), 1)
        self.assertEqual(module._secret_max_age_days_from_seconds(86_400.0), 1)
        self.assertEqual(module._secret_max_age_days_from_seconds(86_401.0), 2)
        self.assertEqual(module._secret_max_age_days_from_seconds(172_800.0), 2)

    def test_agent_operator_backend_defaults_to_claude_api(self) -> None:
        module = _load_runtime_supervisor_script_module()
        args = module.build_arg_parser().parse_args([])
        self.assertEqual(args.agent_operator_backend, "claude_api")
        self.assertEqual(
            args.agent_operator_openfang_base_url,
            "http://127.0.0.1:4200",
        )
        self.assertEqual(args.agent_operator_openfang_advisory_agent_id, "")
        self.assertEqual(args.agent_operator_openfang_strategy_agent_id, "")


if __name__ == "__main__":
    unittest.main()
