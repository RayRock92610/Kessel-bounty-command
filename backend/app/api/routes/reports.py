from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.domain import Report, Role
from typing import List

router = APIRouter()

@router.post("/")
def create_report(report: Report, session: Session = Depends(get_session)):
    # Basic triage logic: Assign a default status if missing
    if not report.status:
        report.status = "submitted"
    session.add(report)
    session.commit()
    session.refresh(report)
    return report

@router.get("/")
def list_reports(session: Session = Depends(get_session)):
    return session.exec(select(Report)).all()
