import asyncio
from contextlib import suppress

from .. import background_tasks, core, json, optional_features
from ..logging import log
from .persistent_dict import PersistentDict

with suppress(ImportError):
    import redis as redis_sync
    import redis.asyncio as redis
    optional_features.register('redis')


class RedisPersistentDict(PersistentDict):

    def __init__(self, *,
                 url: str,
                 id: str,  # pylint: disable=redefined-builtin
                 key_prefix: str = 'nicegui:',
                 ttl: int | None = None
                 ) -> None:
        if not optional_features.has('redis'):
            raise ImportError('Redis is not installed. Please run "pip install nicegui[redis]".')
        self.url = url
        self._redis_client_params = {
            'health_check_interval': 10,
            'socket_connect_timeout': 5,
            'retry_on_timeout': True,
            **({'socket_keepalive': True} if not url.startswith('unix://') else {}),
        }
        self.redis_client = redis.from_url(self.url, **self._redis_client_params)
        self.pubsub = self.redis_client.pubsub()
        self.key = key_prefix + id
        self.ttl = ttl
        self._listener_task: asyncio.Task | None = None
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
        with redis_sync.from_url(self.url, **self._redis_client_params) as redis_client_sync:
            try:
                data = redis_client_sync.get(self.key)
                self.update(json.loads(data) if data else {})
                self._start_listening()
            except Exception:
                log.warning(f'Could not load data from Redis with key {self.key}')

    def _start_listening(self) -> None:
        async def listen():
            try:
                await self.pubsub.subscribe(self.key + 'changes')
                async for message in self.pubsub.listen():
                    t = message['type']
                    if t == 'message':
                        new_data = json.loads(message['data'])
                        if new_data != self:
                            self.update(new_data)
                    elif t in ('unsubscribe', 'punsubscribe') and message.get('data') == 0:
                        break
            except asyncio.CancelledError:
                pass  # Expected during close()
            except Exception:
                log.exception(f'Unexpected error in Redis listener for {self.key}')
            finally:
                if self.pubsub.subscribed:
                    await self.pubsub.unsubscribe()

        def create_listener_task() -> None:
            self._listener_task = background_tasks.create(listen(), name=f'redis-listen-{self.key}')

        if core.loop and core.loop.is_running():
            create_listener_task()
        else:
            core.app.on_startup(create_listener_task)

    def publish(self) -> None:
        """Publish the data to Redis and notify other instances."""
        async def backup() -> None:
            if not await self.redis_client.exists(self.key) and not self:
                return
            pipeline = self.redis_client.pipeline()
            data = json.dumps(self)
            pipeline.set(self.key, data, ex=self.ttl)
            pipeline.publish(self.key + 'changes', data)
            await pipeline.execute()
        if core.loop:
            background_tasks.create_lazy(backup(), name=f'redis-{self.key}')
        else:
            core.app.on_startup(backup())

    async def close(self) -> None:
        """Close Redis connection and subscription."""
        if self._listener_task and not self._listener_task.done():
            self._listener_task.cancel()
            with suppress(asyncio.CancelledError):
                await self._listener_task
        await self.pubsub.aclose()
        await self.redis_client.aclose()

    def clear(self) -> None:
        super().clear()
        if core.loop:
            background_tasks.create_lazy(self.redis_client.delete(self.key), name=f'redis-delete-{self.key}')
        else:
            core.app.on_startup(self.redis_client.delete(self.key))
