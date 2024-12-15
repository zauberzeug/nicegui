import redis.asyncio as redis

from nicegui import background_tasks, core, json, observables
from nicegui.logging import log


class RedisPersistentDict(observables.ObservableDict):

    def __init__(self, redis_url: str = 'redis://localhost:6379', key_prefix: str = 'nicegui:', encoding: str = 'utf-8') -> None:
        self.redis_client = redis.from_url(redis_url)
        self.pubsub = self.redis_client.pubsub()
        self.key_prefix = key_prefix
        self.encoding = encoding
        super().__init__({}, on_change=self.publish)

    async def initialize(self) -> None:
        """Load initial data from Redis and start listening for changes."""
        try:
            data = await self.redis_client.get(self.key_prefix + 'data')
            self.update(json.loads(data) if data else {})
        except Exception:
            log.warning(f'Could not load data from Redis with prefix {self.key_prefix}')
        await self.pubsub.subscribe(self.key_prefix + 'changes')
        async for message in self.pubsub.listen():
            if message['type'] == 'message':
                new_data = json.loads(message['data'])
                if new_data != self:
                    self.update(new_data)

    def publish(self) -> None:
        """Publish the data to Redis and notify other instances."""
        async def backup() -> None:
            pipeline = self.redis_client.pipeline()
            pipeline.set(self.key_prefix + 'data', json.dumps(self))
            pipeline.publish(self.key_prefix + 'changes', json.dumps(self))
            await pipeline.execute()
        if core.loop:
            background_tasks.create_lazy(backup(), name=f'redis-{self.key_prefix}')
        else:
            core.app.on_startup(backup())

    async def close(self) -> None:
        """Close Redis connection and subscription."""
        await self.pubsub.unsubscribe()
        await self.pubsub.close()
        await self.redis_client.close()
