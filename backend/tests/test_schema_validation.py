import pytest
from pydantic import ValidationError

from app.schemas.consultation import ConsultationCreate


def valid_consultation_payload():
    return {
        "patient_name": "Jane Smith",
        "dob": "1985-05-15",
        "phone": "81234567",
        "diagnosis_code": "R51.9",
        "treatment_notes": "Prescribed rest and pain relief.",
    }


@pytest.mark.parametrize("phone", ["123", "71234567", "812345678"])
def test_consultation_schema_rejects_invalid_phone(phone):
    payload = valid_consultation_payload()
    payload["phone"] = phone

    with pytest.raises(ValidationError):
        ConsultationCreate(**payload)


@pytest.mark.parametrize(
    "dob",
    [
        "invalid-date",
        "15-05-1985",
        "1985/05/15",
        "1985-5-1",    # Single-digit month and day (must be strictly YYYY-MM-DD)
        "1985-05-1",   # Single-digit day
        "1985-5-01",   # Single-digit month
        "2025-02-29",  # Impossible leap year date
        "2026-99-99",  # Impossible month and day
        "2099-01-01",  # Future date
        "1899-12-31",  # Unreasonably old date (< 1900)
    ],
)
def test_consultation_schema_rejects_invalid_dob_format_and_impossible_dates(dob):
    payload = valid_consultation_payload()
    payload["dob"] = dob

    with pytest.raises(ValidationError) as exc_info:
        ConsultationCreate(**payload)

    errors = exc_info.value.errors()
    assert any(err["loc"] == ("dob",) for err in errors)


@pytest.mark.parametrize(
    "dob",
    [
        "2025-02-29",
        "2026-99-99",
        "2099-01-01",
        "1800-01-01",
        "1985-5-1",
        "not-a-date",
    ],
)
def test_patient_schema_rejects_invalid_and_impossible_dob(dob):
    from app.schemas.patient import PatientCreate

    with pytest.raises(ValidationError) as exc_info:
        PatientCreate(full_name="John Doe", dob=dob, phone="81234567")

    errors = exc_info.value.errors()
    assert any(err["loc"] == ("dob",) for err in errors)


def test_schema_accepts_valid_leap_year_dob():
    payload = valid_consultation_payload()
    payload["dob"] = "2024-02-29"  # 2024 is a real leap year
    instance = ConsultationCreate(**payload)
    assert instance.dob == "2024-02-29"
