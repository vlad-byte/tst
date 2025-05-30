import pytest
import os
from employee_processor import EmployeeData

@pytest.fixture
def sample_csv(tmp_path):
    data = """id,email,name,department,hours_worked,rate
1,test@example.com,John Doe,Engineering,160,30.5"""
    file = tmp_path / "test.csv"
    file.write_text(data)
    return str(file)

def test_file_processing(sample_csv):
    processor = EmployeeData()
    processor.process_files([sample_csv])
    assert len(processor.employees) == 1
    assert processor.employees[0]["department"] == "Engineering"
    assert processor.employees[0]["hours_worked"] == 160
    assert processor.employees[0]["hourly_rate"] == 30.5