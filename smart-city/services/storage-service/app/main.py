import asyncio
import contextlib
import json
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional

from aiokafka import AIOKafkaConsumer
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .config import Settings
from .database import SessionLocal, engine, get_db
from .models import Base, Location, Sensor, SensorData
from .schemas import LocationCreate, SensorCreate, SensorRead


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("storage-service")

settings = Settings()
KAFKA_BOOTSTRAP = settings.kafka_bootstrap_servers
PROCESSED_TOPIC = settings.kafka_processed_topic
CONSUMER_GROUP = settings.consumer_group

consumer: Optional[AIOKafkaConsumer] = None
consumer_task: Optional[asyncio.Task] = None
stored_events_total = Counter("stored_events_total", "Total processed events stored in DB")


async def consume_processed_events():
    assert consumer is not None
    async for msg in consumer:
        event = json.loads(msg.value.decode("utf-8"))
        async with SessionLocal() as db:
            try:
                sensor_id = event["sensor_id"]
                sensor = await db.get(Sensor, sensor_id)
                if not sensor:
                    location_id = event.get("location_id") or "default-zone"
                    location = await db.get(Location, location_id)
                    if not location:
                        db.add(Location(id=location_id, name="Auto Zone", city="Smart City"))
                    db.add(Sensor(id=sensor_id, type=event["type"], location_id=location_id, status="active"))

                # Normalize to timezone-naive UTC for TIMESTAMP WITHOUT TIME ZONE columns.
                recorded_at = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00")).astimezone(
                    timezone.utc
                )
                recorded_at = recorded_at.replace(tzinfo=None)

                db.add(
                    SensorData(
                        sensor_id=sensor_id,
                        type=event["type"],
                        value=float(event["value"]),
                        rolling_avg=event.get("rolling_avg"),
                        is_valid=bool(event.get("is_valid", False)),
                        recorded_at=recorded_at,
                    )
                )
                await db.commit()
                stored_events_total.inc()
            except Exception as exc:  # noqa: BLE001
                await db.rollback()
                logger.exception("Failed to persist processed event: %s | event=%s", exc, event)


async def _start_storage_consumer():
    global consumer, consumer_task
    try:
        c = AIOKafkaConsumer(
            PROCESSED_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP,
            group_id=CONSUMER_GROUP,
            auto_offset_reset="latest",
        )
        await c.start()
        consumer = c
        consumer_task = asyncio.create_task(consume_processed_events())
        logger.info("Storage consumer started")
    except Exception:
        logger.exception("Storage Kafka consumer failed to start")


@asynccontextmanager
async def lifespan(_: FastAPI):
    global consumer, consumer_task
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    asyncio.create_task(_start_storage_consumer())
    try:
        yield
    finally:
        if consumer_task:
            consumer_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await consumer_task
        if consumer:
            await consumer.stop()


app = FastAPI(title="Storage Service", version="1.0.0", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.service_name}


@app.post("/locations")
async def create_location(payload: LocationCreate, db: AsyncSession = Depends(get_db)):
    location = Location(**payload.model_dump())
    db.add(location)
    await db.commit()
    return {"status": "created", "id": payload.id}


@app.post("/sensors")
async def create_sensor(payload: SensorCreate, db: AsyncSession = Depends(get_db)):
    location = await db.get(Location, payload.location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    sensor = Sensor(**payload.model_dump())
    db.add(sensor)
    await db.commit()
    return {"status": "created", "id": payload.id}


@app.get("/sensors", response_model=list[SensorRead])
async def list_sensors(db: AsyncSession = Depends(get_db)):
    rows = await db.execute(select(Sensor))
    return rows.scalars().all()


@app.get("/metrics")
async def metrics(db: AsyncSession = Depends(get_db)):
    metric_types = ["temperature", "humidity", "aqi", "noise"]
    response = {}
    for metric_type in metric_types:
        avg_stmt = select(func.avg(SensorData.value)).where(SensorData.type == metric_type, SensorData.is_valid.is_(True))
        latest_stmt = (
            select(SensorData.value, SensorData.recorded_at)
            .where(SensorData.type == metric_type)
            .order_by(SensorData.recorded_at.desc())
            .limit(1)
        )
        avg_result = await db.execute(avg_stmt)
        latest_result = await db.execute(latest_stmt)
        latest = latest_result.first()
        response[metric_type] = {
            "average": round(float(avg_result.scalar() or 0.0), 2),
            "latest": float(latest[0]) if latest else None,
            "latest_at": latest[1].isoformat() if latest else None,
        }
    return response


@app.get("/metrics/prometheus")
async def prometheus_metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
