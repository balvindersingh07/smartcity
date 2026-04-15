from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

from .config import Settings
from .retry import async_retry

settings = Settings()
STORAGE_BASE_URL = settings.storage_base_url
NOTIFICATION_BASE_URL = settings.notification_base_url

app = FastAPI(title="API Service", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api_requests_total = Counter("api_requests_total", "Total API requests", ["endpoint"])
api_downstream_failures_total = Counter("api_downstream_failures_total", "Failed downstream calls", ["endpoint"])
api_request_latency_seconds = Histogram("api_request_latency_seconds", "API endpoint latency", ["endpoint"])


@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.service_name}


async def fetch_or_raise(client: httpx.AsyncClient, url: str) -> Any:
    try:
        response = await async_retry(lambda: client.get(url, timeout=10.0), retries=3, base_delay_seconds=0.2)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Downstream service call failed: {exc}") from exc
    return response.json()


@app.get("/metrics")
async def get_metrics():
    api_requests_total.labels(endpoint="/metrics").inc()
    with api_request_latency_seconds.labels(endpoint="/metrics").time():
        async with httpx.AsyncClient() as client:
            try:
                return await fetch_or_raise(client, f"{STORAGE_BASE_URL}/metrics")
            except HTTPException:
                api_downstream_failures_total.labels(endpoint="/metrics").inc()
                raise


@app.get("/sensors")
async def get_sensors():
    api_requests_total.labels(endpoint="/sensors").inc()
    with api_request_latency_seconds.labels(endpoint="/sensors").time():
        async with httpx.AsyncClient() as client:
            try:
                return await fetch_or_raise(client, f"{STORAGE_BASE_URL}/sensors")
            except HTTPException:
                api_downstream_failures_total.labels(endpoint="/sensors").inc()
                raise


@app.get("/alerts")
async def get_alerts():
    api_requests_total.labels(endpoint="/alerts").inc()
    with api_request_latency_seconds.labels(endpoint="/alerts").time():
        async with httpx.AsyncClient() as client:
            try:
                return await fetch_or_raise(client, f"{NOTIFICATION_BASE_URL}/alerts")
            except HTTPException:
                api_downstream_failures_total.labels(endpoint="/alerts").inc()
                raise


@app.get("/metrics/prometheus")
async def prometheus_metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
