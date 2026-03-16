from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum

from database import Base


class AppointmentStatus(PyEnum):
    REQUESTED = "REQUESTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    TREATED = "TREATED"


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    requested_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(AppointmentStatus), nullable=False, default=AppointmentStatus.REQUESTED, index=True)
    doctor_note = Column(Text, nullable=True)
    treated_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    patient = relationship("User", foreign_keys=[patient_id], back_populates="appointments_as_patient")
    doctor = relationship("User", foreign_keys=[doctor_id], back_populates="appointments_as_doctor")
    
    # One-to-one relationships
    prescription = relationship(
        "Prescription", 
        back_populates="appointment",
        uselist=False,
        cascade="all, delete-orphan"
    )
    
    billing = relationship(
        "Billing", 
        back_populates="appointment",
        uselist=False,
        cascade="all, delete-orphan"
    )
    
    # One-to-many relationship
    notifications = relationship(
        "Notification", 
        back_populates="appointment",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Appointment(id={self.id}, status={self.status.value}, patient_id={self.patient_id})>"
