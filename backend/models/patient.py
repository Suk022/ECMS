from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)
    address = Column(Text, nullable=True)
    medical_notes = Column(Text, nullable=True)

    # One-to-one relationship with User
    user = relationship("User", back_populates="patient_profile")

    def __repr__(self):
        return f"<Patient(id={self.id}, user_id={self.user_id})>"
