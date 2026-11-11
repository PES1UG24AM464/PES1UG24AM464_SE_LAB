
import pytest

from blood_donation_screening import (
    process_donor_cohort,
    verify_storage_centrifuge
)


# ==========================================
# PROCESS DONOR COHORT - BRANCH COVERAGE
# ==========================================

def test_invalid_cohort_list():
    with pytest.raises(ValueError):
        process_donor_cohort("invalid", 450)


def test_invalid_volume():
    with pytest.raises(ValueError):
        process_donor_cohort([], 0)


def test_unregistered_clinic():
    cohorts = [{"clinic_registered": False}]
    result = process_donor_cohort(cohorts, 450)
    assert result["status"] == "ZERO_YIELD"


def test_registered_clinic():
    cohorts = [{
        "clinic_registered": True,
        "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}]
    }]
    result = process_donor_cohort(cohorts, 450)
    assert result["status"] == "ACCEPTED"


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


def test_eligible_donor():
    cohorts = [{
        "clinic_registered": True,
        "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}]
    }]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 450


def test_low_hemoglobin_standard():
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


def test_normal_hemoglobin_boundaries():
    cohorts = [{
        "clinic_registered": True,
        "donors": [
            {"age": 25, "weight_kg": 65, "hb": 12.5},
            {"age": 26, "weight_kg": 65, "hb": 18.0}
        ]
    }]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 900


def test_fast_track_enabled():
    cohorts = [{
        "clinic_registered": True,
        "fast_track": True,
        "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}]
    }]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 500


def test_fast_track_disabled():
    cohorts = [{
        "clinic_registered": True,
        "fast_track": False,
        "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}]
    }]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 450


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


def test_accepted_status():
    cohorts = [{
        "clinic_registered": True,
        "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}]
    }]
    result = process_donor_cohort(cohorts, 450)
    assert result["status"] == "ACCEPTED"


# ==========================================
# VERIFY STORAGE CENTRIFUGE - BRANCH COVERAGE
# ==========================================

def test_empty_centrifuge_data():
    assert verify_storage_centrifuge([]) == "NO_DATA"


def test_stable_rpm():
    assert verify_storage_centrifuge([[3500, 3600, 3700]]) == "STABLE"


def test_low_rpm():
    assert verify_storage_centrifuge([[2500, 3500, 3600]]) == "STABLE"


def test_two_consecutive_low_rpm():
    assert verify_storage_centrifuge([[3500, 2500, 2400]]) == "ABORT_SPIN"


def test_rpm_streak_reset():
    assert verify_storage_centrifuge([[2500, 3500, 2500, 3500]]) == "STABLE"


def test_empty_individual_run():
    assert verify_storage_centrifuge([[]]) == "STABLE"
