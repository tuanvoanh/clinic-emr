from sqlalchemy.orm import Session
from app.models.diagnosis import ICD10Code
from typing import List

def get_diagnoses_by_term(db: Session, search_term: str, limit: int = 20) -> List[ICD10Code]:
    """
    Search for ICD-10 disease codes based on a keyword.
    
    Args:
        db (Session): Database session.
        search_term (str): Search keyword (can be code or description).
        limit (int): Maximum number of results to return (default is 20).
        
    Returns:
        List[ICD10Code]: List of matching disease codes.
    """
    if not search_term:
        return db.query(ICD10Code).all()
        
    search = f"%{search_term}%"
    return db.query(ICD10Code).filter(
        (ICD10Code.code.ilike(search)) | (ICD10Code.description.ilike(search))
    ).limit(limit).all()
