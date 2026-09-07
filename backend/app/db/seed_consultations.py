import datetime
import os
import random
import sys

from faker import Faker
from sqlalchemy.orm import Session

# Allow this module to be run directly from the backend directory.
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import SessionLocal
from app.models.consultation import Consultation
from app.models.diagnosis import ICD10Code
from app.models.patient import Patient


CONSULTATION_COUNT = 10_000
SEED_PREFIX = "[SEED:"
TREATMENT_PLANS = [
    "Symptoms reviewed. Continue supportive care and return if symptoms worsen.",
    "Medication prescribed as discussed. Follow up with the clinic in two weeks.",
    "Advised rest, hydration, and regular monitoring of symptoms at home.",
    "Clinical findings discussed. Arrange routine follow-up and repeat assessment.",
    "Lifestyle measures reviewed. Continue current treatment and monitor progress.",
    "Patient reassured and given safety-net advice for any new warning symptoms.",
    "Diagnostic results reviewed. Maintain treatment plan and attend follow-up visit.",
    "Referral options discussed. Patient agreed to conservative management initially.",
]


def build_consultations(
    patient_ids: list[int], diagnosis_codes: list[str], count: int = CONSULTATION_COUNT
) -> list[dict]:
    """Build deterministic consultation data from existing patients and codes."""
    if not patient_ids:
        raise ValueError("No patients found. Run the patient seed first.")
    if not diagnosis_codes:
        raise ValueError("No ICD-10 codes found. Run the ICD-10 seed first.")

    randomizer = random.Random(2026)
    fake = Faker("en_GB")
    Faker.seed(2026)
    seed_end = datetime.datetime(2026, 9, 7, 23, 59, 59)

    return [
        {
            "patient_id": randomizer.choice(patient_ids),
            "diagnosis_code": randomizer.choice(diagnosis_codes),
            "treatment_notes": (
                f"[SEED:{index:05d}] {randomizer.choice(TREATMENT_PLANS)}"
            ),
            "created_at": fake.date_time_between(
                start_date=seed_end - datetime.timedelta(days=730),
                end_date=seed_end,
            ),
        }
        for index in range(1, count + 1)
    ]


def seed_consultations(db: Session, count: int = CONSULTATION_COUNT) -> None:
    """Insert or refresh the deterministic set of generated consultations."""
    patient_ids = [row[0] for row in db.query(Patient.id).all()]
    diagnosis_codes = [row[0] for row in db.query(ICD10Code.code).all()]
    consultations = build_consultations(patient_ids, diagnosis_codes, count)

    existing_by_marker = {
        item.treatment_notes.split("]", 1)[0] + "]": item
        for item in db.query(Consultation).filter(
            Consultation.treatment_notes.startswith(SEED_PREFIX)
        )
    }

    created = 0
    updated = 0
    for item in consultations:
        marker = item["treatment_notes"].split("]", 1)[0] + "]"
        existing = existing_by_marker.get(marker)
        if existing:
            changed = any(
                getattr(existing, field) != item[field]
                for field in (
                    "patient_id",
                    "diagnosis_code",
                    "treatment_notes",
                    "created_at",
                )
            )
            if changed:
                for field, value in item.items():
                    setattr(existing, field, value)
                updated += 1
        else:
            db.add(Consultation(**item))
            created += 1

    db.commit()
    print(f"Consultation seed complete: {created} created, {updated} updated.")


if __name__ == "__main__":
    print("Starting consultation seeding process...")
    db = SessionLocal()
    try:
        seed_consultations(db)
    finally:
        db.close()
    print("Consultation seeding process finished.")
