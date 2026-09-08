import pytest

from app.models.diagnosis import ICD10Code
from app.models.patient import Patient


def test_root_health_check_uses_http_pipeline(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"].startswith("Welcome to ")


def test_protected_endpoint_returns_structured_unauthorized_response(client):
    response = client.get("/api/diagnosis/")

    assert response.status_code == 401
    assert response.json() == {
        "status": "error",
        "status_code": 401,
        "error_code": "unauthorized",
        "message": "Not authenticated. Please provide a Bearer token.",
        "errors": [],
    }


@pytest.mark.parametrize(
    ("url", "field"),
    [
        ("/api/patient/?phone=123", "phone"),
        ("/api/patient/8123", "phone"),
        ("/api/consultation/?page_size=200", "page_size"),
    ],
)
def test_query_and_path_constraints_return_validation_error(
    authenticated_client, url, field
):
    response = authenticated_client.get(url)

    assert response.status_code == 400
    body = response.json()
    assert body["error_code"] == "validation_error"
    assert body["errors"][0]["field"] == field


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("phone", "123"),
        ("phone", "71234567"),
        ("dob", "invalid-date"),
        ("dob", "1985-5-1"),
        ("dob", "2025-02-29"),
        ("dob", "2026-99-99"),
        ("dob", "2099-01-01"),
    ],
)
def test_consultation_body_validation_over_http(
    authenticated_client, field, value
):
    payload = {
        "patient_name": "Jane Smith",
        "dob": "1985-05-15",
        "phone": "81234567",
        "diagnosis_code": "R51.9",
        "treatment_notes": "Prescribed rest and pain relief.",
    }
    payload[field] = value

    response = authenticated_client.post("/api/consultation/", json=payload)

    assert response.status_code == 400
    body = response.json()
    assert body["error_code"] == "validation_error"
    assert body["errors"][0]["field"] == field


def test_create_consultation_creates_patient_and_can_be_listed(
    authenticated_client, db_session
):
    db_session.add(ICD10Code(code="R51.9", description="Headache"))
    db_session.commit()
    payload = {
        "patient_name": "Jane Smith",
        "dob": "1985-05-15",
        "phone": "81234567",
        "diagnosis_code": "R51.9",
        "treatment_notes": "Prescribed rest and pain relief.",
    }

    create_response = authenticated_client.post(
        "/api/consultation/", json=payload
    )
    list_response = authenticated_client.get(
        "/api/consultation/?phone=81234567"
    )

    assert create_response.status_code == 200
    assert create_response.json()["consultation_id"] > 0
    patient = db_session.query(Patient).filter_by(phone="81234567").one()
    assert patient.full_name == "Jane Smith"
    assert list_response.status_code == 200
    body = list_response.json()
    assert body["total"] == 1
    assert body["items"][0]["diagnosis_desc"] == "Headache"


def test_unknown_icd10_returns_business_error(authenticated_client):
    response = authenticated_client.post(
        "/api/consultation/",
        json={
            "patient_name": "Jane Smith",
            "dob": "1985-05-15",
            "phone": "81234567",
            "diagnosis_code": "UNKNOWN",
            "treatment_notes": "Prescribed rest and pain relief.",
        },
    )

    assert response.status_code == 400
    assert response.json()["error_code"] == "invalid_icd10_code"


def test_create_consultation_rolls_back_patient_when_consultation_fails(
    authenticated_client, db_session, monkeypatch
):
    from app.api.endpoints import consultation as consultation_ep

    db_session.add(ICD10Code(code="R51.9", description="Headache"))
    db_session.commit()

    def fail_create_consultation(*args, **kwargs):
        raise RuntimeError("Consultation insert failed unexpectedly")

    monkeypatch.setattr(
        consultation_ep.consultation_repo,
        "create_consultation",
        fail_create_consultation,
    )

    payload = {
        "patient_name": "Jane Smith",
        "dob": "1985-05-15",
        "phone": "81234567",
        "diagnosis_code": "R51.9",
        "treatment_notes": "Prescribed rest and pain relief.",
    }

    with pytest.raises(RuntimeError):
        authenticated_client.post("/api/consultation/", json=payload)

    # Verify atomic rollback: patient record was NOT persisted
    patient = db_session.query(Patient).filter_by(phone="81234567").first()
    assert patient is None
