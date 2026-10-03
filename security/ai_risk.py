
import json
import sys
from pathlib import Path

REPORT = Path("reports/bandit-report.json")

SEVERITY_WEIGHTS = {
    "HIGH": 10,
    "MEDIUM": 5,
    "LOW": 2,
}

CONFIDENCE_WEIGHTS = {
    "HIGH": 1.0,
    "MEDIUM": 0.7,
    "LOW": 0.4,
}


def calculate_risk(findings):
    score = 0

    for issue in findings:
        severity = issue.get("issue_severity", "LOW").upper()
        confidence = issue.get("issue_confidence", "LOW").upper()

        weight = SEVERITY_WEIGHTS.get(severity, 2)
        confidence_factor = CONFIDENCE_WEIGHTS.get(confidence, 0.4)

        score += weight * confidence_factor

    score = min(round(score), 100)

    if score >= 20:
        level = "HIGH"
    elif score >= 8:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level


def main():
    if not REPORT.exists():
        print("ERROR: Bandit report not found.")
        sys.exit(1)

    try:
        data = json.loads(REPORT.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print("ERROR: Bandit report is invalid or unreadable.")
        sys.exit(1)

    findings = data.get("results", [])
    score, level = calculate_risk(findings)

    print(f"Total findings: {len(findings)}")
    print(f"AI risk score: {score}/100")
    print(f"Risk level: {level}")

    if level == "HIGH":
        print("AI RISK CHECK: BLOCKED")
        sys.exit(1)

    print("AI RISK CHECK: PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
