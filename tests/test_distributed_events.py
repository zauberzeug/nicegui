import asyncio
import gc
import json
import os
import subprocess
import sys
import threading
import time
import weakref
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import httpx
import pytest

from nicegui import Event, core, ui
from nicegui.distributed import ZENOH_AVAILABLE, DistributedSession, _normalize_config, _peer_to_endpoint
from nicegui.distributed_event import DistributedEvent
from nicegui.testing import User

pytestmark = pytest.mark.skipif(not ZENOH_AVAILABLE, reason='the "distributed" extra is not installed')

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


def shared_event() -> DistributedEvent[str]:
    """Create the event at a fixed source location so that every instance derives the same topic."""
    return DistributedEvent[str]()


@contextmanager
def wire_observer(observed: list[str]) -> Iterator[Any]:
    """Watch the network like any other Zenoh node and record the topics NiceGUI publishes on."""
    import zenoh  # local import: only reachable when ZENOH_AVAILABLE
    sibling = zenoh.open(zenoh.Config.from_json5(json.dumps({'connect': {'endpoints': [LOOPBACK_ENDPOINT]}})))
    try:
        sibling.declare_subscriber('nicegui/events/**', lambda sample: observed.append(str(sample.key_expr)))
        yield sibling
    finally:
        sibling.close()


@contextmanager
def remote_instance(storage_secret: str) -> Iterator[None]:
    """Act as a second NiceGUI instance on the loopback network, emitting through its own session."""
    local = DistributedSession.get()
    remote = DistributedSession({'connect': {'endpoints': [LOOPBACK_ENDPOINT]}}, storage_secret=storage_secret)
    DistributedSession._instance = remote
    try:
        yield
    finally:
        DistributedSession._instance = local
        remote.shutdown()


async def wait_for(condition: Callable[[], bool], *, retry: Callable[[], Any] | None = None) -> None:
    """Wait for something to arrive over the network (same retry scheme as ``User.should_see``).

    The ``retry`` action is repeated because a freshly declared subscription
    only reaches the other node after a moment, dropping whatever is sent before.
    """
    for _ in range(50):
        if condition():
            return
        if retry is not None:
            retry()
        await asyncio.sleep(0.1)


def test_peer_to_endpoint_default_port():
    assert _peer_to_endpoint('host.example.com') == 'tcp/host.example.com:7447'
    assert _peer_to_endpoint('192.168.1.10') == 'tcp/192.168.1.10:7447'


def test_peer_to_endpoint_explicit_port():
    assert _peer_to_endpoint('host.example.com:9999') == 'tcp/host.example.com:9999'


async def test_the_peer_list_alone_connects_two_instances(monkeypatch):
    """Nothing may be left to scouting: where an explicit peer list is needed, multicast does not travel.

    The second session cannot bind the port the first one took, which is what two instances on one host do.
    """
    import zenoh  # local import: only reachable when ZENOH_AVAILABLE
    monkeypatch.setattr('nicegui.distributed.DEFAULT_ZENOH_PORT', LOOPBACK_PORT + 3)
    sessions = []
    for _ in range(2):
        config = _normalize_config(['127.0.0.1'])
        config.insert_json5('scouting/multicast/enabled', 'false')  # as on a network that does not route multicast
        config.insert_json5('scouting/gossip/enabled', 'false')
        sessions.append(zenoh.open(config))
    received: list[bytes] = []
    try:
        sessions[1].declare_subscriber('nicegui/test', lambda sample: received.append(bytes(sample.payload)))
        await wait_for(lambda: bool(received), retry=lambda: sessions[0].put('nicegui/test', b'hello'))
    finally:
        for session in sessions:
            session.close()
    assert received, 'the peers in the list never reached each other'


def test_session_rejects_without_storage_secret():
    """Without a secret, unrelated deployments would silently cross-talk on the same network."""
    with pytest.raises(ValueError, match='storage_secret'):
        DistributedSession(True, storage_secret=None)
    with pytest.raises(ValueError, match='storage_secret'):
        DistributedSession(True, storage_secret='')


def test_missing_dependency_is_reported_by_name():
    """The "distributed" extra is more than zenoh, so a missing cryptography must not be blamed on zenoh."""
    script = '''
import sys
sys.modules['cryptography'] = None  # as if only the encryption half of the extra were missing
from nicegui.distributed import DistributedSession
try:
    DistributedSession.initialize(True, storage_secret='alpha')
except ImportError as e:
    print(e)
'''
    message = subprocess.run([sys.executable, '-c', script], capture_output=True, text=True, check=True).stdout
    assert 'cryptography' in message
    assert 'zenoh' not in message
    assert 'nicegui[distributed]' in message


def test_a_process_that_does_not_serve_opens_no_session():
    """`run.cpu_bound` workers re-import __main__ and thereby re-run ui.run(), but they serve nothing."""
    script = '''
import multiprocessing
multiprocessing.current_process().name = 'SpawnProcess-1'  # as in a run.cpu_bound worker
from nicegui import ui
from nicegui.distributed import DistributedSession
ui.run(distributed=True, storage_secret='alpha', reload=False, show=False)
print(DistributedSession.get())
'''
    output = subprocess.run([sys.executable, '-c', script], capture_output=True, text=True, check=True).stdout
    assert output.strip() == 'None'


def test_the_serving_process_opens_the_session(tmp_path: Path):
    """With auto-reload the reloader's child serves the app, so that is the process which needs the session.

    Asking the app itself is what makes this observation unambiguous:
    only the process that answers the request is serving.
    """
    app_file = tmp_path / 'app.py'
    app_file.write_text(f'''
from nicegui import app, ui
from nicegui.distributed import DistributedSession

@app.get('/has-session')
def has_session():
    return DistributedSession.get() is not None

ui.run(distributed={{'listen': {{'endpoints': ['tcp/127.0.0.1:{LOOPBACK_PORT + 1}']}}}},
       storage_secret='alpha', reload=True, show=False, port={LOOPBACK_PORT + 2})
''')
    environment = {key: value for key, value in os.environ.items() if key != 'PYTEST_CURRENT_TEST'}
    with subprocess.Popen([sys.executable, str(app_file)], env=environment) as process:
        try:
            for _ in range(300):
                try:
                    assert httpx.get(f'http://127.0.0.1:{LOOPBACK_PORT + 2}/has-session', timeout=1).json() is True
                    break
                except httpx.TransportError:
                    time.sleep(0.1)
            else:
                pytest.fail('the app never came up')
        finally:
            process.terminate()  # the reloader shuts its child down; kill only if it will not go
            try:
                process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                process.kill()


def test_emit_raises_before_local_fire_on_non_json_payload(fresh_session):
    """A non-JSON-serializable arg must raise BEFORE any local callback fires."""
    DistributedSession.initialize(True, storage_secret='alpha')
    fired: list = []
    event = DistributedEvent[object]()
    event.subscribe(fired.append)
    with pytest.raises(TypeError, match='JSON'):
        event.emit({'a', 'set'})
    assert fired == []


async def test_each_event_gets_a_portable_topic(user: User, fresh_session):
    """Every event travels on its own topic, named after module and line so it is portable across hosts."""
    DistributedSession.initialize({'listen': {'endpoints': [LOOPBACK_ENDPOINT]}}, storage_secret='alpha')
    observed: list[str] = []

    @ui.page('/')
    def page():
        first = DistributedEvent[str]()
        second = DistributedEvent[str]()
        ui.button('first', on_click=lambda: first.emit('hello'))
        ui.button('second', on_click=lambda: second.emit('hello'))

    await user.open('/')
    with wire_observer(observed):
        await wait_for(lambda: len(set(observed)) == 1, retry=user.find('first').click)
        await wait_for(lambda: len(set(observed)) == 2, retry=user.find('second').click)
    assert len(set(observed)) == 2
    for key in set(observed):
        assert key.startswith('nicegui/events/')
        assert key.split('/')[-1].startswith(f'event_{__name__}:')


async def test_plain_events_stay_local(user: User, fresh_session):
    """A plain Event must never reach the network, even while distributed mode is active."""
    DistributedSession.initialize({'listen': {'endpoints': [LOOPBACK_ENDPOINT]}}, storage_secret='alpha')
    observed: list[str] = []

    @ui.page('/')
    def page():
        plain = Event[str]()
        distributed = DistributedEvent[str]()
        ui.button('plain', on_click=lambda: plain.emit('hello'))
        ui.button('distributed', on_click=lambda: distributed.emit('hello'))

    await user.open('/')
    with wire_observer(observed):
        await wait_for(lambda: bool(observed), retry=user.find('distributed').click)
        observed.clear()
        user.find('plain').click()
        await asyncio.sleep(0.5)
    assert observed == []


async def test_event_from_another_instance_arrives_on_the_loop_thread(user: User, fresh_session):
    """Remote payloads trigger the callback ON the asyncio loop thread, not the Zenoh worker thread."""
    DistributedSession.initialize({'listen': {'endpoints': [LOOPBACK_ENDPOINT]}}, storage_secret='alpha')
    received: list[tuple[str, threading.Thread]] = []

    @ui.page('/')
    def page():
        shared_event().subscribe(lambda value: received.append((value, threading.current_thread())))

    await user.open('/')
    with remote_instance('alpha'):
        shared_event().emit('hello')
        await wait_for(lambda: bool(received))
    assert [value for value, _ in received] == ['hello']
    assert received[0][1] is threading.main_thread()


async def test_all_events_sharing_a_topic_receive_remote_events(user: User, fresh_session):
    """A topic can carry more than one event, e.g. one per client, and a remote event must reach all of them."""
    DistributedSession.initialize({'listen': {'endpoints': [LOOPBACK_ENDPOINT]}}, storage_secret='alpha')
    first: list[str] = []
    second: list[str] = []

    @ui.page('/')
    def page():
        shared_event().subscribe(first.append)
        shared_event().subscribe(second.append)

    await user.open('/')
    with remote_instance('alpha'):
        shared_event().emit('hello')
        await wait_for(lambda: bool(first) and bool(second))
    assert first == ['hello']
    assert second == ['hello']


def test_subscribing_does_not_keep_the_event_alive(fresh_session):
    """An event created per client (e.g. inside a page function) must not be pinned by its subscription."""
    DistributedSession.initialize({'listen': {'endpoints': [LOOPBACK_ENDPOINT]}}, storage_secret='alpha')
    reference = weakref.ref(shared_event())
    gc.collect()
    assert reference() is None


async def test_own_emission_is_not_echoed_back(user: User, fresh_session):
    """Each instance subscribes to the topic it publishes on, so its own emission must not arrive twice."""
    DistributedSession.initialize({'listen': {'endpoints': [LOOPBACK_ENDPOINT]}}, storage_secret='alpha')
    received: list[str] = []

    @ui.page('/')
    def page():
        event = shared_event()
        event.subscribe(received.append)
        ui.button('emit', on_click=lambda: event.emit('hello'))

    await user.open('/')
    user.find('emit').click()
    await wait_for(lambda: bool(received))
    await asyncio.sleep(0.5)  # leave time for an echo to come back through the network
    assert received == ['hello']


async def test_a_failing_publish_does_not_abort_the_handler(user: User, caplog: pytest.LogCaptureFixture,
                                                            fresh_session):
    """The local callbacks have already run when the publish happens, so a dead transport must not raise."""
    DistributedSession.initialize({'listen': {'endpoints': [LOOPBACK_ENDPOINT]}}, storage_secret='alpha')

    @ui.page('/')
    def page():
        event = shared_event()

        def emit_and_go_on() -> None:
            event.emit('hello')
            ui.label('done')

        ui.button('emit', on_click=emit_and_go_on)

    await user.open('/')
    session = DistributedSession.get()
    assert session is not None
    session.session.close()  # as a transport that went away while the app keeps running
    user.find('emit').click()
    await user.should_see('done')
    assert len(caplog.records) == 1 and 'Failed to publish' in caplog.records[0].message
    caplog.records.pop(0)


async def test_instance_with_different_secret_is_ignored(user: User, fresh_session):
    """Deployments that do not share the storage_secret must not cross-talk."""
    DistributedSession.initialize({'listen': {'endpoints': [LOOPBACK_ENDPOINT]}}, storage_secret='alpha')
    received: list[str] = []

    @ui.page('/')
    def page():
        shared_event().subscribe(received.append)

    await user.open('/')
    with remote_instance('beta'):
        shared_event().emit('leak')
        with remote_instance('alpha'):  # stays connected while a matching instance gets through
            shared_event().emit('hello')
            await wait_for(lambda: bool(received))
    assert received == ['hello']


async def test_payload_without_the_secret_is_rejected(user: User, fresh_session):
    """Confidentiality boundary: seeing the topic on the wire is not enough to inject an event."""
    from cryptography.fernet import Fernet  # local import: only reachable when ZENOH_AVAILABLE
    DistributedSession.initialize({'listen': {'endpoints': [LOOPBACK_ENDPOINT]}}, storage_secret='alpha')
    observed: list[str] = []
    received: list[str] = []

    @ui.page('/')
    def page():
        event = shared_event()
        event.subscribe(received.append)
        ui.button('emit', on_click=lambda: event.emit('local'))

    await user.open('/')
    with wire_observer(observed) as sibling:
        await wait_for(lambda: bool(observed), retry=user.find('emit').click)
        received.clear()
        forged = json.dumps({'instance_id': 'attacker', 'data': {'args': ['leak'], 'kwargs': {}}}).encode()
        publisher = sibling.declare_publisher(observed[0])
        publisher.put(forged)  # not encrypted at all
        publisher.put(Fernet(Fernet.generate_key()).encrypt(forged))  # encrypted with a foreign key
        with remote_instance('alpha'):
            shared_event().emit('hello')
            await wait_for(lambda: bool(received))
    assert received == ['hello']


async def test_an_undecryptable_event_is_reported_once(user: User, caplog: pytest.LogCaptureFixture, fresh_session):
    """Dropping in complete silence looks exactly like having no peers, which is the harder thing to debug."""
    from cryptography.fernet import Fernet  # local import: only reachable when ZENOH_AVAILABLE
    DistributedSession.initialize({'listen': {'endpoints': [LOOPBACK_ENDPOINT]}}, storage_secret='alpha')
    observed: list[str] = []

    def reports() -> list[str]:
        return [record.message for record in caplog.records if 'could not be decrypted' in record.message]

    @ui.page('/')
    def page():
        event = shared_event()
        ui.button('emit', on_click=lambda: event.emit('local'))

    await user.open('/')
    with wire_observer(observed) as sibling:
        await wait_for(lambda: bool(observed), retry=user.find('emit').click)
        publisher = sibling.declare_publisher(observed[0])
        for _ in range(3):
            publisher.put(Fernet(Fernet.generate_key()).encrypt(b'{}'))  # encrypted with a foreign key
        await wait_for(lambda: bool(reports()))
        await asyncio.sleep(0.5)  # leave time for the other two to be dropped as well
    assert len(reports()) == 1
    assert f'event_{__name__}:' in reports()[0]


async def test_unreachable_network_degrades_to_local_events(user: User, fresh_session):
    """A Zenoh session that cannot be opened must not take the app down; events keep working locally."""
    DistributedSession.initialize({'listen': {'endpoints': ['bogus/127.0.0.1:1']}}, storage_secret='alpha')
    assert DistributedSession.get() is None
    received: list[str] = []

    @ui.page('/')
    def page():
        event = shared_event()
        event.subscribe(received.append)
        ui.button('emit', on_click=lambda: event.emit('hello'))

    await user.open('/')
    user.find('emit').click()
    await wait_for(lambda: bool(received))
    assert received == ['hello']


async def test_session_is_released_on_app_shutdown(user: User, fresh_session):
    """Resources must be released on app teardown, so remote events stop arriving once the app has stopped."""
    DistributedSession.initialize({'listen': {'endpoints': [LOOPBACK_ENDPOINT]}}, storage_secret='alpha')
    received: list[str] = []

    @ui.page('/')
    def page():
        shared_event().subscribe(received.append)

    await user.open('/')
    with remote_instance('alpha'):
        shared_event().emit('before')
        await wait_for(lambda: bool(received))
    assert received == ['before']

    await core.app.stop()
    assert DistributedSession.get() is None  # a later emit must not publish on a closed session

    with remote_instance('alpha'):
        shared_event().emit('after')
        await asyncio.sleep(0.5)
    assert received == ['before']


async def test_an_existing_event_follows_a_replaced_session(user: User, fresh_session):
    """Releasing a session and opening another one must not leave the events of the first one deaf.

    The ``user`` fixture is what puts a running event loop behind ``core.loop``, where remote events land.
    """
    DistributedSession.initialize({'listen': {'endpoints': [LOOPBACK_ENDPOINT]}}, storage_secret='alpha')
    received: list[str] = []
    event = shared_event()
    event.subscribe(received.append)

    session = DistributedSession.get()
    assert session is not None
    session.shutdown()
    DistributedSession.initialize({'listen': {'endpoints': [LOOPBACK_ENDPOINT]}}, storage_secret='alpha')

    with remote_instance('alpha'):
        shared_event().emit('hello')
        await wait_for(lambda: bool(received))
    assert received == ['hello']


async def test_shutdown_finishes_even_when_undeclaring_fails(user: User, caplog: pytest.LogCaptureFixture,
                                                             fresh_session):
    """One resource that refuses to go must not leave the transport open and the session still installed."""
    DistributedSession.initialize({'listen': {'endpoints': [LOOPBACK_ENDPOINT]}}, storage_secret='alpha')
    session = DistributedSession.get()
    assert session is not None

    class StubbornPublisher:
        def undeclare(self) -> None:
            raise RuntimeError('not going anywhere')

    session.publishers['stubborn'] = StubbornPublisher()
    received: list[str] = []
    event = shared_event()
    event.subscribe(received.append)  # outside a UI context, so no client teardown unsubscribes it

    @ui.page('/')
    def page():
        ui.label('hello')

    await user.open('/')
    await core.app.stop()
    assert DistributedSession.get() is None

    with remote_instance('alpha'):
        shared_event().emit('after')
        await asyncio.sleep(0.5)
    assert received == []
    assert [record.message for record in caplog.records] == ['Error undeclaring a Zenoh publisher or subscriber']
    caplog.records.clear()
