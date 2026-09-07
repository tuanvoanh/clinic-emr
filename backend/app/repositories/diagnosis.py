from sqlalchemy import case
from sqlalchemy.orm import Session
from app.models.diagnosis import ICD10Code
from typing import List

def get_diagnoses_by_term(db: Session, search_term: str, limit: int = 50) -> List[ICD10Code]:
    """
    Search for ICD-10 disease codes based on a keyword.
    
    Args:
        db (Session): Database session.
        search_term (str): Search keyword (can be code or description).
        limit (int): Maximum number of results to return (default is 50).
        
    Returns:
        List[ICD10Code]: List of matching disease codes.
    """
    query = db.query(ICD10Code)
    if search_term:
        search = f"%{search_term}%"
        code_prefix = f"{search_term}%"
        query = query.filter(
            (ICD10Code.code.ilike(search))
            | (ICD10Code.description.ilike(search))
        )
        query = query.order_by(
            case((ICD10Code.code.ilike(code_prefix), 0), else_=1),
            ICD10Code.code,
        )
    else:
        query = query.order_by(ICD10Code.code)

    return query.limit(limit).all()
