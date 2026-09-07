from pydantic import BaseModel, Field
from typing import Optional

class PatientBase(BaseModel):
    full_name: str = Field(description="Full name of the patient.", json_schema_extra={"example": "John Doe"})
    dob: str = Field(description="Date of birth of the patient, format YYYY-MM-DD.", json_schema_extra={"example": "1990-01-01"})
    phone: str = Field(pattern=r"^\+[1-9]\d{7,14}$", description="Contact phone number of the patient in E.164 international format (8-15 digits total). Unique identifier for patients.", json_schema_extra={"example": "+84901234567"})

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int = Field(description="Unique identifier of the patient in the system.")

    class Config:
        from_attributes = True
