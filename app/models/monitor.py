from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

class Monitor(Base):
    __tablename__ = 'monitors'

    name: Mapped[str | None] = mapped_column(nullable=True)
    url: Mapped[str] = mapped_column(String(2048), unique=True)
    monitor_checks: Mapped['MonitorCheck'] = relationship(back_populates='monitor')

    def __repr__(self):
        return f"<id={self.id}, name={self.name}, url={self.url}>"

from app.models.monitor_check import MonitorCheck