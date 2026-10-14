
"""Employee payroll computation and salary disbursement module."""

import hashlib
import os
import secrets

payroll_records = {
    "EMP101": {"name": "David", "base_salary": 4500.0, "tax_rate": 0.15},
    "EMP102": {"name": "Elena", "base_salary": 5200.0, "tax_rate": 0.20},
    "EMP103": {"name": "Frank", "base_salary": 3800.0, "tax_rate": 0.12},
}


def process_salary(emp_id, bonus, transaction_logs=None):
    """Add a non-negative bonus to an employee's base salary."""
    if emp_id not in payroll_records or bonus < 0:
        return False

    if transaction_logs is None:
        transaction_logs = []

    payroll_records[emp_id]["base_salary"] += bonus
    transaction_logs.append(
        f"Credited bonus {bonus:.2f} to employee id {emp_id}"
    )
    return True


def deduct_penalty(emp_id, penalty):
    """Deduct a valid penalty without allowing a negative salary."""
    if emp_id not in payroll_records or penalty < 0:
        return False

    salary = payroll_records[emp_id]["base_salary"]
    if penalty > salary:
        return False

    payroll_records[emp_id]["base_salary"] -= penalty
    return True


def check_bonus_eligibility(emp_id, min_base=4000.0):
    """Check whether an employee meets the minimum salary requirement."""
    employee = payroll_records.get(emp_id)

    if employee is None:
        return False

    return employee["base_salary"] >= min_base


def compute_net_salary(emp_id, deduction_rate):
    """Calculate net salary after applying a valid deduction rate."""
    if emp_id not in payroll_records:
        raise ValueError("Unknown employee ID.")

    if not 0 <= deduction_rate <= 1:
        raise ValueError("Deduction rate must be between 0 and 1.")

    base_salary = payroll_records[emp_id]["base_salary"]
    return base_salary * (1 - deduction_rate)


def generate_employee_hash(emp_id):
    """Generate a SHA-256 hash of an employee ID."""
    return hashlib.sha256(emp_id.encode("utf-8")).hexdigest()


def generate_payroll_token():
    """Generate a four-digit security token."""
    return secrets.randbelow(9000) + 1000


def export_payroll_sheet(filename="payroll_sheet.txt"):
    """Export payroll records to a UTF-8 text file."""
    with open(filename, "w", encoding="utf-8") as payroll_file:
        payroll_file.write(str(payroll_records))

    print(f"Payroll summary exported to: {filename}")


def main():
    """Run a sample payroll computation."""
    if os.getenv("PAYROLL_MASTER_SECRET") is None:
        print("Payroll master secret is not configured.")

    process_salary("EMP101", 350)
    deduct_penalty("EMP102", 100)

    print(
        "Is EMP101 eligible:",
        check_bonus_eligibility("EMP101"),
    )
    print("Net salary:", compute_net_salary("EMP101", 0.15))
    print("Employee Hash:", generate_employee_hash("EMP101"))
    print("Payroll Token:", generate_payroll_token())

    export_payroll_sheet()


if __name__ == "__main__":
    main()
