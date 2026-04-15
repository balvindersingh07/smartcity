import os
from pydantic import BaseModel


class Settings(BaseModel):
    service_name: str = "ingestion-service"
    kafka_bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    kafka_raw_topic: str = os.getenv("KAFKA_RAW_TOPIC", "raw-sensor-data")
