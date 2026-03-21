from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field

from models.billing import BillingStatus


class BillingCreate(BaseModel):
    """New billing record schema."""
    appointment_id: int = Field(..., description="Associated appointment ID")
    amount: Decimal = Field(..., gt=0, description="Billing amount (must be greater than 0)")


class BillingResponse(BaseModel):
    """Billing response schema."""
    id: int
    appointment_id: int
    amount: Decimal
    status: BillingStatus
    paid_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BillingPay(BaseModel):
    """Schema for marking billing as paid (empty body)."""
    pass
