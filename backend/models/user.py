from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum

from database import Base


class UserRole(PyEnum):
    DOCTOR = "DOCTOR"
    RECEPTIONIST = "RECEPTIONIST"
    PATIENT = "PATIENT"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    phone = Column(String(15), nullable=True)
    role = Column(Enum(UserRole), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    appointments_as_patient = relationship(
        "Appointment", 
        back_populates="patient",
        foreign_keys="Appointment.patient_id"
    )
    
    appointments_as_doctor = relationship(
        "Appointment", 
        back_populates="doctor",
        foreign_keys="Appointment.doctor_id"
    )
    
    patient_profile = relationship(
        "Patient", 
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role.value})>"
