import os
from pydantic import BaseModel


class Settings(BaseModel):
    service_name: str = "storage-service"
    kafka_bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    kafka_processed_topic: str = os.getenv("KAFKA_PROCESSED_TOPIC", "processed-sensor-data")
    consumer_group: str = "storage-service-group"
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://smartcity:smartcity@postgres:5432/smartcity")
