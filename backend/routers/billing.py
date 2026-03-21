from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.billing import Billing, BillingStatus
from ..models.appointment import Appointment, AppointmentStatus
from ..models.user import User
from ..schemas.billing import BillingCreate, BillingResponse, BillingPay
from ..core.dependencies import get_current_user, require_doctor, require_receptionist
from ..services.notification_service import send_notification
from ..models.notification import NotificationType

router = APIRouter(prefix="/billing", tags=["billing"])


@router.post("/", response_model=BillingResponse, status_code=status.HTTP_201_CREATED)
def create_billing(
    billing_data: BillingCreate,
    current_user: User = Depends(require_doctor),
    db: Session = Depends(get_db)
):
    """
    Create a new billing record.
    Only doctors can create billing records.
    Appointment must be in APPROVED status.
    Only one billing record per appointment allowed.
    """
    # Verify appointment exists and is approved
    appointment = db.query(Appointment).filter(Appointment.id == billing_data.appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Validate appointment status
    if appointment.status != AppointmentStatus.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot create billing for appointment with status {appointment.status.value}. Appointment must be APPROVED."
        )
    
    # Check if billing already exists for this appointment
    existing_billing = db.query(Billing).filter(
        Billing.appointment_id == billing_data.appointment_id
    ).first()
    
    if existing_billing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Billing record already exists for this appointment"
        )
    
    # Create billing record with PENDING status
    billing = Billing(
        appointment_id=billing_data.appointment_id,
        amount=billing_data.amount,
        status=BillingStatus.PENDING
    )
    
    db.add(billing)
    db.commit()
    db.refresh(billing)
    
    return billing


@router.patch("/{billing_id}/pay", response_model=BillingResponse)
def mark_billing_paid(
    billing_id: int,
    current_user: User = Depends(require_receptionist),
    db: Session = Depends(get_db)
):
    """
    Mark billing as paid.
    Only receptionists can mark billing as paid.
    Updates status to PAID and sets paid_at timestamp.
    """
    # Get billing record
    billing = db.query(Billing).filter(Billing.id == billing_id).first()
    if not billing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Billing record not found"
        )
    
    # Validate status transition
    if billing.status != BillingStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot mark billing as paid. Current status is {billing.status.value}, expected PENDING."
        )
    
    # Update status and timestamp
    billing.status = BillingStatus.PAID
    billing.paid_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(billing)
    
    # Send reminder notification to patient
    appointment = db.query(Appointment).filter(Appointment.id == billing.appointment_id).first()
    if appointment:
        send_notification(
            db=db,
            patient_id=appointment.patient_id,
            appointment_id=appointment.id,
            notification_type=NotificationType.REMINDER,
            message="Payment confirmed. Please follow the care instructions provided by your doctor."
        )
    
    return billing
