from sqlalchemy.orm import Session
from app.models.monitor_check import MonitorCheck
from datetime import datetime, timezone
from sqlalchemy import select

class MonitorCheckRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_monitor_check(
            self,
            monitor_id,
            status_code,
            response_time_ms,
            is_success,
            error_message
    ):
        new_monitor_check = MonitorCheck(
            monitor_id=monitor_id,
            checked_at=datetime.now(timezone.utc),
            status_code=status_code,
            response_time_ms=response_time_ms,
            is_success=is_success,
            error_message=error_message
        )
        self.db.add(new_monitor_check)
        return new_monitor_check

    def list_checks_monitor(self, monitor_id: int, limit: int):
        return self.db.scalars(
            select(MonitorCheck)
            .where(MonitorCheck.monitor_id==monitor_id)
            .order_by(MonitorCheck.checked_at.desc())
            .limit(limit)
            ).all()