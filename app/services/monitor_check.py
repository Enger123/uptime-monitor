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

    def check_monitor(self, monitor_id: int) -> MonitorChecksResponse:
        monitor = self.monitor_repository.get_monitor(monitor_id)
        if not monitor:
            raise HTTPException(status_code=404, detail='Monitor not found')
        start = time.perf_counter()
        try:
            response = httpx.get(monitor.url, timeout=5)
            elapsed = (time.perf_counter() - start) * 1000
            status_code = response.status_code
            is_success = response.is_success
            error_message = None

        except httpx.RequestError as e:
            elapsed = (time.perf_counter() - start) * 1000
            status_code = None
            is_success = False
            error_message = f"{e}"
            
        new_monitor_check = self.monitor_check_repository.create_monitor_check(
            monitor_id=monitor_id,
            status_code=status_code,
            response_time_ms=elapsed,
            is_success=is_success,
            error_message=error_message
        )            
        self.db.commit()
        self.db.refresh(new_monitor_check)
        return MonitorChecksResponse.model_validate(new_monitor_check)

    def list_checks_monitor(self, monitor_id: int, limit: int) -> list[MonitorChecksResponse]:
        monitor = self.monitor_repository.get_monitor(monitor_id)
        if not monitor:
            raise HTTPException(status_code=404, detail='Monitor not found')
        if limit < 0:
            raise HTTPException(status_code=409, detail='Limit can not be negative')
        monitor_checks = self.monitor_check_repository.list_checks_monitor(
            monitor_id, limit
        )
        return [MonitorChecksResponse.model_validate(check)
            for check in monitor_checks]