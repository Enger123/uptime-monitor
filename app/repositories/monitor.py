from sqlalchemy.orm import Session
from app.models.monitor import Monitor
from sqlalchemy import select

class MonitorRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_monitor(self, name: str, url: str):
        new_link = Monitor(
            name=name,
            url=url
        )
        self.db.add(new_link)
        return new_link

    def get_monitors(self):
        return self.db.scalars(
            select(Monitor)).all()
        
    def get_monitor(self, monitor_id: int):
        return self.db.scalars(
            select(Monitor)
            .where(Monitor.id==monitor_id)).first()

    def get_monitor_by_its_url(self, url: str):
        return self.db.scalars(
            select(Monitor)
        .where(Monitor.url==url)).first()

    def delete_monitor(self, monitor):
        self.db.delete(monitor)