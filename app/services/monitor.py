from sqlalchemy.orm import Session
from app.repositories.monitor import MonitorRepository
from app.schemas.monitor import UrlGiven, MonitorResponse, MonitorUpdateSchema
from fastapi import HTTPException

class MonitorService:
    def __init__(self, db: Session):
        self.db = db
        self.monitor_repository = MonitorRepository(db)

    def create_monitor(self, link: UrlGiven):
        checking_url = self.monitor_repository.get_monitor_by_its_url(str(link.url))
        if checking_url is not None:
            raise HTTPException(status_code=409, detail='Url is already in monitors')

        new_link = self.monitor_repository.create_monitor(link.name, str(link.url))
        self.db.commit()
        self.db.refresh(new_link)
        return MonitorResponse.model_validate(new_link)

    def get_monitors(self):
        monitors = self.monitor_repository.get_monitors()
        return [MonitorResponse.model_validate(monitor)
            for monitor in monitors]

    def get_monitor(self, monitor_id: int):
        monitor = self.monitor_repository.get_monitor(monitor_id)
        if not monitor:
            raise HTTPException(status_code=404, detail='Monitor not found')
        return MonitorResponse.model_validate(monitor)

    def change_monitor(self, monitor_id, new_monitor: MonitorUpdateSchema):
        monitor = self.monitor_repository.get_monitor(monitor_id)
        if not monitor:
            raise HTTPException(status_code=404, detail='Monitor not found')
        if new_monitor.name is not None:
            monitor.name = new_monitor.name
        if new_monitor.url is not None:
            monitor.url = new_monitor.url
        self.db.commit()
        self.db.refresh(monitor)
        return MonitorResponse.model_validate(monitor)

    def delete_monitor(self, monitor_id: int):
        monitor = self.monitor_repository.get_monitor(monitor_id)
        if not monitor:
            raise HTTPException(status_code=404, detail='Monitor not found')
        self.monitor_repository.delete_monitor(monitor)
        self.db.commit()

    

