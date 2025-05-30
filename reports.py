import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Union


class Report(ABC):
    @abstractmethod
    def generate(self, data) -> List[Dict[str, Any]]:
        pass

    def print_console(self, data):
        departments = {}
        for emp in data.employees:
            dept = emp["department"]
            if dept not in departments:
                departments[dept] = []
            departments[dept].append(emp)
        col_widths = {
            'name': 20,
            'hours': 8,
            'rate': 8,
            'payout': 10
        }
        row_format = "| {:<20} | {:>6} | {:>6} | {:>8} |"
        print(row_format.format("Department/Name", "Hours", "Rate", "Payout"))
        print("|" + "-" * 22 + "|" + "-" * 8 + "|" + "-" * 8 + "|" + "-" * 10 + "|")
        for dept, employees in departments.items():
            print(f"| {dept}")
            total_hours = 0
            total_payout = 0
            for emp in employees:
                name = emp.get("name", "")
                hours = emp["hours_worked"]
                rate = emp["hourly_rate"]
                payout = hours * rate
                total_hours += hours
                total_payout += payout

                print(row_format.format(
                    "  " + name, hours, rate, f"${payout}"
                ))
            print(row_format.format(
                "", total_hours, "", f"${total_payout}"
            ))
            print()


class PayoutReport(Report):
    def generate(self, data) -> List[Dict[str, Any]]:
        if not hasattr(data, 'employees') or not data.employees:
            return []
        department_stats = {}
        for emp in data.employees:
            dept = emp["department"]
            hours = emp["hours_worked"]
            payout = hours * emp["hourly_rate"]
            if dept not in department_stats:
                department_stats[dept] = {
                    "count": 0,
                    "total_hours": 0,
                    "total_payout": 0.0
                }
            department_stats[dept]["count"] += 1
            department_stats[dept]["total_hours"] += hours
            department_stats[dept]["total_payout"] += payout
        report = []
        for dept, stats in sorted(department_stats.items()):
            avg = stats["total_payout"] / stats["count"]
            report.append({
                "Department": dept,
                "Count": stats["count"],
                "Hours": stats["total_hours"],
                "Payout": round(stats["total_payout"], 2),
                "Avg": round(avg, 2)
            })
        return report


class ReportFactory:
    reports = {"payout": PayoutReport}

    @staticmethod
    def create_report(report_name: str) -> Report:
        report_class = ReportFactory.reports.get(report_name.lower())
        if not report_class:
            raise ValueError(f"Unsupported report type: {report_name}")
        return report_class()