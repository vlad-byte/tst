from typing import List, Dict


class EmployeeData:
    def __init__(self):
        self.employees: List[Dict] = []

    def process_files(self, file_paths: List[str]):
        for path in file_paths:
            self._process_file(path)

    def _process_file(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
            headers = self._parse_header(lines[0])
            for line in lines[1:]:
                self._process_line(line, headers)
        except Exception as e:
            raise

    def _process_line(self, line: str, headers: Dict[str, int]):
        values = line.split(",")
        try:
            self.employees.append({
                "name": values[headers["name"]].strip(),
                "department": values[headers["department"]].strip(),
                "hours_worked": int(values[headers["hours_worked"]].strip()),
                "hourly_rate": float(values[headers[headers["_rate_key"]]].strip())
            })
        except (ValueError, IndexError):
            pass
    def _parse_header(self, header_line: str) -> Dict[str, int]:
        headers = header_line.split(",")
        mapping = {}
        for idx, header in enumerate(headers):
            header = header.strip().lower()
            mapping[header] = idx
        required = {"department", "hours_worked"}
        rate_keys = {"hourly_rate", "rate", "salary"}
        if not required.issubset(mapping.keys()):
            raise ValueError("Missing required columns in header")
        rate_found = rate_keys.intersection(mapping.keys())
        if not rate_found:
            raise ValueError("No valid rate column found")
        mapping["_rate_key"] = next(iter(rate_found))
        return mapping
