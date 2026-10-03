
import unittest

from security.ai_risk import calculate_risk


class TestAIRisk(unittest.TestCase):

    def test_no_findings_is_low_risk(self):
        score, level = calculate_risk([])
        self.assertEqual(score, 0)
        self.assertEqual(level, "LOW")

    def test_high_severity_finding_is_high_risk(self):
        findings = [
            {
                "issue_severity": "HIGH",
                "issue_confidence": "HIGH",
            },
            {
                "issue_severity": "HIGH",
                "issue_confidence": "HIGH",
            },
        ]
        score, level = calculate_risk(findings)
        self.assertEqual(score, 20)
        self.assertEqual(level, "HIGH")

    def test_medium_severity_finding(self):
        findings = [
            {
                "issue_severity": "MEDIUM",
                "issue_confidence": "HIGH",
            }
        ]
        score, level = calculate_risk(findings)
        self.assertEqual(score, 5)
        self.assertEqual(level, "LOW")


if __name__ == "__main__":
    unittest.main()
