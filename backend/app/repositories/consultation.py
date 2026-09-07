from sqlalchemy.orm import Session
from app.models.consultation import Consultation
from app.models.patient import Patient
from app.models.diagnosis import ICD10Code
from app.schemas.consultation import ConsultationCreate
from typing import List, Dict, Any

def create_consultation(db: Session, patient_id: int, consultation_in: ConsultationCreate) -> Consultation:
    """
    Create a new consultation record.
    
    Args:
        db (Session): Database session.
        patient_id (int): ID of the patient.
        consultation_in (ConsultationCreate): Consultation details (disease code, notes, etc.).
        
    Returns:
        Consultation: The newly created Consultation object.
    """
    db_consultation = Consultation(
        patient_id=patient_id,
        diagnosis_code=consultation_in.diagnosis_code,
        treatment_notes=consultation_in.treatment_notes
    )
    db.add(db_consultation)
    db.commit()
    db.refresh(db_consultation)
    return db_consultation

def get_all_consultations(db: Session, search_term: str = "") -> List[Dict[str, Any]]:
    """
    Get a list of all consultation records, with optional search by patient name or disease code.
    
    Args:
        db (Session): Database session.
        search_term (str): Search keyword (Patient name or disease code).
        
    Returns:
        List[Dict[str, Any]]: List of consultation records along with detailed information (joined tables).
    """
    query = db.query(
        Consultation.id,
        Consultation.patient_id,
        Patient.full_name,
        Patient.dob,
        Patient.phone,
        Consultation.diagnosis_code,
        ICD10Code.description.label("diagnosis_desc"),
        Consultation.treatment_notes,
        Consultation.created_at
    ).join(Patient, Consultation.patient_id == Patient.id)\
     .join(ICD10Code, Consultation.diagnosis_code == ICD10Code.code)

    if search_term:
        search = f"%{search_term}%"
        query = query.filter(
            (Patient.full_name.ilike(search)) | 
            (Patient.phone.ilike(search)) |
            (Consultation.diagnosis_code.ilike(search))
        )
        
    # Order by newest first
    query = query.order_by(Consultation.created_at.desc())
    
    # Execute and format result
    results = query.all()
    
    # Convert SQLAlchemy Row results to dict format to be compatible with Pydantic response schema
    consultations = []
    for row in results:
        consultations.append({
            "id": row.id,
            "patient_id": row.patient_id,
            "full_name": row.full_name,
            "dob": row.dob,
            "phone": row.phone,
            "diagnosis_code": row.diagnosis_code,
            "diagnosis_desc": row.diagnosis_desc,
            "treatment_notes": row.treatment_notes,
            "created_at": row.created_at
        })
        
    return consultations
