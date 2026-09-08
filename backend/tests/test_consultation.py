from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.api.endpoints import consultation
from app.core.exceptions import AppException, ErrorCode
from app.schemas.consultation import ConsultationCreate


@pytest.fixture
def consultation_in():
    return ConsultationCreate(
        patient_name="Jane Smith",
        dob="1985-05-15",
        phone="81234567",
        diagnosis_code="R51.9",
        treatment_notes="Prescribed rest and pain relief.",
    )


def test_create_consultation_reuses_existing_patient(monkeypatch, consultation_in):
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = SimpleNamespace(
        code="R51.9"
    )
    existing_patient = SimpleNamespace(id=3)
    monkeypatch.setattr(
        consultation.patient_repo,
        "get_patient_by_phone",
        MagicMock(return_value=existing_patient),
    )
    create_patient = MagicMock()
    monkeypatch.setattr(consultation.patient_repo, "create_patient", create_patient)
    create_consultation = MagicMock(return_value=SimpleNamespace(id=42))
    monkeypatch.setattr(
        consultation.consultation_repo,
        "create_consultation",
        create_consultation,
    )

    result = consultation.create_consultation(consultation_in=consultation_in, db=db)

    assert result == {
        "message": "Consultation record created successfully",
        "consultation_id": 42,
    }
    create_patient.assert_not_called()
    create_consultation.assert_called_once_with(
        db, patient=existing_patient, consultation_in=consultation_in, commit=False
    )


def test_create_consultation_creates_missing_patient(monkeypatch, consultation_in):
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = SimpleNamespace(
        code="R51.9"
    )
    monkeypatch.setattr(
        consultation.patient_repo,
        "get_patient_by_phone",
        MagicMock(return_value=None),
    )
    new_patient = SimpleNamespace(id=4)
    create_patient = MagicMock(return_value=new_patient)
    monkeypatch.setattr(consultation.patient_repo, "create_patient", create_patient)
    monkeypatch.setattr(
        consultation.consultation_repo,
        "create_consultation",
        MagicMock(return_value=SimpleNamespace(id=43)),
    )

    consultation.create_consultation(consultation_in=consultation_in, db=db)

    patient_in = create_patient.call_args.kwargs["patient_in"]
    assert patient_in.full_name == consultation_in.patient_name
    assert patient_in.dob == consultation_in.dob
    assert patient_in.phone == consultation_in.phone


def test_create_consultation_recovers_from_integrity_error(monkeypatch, consultation_in):
    from sqlalchemy.exc import IntegrityError

    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = SimpleNamespace(
        code="R51.9"
    )

    # Initial check returns None (patient not found)
    # After IntegrityError rollback, second get_patient_by_phone returns the concurrently created patient
    concurrent_patient = SimpleNamespace(id=99)
    monkeypatch.setattr(
        consultation.patient_repo,
        "get_patient_by_phone",
        MagicMock(side_effect=[None, concurrent_patient]),
    )
    # First create_patient simulates race condition: concurrent insert happened, raising IntegrityError
    orig_exc = Exception("UNIQUE constraint failed: patients.phone")
    monkeypatch.setattr(
        consultation.patient_repo,
        "create_patient",
        MagicMock(side_effect=IntegrityError("statement", {}, orig_exc)),
    )
    create_consultation = MagicMock(return_value=SimpleNamespace(id=88))
    monkeypatch.setattr(
        consultation.consultation_repo,
        "create_consultation",
        create_consultation,
    )

    result = consultation.create_consultation(consultation_in=consultation_in, db=db)

    assert result == {
        "message": "Consultation record created successfully",
        "consultation_id": 88,
    }
    db.rollback.assert_called_once()
    create_consultation.assert_called_once_with(
        db, patient=concurrent_patient, consultation_in=consultation_in, commit=True
    )


def test_create_consultation_rejects_unknown_icd10_code(consultation_in):
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(AppException) as exc_info:
        consultation.create_consultation(consultation_in=consultation_in, db=db)

    assert exc_info.value.error_code == ErrorCode.INVALID_ICD10_CODE.code
    assert exc_info.value.status_code == 400


@pytest.mark.parametrize(
    ("total", "page_size", "expected_pages"),
    [(21, 10, 3), (20, 10, 2), (0, 10, 0)],
)
def test_list_consultations_calculates_total_pages(
    monkeypatch, total, page_size, expected_pages
):
    db = MagicMock()
    items = [SimpleNamespace(id=1)] if total else []
    get_all = MagicMock(return_value=(items, total))
    monkeypatch.setattr(
        consultation.consultation_repo, "get_all_consultations", get_all
    )

    result = consultation.list_consultations(
        phone="81234567",
        diagnosis_code="R51.9",
        page=2,
        page_size=page_size,
        db=db,
    )

    assert result == {
        "items": items,
        "total": total,
        "page": 2,
        "page_size": page_size,
        "total_pages": expected_pages,
    }
    get_all.assert_called_once_with(
        db,
        phone="81234567",
        diagnosis_code="R51.9",
        page=2,
        page_size=page_size,
    )
