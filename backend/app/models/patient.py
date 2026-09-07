from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base

from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

class Patient(Base):
    """
    Model for storing patient information.
    Includes full name, date of birth, and unique phone number.
    """
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(index=True)
    dob: Mapped[str] = mapped_column(index=True)
    phone: Mapped[str] = mapped_column(unique=True, index=True)

    # One-to-Many relationship with Consultation table
    consultations = relationship("Consultation", back_populates="patient")
