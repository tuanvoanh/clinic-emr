from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.api.endpoints import diagnosis, patient
from app.core.exceptions import AppException, ErrorCode


def test_search_diagnoses_trims_search_term(monkeypatch):
    db = MagicMock()
    diagnoses = [SimpleNamespace(code="A00", description="Cholera")]
    search = MagicMock(return_value=diagnoses)
    monkeypatch.setattr(diagnosis.diagnosis_repo, "get_diagnoses_by_term", search)

    result = diagnosis.search_diagnoses(search="  A00  ", limit=10, db=db)

    assert result == diagnoses
    search.assert_called_once_with(db, search_term="A00", limit=10)


def test_search_patients_delegates_filters(monkeypatch):
    db = MagicMock()
    patients = [SimpleNamespace(id=1, phone="81234567")]
    search = MagicMock(return_value=patients)
    monkeypatch.setattr(patient.patient_repo, "search_patients_by_phone", search)

    result = patient.search_patients(phone="812", limit=5, db=db)

    assert result == patients
    search.assert_called_once_with(db, phone_prefix="812", limit=5)


def test_get_patient_by_phone_returns_patient(monkeypatch):
    db = MagicMock()
    expected = SimpleNamespace(id=1, phone="81234567")
    get_patient = MagicMock(return_value=expected)
    monkeypatch.setattr(patient.patient_repo, "get_patient_by_phone", get_patient)

    result = patient.get_patient_by_phone(phone="81234567", db=db)

    assert result is expected
    get_patient.assert_called_once_with(db, phone="81234567")


def test_get_patient_by_phone_raises_when_missing(monkeypatch):
    monkeypatch.setattr(
        patient.patient_repo, "get_patient_by_phone", MagicMock(return_value=None)
    )

    with pytest.raises(AppException) as exc_info:
        patient.get_patient_by_phone(phone="81234567", db=MagicMock())

    assert exc_info.value.error_code == ErrorCode.PATIENT_NOT_FOUND.code
    assert exc_info.value.status_code == 404
