from datetime import datetime, timedelta, timezone

from app.models.consultation import Consultation
from app.models.diagnosis import ICD10Code
from app.models.patient import Patient
from app.repositories import consultation as consultation_repo
from app.repositories import patient as patient_repo
from app.schemas.consultation import ConsultationCreate
from app.schemas.patient import PatientCreate


def seed_consultations(db_session):
    jane = Patient(full_name="Jane Smith", dob="1985-05-15", phone="81234567")
    john = Patient(full_name="John Doe", dob="1990-01-01", phone="91234567")
    db_session.add_all(
        [
            jane,
            john,
            ICD10Code(code="A00", description="Cholera"),
            ICD10Code(code="R51.9", description="Headache"),
        ]
    )
    db_session.flush()
    now = datetime.now(timezone.utc)
    db_session.add_all(
        [
            Consultation(
                patient=jane,
                diagnosis_code="A00",
                treatment_notes="Older consultation",
                created_at=now - timedelta(days=2),
            ),
            Consultation(
                patient=jane,
                diagnosis_code="R51.9",
                treatment_notes="Newest consultation",
                created_at=now,
            ),
            Consultation(
                patient=john,
                diagnosis_code="R51.9",
                treatment_notes="Other patient",
                created_at=now - timedelta(days=1),
            ),
        ]
    )
    db_session.commit()


def test_create_patient_and_consultation_with_real_database(db_session):
    patient = patient_repo.get_patient_by_phone(db_session, "81234567")
    assert patient is None

    patient = patient_repo.create_patient(
        db_session,
        PatientCreate(
            full_name="Jane Smith", dob="1985-05-15", phone="81234567"
        ),
    )
    db_session.add(ICD10Code(code="R51.9", description="Headache"))
    db_session.commit()
    created = consultation_repo.create_consultation(
        db_session,
        patient,
        ConsultationCreate(
            patient_name=patient.full_name,
            dob=patient.dob,
            phone=patient.phone,
            diagnosis_code="R51.9",
            treatment_notes="Prescribed rest and pain relief.",
        ),
    )

    assert created.id is not None
    assert created.patient_id == patient.id
    assert patient_repo.get_patient_by_phone(db_session, "81234567").id == patient.id


def test_consultation_query_filters_phone_and_orders_newest_first(db_session):
    seed_consultations(db_session)

    items, total = consultation_repo.get_all_consultations(
        db_session, phone=" 81234567 ", page=1, page_size=10
    )

    assert total == 2
    assert [item["treatment_notes"] for item in items] == [
        "Newest consultation",
        "Older consultation",
    ]
    assert all(item["phone"] == "81234567" for item in items)


def test_consultation_query_filters_diagnosis_and_paginates(db_session):
    seed_consultations(db_session)

    first_page, total = consultation_repo.get_all_consultations(
        db_session, diagnosis_code=" R51.9 ", page=1, page_size=1
    )
    second_page, second_total = consultation_repo.get_all_consultations(
        db_session, diagnosis_code="R51.9", page=2, page_size=1
    )

    assert total == second_total == 2
    assert first_page[0]["treatment_notes"] == "Newest consultation"
    assert second_page[0]["treatment_notes"] == "Other patient"
