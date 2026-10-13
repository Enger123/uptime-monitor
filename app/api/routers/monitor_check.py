from fastapi import APIRouter
from app.api.dependencies import MonitorCheckServiceDep


router = APIRouter()


@router.post("/monitors/{monitor_id}/checks")
def check_monitor(monitor_id: int, monitor_service: MonitorCheckServiceDep):
    return monitor_service.check_monitor(monitor_id)
