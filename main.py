import argparse
import sys
from employee_processor import EmployeeData
from reports import ReportFactory


def main():
    parser = argparse.ArgumentParser(description="Employee report generator")
    parser.add_argument(
        "files",
        nargs="+",
        help="CSV files with employee data (one or more files)"
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=["payout"],
        help="Report type (e.g., payout)"
    )
    parser.add_argument(
        "--format",
        default="console",
        choices=["console", "json"],
        help="Output format (default: console)"
    )
    args = parser.parse_args()
    try:
        data = EmployeeData()
        data.process_files(args.files)
        report = ReportFactory.create_report(args.report)
        report.print_console(data)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
