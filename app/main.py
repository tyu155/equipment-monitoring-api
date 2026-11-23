from fastapi import FastAPI

from app.config import settings
from app.routers.equipment import router as equipment_router

app = FastAPI(
    title=settings.app_name,
    description="REST API for industrial equipment and sensor measurements.",
    version="1.0.0",
)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


app.include_router(equipment_router)
