from .. import background_tasks, core, json, optional_features
from ..logging import log
from .persistent_dict import PersistentDict
from typing import Optional

try:
    import redis as redis_sync
    import redis.asyncio as redis
    optional_features.register('redis')
except ImportError:
    pass


class RedisPersistentDict(PersistentDict):

    def __init__(self, *, url: str, id: str, key_prefix: str = 'nicegui:',
                 skip_redis_publish:  Optional[bool] = False) -> None:  # pylint: disable=redefined-builtin
                # TODO: is Optional required for skip_redis_publish? I think this is only used in one location.
        if not optional_features.has('redis'):
            raise ImportError('Redis is not installed. Please run "pip install nicegui[redis]".')
        self.url = url
        self.key = key_prefix + id
        self.skip_redis_publish = skip_redis_publish
        self.redis_client = None
        self.pubsub = None
        super().__init__(data={}, on_change=self.publish)

    async def _init_redis_client(self):
        if not self.redis_client:
            self.redis_client = redis.from_url(
                self.url,
                health_check_interval=10,
                socket_connect_timeout=5,
                retry_on_timeout=True,
                socket_keepalive=True,
            )

    async def _init_pubsub(self):
        if not self.redis_client:
            await self._init_redis_client()
        if not self.pubsub:
            self.pubsub = self.redis_client.pubsub()

    async def initialize(self) -> None:
        '''Load initial data from Redis and start listening for changes.'''
        if self.skip_redis_publish:
            print(f'⚠️ SKIPPING INIT ON {self.key} because URI PREFIX EXEMPTED') # TODO: remove before pull request commit
            return
        async with redis.from_url(
            self.url,
            health_check_interval=10,
            socket_connect_timeout=5,
            retry_on_timeout=True,
            socket_keepalive=True,
        ) as redis_client_sync:
            try:
                data = await redis_client_sync.get(self.key)
                self.update(json.loads(data) if data else {})
                self._start_listening()
            except Exception:
                log.warning(f'Could not load data from Redis with key {self.key}')

    def initialize_sync(self) -> None:
        '''Load initial data from Redis and start listening for changes in a synchronous context.'''
        print(f'.... initialize_sync() {self.key}')  # TODO: remove before pull request commit
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
                log.warning(f'Could not load data from Redis with key {self.key} - {self}')

    def _start_listening(self) -> None:
        async def listen():
            print(f'✅ SUBSCRIBING TO {self.key} - {self}')  # TODO: remove before pull request commit
            if not self.pubsub:
                await self._init_pubsub()
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
        '''Publish the data to Redis and notify other instances.'''
        async def backup() -> None:
            async with redis.from_url(
                    self.url,
                    health_check_interval=10,
                    socket_connect_timeout=5,
                    retry_on_timeout=True,
                    socket_keepalive=True,
            ) as redis_client:
                pipeline = redis_client.pipeline()
                pipeline.set(self.key, json.dumps(self))
                pipeline.publish(self.key + 'changes', json.dumps(self))
                await pipeline.execute()
        if self.skip_redis_publish:
            print(f'⚠️ SKIPPING PUBLISH ON {self.key} because URI PREFIX EXEMPTED') # TODO: remove before pull request commit
            return
        if core.loop:
            background_tasks.create_lazy(backup(), name=f'redis-{self.key}')
        else:
            core.app.on_startup(backup())

    async def close(self) -> None:
        '''Close Redis connection and subscription.'''
        if self.skip_redis_publish:
            print(f'⚠️ SKIPPING CLOSE ON {self.key} because URI PREFIX EXEMPTED') # TODO: remove before pull request commit
            return
        if self.pubsub:
            await self.pubsub.unsubscribe()
            await self.pubsub.close()
        if self.redis_client:
            await self.redis_client.close()

    def clear(self) -> None:
        super().clear()
        if self.skip_redis_publish:
            print(f'⚠️ SKIPPING REDIS CLEAR ON {self.key} because URI PREFIX EXEMPTED') # TODO: remove before pull request commit
            return
        else: # TODO: remove before pull request commit
            print(f'✅ CLEARING REDIS KEY {self.key} - {self}') # TODO: remove before pull request commit
        if core.loop:
            if self.redis_client:
                background_tasks.create_lazy(self.redis_client.delete(self.key), name=f'redis-delete-{self.key}')
        else:
            if self.redis_client:
                core.app.on_startup(self.redis_client.delete(self.key))
