from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.core.exceptions import AppException, ErrorCode
from app.schemas.patient import PatientResponse
from app.repositories import patient as patient_repo

router = APIRouter()

@router.get("/", response_model=List[PatientResponse], summary="Search patients by phone number prefix (min 6 digits)", description="""
Search patients by phone prefix using index-friendly startswith (e.g. '812345...').
Requires entering at least 6 digits (Singapore mobile numbers: 6 to 8 digits, starting with 8 or 9).
Optimized to leverage B-Tree database indexing without full table scans.
""")
def search_patients(
    phone: str = Query(
        ...,
        min_length=6,
        max_length=8,
        pattern=r"^[89]\d{5,7}$",
        description="Singapore mobile phone number prefix to search (must enter minimum 6 digits, e.g. '812345')"
    ),
    limit: int = Query(20, ge=1, le=100, description="Max results to return"),
    db: Session = Depends(get_db)
):
    """
    Endpoint GET /api/patient?phone=...
    """
    return patient_repo.search_patients_by_phone(db, phone_prefix=phone, limit=limit)

@router.get("/{phone}", response_model=PatientResponse, summary="Get patient by exact phone number", description="""
Retrieve patient details using their exact unique phone number.
Enforces strict 8-digit Singapore mobile phone format validation before querying the database.
""")
def get_patient_by_phone(
    phone: str = Path(
        ...,
        pattern=r"^[89]\d{7}$",
        description="Exact 8-digit Singapore mobile phone number (starts with 8 or 9)"
    ),
    db: Session = Depends(get_db)
):
    """
    Endpoint GET /api/patient/{phone}
    """
    patient = patient_repo.get_patient_by_phone(db, phone=phone)
    if not patient:
        raise AppException(error_code=ErrorCode.PATIENT_NOT_FOUND, status_code=404)
    return patient
