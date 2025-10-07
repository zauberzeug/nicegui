import pickle
import uuid
from typing import Any, Callable, Union

from .logging import log

try:
    import zenoh  # from eclipse-zenoh package
    ZENOH_AVAILABLE = True
except ImportError:
    ZENOH_AVAILABLE = False
    zenoh = None  # type: ignore


class DistributedSession:
    """Manages distributed event communication via Zenoh pub/sub."""

    _instance: Union['DistributedSession', None] = None

    def __init__(self, config: Union[dict, bool]) -> None:
        """Initialize a Zenoh session for distributed events.

        :param config: Zenoh configuration (True for defaults, dict for custom config)
        """
        if not ZENOH_AVAILABLE:
            raise ImportError('zenoh is required for distributed events. '
                              'Install with: pip install "nicegui[distributed]"')

        zenoh_config = zenoh.Config() if config is True else zenoh.Config.from_obj(config)
        self.session = zenoh.open(zenoh_config)
        self.instance_id = str(uuid.uuid4())
        self.publishers: dict[str, Any] = {}
        self.subscribers: dict[str, Any] = {}
        log.info(f'Distributed events enabled via Zenoh (instance: {self.instance_id[:8]}...)')

    @classmethod
    def get(cls) -> Union['DistributedSession', None]:
        """Get the active distributed session, if any."""
        return cls._instance

    @classmethod
    def initialize(cls, config: Union[dict, bool]) -> None:
        """Initialize the global distributed session.

        :param config: Zenoh configuration (True for defaults, dict for custom config)
        """
        if cls._instance is None:
            cls._instance = cls(config)

    def publish(self, topic: str, data: Any) -> None:
        """Publish data to a topic.

        :param topic: topic name
        :param data: data to publish (will be pickled)
        """
        try:
            payload = pickle.dumps({
                'instance_id': self.instance_id,
                'data': data,
            })
            if topic not in self.publishers:
                self.publishers[topic] = self.session.declare_publisher(f'nicegui/events/{topic}')
            self.publishers[topic].put(payload)
        except Exception as e:
            log.exception(f'Failed to publish event to topic {topic}: {e}')
            raise

    def subscribe(self, topic: str, callback: Callable[[Any], None]) -> None:
        """Subscribe to a topic.

        :param topic: topic name
        :param callback: function to call when data arrives
        """
        def handler(sample: Any) -> None:
            try:
                payload = pickle.loads(bytes(sample.payload))
                # NOTE: Ignore events from our own instance (deduplication)
                if payload['instance_id'] == self.instance_id:
                    return
                callback(payload['data'])
            except Exception as e:
                log.exception(f'Failed to deserialize event from topic {topic}: {e}')
                raise

        if topic not in self.subscribers:
            self.subscribers[topic] = self.session.declare_subscriber(
                f'nicegui/events/{topic}',
                handler
            )

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
