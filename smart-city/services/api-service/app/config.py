import os
from pydantic import BaseModel


class Settings(BaseModel):
    service_name: str = "api-service"
    storage_base_url: str = os.getenv("STORAGE_SERVICE_URL", "http://storage-service:8003")
    notification_base_url: str = os.getenv("NOTIFICATION_SERVICE_URL", "http://notification-service:8005")
