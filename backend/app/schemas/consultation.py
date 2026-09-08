from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

from app.schemas.validators import DOB_PATTERN, validate_date_of_birth

class ConsultationCreate(BaseModel):
    """
    Schema for receiving input data when creating a new consultation record.
    Includes both patient information (creates a new one if not exists) and consultation details.
    """
    patient_name: str = Field(min_length=2, max_length=150, description="Full name of the patient.", json_schema_extra={"example": "Jane Smith"})
    dob: str = Field(pattern=DOB_PATTERN, description="Date of birth of the patient (YYYY-MM-DD).", json_schema_extra={"example": "1985-05-15"})
    phone: str = Field(pattern=r"^[89]\d{7}$", description="Patient's Singapore mobile phone number (8 digits, starts with 8 or 9). Unique identifier for patients.", json_schema_extra={"example": "81234567"})
    
    diagnosis_code: str = Field(min_length=1, max_length=20, description="ICD-10 diagnosis code.", json_schema_extra={"example": "R51.9"})
    treatment_notes: str = Field(min_length=5, description="Treatment notes, symptoms, and doctor's instructions.", json_schema_extra={"example": "Patient has a tension headache, prescribed mild pain relievers and rest."})

    @field_validator("dob")
    @classmethod
    def validate_dob(cls, v: str) -> str:
        return validate_date_of_birth(v)

class ConsultationResponse(BaseModel):
    """
    Schema for outputting historical consultation data.
    """
    id: int = Field(description="Unique identifier of the consultation.")
    patient_id: int = Field(description="Unique identifier of the patient.")
    full_name: str = Field(description="Patient's full name.")
    dob: str = Field(description="Date of birth.")
    phone: str = Field(description="Patient's unique phone number.")
    diagnosis_code: str = Field(description="ICD-10 disease code.")
    diagnosis_desc: str = Field(description="Description of the ICD-10 code.")
    treatment_notes: str = Field(description="Treatment notes.")
    created_at: datetime = Field(description="Time the consultation was created.")

    class Config:
        from_attributes = True

class PaginatedConsultationResponse(BaseModel):
    """
    Schema for paginated consultation list response.
    """
    items: List[ConsultationResponse] = Field(description="List of consultations for the current page.")
    total: int = Field(description="Total number of matching consultation records.")
    page: int = Field(description="Current page number.")
    page_size: int = Field(description="Number of items per page.")
    total_pages: int = Field(description="Total number of pages.")

