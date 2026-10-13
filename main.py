from fastapi import FastAPI
from app.api.routers.monitor import router as monitors_router
from app.api.routers.monitor_check import router as monitor_check_router

app = FastAPI()

app.include_router(monitors_router)
app.include_router(monitor_check_router)