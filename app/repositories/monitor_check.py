from sqlalchemy.orm import Session
from app.models.monitor_check import MonitorCheck
from datetime import datetime

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
            checked_at=datetime.now(),
            status_code=status_code,
            response_time_ms=f"{response_time_ms} ms",
            is_success=is_success,
            error_message=error_message
        )
        self.db.add(new_monitor_check)
        return new_monitor_check