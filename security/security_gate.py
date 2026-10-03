
import json
import sys
from pathlib import Path

REPORT = Path("reports/bandit-report.json")

def main():
    if not REPORT.exists():
        print("BLOCKED: Security scan report was not generated.")
        sys.exit(1)

    try:
        data = json.loads(REPORT.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print("BLOCKED: Security report is invalid or unreadable.")
        sys.exit(1)

    results = data.get("results", [])
    high = [
        issue for issue in results
        if issue.get("issue_severity", "").upper() == "HIGH"
    ]

    print(f"Total findings: {len(results)}")
    print(f"High-severity findings: {len(high)}")

    for issue in high:
        print(
            f"- {issue.get('test_id')}: "
            f"{issue.get('issue_text')} "
            f"(file: {issue.get('filename')})"
        )

    if high:
        print("SECURITY GATE: BLOCKED")
        sys.exit(1)

    print("SECURITY GATE: PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
