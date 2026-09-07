from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.core.exceptions import AppException
from app.schemas.patient import PatientResponse
from app.repositories import patient as patient_repo

router = APIRouter()

@router.get("/", response_model=List[PatientResponse], summary="Search patients by phone number prefix", description="""
Search patients by phone prefix using index-friendly startswith (e.g. '812345...').
Requires at least 6 digits (starting with 8 or 9).
Optimized to leverage B-Tree database indexing without full table scans.
""")
def search_patients(
    phone: str = Query(
        ...,
        min_length=6,
        max_length=8,
        pattern=r"^[89]\d{5,7}$",
        description="Phone number prefix to search (at least 6 digits, e.g. '812345')"
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
""")
def get_patient_by_phone(
    phone: str,
    db: Session = Depends(get_db)
):
    """
    Endpoint GET /api/patient/{phone}
    """
    patient = patient_repo.get_patient_by_phone(db, phone=phone)
    if not patient:
        raise AppException(error_code="patient_not_found", status_code=404)
    return patient
