from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime

class MonitorCheck(Base):
    __tablename__ = 'monitor_checks'

    monitor_id: Mapped[int] = mapped_column(ForeignKey('monitors.id'))
    checked_at: Mapped[datetime]
    status_code: Mapped[int | None] = mapped_column(nullable=True)
    response_time_ms: Mapped[float]
    is_success: Mapped[bool]
    error_message: Mapped[str | None] = mapped_column(nullable=True)
    monitor: Mapped['Monitor'] = relationship(back_populates='monitor_checks')

    def __repr__(self):
        return f"<id={self.id}, monitor_id={self.monitor_id}, checked_at={self.checked_at}, status_code={self.status_code}, response_time_ms={self.response_time_ms}, is_success={self.is_success}, error_message={self.error_message}>"


from app.models.monitor import Monitor
