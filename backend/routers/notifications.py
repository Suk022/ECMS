from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.notification import Notification
from models.user import User
from core.dependencies import require_patient

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/me", response_model=List[dict])
def get_my_notifications(
    current_user: User = Depends(require_patient),
    db: Session = Depends(get_db)
):
    """
    Get all notifications for the current patient.
    Only patients can access their own notifications.
    """
    # Get all notifications for this patient
    notifications = db.query(Notification).filter(
        Notification.patient_id == current_user.id
    ).order_by(Notification.sent_at.asc()).all()
    
    # Convert to response format
    notification_list = []
    for notification in notifications:
        notification_data = {
            "id": notification.id,
            "appointment_id": notification.appointment_id,
            "type": notification.type.value,
            "message": notification.message,
            "channel": notification.channel,
            "sent_at": notification.sent_at
        }
        notification_list.append(notification_data)
    
    return notification_list
