import json
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Literal, Optional

from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from pydantic import BaseModel, Field

from .config import Settings
from .retry import async_retry

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("ingestion-service")


settings = Settings()
producer: Optional[AIOKafkaProducer] = None
ingested_count = 0
ingest_requests_total = Counter("ingest_requests_total", "Total ingest requests")
ingest_publish_failures_total = Counter("ingest_publish_failures_total", "Total failed publish attempts")
ingest_publish_duration_seconds = Histogram("ingest_publish_duration_seconds", "Kafka publish duration in seconds")


class SensorEvent(BaseModel):
    sensor_id: str = Field(..., min_length=2, max_length=64)
    type: Literal["temperature", "humidity", "aqi", "noise"]
    value: float
    timestamp: datetime
    location_id: Optional[str] = None


@asynccontextmanager
async def lifespan(_: FastAPI):
    global producer
    producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_bootstrap_servers)
    await producer.start()
    logger.info("Kafka producer started on %s", settings.kafka_bootstrap_servers)
    try:
        yield
    finally:
        if producer:
            await producer.stop()
            logger.info("Kafka producer stopped")


app = FastAPI(title="Ingestion Service", version="1.0.0", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.service_name}


@app.get("/metrics/internal")
async def internal_metrics():
    return {"ingested_events": ingested_count}


@app.post("/ingest")
async def ingest_event(event: SensorEvent):
    global ingested_count
    if producer is None:
        raise HTTPException(status_code=503, detail="Kafka producer not initialized")

    payload = event.model_dump(mode="json")
    ingest_requests_total.inc()
    with ingest_publish_duration_seconds.time():
        try:
            await async_retry(
                lambda: producer.send_and_wait(
                    settings.kafka_raw_topic,
                    json.dumps(payload).encode("utf-8"),
                    key=event.sensor_id.encode("utf-8"),
                ),
                retries=4,
                base_delay_seconds=0.15,
            )
        except Exception as exc:  # noqa: BLE001
            ingest_publish_failures_total.inc()
            raise HTTPException(status_code=503, detail=f"Kafka publish failed: {exc}") from exc

    ingested_count += 1
    logger.info("Published event sensor_id=%s type=%s", event.sensor_id, event.type)
    return {"status": "accepted", "topic": settings.kafka_raw_topic}


@app.get("/metrics/prometheus")
async def prometheus_metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
