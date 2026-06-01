import hashlib
import hmac
import json
import uuid
from collections.abc import Callable
from typing import Any

from . import core
from .logging import log

try:
    import zenoh
    from zenoh import Sample
    ZENOH_AVAILABLE = True
except ImportError:
    ZENOH_AVAILABLE = False
    zenoh = None  # type: ignore
    Sample = Any  # type: ignore

DEFAULT_ZENOH_PORT = 7447
TOPIC_NAMESPACE_INFO = b'nicegui-distributed-v1'


def _peer_to_endpoint(peer: str) -> str:
    """Turn ``host`` or ``host:port`` into a Zenoh ``tcp/host:port`` endpoint."""
    return f'tcp/{peer}' if ':' in peer else f'tcp/{peer}:{DEFAULT_ZENOH_PORT}'


def _normalize_config(config: bool | list[str] | dict) -> Any:
    """Build a ``zenoh.Config`` from the user-friendly shortcuts accepted by ``ui.run``."""
    if config is True:
        return zenoh.Config()
    if isinstance(config, list):
        # NOTE: shortcut for the 99% case - "connect to these peers" without raw Zenoh JSON5
        peers_json = json.dumps([_peer_to_endpoint(p) for p in config])
        zenoh_config = zenoh.Config()
        zenoh_config.insert_json5('mode', '"peer"')
        zenoh_config.insert_json5('connect/endpoints', peers_json)
        return zenoh_config
    # NOTE: zenoh 1.x dropped Config.from_obj; from_json5 accepts a JSON string for the same effect.
    return zenoh.Config.from_json5(json.dumps(config))


class DistributedSession:
    """Manages distributed event communication via Zenoh pub/sub.

    This is an internal class used by the Event system to handle distributed messaging.
    Publishers and subscribers are kept alive for the lifetime of the session.
    Event instances are expected to be long-lived (typically module-level),
    so no automatic cleanup of unused topics is performed.
    """

    _instance: 'DistributedSession | None' = None

    def __init__(self, config: bool | list[str] | dict, storage_secret: str | None = None) -> None:
        """Initialize a Zenoh session for distributed events.

        :param config: True for defaults, list of "host" / "host:port" peers, or a raw Zenoh config dict
        :param storage_secret: NiceGUI's storage_secret; used to derive a topic namespace so that
                               instances sharing the same secret sync, and instances with different
                               secrets stay isolated even when the Zenoh transport reaches them
        """
        if not ZENOH_AVAILABLE:
            raise ImportError('zenoh is required for distributed events. '
                              'Install with: pip install "nicegui[distributed]"')
        if not storage_secret:
            raise ValueError(
                'distributed events require ui.run(storage_secret=...). '
                'Without a secret, unrelated deployments would silently cross-talk on '
                'the same network. Pass the same secret on every node you want to sync.'
            )

        self.session = zenoh.open(_normalize_config(config))
        self.instance_id = str(uuid.uuid4())
        self.namespace = self._derive_namespace(storage_secret)
        self.publishers: dict[str, Any] = {}
        self.subscribers: dict[str, Any] = {}
        log.info(f'Distributed events enabled via Zenoh '
                 f'(instance: {self.instance_id[:8]}..., namespace: {self.namespace})')

    @staticmethod
    def _derive_namespace(storage_secret: str) -> str:
        """Topic namespace derived from storage_secret via HMAC-SHA256.

        HMAC means the namespace on the wire never reveals the secret and gives no meaningful
        brute-force surface beyond what the secret already provides for cookie signing.
        """
        return hmac.new(storage_secret.encode(), TOPIC_NAMESPACE_INFO, hashlib.sha256).hexdigest()[:16]

    def wire_topic(self, logical_topic: str) -> str:
        """Map a logical (per-event) topic to the namespaced topic actually used on Zenoh."""
        return f'nicegui/events/{self.namespace}/{logical_topic}'

    @classmethod
    def get(cls) -> 'DistributedSession | None':
        """Get the active distributed session, if any."""
        return cls._instance

    @classmethod
    def initialize(cls, config: bool | list[str] | dict, storage_secret: str | None = None) -> None:
        """Initialize the global distributed session.

        :param config: True for defaults, list of "host" / "host:port" peers, or a raw Zenoh config dict
        :param storage_secret: NiceGUI's storage_secret, used to derive the topic namespace
        """
        if cls._instance is None:
            cls._instance = cls(config, storage_secret=storage_secret)
            cls._setup_existing_events()
            # Release the Zenoh session, publishers and subscribers when the app shuts down.
            core.app.on_shutdown(cls._instance.shutdown)

    @classmethod
    def _setup_existing_events(cls) -> None:
        """Set up distributed mode for all existing DistributedEvent instances."""
        from .distributed_event import DistributedEvent  # pylint: disable=import-outside-toplevel,cyclic-import
        for event in DistributedEvent.instances:
            if isinstance(event, DistributedEvent):
                event._setup_distributed()  # pylint: disable=protected-access

    def publish(self, topic: str, data: Any) -> None:
        """Publish data to a topic.

        :param topic: logical topic name (will be namespaced)
        :param data: data to publish (must be JSON-serializable)
        """
        wire = self.wire_topic(topic)
        try:
            payload = json.dumps({
                'instance_id': self.instance_id,
                'data': data,
            }).encode('utf-8')
            if wire not in self.publishers:
                self.publishers[wire] = self.session.declare_publisher(wire)
            self.publishers[wire].put(payload)
        except (TypeError, ValueError) as e:
            log.error(f'Failed to serialize event data for topic {topic}: {e}. '
                      'Event data must be JSON-serializable (str, int, float, bool, list, dict, None).')
            raise
        except Exception as e:
            log.exception(f'Failed to publish event to topic {topic}: {e}')
            raise

    def subscribe(self, topic: str, callback: Callable[[Any], None]) -> None:
        """Subscribe to a topic.

        :param topic: logical topic name (will be namespaced)
        :param callback: function to call when data arrives
        """
        wire = self.wire_topic(topic)

        def handler(sample: Sample) -> None:
            try:
                payload = json.loads(bytes(sample.payload).decode('utf-8'))
                # NOTE: Ignore events from our own instance (deduplication)
                if payload['instance_id'] == self.instance_id:
                    return
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                log.error(f'Failed to deserialize event from topic {topic}: {e}')
                return
            except Exception as e:  # pylint: disable=broad-except
                log.exception(f'Failed to handle event from topic {topic}: {e}')
                return
            # NOTE: Zenoh invokes this callback on a Rust-managed worker thread; downstream
            # NiceGUI machinery (slot weakrefs, asyncio.create_task) must run on the loop thread.
            data = payload['data']
            if core.loop is not None:
                core.loop.call_soon_threadsafe(callback, data)
            else:
                # No loop yet (e.g. during early startup or in stand-alone scripts) - run inline.
                callback(data)

        if wire not in self.subscribers:
            self.subscribers[wire] = self.session.declare_subscriber(wire, handler)

    def shutdown(self) -> None:
        """Clean up the Zenoh session."""
        try:
            for pub in self.publishers.values():
                pub.undeclare()
            for sub in self.subscribers.values():
                sub.undeclare()
            self.session.close()
            log.info('Distributed session closed')
        except Exception:
            log.exception('Error during distributed session shutdown')
