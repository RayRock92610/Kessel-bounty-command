from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON
import uuid
from datetime import datetime, date
from .base import utc_now

class MetricsSnapshot(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    snapshot_date: date = Field(index=True)
    program_id: Optional[uuid.UUID] = Field(default=None, index=True)
    team_id: Optional[uuid.UUID] = Field(default=None, index=True)
    metric_key: str = Field(index=True)
    metric_value_numeric: Optional[float] = Field(default=None)
    metric_value_json: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=utc_now)
