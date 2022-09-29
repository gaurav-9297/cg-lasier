from .base import AsyncCacheAdapterBase
from lasier.types import Timeout


class Adapter(AsyncCacheAdapterBase):
    async def flushdb(self) -> None:
        try:
            await self._pool.flushdb(async_op=True)
        except Exception as e:
            print(f"flushdb error:{e}")
            pass

    async def expire(self, key: str, timeout: Timeout = None) -> None:
        await self._pool.expire(key, timeout)
