from pydantic import BaseModel
from datetime import datetime

class MonitorChecksResponse(BaseModel):
    id: int
    monitor_id: int
    checked_at: datetime
    status_code: int | None = None
    response_time_ms: float
    is_success: bool
    error_message: str | None = None
    model_config={'from_attributes': True}
