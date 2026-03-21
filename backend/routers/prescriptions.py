from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.prescription import Prescription
from ..models.appointment import Appointment, AppointmentStatus
from ..models.user import User
from ..schemas.prescription import PrescriptionCreate, PrescriptionResponse
from ..core.dependencies import get_current_user, require_doctor, require_receptionist

router = APIRouter(prefix="/prescriptions", tags=["prescriptions"])


@router.post("/", response_model=PrescriptionResponse, status_code=status.HTTP_201_CREATED)
def create_prescription(
    prescription_data: PrescriptionCreate,
    current_user: User = Depends(require_doctor),
    db: Session = Depends(get_db)
):
    """
    Create a new prescription.
    Only doctors can create prescriptions.
    Appointment must be in APPROVED status.
    Only one prescription per appointment allowed.
    """
    # Verify appointment exists and is approved
    appointment = db.query(Appointment).filter(Appointment.id == prescription_data.appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Validate appointment status
    if appointment.status != AppointmentStatus.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot create prescription for appointment with status {appointment.status.value}. Appointment must be APPROVED."
        )
    
    # Check if prescription already exists for this appointment
    existing_prescription = db.query(Prescription).filter(
        Prescription.appointment_id == prescription_data.appointment_id
    ).first()
    
    if existing_prescription:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prescription already exists for this appointment"
        )
    
    # Create prescription
    prescription = Prescription(
        appointment_id=prescription_data.appointment_id,
        doctor_id=current_user.id,
        clinical_notes=prescription_data.clinical_notes,
        medications=prescription_data.medications
    )
    
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    
    return prescription


@router.get("/{appointment_id}", response_model=PrescriptionResponse)
def get_prescription(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get prescription for a specific appointment.
    Only doctors and receptionists can access prescriptions.
    """
    # Verify user role (doctor or receptionist)
    if current_user.role.value not in ["DOCTOR", "RECEPTIONIST"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Only doctors and receptionists can view prescriptions"
        )
    
    # Get prescription
    prescription = db.query(Prescription).filter(
        Prescription.appointment_id == appointment_id
    ).first()
    
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription not found for this appointment"
        )
    
    return prescription
