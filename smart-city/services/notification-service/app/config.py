import os
from pydantic import BaseModel


class Settings(BaseModel):
    service_name: str = "notification-service"
    kafka_bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    kafka_alerts_topic: str = os.getenv("KAFKA_ALERTS_TOPIC", "sensor-alerts")
    consumer_group: str = "notification-service-group"
