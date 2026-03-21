from datetime import datetime, time
from typing import Optional
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field, field_validator, ConfigDict

from models.appointment import AppointmentStatus


class AppointmentCreate(BaseModel):
    """New appointment request schema."""
    requested_date: datetime = Field(..., description="Preferred appointment date and time")
    query: str = Field(..., max_length=500, description="Patient's reason/query for appointment")
    urgency: Optional[str] = Field(None, description="Optional urgency level")
    past_history: Optional[str] = Field(None, description="Optional past medical history")

    @field_validator('requested_date')
    @classmethod
    def validate_appointment_time(cls, v: datetime) -> datetime:
        """Validate appointment time is between 9 AM and 5 PM IST."""

        # timezone-aware datetime required
        if v.tzinfo is None:
            raise ValueError("Datetime must be timezone-aware (include timezone info).")

        # Convert to IST
        ist = ZoneInfo("Asia/Kolkata")
        local_time = v.astimezone(ist)

        # Define allowed window
        start_time = time(9, 0)   # 9:00 AM
        end_time = time(17, 0)    # 5:00 PM

        # Validate
        if not (start_time <= local_time.time() < end_time):
            raise ValueError("Appointments can only be requested between 9 AM and 5 PM IST.")

        return v


class AppointmentResponse(BaseModel):
    """Appointment response schema."""
    id: int
    patient_id: int
    doctor_id: int
    requested_date: datetime
    status: AppointmentStatus
    doctor_note: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PatientAppointmentResponse(BaseModel):
    """Patient appointment response with names."""
    patient_name: str
    doctor_name: str
    requested_date: datetime
    status: AppointmentStatus
    doctor_note: Optional[str] = None
    query: str
    urgency: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class DoctorAppointmentResponse(BaseModel):
    """Doctor appointment response with patient details."""
    id: int
    patient_id: int
    patient_name: str
    requested_date: datetime
    status: AppointmentStatus
    doctor_note: Optional[str] = None
    created_at: datetime
    query: str
    urgency: Optional[str] = None
    past_history: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AppointmentApprove(BaseModel):
    """Schema for approving an appointment (empty body)."""
    pass


class AppointmentReject(BaseModel):
    """Reject appointment with note schema."""
    doctor_note: str = Field(..., min_length=1, description="Reason for rejection")


class AppointmentTreat(BaseModel):
    """Mark appointment as treated schema (empty body)."""
    pass
