from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.appointment import Appointment, AppointmentStatus
from ..models.user import User, UserRole
from ..schemas.appointment import (
    AppointmentCreate, 
    AppointmentResponse,
    PatientAppointmentResponse,
    DoctorAppointmentResponse,
    AppointmentApprove, 
    AppointmentReject
)
from ..core.dependencies import get_current_user, require_doctor, require_patient
from ..services.notification_service import send_notification
from ..models.notification import NotificationType

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("/", response_model=PatientAppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(
    appointment_data: AppointmentCreate,
    current_user: User = Depends(require_patient),
    db: Session = Depends(get_db)
):
    """Create new appointment request."""
    # find available doctor
    doctor = db.query(User).filter(User.role == UserRole.DOCTOR).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No doctor available. Please contact clinic administration."
        )

    # check: if current user is making multiple appointment requests
    existing_appointments = db.query(Appointment).filter(
        Appointment.patient_id == current_user.id,
        Appointment.status == AppointmentStatus.REQUESTED
    ).all()
    if existing_appointments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a pending appointment request."
        )

    # create appointment with REQUESTED status
    appointment = Appointment(
        patient_id=current_user.id,
        doctor_id=doctor.id,
        requested_date=appointment_data.requested_date,
        query=appointment_data.query,
        urgency=appointment_data.urgency,
        past_history=appointment_data.past_history,
        status=AppointmentStatus.REQUESTED
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    
    # return response with names
    response_data = {
        "id": appointment.id,
        "patient_name": current_user.name,
        "doctor_name": doctor.name,
        "requested_date": appointment.requested_date,
        "status": appointment.status,
        "doctor_note": appointment.doctor_note,
        "query": appointment.query,
        "urgency": appointment.urgency
    }
    
    return PatientAppointmentResponse(**response_data)


@router.get("/requested", response_model=List[DoctorAppointmentResponse])
def get_requested_appointments(
    current_user: User = Depends(require_doctor),
    db: Session = Depends(get_db)
):
    """Get pending appointment requests."""
    appointments = db.query(Appointment).filter(
        Appointment.status == AppointmentStatus.REQUESTED
    ).order_by(Appointment.created_at.asc()).all()
    
    # build response with patient names
    appointment_responses = []
    for appointment in appointments:
        # get patient name
        patient = db.query(User).filter(User.id == appointment.patient_id).first()
        patient_name = patient.name if patient else "Unknown Patient"
        
        response_data = {
            "id": appointment.id,
            "patient_id": appointment.patient_id,
            "patient_name": patient_name,
            "requested_date": appointment.requested_date,
            "status": appointment.status,
            "doctor_note": appointment.doctor_note,
            "created_at": appointment.created_at,
            "query": appointment.query,
            "urgency": appointment.urgency,
            "past_history": appointment.past_history
        }
        appointment_responses.append(DoctorAppointmentResponse(**response_data))
    
    return appointment_responses


@router.get("/approved", response_model=List[DoctorAppointmentResponse])
def get_approved_appointments(
    current_user: User = Depends(require_doctor),
    db: Session = Depends(get_db)
):
    """Get approved appointments."""
    appointments = db.query(Appointment).filter(
        Appointment.status == AppointmentStatus.APPROVED
    ).order_by(Appointment.requested_date.asc()).all()
    
    # build response with patient names
    appointment_responses = []
    for appointment in appointments:
        # get patient name
        patient = db.query(User).filter(User.id == appointment.patient_id).first()
        patient_name = patient.name if patient else "Unknown Patient"
        
        response_data = {
            "id": appointment.id,
            "patient_id": appointment.patient_id,
            "patient_name": patient_name,
            "requested_date": appointment.requested_date,
            "status": appointment.status,
            "doctor_note": appointment.doctor_note,
            "created_at": appointment.created_at,
            "query": appointment.query,
            "urgency": appointment.urgency,
            "past_history": appointment.past_history
        }
        appointment_responses.append(DoctorAppointmentResponse(**response_data))
    
    return appointment_responses


@router.get("/", response_model=List[DoctorAppointmentResponse])
def get_appointments(
    current_user: User = Depends(require_doctor),
    db: Session = Depends(get_db)
):
    """Get all appointments."""
    appointments = db.query(Appointment).all()
    
    # build response with patient names
    appointment_responses = []
    for appointment in appointments:
        # get patient name
        patient = db.query(User).filter(User.id == appointment.patient_id).first()
        patient_name = patient.name if patient else "Unknown Patient"
        
        response_data = {
            "id": appointment.id,
            "patient_id": appointment.patient_id,
            "patient_name": patient_name,
            "requested_date": appointment.requested_date,
            "status": appointment.status,
            "doctor_note": appointment.doctor_note,
            "created_at": appointment.created_at,
            "query": appointment.query,
            "urgency": appointment.urgency,
            "past_history": appointment.past_history
        }
        appointment_responses.append(DoctorAppointmentResponse(**response_data))
    
    return appointment_responses


@router.patch("/{appointment_id}/approve", response_model=AppointmentResponse)
def approve_appointment(
    appointment_id: int,
    current_user: User = Depends(require_doctor),
    db: Session = Depends(get_db)
):
    """Approve appointment."""
    # get appointment
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )

    # status lock — can't approve what's already moved
    if appointment.status != AppointmentStatus.REQUESTED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot approve appointment with status {appointment.status.value}"
        )

    # update status
    appointment.status = AppointmentStatus.APPROVED
    db.commit()
    db.refresh(appointment)

    # send approval notification
    send_notification(
        db=db,
        patient_id=appointment.patient_id,
        appointment_id=appointment.id,
        notification_type=NotificationType.APPROVAL,
        message=f"Your appointment on {appointment.requested_date} has been confirmed."
    )

    return appointment


@router.patch("/{appointment_id}/reject", response_model=AppointmentResponse)
def reject_appointment(
    appointment_id: int,
    rejection_data: AppointmentReject,
    current_user: User = Depends(require_doctor),
    db: Session = Depends(get_db)
):
    """Reject appointment with note."""
    # get appointment
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )

    # status lock — can't reject what's already moved
    if appointment.status != AppointmentStatus.REQUESTED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot reject appointment with status {appointment.status.value}"
        )

    # update status and note
    appointment.status = AppointmentStatus.REJECTED
    appointment.doctor_note = rejection_data.doctor_note
    db.commit()
    db.refresh(appointment)

    # send rejection notification
    send_notification(
        db=db,
        patient_id=appointment.patient_id,
        appointment_id=appointment.id,
        notification_type=NotificationType.REJECTION,
        message=rejection_data.doctor_note
    )

    return appointment

