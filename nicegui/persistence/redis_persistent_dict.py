from .. import background_tasks, core, json, optional_features
from ..logging import log
from .persistent_dict import PersistentDict

try:
    import redis as redis_sync
    import redis.asyncio as redis
    optional_features.register('redis')
except ImportError:
    pass


class RedisPersistentDict(PersistentDict):

    def __init__(self, *, url: str, id: str, key_prefix: str = 'nicegui:') -> None:  # pylint: disable=redefined-builtin
        if not optional_features.has('redis'):
            raise ImportError('Redis is not installed. Please run "pip install nicegui[redis]".')
        self.url = url
        self.redis_client = redis.from_url(
            url,
            health_check_interval=10,
            socket_connect_timeout=5,
            retry_on_timeout=True,
            socket_keepalive=True,
        )
        self.pubsub = self.redis_client.pubsub()
        self.key = key_prefix + id
        super().__init__(data={}, on_change=self.publish)

    async def initialize(self) -> None:
        """Load initial data from Redis and start listening for changes."""
        try:
            data = await self.redis_client.get(self.key)
            self.update(json.loads(data) if data else {})
            self._start_listening()
        except Exception:
            log.warning(f'Could not load data from Redis with key {self.key}')

    def initialize_sync(self) -> None:
        """Load initial data from Redis and start listening for changes in a synchronous context."""
        with redis_sync.from_url(
            self.url,
            health_check_interval=10,
            socket_connect_timeout=5,
            retry_on_timeout=True,
            socket_keepalive=True,
        ) as redis_client_sync:
            try:
                data = redis_client_sync.get(self.key)
                self.update(json.loads(data) if data else {})
                self._start_listening()
            except Exception:
                log.warning(f'Could not load data from Redis with key {self.key}')

    def _start_listening(self) -> None:
        async def listen():
            await self.pubsub.subscribe(self.key + 'changes')
            async for message in self.pubsub.listen():
                if message['type'] == 'message':
                    new_data = json.loads(message['data'])
                    if new_data != self:
                        self.update(new_data)

        if core.loop and core.loop.is_running():
            background_tasks.create(listen(), name=f'redis-listen-{self.key}')
        else:
            core.app.on_startup(listen())

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
        if core.loop:
            background_tasks.create_lazy(self.redis_client.delete(self.key), name=f'redis-delete-{self.key}')
        else:
            core.app.on_startup(self.redis_client.delete(self.key))
