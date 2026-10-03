import asyncio
import time
from typing import Literal

from litellm.integrations.custom_logger import CustomLogger
from litellm.proxy.proxy_server import DualCache, UserAPIKeyAuth

MIN_REQUEST_INTERVAL_SECONDS = 1.6


class NIMRequestPacer(CustomLogger):
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._last_request_at: float | None = None

    async def async_pre_call_hook(
        self,
        user_api_key_dict: UserAPIKeyAuth,
        cache: DualCache,
        data: dict,
        call_type: Literal[
            "completion",
            "text_completion",
            "embeddings",
            "image_generation",
            "moderation",
            "audio_transcription",
        ],
    ) -> dict:
        if data.get("model") == "kimi-k3":
            async with self._lock:
                now = time.monotonic()
                if self._last_request_at is not None:
                    delay = MIN_REQUEST_INTERVAL_SECONDS - (now - self._last_request_at)
                    if delay > 0:
                        print(f"Spacing NVIDIA NIM request by {delay:.2f}s")
                        await asyncio.sleep(delay)
                self._last_request_at = time.monotonic()

        return data


proxy_handler_instance = NIMRequestPacer()
