from app.db.session import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.params import Depends
from app.services.monitor import MonitorService
from app.services.monitor_check import MonitorCheckService

DBSession = Annotated[Session, Depends(get_db)]

def get_monitor_service(db: DBSession):
    return MonitorService(db)

def get_monitor_check_service(db: DBSession):
    return MonitorCheckService(db)

MonitorServiceDep = Annotated[MonitorService, Depends(get_monitor_service)]
MonitorCheckServiceDep = Annotated[MonitorCheckService, Depends(get_monitor_check_service)]
