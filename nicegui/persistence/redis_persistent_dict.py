from .. import background_tasks, core, json, optional_features
from ..logging import log
from .persistent_dict import PersistentDict

try:
    import redis.asyncio as redis
    optional_features.register('redis')
except ImportError:
    pass


class RedisPersistentDict(PersistentDict):

    def __init__(self, *, url: str, id: str, key_prefix: str = 'nicegui:') -> None:  # pylint: disable=redefined-builtin
        if not optional_features.has('redis'):
            raise ImportError('Redis is not installed. Please run "pip install nicegui[redis]".')
        self.redis_client = redis.from_url(url)
        self.pubsub = self.redis_client.pubsub()
        self.key = key_prefix + id
        super().__init__(data={}, on_change=self.publish)

    async def initialize(self) -> None:
        """Load initial data from Redis and start listening for changes."""
        try:
            data = await self.redis_client.get(self.key)
            self.update(json.loads(data) if data else {})
        except Exception:
            log.warning(f'Could not load data from Redis with key {self.key}')
        await self.pubsub.subscribe(self.key + 'changes')

        async def listen():
            async for message in self.pubsub.listen():
                if message['type'] == 'message':
                    new_data = json.loads(message['data'])
                    if new_data != self:
                        self.update(new_data)

        background_tasks.create(listen(), name=f'redis-listen-{self.key}')

    def publish(self) -> None:
        """Publish the data to Redis and notify other instances."""
        async def backup() -> None:
            pipeline = self.redis_client.pipeline()
            pipeline.set(self.key, json.dumps(self))
            pipeline.publish(self.key + 'changes', json.dumps(self))
            await pipeline.execute()
        if core.loop:
            background_tasks.create_lazy(backup(), name=f'redis-{self.key}')
        else:
            core.app.on_startup(backup())

    async def close(self) -> None:
        """Close Redis connection and subscription."""
        await self.pubsub.unsubscribe()
        await self.pubsub.close()
        await self.redis_client.close()

    def clear(self) -> None:
        super().clear()
        self.redis_client.delete(self.key)
