from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.schemas.patient import PatientCreate
from typing import Optional, List

def search_patients_by_phone(db: Session, phone_prefix: str, limit: int = 20) -> List[Patient]:
    """
    Search patients by phone prefix using startswith (generates 'phone LIKE prefix%').
    This effectively uses the B-Tree index on the phone column without full table scans.
    
    Args:
        db (Session): Database session.
        phone_prefix (str): Beginning digits of the phone number.
        limit (int): Maximum records to return.
        
    Returns:
        List[Patient]: Matching patient records.
    """
    if not phone_prefix:
        return db.query(Patient).limit(limit).all()
        
    return db.query(Patient).filter(
        Patient.phone.startswith(phone_prefix)
    ).limit(limit).all()

def get_patient_by_phone(db: Session, phone: str) -> Optional[Patient]:
    """
    Search for a patient based on unique phone number.
    
    Args:
        db (Session): Database session.
        phone (str): Contact phone number of the patient.
        
    Returns:
        Optional[Patient]: Patient object if found, otherwise None.
    """
    return db.query(Patient).filter(Patient.phone == phone).first()

def get_patient_by_details(db: Session, full_name: str, dob: str) -> Optional[Patient]:
    """
    Search for a patient based on full name and date of birth.
    
    Args:
        db (Session): Database session.
        full_name (str): Full name of the patient.
        dob (str): Date of birth (YYYY-MM-DD).
        
    Returns:
        Optional[Patient]: Patient object if found, otherwise None.
    """
    return db.query(Patient).filter(
        Patient.full_name == full_name,
        Patient.dob == dob
    ).first()

def create_patient(
    db: Session, patient_in: PatientCreate, commit: bool = True
) -> Patient:
    """
    Create a new patient record.
    
    Args:
        db (Session): Database session.
        patient_in (PatientCreate): Schema containing patient information to create.
        commit (bool): Whether to commit the transaction immediately (default True).
        
    Returns:
        Patient: The newly created Patient object.
    """
    db_patient = Patient(
        full_name=patient_in.full_name,
        dob=patient_in.dob,
        phone=patient_in.phone
    )
    db.add(db_patient)
    if commit:
        db.commit()
        db.refresh(db_patient)
    else:
        db.flush()
    return db_patient
