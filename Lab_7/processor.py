
def validate_blood_type(blood_code):
    """
    Validates and standardizes a blood group and Rh factor.
    Example: 'o+' -> 'O Positive'.
    """
    if not isinstance(blood_code, str):
        return "Invalid blood type: input must be a string"

    cleaned = blood_code.strip().upper()

    if len(cleaned) < 2:
        return "Invalid blood type: incomplete input"

    antigen = cleaned[:-1]
    rh_char = cleaned[-1]

    if antigen not in ("A", "B", "AB", "O"):
        return "Invalid blood type: unknown ABO group"

    rh_map = {"+": "Positive", "-": "Negative"}

    if rh_char not in rh_map:
        return "Invalid blood type: Rh factor must be + or -"

    return f"{antigen} {rh_map[rh_char]}"


def calculate_pulse_pressure(bp_string):
    """
    Calculates pulse pressure and arterial ratio.
    Expected format: '120/80'.
    """
    if not isinstance(bp_string, str):
        return "Invalid BP: input must be a string"

    parts = bp_string.strip().split("/")

    if len(parts) != 2:
        return "Invalid BP: expected systolic/diastolic format"

    try:
        systolic = int(parts[0].strip())
        diastolic = int(parts[1].strip())
    except ValueError:
        return "Invalid BP: values must be integers"

    if systolic <= 0 or diastolic <= 0:
        return "Invalid BP: values must be positive"

    if systolic < diastolic:
        return "Invalid BP: systolic must not be less than diastolic"

    pulse_diff = systolic - diastolic
    ratio = round(systolic / diastolic, 2)

    return f"Diff: {pulse_diff}, Ratio: {ratio}"


def parse_donor_registry(donor_entry):
    """
    Parses a pipe-delimited donor record:
    'DonorID|WeightKg|Hemoglobin'.
    """
    if not isinstance(donor_entry, str):
        return "Invalid donor record: input must be a string"

    fields = donor_entry.split("|")

    if len(fields) != 3:
        return "Invalid donor record: expected exactly 3 fields"

    donor_id = fields[0].strip()

    if not donor_id:
        return "Invalid donor record: donor ID cannot be empty"

    try:
        weight = float(fields[1])
        hemoglobin = float(fields[2])
    except ValueError:
        return "Invalid donor record: weight and hemoglobin must be numeric"

    if weight < 0 or hemoglobin < 0:
        return "Invalid donor record: values cannot be negative"

    if not (weight < float("inf") and hemoglobin < float("inf")):
        return "Invalid donor record: values must be finite"

    eligible = weight >= 50.0 and hemoglobin >= 12.5

    return f"Donor {donor_id}: {'Eligible' if eligible else 'Deferred'}"


def main():
    print("==== Running validate_blood_type ====")
    b_input = input("Enter blood type (e.g. A+, O-, AB+): ")
    print("Validated:", validate_blood_type(b_input))

    print("\n==== Running calculate_pulse_pressure ====")
    bp_input = input("Enter BP (e.g. 120/80): ")
    print("BP Metrics:", calculate_pulse_pressure(bp_input))

    print("\n==== Running parse_donor_registry ====")
    d_input = input("Enter record (ID|Weight|Hemoglobin): ")
    print("Status:", parse_donor_registry(d_input))


if __name__ == "__main__":
    main()
