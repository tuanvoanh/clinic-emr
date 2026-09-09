from app.core.config import settings
from app.core.database import SessionLocal
from app.db.seed_consultations import seed_consultations
from app.db.seed_icd10 import seed_icd10_codes
from app.db.seed_patients import seed_patients
from app.repositories.user import user_repo
from app.schemas.user import UserCreate


def seed_demo() -> None:
    """Prepare a complete, idempotent dataset for the Docker demo."""
    db = SessionLocal()
    try:
        if not user_repo.get_by_email(db, settings.FIRST_SUPERUSER_EMAIL):
            user_repo.create(
                db,
                UserCreate(
                    email=settings.FIRST_SUPERUSER_EMAIL,
                    password=settings.FIRST_SUPERUSER_PASSWORD,
                    full_name=settings.FIRST_SUPERUSER_FULL_NAME,
                    is_superuser=True,
                ),
            )
            print(f"Demo administrator created: {settings.FIRST_SUPERUSER_EMAIL}")

        seed_icd10_codes(db)
        seed_patients(db)
        seed_consultations(db)
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo()
