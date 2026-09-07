import os
import sys

from faker import Faker
from sqlalchemy.orm import Session

# Allow this module to be run directly from the backend directory.
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import SessionLocal
from app.models.patient import Patient


PATIENT_COUNT = 1_000
PHONE_BASE = 1_000_000


def build_patients(count: int = PATIENT_COUNT) -> list[dict[str, str]]:
    """Build deterministic Singapore patient data with unique mobile numbers."""
    fake = Faker("en_GB")
    Faker.seed(2026)

    return [
        {
            "full_name": fake.name(),
            "dob": fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
            "phone": f"{8 + index % 2}{PHONE_BASE + index:07d}",
        }
        for index in range(count)
    ]


def seed_patients(db: Session, count: int = PATIENT_COUNT) -> None:
    """Insert new patients and refresh generated data for existing seed phones."""
    patients = build_patients(count)
    phones = [item["phone"] for item in patients]
    existing_by_phone = {
        patient.phone: patient
        for patient in db.query(Patient).filter(Patient.phone.in_(phones))
    }

    created = 0
    updated = 0
    for item in patients:
        existing = existing_by_phone.get(item["phone"])
        if existing:
            if existing.full_name != item["full_name"] or existing.dob != item["dob"]:
                existing.full_name = item["full_name"]
                existing.dob = item["dob"]
                updated += 1
        else:
            db.add(Patient(**item))
            created += 1

    db.commit()
    print(f"Patient seed complete: {created} created, {updated} updated.")


if __name__ == "__main__":
    print("Starting patient seeding process...")
    db = SessionLocal()
    try:
        seed_patients(db)
    finally:
        db.close()
    print("Patient seeding process finished.")
