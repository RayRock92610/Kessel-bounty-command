from typing import Optional
from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime
from .base import utc_now

class Bounty(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    report_id: uuid.UUID = Field(foreign_key="report.id", index=True)
    researcher_id: uuid.UUID = Field(index=True)
    amount: float
    currency: str = Field(default="USD")
    reward_band: str
    decision_notes: str = Field(default="")
    decided_by_user_id: uuid.UUID = Field(foreign_key="user.id")
    paid_status: str = Field(default="pending") # pending/processing/paid/cancelled
    paid_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
