from fastapi import APIRouter
from app.api.endpoints import diagnosis, consultation

api_router = APIRouter()

api_router.include_router(diagnosis.router, prefix="/diagnosis", tags=["Diagnosis"])
api_router.include_router(consultation.router, prefix="/consultation", tags=["Consultation"])
