from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum

from database import Base


class BillingStatus(PyEnum):
    PENDING = "PENDING"
    PAID = "PAID"


class Billing(Base):
    __tablename__ = "billing"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(
        Integer, 
        ForeignKey("appointments.id", ondelete="CASCADE"), 
        unique=True, 
        nullable=False, 
        index=True
    )
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(BillingStatus), nullable=False, default=BillingStatus.PENDING, index=True)
    paid_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    appointment = relationship("Appointment", back_populates="billing")

    def __repr__(self):
        return f"<Billing(id={self.id}, appointment_id={self.appointment_id}, amount={self.amount}, status={self.status.value})>"
