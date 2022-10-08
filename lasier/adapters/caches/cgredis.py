from .base import AsyncCacheAdapterBase
from lasier.types import Timeout


class Adapter(AsyncCacheAdapterBase):
    async def add(self, key: str, value: int, timeout: Timeout = None) -> None:
        try:
            await super().set(key, value, timeout, exist="SET_IF_NOT_EXIST")
        except ValueError:
            return
