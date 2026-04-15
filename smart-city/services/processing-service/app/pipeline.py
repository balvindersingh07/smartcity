from collections import defaultdict, deque
from datetime import datetime
from typing import Any, Dict, Tuple


VALID_RANGES = {
    "temperature": (-40.0, 85.0),
    "humidity": (0.0, 100.0),
    "aqi": (0.0, 500.0),
    "noise": (0.0, 180.0),
}

ANOMALY_THRESHOLDS = {
    "temperature": 45.0,
    "humidity": 90.0,
    "aqi": 150.0,
    "noise": 90.0,
}


class StreamState:
    def __init__(self, window_size: int = 50):
        self.window_size = window_size
        self.buffers: Dict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))

    def update(self, metric_type: str, value: float) -> float:
        self.buffers[metric_type].append(value)
        values = self.buffers[metric_type]
        return round(sum(values) / len(values), 2)


def validate_event(event: Dict[str, Any]) -> bool:
    metric_type = event.get("type")
    value = event.get("value")
    if metric_type not in VALID_RANGES:
        return False
    low, high = VALID_RANGES[metric_type]
    return isinstance(value, (int, float)) and low <= float(value) <= high


def detect_anomaly(event: Dict[str, Any]) -> bool:
    threshold = ANOMALY_THRESHOLDS.get(event.get("type"))
    if threshold is None:
        return False
    return float(event.get("value", 0)) >= threshold


def process_event(event: Dict[str, Any], state: StreamState) -> Tuple[Dict[str, Any], Dict[str, Any] | None]:
    is_valid = validate_event(event)
    rolling_avg = state.update(event["type"], float(event["value"])) if is_valid else None

    processed = {
        **event,
        "processed_at": datetime.utcnow().isoformat(),
        "is_valid": is_valid,
        "rolling_avg": rolling_avg,
    }

    alert = None
    if is_valid and detect_anomaly(event):
        alert = {
            "sensor_id": event["sensor_id"],
            "type": event["type"],
            "value": event["value"],
            "threshold": ANOMALY_THRESHOLDS[event["type"]],
            "timestamp": event["timestamp"],
            "severity": "critical",
            "message": f"{event['type']} threshold exceeded",
        }

    return processed, alert
