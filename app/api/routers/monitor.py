from app.schemas.monitor import UrlGiven, MonitorUpdateSchema, MonitorResponse
from fastapi import APIRouter, status
from app.api.dependencies import MonitorServiceDep

router = APIRouter()

@router.post("/monitors", 
             response_model=MonitorResponse, 
             status_code=status.HTTP_201_CREATED
             )
def create_monitor(
    link: UrlGiven,
    monitor_service: MonitorServiceDep
    ):
    return monitor_service.create_monitor(link)

@router.get("/monitors", response_model=list[MonitorResponse])
def get_monitors(
    monitor_service: MonitorServiceDep
):
    return monitor_service.get_monitors()

@router.get("/monitors/{monitor_id}", response_model=MonitorResponse)
def get_monitor(
    monitor_id: int,
    monitor_service: MonitorServiceDep
):
    return monitor_service.get_monitor(monitor_id)

@router.patch("/monitors/{monitor_id}", response_model=MonitorResponse)
def change_monitor(
    monitor_id: int,
    new_monitor: MonitorUpdateSchema,
    monitor_service: MonitorServiceDep
):
    return monitor_service.change_monitor(monitor_id, new_monitor)

@router.delete("/monitors/{monitor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_monitor(
    monitor_id: int,
    monitor_service: MonitorServiceDep
):
    return monitor_service.delete_monitor(monitor_id)

