from datetime import datetime, timedelta
from app.models.domain import Report, ReportState

class TriageService:
    @staticmethod
    def calculate_sla(report: Report):
        sla_hours = {"critical": 24, "high": 48, "medium": 96, "low": 168}
        hours = sla_hours.get(report.severity.lower(), 72)
        report.triage_due_at = datetime.utcnow() + timedelta(hours=hours)
        return report
