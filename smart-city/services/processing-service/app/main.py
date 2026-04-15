import asyncio
import contextlib
import json
import logging
from contextlib import asynccontextmanager
from typing import Optional

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

from .config import Settings
from .pipeline import StreamState, process_event
from .retry import async_retry


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("processing-service")


settings = Settings()
consumer: Optional[AIOKafkaConsumer] = None
producer: Optional[AIOKafkaProducer] = None
consumer_task: Optional[asyncio.Task] = None
stream_state = StreamState(window_size=30)
processed_count = 0
processed_events_total = Counter("processed_events_total", "Total processed events")
invalid_events_total = Counter("invalid_events_total", "Total invalid events routed to DLQ")
alerts_generated_total = Counter("alerts_generated_total", "Total alerts generated")
processing_latency_seconds = Histogram("processing_latency_seconds", "Event processing latency")


async def consume_and_process():
    global processed_count
    assert consumer is not None and producer is not None

    async for msg in consumer:
        with processing_latency_seconds.time():
            event = json.loads(msg.value.decode("utf-8"))
            processed, alert = process_event(event, stream_state)
            processed_events_total.inc()

            if not processed.get("is_valid", False):
                invalid_events_total.inc()
                await async_retry(
                    lambda: producer.send_and_wait(
                        settings.kafka_dlq_topic,
                        json.dumps(
                            {
                                "reason": "validation_failed",
                                "event": event,
                            }
                        ).encode("utf-8"),
                        key=event["sensor_id"].encode("utf-8"),
                    ),
                    retries=4,
                    base_delay_seconds=0.15,
                )
                continue

            await async_retry(
                lambda: producer.send_and_wait(
                    settings.kafka_processed_topic,
                    json.dumps(processed).encode("utf-8"),
                    key=event["sensor_id"].encode("utf-8"),
                ),
                retries=4,
                base_delay_seconds=0.15,
            )
            processed_count += 1

            if alert:
                alerts_generated_total.inc()
                await async_retry(
                    lambda: producer.send_and_wait(
                        settings.kafka_alerts_topic,
                        json.dumps(alert).encode("utf-8"),
                        key=event["sensor_id"].encode("utf-8"),
                    ),
                    retries=4,
                    base_delay_seconds=0.15,
                )
                logger.warning("Alert generated for sensor_id=%s", event["sensor_id"])


@asynccontextmanager
async def lifespan(_: FastAPI):
    global consumer, producer, consumer_task
    consumer = AIOKafkaConsumer(
        settings.kafka_raw_topic,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id=settings.consumer_group,
        auto_offset_reset="latest",
        enable_auto_commit=True,
    )
    producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_bootstrap_servers)
    await consumer.start()
    await producer.start()
    consumer_task = asyncio.create_task(consume_and_process())
    logger.info("Processing consumer started")
    try:
        yield
    finally:
        if consumer_task:
            consumer_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await consumer_task
        if consumer:
            await consumer.stop()
        if producer:
            await producer.stop()
        logger.info("Processing consumer stopped")


app = FastAPI(title="Processing Service", version="1.0.0", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.service_name}


@app.get("/aggregates")
async def aggregates():
    response = {}
    for metric_type, values in stream_state.buffers.items():
        if values:
            response[metric_type] = round(sum(values) / len(values), 2)
    return {"processed_events": processed_count, "rolling_averages": response}


@app.get("/metrics/prometheus")
async def prometheus_metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
