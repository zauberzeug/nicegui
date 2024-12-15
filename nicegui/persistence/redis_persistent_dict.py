from nicegui import background_tasks, core, json
from nicegui.logging import log

from .. import optional_features

try:
    import redis.asyncio as redis
    optional_features.register('redis')
except ImportError:
    pass


from .persistent_dict import PersistentDict


class RedisPersistentDict(PersistentDict):

    def __init__(self, redis_url: str, id: str, key_prefix: str = 'nicegui:') -> None:  # pylint: disable=redefined-builtin
        if not optional_features.has('redis'):
            raise ImportError('Redis is not installed. Please run "pip install nicegui[redis]".')
        self.redis_client = redis.from_url(redis_url)
        self.pubsub = self.redis_client.pubsub()
        self.key = key_prefix + id
        super().__init__({}, on_change=self.publish)

    async def initialize(self) -> None:
        """Load initial data from Redis and start listening for changes."""
        try:
            data = await self.redis_client.get(self.key)
            print(f'loading data: {data} for {self.key}')
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
            print(f'backup {self.key} with {json.dumps(self)}')
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
