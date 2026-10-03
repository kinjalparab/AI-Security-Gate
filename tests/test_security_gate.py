
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SECURITY_GATE = PROJECT_ROOT / "security" / "security_gate.py"


class TestSecurityGate(unittest.TestCase):

    def run_gate(self, findings):
        with tempfile.TemporaryDirectory() as temp_dir:
            report = Path(temp_dir) / "bandit-report.json"
            report.write_text(
                json.dumps({"results": findings}),
                encoding="utf-8",
            )

            # Run the gate in a temporary working directory
            # so the real Bandit report remains untouched.
            test_gate = SECURITY_GATE.read_text(encoding="utf-8")
            test_gate = test_gate.replace(
                'Path("reports/bandit-report.json")',
                f'Path(r"{report}")',
            )

            temporary_script = Path(temp_dir) / "security_gate.py"
            temporary_script.write_text(test_gate, encoding="utf-8")

            return subprocess.run(
                [sys.executable, str(temporary_script)],
                capture_output=True,
                text=True,
                cwd=temp_dir,
            )

    def test_high_severity_finding_blocks(self):
        result = self.run_gate([
            {
                "test_id": "TEST-HIGH",
                "issue_severity": "HIGH",
                "issue_text": "Simulated high-severity finding",
                "filename": "test_file.py",
            }
        ])

        self.assertEqual(result.returncode, 1)
        self.assertIn("SECURITY GATE: BLOCKED", result.stdout)

    def test_no_high_severity_findings_passes(self):
        result = self.run_gate([
            {
                "test_id": "TEST-LOW",
                "issue_severity": "LOW",
                "issue_text": "Simulated low-severity finding",
                "filename": "test_file.py",
            }
        ])

        self.assertEqual(result.returncode, 0)
        self.assertIn("SECURITY GATE: PASSED", result.stdout)


if __name__ == "__main__":
    unittest.main()
