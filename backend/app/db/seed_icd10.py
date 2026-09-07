import os
import sys

from sqlalchemy.orm import Session

# Allow this module to be run directly from the backend directory.
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import SessionLocal
from app.models.diagnosis import ICD10Code


# Four representative 2026 ICD-10-CM codes for every initial except reserved U.
SAMPLE_ICD10_CODES = [
    {"code": "A00.0", "description": "Cholera due to Vibrio cholerae 01, biovar cholerae"},
    {"code": "A09", "description": "Infectious gastroenteritis and colitis, unspecified"},
    {"code": "A15.0", "description": "Tuberculosis of lung"},
    {"code": "A41.9", "description": "Sepsis, unspecified organism"},
    {"code": "B00.9", "description": "Herpesviral infection, unspecified"},
    {"code": "B20", "description": "Human immunodeficiency virus [HIV] disease"},
    {"code": "B34.9", "description": "Viral infection, unspecified"},
    {"code": "B35.3", "description": "Tinea pedis"},
    {"code": "C18.9", "description": "Malignant neoplasm of colon, unspecified"},
    {"code": "C34.90", "description": "Unspecified part of unspecified bronchus or lung"},
    {"code": "C50.919", "description": "Malignant neoplasm of unspecified site of unspecified female breast"},
    {"code": "C61", "description": "Malignant neoplasm of prostate"},
    {"code": "D50.9", "description": "Iron deficiency anemia, unspecified"},
    {"code": "D64.9", "description": "Anemia, unspecified"},
    {"code": "D69.6", "description": "Thrombocytopenia, unspecified"},
    {"code": "D89.9", "description": "Disorder involving the immune mechanism, unspecified"},
    {"code": "E03.9", "description": "Hypothyroidism, unspecified"},
    {"code": "E11.9", "description": "Type 2 diabetes mellitus without complications"},
    {"code": "E55.9", "description": "Vitamin D deficiency, unspecified"},
    {"code": "E78.5", "description": "Hyperlipidemia, unspecified"},
    {"code": "F32.A", "description": "Depression, unspecified"},
    {"code": "F41.9", "description": "Anxiety disorder, unspecified"},
    {"code": "F43.10", "description": "Post-traumatic stress disorder, unspecified"},
    {"code": "F90.9", "description": "Attention-deficit hyperactivity disorder, unspecified type"},
    {"code": "G40.909", "description": "Epilepsy, unspecified, not intractable, without status epilepticus"},
    {"code": "G43.909", "description": "Migraine, unspecified, not intractable, without status migrainosus"},
    {"code": "G47.00", "description": "Insomnia, unspecified"},
    {"code": "G89.29", "description": "Other chronic pain"},
    {"code": "H10.9", "description": "Unspecified conjunctivitis"},
    {"code": "H52.4", "description": "Presbyopia"},
    {"code": "H66.90", "description": "Otitis media, unspecified, unspecified ear"},
    {"code": "H91.90", "description": "Unspecified hearing loss, unspecified ear"},
    {"code": "I10", "description": "Essential (primary) hypertension"},
    {"code": "I25.10", "description": "Atherosclerotic heart disease of native coronary artery without angina pectoris"},
    {"code": "I48.91", "description": "Unspecified atrial fibrillation"},
    {"code": "I50.9", "description": "Heart failure, unspecified"},
    {"code": "J00", "description": "Acute nasopharyngitis [common cold]"},
    {"code": "J06.9", "description": "Acute upper respiratory infection, unspecified"},
    {"code": "J18.9", "description": "Pneumonia, unspecified organism"},
    {"code": "J45.909", "description": "Unspecified asthma, uncomplicated"},
    {"code": "K21.9", "description": "Gastro-esophageal reflux disease without esophagitis"},
    {"code": "K52.9", "description": "Noninfective gastroenteritis and colitis, unspecified"},
    {"code": "K59.00", "description": "Constipation, unspecified"},
    {"code": "K76.0", "description": "Fatty (change of) liver, not elsewhere classified"},
    {"code": "L20.9", "description": "Atopic dermatitis, unspecified"},
    {"code": "L30.9", "description": "Dermatitis, unspecified"},
    {"code": "L50.9", "description": "Urticaria, unspecified"},
    {"code": "L70.9", "description": "Acne, unspecified"},
    {"code": "M17.9", "description": "Osteoarthritis of knee, unspecified"},
    {"code": "M25.50", "description": "Pain in unspecified joint"},
    {"code": "M54.50", "description": "Low back pain, unspecified"},
    {"code": "M79.10", "description": "Myalgia, unspecified site"},
    {"code": "N18.9", "description": "Chronic kidney disease, unspecified"},
    {"code": "N39.0", "description": "Urinary tract infection, site not specified"},
    {"code": "N40.0", "description": "Benign prostatic hyperplasia without lower urinary tract symptoms"},
    {"code": "N92.6", "description": "Irregular menstruation, unspecified"},
    {"code": "O21.9", "description": "Vomiting of pregnancy, unspecified"},
    {"code": "O24.419", "description": "Gestational diabetes mellitus in pregnancy, unspecified control"},
    {"code": "O80", "description": "Encounter for full-term uncomplicated delivery"},
    {"code": "O99.280", "description": "Endocrine, nutritional and metabolic diseases complicating pregnancy, unspecified trimester"},
    {"code": "P07.30", "description": "Preterm newborn, unspecified weeks of gestation"},
    {"code": "P22.0", "description": "Respiratory distress syndrome of newborn"},
    {"code": "P59.9", "description": "Neonatal jaundice, unspecified"},
    {"code": "P92.9", "description": "Feeding problem of newborn, unspecified"},
    {"code": "Q21.12", "description": "Patent foramen ovale"},
    {"code": "Q35.9", "description": "Cleft palate, unspecified"},
    {"code": "Q65.89", "description": "Other congenital deformities of hip"},
    {"code": "Q90.9", "description": "Down syndrome, unspecified"},
    {"code": "R05.9", "description": "Cough, unspecified"},
    {"code": "R10.9", "description": "Unspecified abdominal pain"},
    {"code": "R50.9", "description": "Fever, unspecified"},
    {"code": "R51.9", "description": "Headache, unspecified"},
    {"code": "S09.90XA", "description": "Unspecified injury of head, initial encounter"},
    {"code": "S39.012A", "description": "Strain of muscle, fascia and tendon of lower back, initial encounter"},
    {"code": "S52.509A", "description": "Unspecified fracture of the lower end of unspecified radius, initial encounter"},
    {"code": "S93.409A", "description": "Sprain of unspecified ligament of unspecified ankle, initial encounter"},
    {"code": "T14.90XA", "description": "Injury, unspecified, initial encounter"},
    {"code": "T78.40XA", "description": "Allergy, unspecified, initial encounter"},
    {"code": "T81.9XXA", "description": "Unspecified complication of procedure, initial encounter"},
    {"code": "T88.7XXA", "description": "Unspecified adverse effect of drug or medicament, initial encounter"},
    {"code": "V00.9XXA", "description": "Pedestrian on other conveyance injured in transport accident, initial encounter"},
    {"code": "V49.9XXA", "description": "Car occupant injured in unspecified traffic accident, initial encounter"},
    {"code": "V87.7XXA", "description": "Person injured in collision between other specified motor vehicles, initial encounter"},
    {"code": "V89.2XXA", "description": "Person injured in unspecified motor-vehicle accident, traffic, initial encounter"},
    {"code": "W01.0XXA", "description": "Fall on same level from slipping, tripping and stumbling without subsequent striking against object, initial encounter"},
    {"code": "W10.9XXA", "description": "Fall on and from unspecified stairs and steps, initial encounter"},
    {"code": "W19.XXXA", "description": "Unspecified fall, initial encounter"},
    {"code": "W54.0XXA", "description": "Bitten by dog, initial encounter"},
    {"code": "X08.8XXA", "description": "Exposure to other specified smoke, fire and flames, initial encounter"},
    {"code": "X30.XXXA", "description": "Exposure to excessive natural heat, initial encounter"},
    {"code": "X50.9XXA", "description": "Overexertion from unspecified strenuous movement or load, initial encounter"},
    {"code": "X58.XXXA", "description": "Exposure to other specified factors, initial encounter"},
    {"code": "Y04.0XXA", "description": "Assault by unarmed brawl or fight, initial encounter"},
    {"code": "Y09", "description": "Assault by unspecified means"},
    {"code": "Y83.9", "description": "Surgical procedure, unspecified as the cause of abnormal reaction or later complication"},
    {"code": "Y92.9", "description": "Unspecified place or not applicable"},
    {"code": "Z00.00", "description": "Encounter for general adult medical examination without abnormal findings"},
    {"code": "Z23", "description": "Encounter for immunization"},
    {"code": "Z71.1", "description": "Person with feared health complaint in whom no diagnosis is made"},
    {"code": "Z76.0", "description": "Encounter for issue of repeat prescription"},
]

EXPECTED_INITIALS = set("ABCDEFGHIJKLMNOPQRSTVWXYZ")


def seed_icd10_codes(db: Session):
    """Insert new codes and refresh descriptions for codes already present."""
    assert len(SAMPLE_ICD10_CODES) == 100
    assert {item["code"][0] for item in SAMPLE_ICD10_CODES} == EXPECTED_INITIALS

    existing_codes = {
        item.code: item
        for item in db.query(ICD10Code).filter(
            ICD10Code.code.in_([item["code"] for item in SAMPLE_ICD10_CODES])
        )
    }

    created = 0
    updated = 0
    for item in SAMPLE_ICD10_CODES:
        existing = existing_codes.get(item["code"])
        if existing:
            if existing.description != item["description"]:
                existing.description = item["description"]
                updated += 1
        else:
            db.add(ICD10Code(**item))
            created += 1

    db.commit()
    print(f"ICD-10 seed complete: {created} created, {updated} updated.")


if __name__ == "__main__":
    print("Starting database seeding process...")
    db = SessionLocal()
    try:
        seed_icd10_codes(db)
    finally:
        db.close()
    print("Seeding process finished.")
