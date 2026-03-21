from .auth import router as auth_router
from .appointments import router as appointments_router
from .prescriptions import router as prescriptions_router
from .billing import router as billing_router
from .notifications import router as notifications_router

__all__ = ["auth_router", "appointments_router", "prescriptions_router", "billing_router", "notifications_router"]
