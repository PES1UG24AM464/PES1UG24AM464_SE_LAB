
import pytest

from blood_donation_screening import (
    process_donor_cohort,
    verify_storage_centrifuge
)


# ==========================================
# PROCESS DONOR COHORT - CODE COVERAGE TESTS
# ==========================================

def test_invalid_cohort_type():
    with pytest.raises(ValueError):
        process_donor_cohort("invalid", 450)


def test_invalid_standard_volume():
    with pytest.raises(ValueError):
        process_donor_cohort([], 0)


def test_unregistered_clinic():
    cohorts = [{"clinic_registered": False}]
    result = process_donor_cohort(cohorts, 450)
    assert result["status"] == "ZERO_YIELD"


def test_missing_cohort_fields():
    cohorts = [{"clinic_registered": True}]
    result = process_donor_cohort(cohorts, 450)
    assert result["status"] == "ZERO_YIELD"


def test_underage_donor():
    cohorts = [{
        "clinic_registered": True,
        "donors": [{"age": 16, "weight_kg": 65, "hb": 14.0}]
    }]
    result = process_donor_cohort(cohorts, 450)
    assert result["status"] == "ZERO_YIELD"


def test_underweight_donor():
    cohorts = [{
        "clinic_registered": True,
        "donors": [{"age": 25, "weight_kg": 45, "hb": 14.0}]
    }]
    result = process_donor_cohort(cohorts, 450)
    assert result["status"] == "ZERO_YIELD"


def test_low_hemoglobin_standard_cohort():
    cohorts = [{
        "clinic_registered": True,
        "type": "standard",
        "donors": [{"age": 25, "weight_kg": 65, "hb": 12.0}]
    }]
    result = process_donor_cohort(cohorts, 450)
    assert result["status"] == "ZERO_YIELD"


def test_low_hemoglobin_high_altitude():
    cohorts = [{
        "clinic_registered": True,
        "type": "high_altitude",
        "donors": [
            {"age": 25, "weight_kg": 65, "hb": 14.0},
            {"age": 26, "weight_kg": 70, "hb": 12.0},
            {"age": 30, "weight_kg": 65, "hb": 15.0}
        ]
    }]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 0
    assert result["status"] == "ZERO_YIELD"


def test_high_hemoglobin():
    cohorts = [{
        "clinic_registered": True,
        "donors": [{"age": 25, "weight_kg": 65, "hb": 19.0}]
    }]
    result = process_donor_cohort(cohorts, 450)
    assert result["status"] == "ZERO_YIELD"


def test_accepted_donor():
    cohorts = [{
        "clinic_registered": True,
        "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}]
    }]
    result = process_donor_cohort(cohorts, 450)
    assert result == {
        "collected_ml": 450,
        "status": "ACCEPTED"
    }


def test_fast_track_cohort():
    cohorts = [{
        "clinic_registered": True,
        "fast_track": True,
        "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}]
    }]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 500
    assert result["status"] == "ACCEPTED"


def test_high_deferral_status():
    cohorts = [{
        "clinic_registered": True,
        "donors": [
            {"age": 16, "weight_kg": 65, "hb": 14.0},
            {"age": 16, "weight_kg": 65, "hb": 14.0},
            {"age": 16, "weight_kg": 65, "hb": 14.0},
            {"age": 16, "weight_kg": 65, "hb": 14.0},
            {"age": 16, "weight_kg": 65, "hb": 14.0}
        ]
    }]
    result = process_donor_cohort(cohorts, 450)
    assert result["status"] == "HIGH_DEFERRAL"


# ==========================================
# VERIFY STORAGE CENTRIFUGE - CODE COVERAGE
# ==========================================

def test_no_centrifuge_data():
    assert verify_storage_centrifuge([]) == "NO_DATA"


def test_stable_centrifuge():
    runs = [[3500, 3600, 3700, 3800]]
    assert verify_storage_centrifuge(runs) == "STABLE"


def test_single_low_rpm():
    runs = [[2500, 3500, 3600]]
    assert verify_storage_centrifuge(runs) == "STABLE"


def test_two_consecutive_low_rpm():
    runs = [[3500, 2500, 2400, 3600]]
    assert verify_storage_centrifuge(runs) == "ABORT_SPIN"


def test_low_rpm_streak_reset():
    runs = [[2500, 3500, 2500, 3500]]
    assert verify_storage_centrifuge(runs) == "STABLE"


def test_empty_centrifuge_run():
    runs = [[]]
    assert verify_storage_centrifuge(runs) == "STABLE"
