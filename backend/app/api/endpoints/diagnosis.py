from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.schemas.diagnosis import ICD10CodeResponse
from app.repositories import diagnosis as diagnosis_repo

router = APIRouter()

@router.get("/", response_model=List[ICD10CodeResponse], summary="Search for ICD-10 diagnosis codes", description="""
Search for ICD-10 disease codes or descriptions based on a keyword. 
If no keyword is provided, it will return the first codes ordered by code.
""")
def search_diagnoses(
    search: str = Query("", description="Search keyword (can be code or disease name)"),
    limit: int = Query(50, ge=1, le=100, description="Max results to return"),
    db: Session = Depends(get_db)
):
    """
    Endpoint GET /api/diagnosis
    """
    return diagnosis_repo.get_diagnoses_by_term(
        db, search_term=search.strip(), limit=limit
    )
