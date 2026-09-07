import sys
import os

# Add the parent directory to sys.path so we can import 'app' when running as a script
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.models.diagnosis import ICD10Code
from app.core.database import SessionLocal

# List of sample ICD-10 codes
SAMPLE_ICD10_CODES = [
    {"code": "A00.0", "description": "Cholera due to Vibrio cholerae 01, biovar cholerae"},
    {"code": "A00.1", "description": "Cholera due to Vibrio cholerae 01, biovar eltor"},
    {"code": "A00.9", "description": "Cholera, unspecified"},
    {"code": "A01.00", "description": "Typhoid fever, unspecified"},
    {"code": "A01.01", "description": "Typhoid meningitis"},
    {"code": "A01.02", "description": "Typhoid fever with heart involvement"},
    {"code": "A01.03", "description": "Typhoid pneumonia"},
    {"code": "A01.04", "description": "Typhoid arthritis"},
    {"code": "A01.05", "description": "Typhoid osteomyelitis"},
    {"code": "A01.09", "description": "Typhoid fever with other complications"},
    {"code": "A01.1", "description": "Paratyphoid fever A"},
    {"code": "A01.2", "description": "Paratyphoid fever B"},
    {"code": "A01.3", "description": "Paratyphoid fever C"},
    {"code": "A01.4", "description": "Paratyphoid fever, unspecified"},
    {"code": "A02.0", "description": "Salmonella enteritis"},
    {"code": "A02.1", "description": "Salmonella sepsis"},
    {"code": "A02.20", "description": "Localized salmonella infection, unspecified"},
    {"code": "A02.21", "description": "Salmonella meningitis"},
    {"code": "A02.22", "description": "Salmonella pneumonia"},
    {"code": "A02.23", "description": "Salmonella arthritis"},
    {"code": "A02.24", "description": "Salmonella osteomyelitis"},
    {"code": "A02.25", "description": "Salmonella pyelonephritis"},
    {"code": "A02.29", "description": "Salmonella with other localized infection"},
    {"code": "A02.8", "description": "Other specified salmonella infections"},
    {"code": "A02.9", "description": "Salmonella infection, unspecified"},
    {"code": "A03.0", "description": "Shigellosis due to Shigella dysenteriae"},
    {"code": "A03.1", "description": "Shigellosis due to Shigella flexneri"},
    {"code": "A03.2", "description": "Shigellosis due to Shigella boydii"},
    {"code": "A03.3", "description": "Shigellosis due to Shigella sonnei"},
    {"code": "A03.8", "description": "Other shigellosis"},
    {"code": "A03.9", "description": "Shigellosis, unspecified"},
    {"code": "A04.0", "description": "Enteropathogenic Escherichia coli infection"},
    {"code": "A04.1", "description": "Enterotoxigenic Escherichia coli infection"},
    {"code": "A04.2", "description": "Enteroinvasive Escherichia coli infection"},
    {"code": "A04.3", "description": "Enterohemorrhagic Escherichia coli infection"},
    {"code": "A04.4", "description": "Other intestinal Escherichia coli infections"},
    {"code": "A04.5", "description": "Campylobacter enteritis"},
    {"code": "A04.6", "description": "Enteritis due to Yersinia enterocolitica"},
    {"code": "A04.71", "description": "Enterocolitis due to Clostridium difficile, recurrent"},
    {"code": "A04.72", "description": "Enterocolitis due to Clostridium difficile, not specified as recurrent"},
    {"code": "A04.8", "description": "Other specified bacterial intestinal infections"},
    {"code": "A04.9", "description": "Bacterial intestinal infection, unspecified"},
    {"code": "A05.0", "description": "Foodborne staphylococcal intoxication"},
    {"code": "A05.1", "description": "Botulism food poisoning"},
    {"code": "A05.2", "description": "Foodborne Clostridium perfringens [Clostridium welchii] intoxication"},
    {"code": "A05.3", "description": "Foodborne Vibrio parahaemolyticus intoxication"},
    {"code": "A05.4", "description": "Foodborne Bacillus cereus intoxication"},
    {"code": "A05.5", "description": "Foodborne Vibrio vulnificus intoxication"},
    {"code": "A05.8", "description": "Other specified bacterial foodborne intoxications"},
    {"code": "A05.9", "description": "Bacterial foodborne intoxication, unspecified"},
    {"code": "A06.0", "description": "Acute amebic dysentery"},
    {"code": "A06.1", "description": "Chronic intestinal amebiasis"},
    {"code": "A06.2", "description": "Amebic nondysenteric colitis"},
    {"code": "A06.3", "description": "Ameboma of intestine"},
    {"code": "A06.4", "description": "Amebic liver abscess"},
    {"code": "A06.5", "description": "Amebic lung abscess"},
    {"code": "A06.6", "description": "Amebic brain abscess"},
    {"code": "A06.7", "description": "Cutaneous amebiasis"},
    {"code": "A06.81", "description": "Amebic cystitis"},
    {"code": "A06.82", "description": "Other amebic genitourinary infections"},
    {"code": "A06.89", "description": "Other amebic infections"},
    {"code": "A06.9", "description": "Amebiasis, unspecified"},
    {"code": "A07.0", "description": "Balantidiasis"},
    {"code": "A07.1", "description": "Giardiasis [lambliasis]"},
    {"code": "A07.2", "description": "Cryptosporidiosis"},
    {"code": "A07.3", "description": "Isosporiasis"},
    {"code": "A07.4", "description": "Cyclosporiasis"},
    {"code": "A07.8", "description": "Other specified protozoal intestinal diseases"},
    {"code": "A07.9", "description": "Protozoal intestinal disease, unspecified"},
    {"code": "A08.0", "description": "Rotaviral enteritis"},
    {"code": "A08.11", "description": "Acute gastroenteropathy due to Norwalk agent"},
    {"code": "A08.19", "description": "Acute gastroenteropathy due to other small round viruses"},
    {"code": "A08.2", "description": "Adenoviral enteritis"},
    {"code": "A08.31", "description": "Calicivirus enteritis"},
    {"code": "A08.32", "description": "Astrovirus enteritis"},
    {"code": "A08.39", "description": "Other viral enteritis"},
    {"code": "A08.4", "description": "Viral intestinal infection, unspecified"},
    {"code": "A08.8", "description": "Other specified intestinal infections"},
    {"code": "A09", "description": "Infectious gastroenteritis and colitis, unspecified"},
    {"code": "A15.0", "description": "Tuberculosis of lung"},
    {"code": "A15.4", "description": "Tuberculosis of intrathoracic lymph nodes"},
    {"code": "A15.5", "description": "Tuberculosis of larynx, trachea and bronchus"},
    {"code": "A15.6", "description": "Tuberculous pleurisy"},
    {"code": "A15.7", "description": "Primary respiratory tuberculosis"},
    {"code": "A15.8", "description": "Other respiratory tuberculosis"},
    {"code": "A15.9", "description": "Respiratory tuberculosis unspecified"},
    {"code": "A17.0", "description": "Tuberculous meningitis"},
    {"code": "A17.1", "description": "Meningeal tuberculoma"},
    {"code": "A17.81", "description": "Tuberculoma of brain and spinal cord"},
    {"code": "A17.82", "description": "Tuberculous meningoencephalitis"},
    {"code": "A17.83", "description": "Tuberculous neuritis"},
    {"code": "A17.89", "description": "Other tuberculosis of nervous system"},
    {"code": "A17.9", "description": "Tuberculosis of nervous system, unspecified"},
    {"code": "A18.01", "description": "Tuberculosis of spine"},
    {"code": "A18.02", "description": "Tuberculous arthritis of other joints"},
    {"code": "A18.03", "description": "Tuberculosis of other bones"},
    {"code": "A18.09", "description": "Other musculoskeletal tuberculosis"},
    {"code": "A18.10", "description": "Tuberculosis of genitourinary system, unspecified"},
    {"code": "A18.11", "description": "Tuberculosis of kidney and ureter"},
    {"code": "A18.12", "description": "Tuberculosis of bladder"},
]

def seed_icd10_codes(db: Session):
    """
    Function to check and automatically seed sample ICD-10 codes into the database if the table is empty.
    """
    if db.query(ICD10Code).first() is None:
        print("Seeding sample ICD-10 data into the database...")
        for item in SAMPLE_ICD10_CODES:
            db_code = ICD10Code(code=item["code"], description=item["description"])
            db.add(db_code)
        db.commit()
        print("Data seeded successfully!")
    else:
        print("ICD-10 data already exists, skipping seed step.")

if __name__ == "__main__":
    print("Starting database seeding process...")
    db = SessionLocal()
    try:
        seed_icd10_codes(db)
    finally:
        db.close()
    print("Seeding process finished.")
