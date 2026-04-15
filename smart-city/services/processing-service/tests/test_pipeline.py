from app.pipeline import StreamState, process_event, validate_event


def test_validate_event_happy_path():
    event = {"sensor_id": "s-1", "type": "temperature", "value": 30, "timestamp": "2026-01-01T00:00:00Z"}
    assert validate_event(event) is True


def test_validate_event_invalid_range():
    event = {"sensor_id": "s-1", "type": "temperature", "value": 300, "timestamp": "2026-01-01T00:00:00Z"}
    assert validate_event(event) is False


def test_process_event_returns_rolling_average():
    state = StreamState(window_size=5)
    event = {"sensor_id": "s-1", "type": "humidity", "value": 50, "timestamp": "2026-01-01T00:00:00Z"}
    processed, alert = process_event(event, state)
    assert processed["rolling_avg"] == 50.0
    assert alert is None
