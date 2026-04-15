import asyncio
from typing import Awaitable, Callable, TypeVar


T = TypeVar("T")


async def async_retry(
    operation: Callable[[], Awaitable[T]],
    retries: int = 3,
    base_delay_seconds: float = 0.25,
) -> T:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            return await operation()
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt == retries - 1:
                break
            await asyncio.sleep(base_delay_seconds * (2**attempt))
    assert last_error is not None
    raise last_error
