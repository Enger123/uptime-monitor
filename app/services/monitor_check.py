from sqlalchemy.orm import Session
from app.repositories.monitor_check import MonitorCheckRepository
from app.repositories.monitor import MonitorRepository
from fastapi import HTTPException
import httpx, time
from app.schemas.monitor_checks import MonitorChecksResponse

class MonitorCheckService:
    def __init__(self, db: Session):
        self.db = db
        self.monitor_check_repository = MonitorCheckRepository(db)
        self.monitor_repository = MonitorRepository(db)

    def check_monitor(self, monitor_id: int):
        monitor = self.monitor_repository.get_monitor(monitor_id)
        if not monitor:
            raise HTTPException(status_code=404, detail='Monitor not found')
        start = time.perf_counter()
        response = httpx.get(monitor.url)
        elapsed = time.perf_counter() - start
        new_monitor_check = self.monitor_check_repository.create_monitor_check(
            monitor_id=monitor_id,
            status_code=response.status_code,
            response_time_ms=elapsed,
            is_success=True,
            error_message=None
        )
        self.db.commit()
        self.db.refresh(new_monitor_check)
        return MonitorChecksResponse.model_validate(new_monitor_check)