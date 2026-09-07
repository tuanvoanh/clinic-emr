# Gather all models for easy import when running metadata.create_all()
from .base import Base
from .patient import Patient
from .diagnosis import ICD10Code
from .consultation import Consultation
