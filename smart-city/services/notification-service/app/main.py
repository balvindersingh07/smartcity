import asyncio
import contextlib
import json
from collections import deque
from contextlib import asynccontextmanager
from typing import Optional

from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

from .config import Settings
settings = Settings()
KAFKA_BOOTSTRAP = settings.kafka_bootstrap_servers
ALERTS_TOPIC = settings.kafka_alerts_topic
CONSUMER_GROUP = settings.consumer_group

consumer: Optional[AIOKafkaConsumer] = None
consumer_task: Optional[asyncio.Task] = None
alerts_buffer = deque(maxlen=200)
alerts_consumed_total = Counter("alerts_consumed_total", "Total alerts consumed")


async def consume_alerts():
    assert consumer is not None
    async for msg in consumer:
        alert = json.loads(msg.value.decode("utf-8"))
        alerts_buffer.appendleft(alert)
        alerts_consumed_total.inc()


@asynccontextmanager
async def lifespan(_: FastAPI):
    global consumer, consumer_task
    consumer = AIOKafkaConsumer(
        ALERTS_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id=CONSUMER_GROUP,
        auto_offset_reset="latest",
    )
    await consumer.start()
    consumer_task = asyncio.create_task(consume_alerts())
    try:
        yield
    finally:
        if consumer_task:
            consumer_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await consumer_task
        if consumer:
            await consumer.stop()


app = FastAPI(title="Notification Service", version="1.0.0", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.service_name}


@app.get("/alerts")
async def alerts():
    return {"count": len(alerts_buffer), "items": list(alerts_buffer)}


@app.get("/metrics/prometheus")
async def prometheus_metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
