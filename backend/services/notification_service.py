from sqlalchemy.orm import Session
from models.notification import Notification, NotificationType


def send_notification(
    db: Session,
    patient_id: int,
    appointment_id: int,
    notification_type: NotificationType,
    message: str
) -> Notification:
    """Create notification record in database."""
    try:
        # create notification record
        notification = Notification(
            patient_id=patient_id,
            appointment_id=appointment_id,
            type=notification_type,
            message=message,
            channel="EMAIL"  # default channel for now
        )
        
        # add to database and commit
        db.add(notification)
        db.commit()
        db.refresh(notification)
        
        return notification
        
    except Exception as e:
        # rollback on error
        db.rollback()
        raise e
