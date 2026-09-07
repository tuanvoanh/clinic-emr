import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.base import Base

class Consultation(Base):
    """
    Model for storing medical consultation records.
    Links to Patient and ICD10Code models.
    """
    __tablename__ = "consultations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"))
    diagnosis_code: Mapped[str] = mapped_column(ForeignKey("icd10_codes.code"))
    treatment_notes: Mapped[str] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column(default=lambda: datetime.datetime.now(datetime.timezone.utc))

    # Relationships
    patient = relationship("Patient", back_populates="consultations")
    diagnosis = relationship("ICD10Code", back_populates="consultations")
