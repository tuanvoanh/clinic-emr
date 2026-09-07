from fastapi import APIRouter, Depends
from app.api.endpoints import diagnosis, consultation, patient, auth
from app.api.dependencies import get_current_user

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(diagnosis.router, prefix="/diagnosis", tags=["Diagnosis"], dependencies=[Depends(get_current_user)])
api_router.include_router(consultation.router, prefix="/consultation", tags=["Consultation"], dependencies=[Depends(get_current_user)])
api_router.include_router(patient.router, prefix="/patient", tags=["Patient"], dependencies=[Depends(get_current_user)])
