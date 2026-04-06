from typing import Optional
from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime
from .base import utc_now

class Comment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    report_id: uuid.UUID = Field(foreign_key="report.id", index=True)
    author_user_id: uuid.UUID = Field(foreign_key="user.id")
    comment_type: str = Field(default="comment") # comment/status_change/system_note
    body: str
    visibility: str = Field(default="internal") # internal/researcher/private
    created_at: datetime = Field(default_factory=utc_now)
