import os
from pydantic import BaseModel


class Settings(BaseModel):
    service_name: str = "processing-service"
    kafka_bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    kafka_raw_topic: str = os.getenv("KAFKA_RAW_TOPIC", "raw-sensor-data")
    kafka_processed_topic: str = os.getenv("KAFKA_PROCESSED_TOPIC", "processed-sensor-data")
    kafka_alerts_topic: str = os.getenv("KAFKA_ALERTS_TOPIC", "sensor-alerts")
    kafka_dlq_topic: str = os.getenv("KAFKA_DLQ_TOPIC", "sensor-dlq")
    consumer_group: str = "processing-service-group"
