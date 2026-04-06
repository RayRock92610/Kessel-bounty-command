from sqlmodel import Session, select, func
from sqlalchemy import case, extract
from app.models.report import Report
from app.models.metrics_snapshot import MetricsSnapshot
from datetime import datetime, timezone

class MetricsCalculator:
    def __init__(self, session: Session):
        self.session = session

    def calculate_open_findings_by_severity(self):
        """Calculates the count of unresolved reports grouped by severity."""
        statement = (
            select(Report.severity, func.count(Report.id).label("count"))
            .where(Report.state.not_in(["resolved", "closed", "rejected_invalid", "duplicate"]))
            .group_by(Report.severity)
        )
        results = self.session.exec(statement).all()
        return {row.severity: row.count for row in results}

    def calculate_mttr(self):
        """Calculates Mean Time To Resolution (MTTR) in hours for resolved reports."""
        # Extract epoch difference between created_at and resolved_at
        time_diff = extract('epoch', Report.resolved_at) - extract('epoch', Report.created_at)
        
        statement = (
            select(func.avg(time_diff).label("avg_resolution_seconds"))
            .where(Report.state == "resolved")
            .where(Report.resolved_at != None)
        )
        result = self.session.exec(statement).first()
        
        if result and result > 0:
            return round(result / 3600, 2) # Convert seconds to hours
        return 0.0

    def calculate_duplicate_rate(self):
        """Calculates the percentage of reports marked as duplicate."""
        total_statement = select(func.count(Report.id))
        total_reports = self.session.exec(total_statement).first() or 0
        
        if total_reports == 0:
            return 0.0
            
        dup_statement = select(func.count(Report.id)).where(Report.state == "duplicate")
        dup_reports = self.session.exec(dup_statement).first() or 0
        
        return round((dup_reports / total_reports) * 100, 2)

    def generate_daily_snapshot(self):
        """Generates and saves the daily metrics snapshot."""
        today = datetime.now(timezone.utc).date()
        
        # 1. Open Findings
        open_findings = self.calculate_open_findings_by_severity()
        snapshot_open = MetricsSnapshot(
            snapshot_date=today,
            metric_key="open_findings_by_severity",
            metric_value_json=open_findings
        )
        
        # 2. MTTR
        mttr_hours = self.calculate_mttr()
        snapshot_mttr = MetricsSnapshot(
            snapshot_date=today,
            metric_key="mttr_hours",
            metric_value_numeric=mttr_hours
        )
        
        # 3. Duplicate Rate
        dup_rate = self.calculate_duplicate_rate()
        snapshot_dup = MetricsSnapshot(
            snapshot_date=today,
            metric_key="duplicate_rate_percentage",
            metric_value_numeric=dup_rate
        )
        
        self.session.add_all([snapshot_open, snapshot_mttr, snapshot_dup])
        self.session.commit()
        
        return {
            "open_findings": open_findings,
            "mttr_hours": mttr_hours,
            "duplicate_rate": dup_rate
        }
