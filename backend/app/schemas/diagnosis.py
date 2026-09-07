from pydantic import BaseModel, Field

class ICD10CodeBase(BaseModel):
    code: str = Field(description="Standard ICD-10 disease code.", json_schema_extra={"example": "J45.909"})
    description: str = Field(description="Detailed description of the disease code.", json_schema_extra={"example": "Unspecified asthma, uncomplicated"})

class ICD10CodeResponse(ICD10CodeBase):
    class Config:
        from_attributes = True
