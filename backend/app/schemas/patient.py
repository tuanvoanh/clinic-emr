from pydantic import BaseModel, Field
from typing import Optional

class PatientBase(BaseModel):
    full_name: str = Field(description="Full name of the patient.", json_schema_extra={"example": "John Doe"})
    dob: str = Field(description="Date of birth of the patient, format YYYY-MM-DD.", json_schema_extra={"example": "1990-01-01"})
    phone: str = Field(pattern=r"^[89]\d{7}$", description="Singapore mobile phone number (8 digits, starts with 8 or 9). Unique identifier for patients.", json_schema_extra={"example": "81234567"})

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int = Field(description="Unique identifier of the patient in the system.")

    class Config:
        from_attributes = True
