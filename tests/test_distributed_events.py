import asyncio
import json

import pytest

from nicegui import Event, ui
from nicegui.distributed import ZENOH_AVAILABLE, DistributedSession, _peer_to_endpoint
from nicegui.distributed_event import DistributedEvent
from nicegui.testing import User

pytestmark = pytest.mark.skipif(not ZENOH_AVAILABLE, reason='eclipse-zenoh not installed')

LOOPBACK_PORT = 17447  # uncommon port to reduce collision risk in CI
LOOPBACK_ENDPOINT = f'tcp/127.0.0.1:{LOOPBACK_PORT}'


@pytest.fixture
def fresh_session():
    """Reset the DistributedSession singleton around each test."""
    DistributedSession._instance = None
    yield
    session = DistributedSession.get()
    if session is not None:
        session.shutdown()
    DistributedSession._instance = None


def test_regular_event_stays_local():
    event = Event[str]()
    assert not hasattr(event, '_zenoh_setup_done')
    assert not hasattr(event, 'topic')


def test_distributed_event_topic_drops_absolute_path():
    """The topic must be portable across hosts: no directory separators allowed."""
    event = DistributedEvent[str]()
    assert event.topic.startswith('event_')
    assert ':' in event.topic
    assert '/' not in event.topic
    assert '\\' not in event.topic


def test_distributed_event_topics_differ_by_line():
    event1 = DistributedEvent[str]()
    event2 = DistributedEvent[int]()
    assert event1.topic != event2.topic


def test_peer_to_endpoint_default_port():
    assert _peer_to_endpoint('host.example.com') == 'tcp/host.example.com:7447'
    assert _peer_to_endpoint('192.168.1.10') == 'tcp/192.168.1.10:7447'


def test_peer_to_endpoint_explicit_port():
    assert _peer_to_endpoint('host.example.com:9999') == 'tcp/host.example.com:9999'


def test_session_rejects_without_storage_secret():
    """Without a secret, unrelated deployments would silently cross-talk on the same network."""
    with pytest.raises(ValueError, match='storage_secret'):
        DistributedSession(True, storage_secret=None)
    with pytest.raises(ValueError, match='storage_secret'):
        DistributedSession(True, storage_secret='')


def test_namespace_is_deterministic_and_isolating():
    ns_a = DistributedSession._derive_namespace('alpha')
    ns_b = DistributedSession._derive_namespace('beta')
    assert ns_a != ns_b
    assert DistributedSession._derive_namespace('alpha') == ns_a
    assert len(ns_a) == 16  # 16 hex chars from HMAC-SHA256 truncated


def test_wire_topic_includes_namespace(fresh_session):
    DistributedSession.initialize(True, storage_secret='alpha')
    session = DistributedSession.get()
    assert session is not None
    expected_ns = DistributedSession._derive_namespace('alpha')
    assert session.wire_topic('foo') == f'nicegui/events/{expected_ns}/foo'


async def test_emit_registers_publisher_on_wire_topic(user: User, fresh_session):
    """Emitting a DistributedEvent must declare a publisher on the namespaced wire topic."""
    DistributedSession.initialize(True, storage_secret='alpha')

    @ui.page('/')
    def page():
        event = DistributedEvent[str]()
        ui.button('emit', on_click=lambda: event.emit('hello'))

    await user.open('/')
    user.find('emit').click()

    session = DistributedSession.get()
    assert session is not None
    expected_ns = DistributedSession._derive_namespace('alpha')
    wire_topics = list(session.publishers)
    assert any(wire.startswith(f'nicegui/events/{expected_ns}/') for wire in wire_topics)


async def test_remote_event_invokes_local_callback(user: User, fresh_session):
    """A payload arriving from a sibling Zenoh peer on the namespaced wire topic must trigger callbacks."""
    import zenoh  # local import: only reachable when ZENOH_AVAILABLE
    DistributedSession.initialize({'listen': {'endpoints': [LOOPBACK_ENDPOINT]}}, storage_secret='alpha')
    received: list[str] = []

    @ui.page('/')
    def page():
        event = DistributedEvent[str]()
        event.subscribe(received.append)

    await user.open('/')

    session = DistributedSession.get()
    assert session is not None
    wire_topic = next(iter(session.subscribers))

    sibling_config = zenoh.Config.from_json5(json.dumps({'connect': {'endpoints': [LOOPBACK_ENDPOINT]}}))
    sibling = zenoh.open(sibling_config)
    try:
        sibling_pub = sibling.declare_publisher(wire_topic)
        sibling_pub.put(json.dumps({
            'instance_id': 'sibling',
            'data': {'args': ('hello',), 'kwargs': {}},
        }).encode())
        for _ in range(50):
            if received:
                break
            await asyncio.sleep(0.1)
    finally:
        sibling.close()

    assert received == ['hello']
