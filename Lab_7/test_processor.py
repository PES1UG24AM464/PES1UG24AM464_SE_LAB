
from hypothesis import given, strategies as st
from processor import validate_blood_type, calculate_pulse_pressure, parse_donor_registry


@given(st.one_of(st.text(), st.none()))
def test_validate_blood_type_no_crash(s):
    try:
        result = validate_blood_type(s)
        assert isinstance(result, str)
    except Exception as e:
        assert False, f"Blood type function crashed: {e}"


@given(st.one_of(st.text(), st.none()))
def test_calculate_pulse_pressure_safe(s):
    try:
        result = calculate_pulse_pressure(s)
        assert isinstance(result, str)
    except Exception as e:
        assert False, f"Blood pressure function crashed: {e}"


@given(st.one_of(st.text(), st.none()))
def test_parse_donor_registry_safe(s):
    try:
        result = parse_donor_registry(s)
        assert isinstance(result, str)
    except Exception as e:
        assert False, f"Donor registry function crashed: {e}"
