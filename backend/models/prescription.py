from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(
        Integer, 
        ForeignKey("appointments.id", ondelete="CASCADE"), 
        unique=True, 
        nullable=False, 
        index=True
    )
    doctor_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    clinical_notes = Column(Text, nullable=True)
    medications = Column(JSON, nullable=True)  # Using JSON for PostgreSQL JSONB compatibility
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    appointment = relationship("Appointment", back_populates="prescription")
    doctor = relationship("User", foreign_keys=[doctor_id])

    def __repr__(self):
        return f"<Prescription(id={self.id}, appointment_id={self.appointment_id}, doctor_id={self.doctor_id})>"
