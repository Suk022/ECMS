from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class PrescriptionCreate(BaseModel):
    """Schema for creating a new prescription."""
    appointment_id: int = Field(..., description="Associated appointment ID")
    clinical_notes: Optional[str] = Field(None, description="Doctor's clinical observations")
    medications: Optional[List[Dict[str, Any]]] = Field(
        default=[], 
        description="List of medications with name, dose, frequency, duration"
    )


class PrescriptionResponse(BaseModel):
    """Prescription response schema."""
    id: int
    appointment_id: int
    doctor_id: int
    clinical_notes: Optional[str] = None
    medications: Optional[List[Dict[str, Any]]] = None
    created_at: datetime

    class Config:
        from_attributes = True
