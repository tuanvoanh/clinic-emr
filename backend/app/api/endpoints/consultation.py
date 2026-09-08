import math
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.exceptions import AppException, ErrorCode
from app.schemas.consultation import (
    ConsultationCreate, 
    ConsultationResponse, 
    PaginatedConsultationResponse
)
from app.schemas.patient import PatientCreate
from app.repositories import patient as patient_repo
from app.repositories import consultation as consultation_repo
from app.repositories import diagnosis as diagnosis_repo
from app.models.diagnosis import ICD10Code

router = APIRouter()

@router.post("/", response_model=dict, summary="Create a new consultation record", description="""
Receives patient information and consultation details.
The system will check if the patient already exists based on Phone Number (unique identifier).
- If not: Automatically creates a new patient record.
- If yes: Reuses the ID of that existing patient.
Then creates and stores the consultation record atomically.
""")
def create_consultation(
    consultation_in: ConsultationCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint POST /api/consultation
    """
    # 1. Validate ICD-10 code
    db_code = db.query(ICD10Code).filter(ICD10Code.code == consultation_in.diagnosis_code).first()
    if not db_code:
        raise AppException(error_code=ErrorCode.INVALID_ICD10_CODE, status_code=400)

    # 2 & 3. Process patient information and create consultation atomically
    patient = patient_repo.get_patient_by_phone(
        db, 
        phone=consultation_in.phone
    )
    
    try:
        if not patient:
            patient_create = PatientCreate(
                full_name=consultation_in.patient_name,
                dob=consultation_in.dob,
                phone=consultation_in.phone
            )
            patient = patient_repo.create_patient(db, patient_in=patient_create, commit=False)
            
        new_consultation = consultation_repo.create_consultation(
            db,
            patient=patient,
            consultation_in=consultation_in,
            commit=False
        )
        db.commit()
    except IntegrityError:
        db.rollback()
        # Handle race condition: patient was concurrently created by another request
        patient = patient_repo.get_patient_by_phone(db, phone=consultation_in.phone)
        if not patient:
            raise AppException(
                error_code=ErrorCode.INTERNAL_SERVER_ERROR,
                status_code=500,
                message="Failed to create consultation record due to concurrent conflict."
            )
        try:
            new_consultation = consultation_repo.create_consultation(
                db,
                patient=patient,
                consultation_in=consultation_in,
                commit=True
            )
        except Exception:
            db.rollback()
            raise AppException(
                error_code=ErrorCode.INTERNAL_SERVER_ERROR,
                status_code=500,
                message="Failed to complete consultation record creation."
            )
    except Exception:
        db.rollback()
        raise

    return {
        "message": "Consultation record created successfully",
        "consultation_id": new_consultation.id
    }


@router.get("/", response_model=PaginatedConsultationResponse, summary="Get paginated list of consultations", description="""
Retrieves the history of medical consultations with pagination.
Supports filtering by exact patient phone number (`phone`) or exact ICD-10 disease code (`diagnosis_code`).
Sorted strictly by creation time (created_at DESC - newest to oldest).
""")
def list_consultations(
    phone: Optional[str] = Query(
        None, 
        pattern=r"^[89]\d{7}$", 
        description="Filter consultations by exact Singapore mobile phone number (8 digits, starts with 8 or 9)"
    ),
    diagnosis_code: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=20, 
        description="Filter consultations by exact ICD-10 diagnosis code (e.g. 'A00.0')"
    ),
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db)
):
    """
    Endpoint GET /api/consultation?phone=...&diagnosis_code=...&page=1&page_size=10
    """
    items, total = consultation_repo.get_all_consultations(
        db, 
        phone=phone,
        diagnosis_code=diagnosis_code,
        page=page, 
        page_size=page_size
    )
    total_pages = math.ceil(total / page_size) if total > 0 else 0

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }
