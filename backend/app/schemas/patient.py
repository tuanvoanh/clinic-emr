from pydantic import BaseModel, Field, field_validator
from typing import Optional

from app.schemas.validators import DOB_PATTERN, validate_date_of_birth

class PatientBase(BaseModel):
    full_name: str = Field(description="Full name of the patient.", json_schema_extra={"example": "John Doe"})
    dob: str = Field(pattern=DOB_PATTERN, description="Date of birth of the patient, format YYYY-MM-DD.", json_schema_extra={"example": "1990-01-01"})
    phone: str = Field(pattern=r"^[89]\d{7}$", description="Singapore mobile phone number (8 digits, starts with 8 or 9). Unique identifier for patients.", json_schema_extra={"example": "81234567"})

    @field_validator("dob")
    @classmethod
    def validate_dob(cls, v: str) -> str:
        return validate_date_of_birth(v)

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int = Field(description="Unique identifier of the patient in the system.")

    class Config:
        from_attributes = True
