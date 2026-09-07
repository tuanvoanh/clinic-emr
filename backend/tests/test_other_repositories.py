from app.models.diagnosis import ICD10Code
from app.repositories import diagnosis as diagnosis_repo
from app.repositories.user import user_repo
from app.schemas.user import UserCreate


def test_diagnosis_repository_orders_codes_when_search_is_empty(db_session):
    db_session.add_all(
        [
            ICD10Code(code="R51.9", description="Headache"),
            ICD10Code(code="A00", description="Cholera"),
            ICD10Code(code="B00", description="Herpesviral infections"),
        ]
    )
    db_session.commit()

    results = diagnosis_repo.get_diagnoses_by_term(
        db_session, search_term="", limit=2
    )

    assert [item.code for item in results] == ["A00", "B00"]


def test_diagnosis_repository_searches_code_and_description(db_session):
    db_session.add_all(
        [
            ICD10Code(code="R51.9", description="Headache"),
            ICD10Code(code="A00", description="Condition related to R51"),
            ICD10Code(code="B00", description="Herpesviral infections"),
        ]
    )
    db_session.commit()

    results = diagnosis_repo.get_diagnoses_by_term(
        db_session, search_term="r51", limit=10
    )

    assert [item.code for item in results] == ["R51.9", "A00"]


def test_user_repository_creates_and_finds_user(db_session):
    created = user_repo.create(
        db_session,
        UserCreate(
            email="doctor@example.com",
            password="strong-password",
            full_name="Doctor Jane",
            is_active=True,
            is_superuser=False,
        ),
    )

    assert created.id is not None
    assert created.hashed_password != "strong-password"
    assert user_repo.get(db_session, user_id=created.id) is created
    assert user_repo.get_by_email(db_session, email=created.email) is created
    assert user_repo.get(db_session, user_id=9999) is None
    assert user_repo.get_by_email(db_session, email="missing@example.com") is None
