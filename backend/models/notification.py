from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum

from database import Base


class NotificationType(PyEnum):
    APPROVAL = "APPROVAL"
    REJECTION = "REJECTION"
    REMINDER = "REMINDER"
    COMPLETION = "COMPLETION"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    appointment_id = Column(
        Integer, 
        ForeignKey("appointments.id", ondelete="CASCADE"), 
        nullable=True, 
        index=True
    )
    type = Column(Enum(NotificationType), nullable=False, index=True)
    message = Column(Text, nullable=False)
    channel = Column(String(10), nullable=False, default="EMAIL")
    sent_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    patient = relationship("User", foreign_keys=[patient_id])
    appointment = relationship("Appointment", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.id}, type={self.type.value}, patient_id={self.patient_id})>"
