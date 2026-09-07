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


@pytest.mark.parametrize("dob", ["invalid-date", "15-05-1985", "1985/05/15"])
def test_consultation_schema_rejects_invalid_dob_format(dob):
    payload = valid_consultation_payload()
    payload["dob"] = dob

    with pytest.raises(ValidationError):
        ConsultationCreate(**payload)
