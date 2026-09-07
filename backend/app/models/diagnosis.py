from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.base import Base

class ICD10Code(Base):
    """
    Model for storing the list of standard ICD-10 disease codes.
    """
    __tablename__ = "icd10_codes"

    code: Mapped[str] = mapped_column(primary_key=True, index=True)
    description: Mapped[str] = mapped_column()

    # One-to-Many relationship with Consultation table
    consultations = relationship("Consultation", back_populates="diagnosis")
