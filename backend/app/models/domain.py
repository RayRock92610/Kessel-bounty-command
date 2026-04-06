from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, JSON, Text
from sqlmodel import SQLModel, Field

# 1. User | 2. Role 
class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True); permissions: Dict[str, bool] = Field(default_factory=dict, sa_column=Column(JSON))

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True); password_hash: str
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")

# 3. Team | 4. Program | 6. ScopeRule
class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str; slug: str = Field(unique=True)

class Program(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str; slug: str = Field(unique=True); policy_markdown: str = Field(sa_column=Column(Text))

class ScopeRule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    program_id: int = Field(foreign_key="program.id"); pattern: str; rule_type: str = "include"

# 5. Asset | 7. Researcher | 8. Report | 13. SLAProfile
class Asset(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    program_id: int = Field(index=True); identifier: str; asset_type: str

class Researcher(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    handle: str = Field(unique=True); payout_email: str

class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    report_code: str = Field(index=True, unique=True); title: str; severity: str = "info"; status: str = "submitted"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SLAProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str; triage_hours: int

# 9. Weakness | 10. Evidence | 11. Comment | 12. Bounty
class Weakness(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str; slug: str = Field(unique=True); family: str; cwe_id: int

class Evidence(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    report_id: int = Field(foreign_key="report.id"); file_path: str

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    report_id: int = Field(foreign_key="report.id"); body: str

class Bounty(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    report_id: int = Field(foreign_key="report.id"); amount: float

# 14. Notification | 15. Integration | 16. AuditEvent | 17. MetricSnapshot
class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int; message: str

class Integration(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    service_name: str; api_key: str

class AuditEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_type: str; details: str; created_at: datetime = Field(default_factory=datetime.utcnow)

class MetricSnapshot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    metric_name: str; value: float; timestamp: datetime = Field(default_factory=datetime.utcnow)

# 18. SponsorshipTier (The New Entity)
class SponsorshipTier(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str; amount: float; description: str
