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

from typing import List, Dict, Any, Tuple, Optional

def get_all_consultations(
    db: Session, 
    search_term: Optional[str] = None,
    phone: Optional[str] = None,
    diagnosis_code: Optional[str] = None,
    page: int = 1, 
    page_size: int = 10
) -> Tuple[List[Dict[str, Any]], int]:
    """
    Get a paginated list of all consultation records sorted by created_at DESC (newest to oldest),
    with optional filtering by phone, disease code, or general search.
    
    Args:
        db (Session): Database session.
        search_term (Optional[str]): General search keyword.
        phone (Optional[str]): Patient phone number filter.
        diagnosis_code (Optional[str]): ICD-10 disease code filter.
        page (int): Page number (1-indexed).
        page_size (int): Number of items per page.
        
    Returns:
        Tuple[List[Dict[str, Any]], int]: (List of consultation records for the page, total matching records).
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

    # Specific filter by patient phone (utilizes index with startswith)
    if phone:
        query = query.filter(Patient.phone.startswith(phone.strip()))

    # Specific filter by ICD-10 diagnosis code
    if diagnosis_code:
        query = query.filter(Consultation.diagnosis_code.ilike(f"{diagnosis_code.strip()}%"))

    # General search across multiple fields
    if search_term:
        search = f"%{search_term.strip()}%"
        query = query.filter(
            (Patient.full_name.ilike(search)) | 
            (Patient.phone.ilike(search)) |
            (Consultation.diagnosis_code.ilike(search))
        )
        
    # Get total count of matching records before pagination
    total = query.count()
    
    # Order by created_at DESC (newest to oldest)
    query = query.order_by(Consultation.created_at.desc())
    
    # Apply offset and limit for pagination
    offset = (page - 1) * page_size
    results = query.offset(offset).limit(page_size).all()
    
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
        
    return consultations, total
