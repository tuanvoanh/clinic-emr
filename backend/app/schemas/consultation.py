from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ConsultationCreate(BaseModel):
    """
    Schema for receiving input data when creating a new consultation record.
    Includes both patient information (creates a new one if not exists) and consultation details.
    """
    patient_name: str = Field(min_length=2, max_length=150, description="Full name of the patient.", json_schema_extra={"example": "Jane Smith"})
    dob: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$", description="Date of birth of the patient (YYYY-MM-DD).", json_schema_extra={"example": "1985-05-15"})
    phone: str = Field(pattern=r"^\d{8,15}$", description="Patient's phone number containing only digits (8-15 digits, without country code). Unique identifier for patients.", json_schema_extra={"example": "81234567"})
    
    diagnosis_code: str = Field(min_length=1, max_length=20, description="ICD-10 diagnosis code.", json_schema_extra={"example": "R51.9"})
    treatment_notes: str = Field(min_length=5, description="Treatment notes, symptoms, and doctor's instructions.", json_schema_extra={"example": "Patient has a tension headache, prescribed mild pain relievers and rest."})

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
