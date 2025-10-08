from unittest.mock import MagicMock, patch

from nicegui import Event, ui
from nicegui.distributed import DistributedSession
from nicegui.testing import User


def test_local_event_skips_distributed_setup():
    """Events marked as local=True don't set up distributed handling."""
    with patch.object(DistributedSession, 'get', return_value=MagicMock()):
        event = Event[str](local=True)
        assert not event._zenoh_setup_done  # pylint: disable=protected-access


def test_distributed_event_calls_publish():
    """Events call publish when distributed session exists."""
    mock_session = MagicMock()
    with patch.object(DistributedSession, 'get', return_value=mock_session):
        event = Event[str]()
        event.emit('hello')
        mock_session.publish.assert_called_once()
        call_args = mock_session.publish.call_args
        assert call_args[0][1] == {'args': ('hello',), 'kwargs': {}}


def test_event_topic_generation():
    """Event topics are generated from file location."""
    event1 = Event[str]()
    event2 = Event[int]()  # Different line
    assert event1.topic != event2.topic
    assert 'test_distributed_events.py' in event1.topic
    assert ':' in event1.topic  # Contains line number


def test_setup_existing_events():
    """DistributedSession.initialize() sets up existing events."""
    mock_config = MagicMock()
    mock_session = MagicMock()

    with patch('nicegui.distributed.zenoh') as mock_zenoh:
        mock_zenoh.Config.return_value = mock_config
        mock_zenoh.open.return_value = mock_session
        with patch.object(DistributedSession, '_instance', None):
            DistributedSession.initialize(True)
            assert DistributedSession.get() is not None


async def test_distributed_event_publishes_in_ui(user: User):
    """Distributed events publish to session when emitted in UI context."""
    mock_session = MagicMock()

    with patch.object(DistributedSession, 'get', return_value=mock_session):
        event = Event[str]()

        @ui.page('/')
        def page():
            ui.button('Test', on_click=lambda: event.emit('hello'))

        await user.open('/')
        user.find('Test').click()
        await user.wait(0.1)

        # Verify the event was published to the distributed session
        mock_session.publish.assert_called()
        call_args = mock_session.publish.call_args
        assert call_args[0][1] == {'args': ('hello',), 'kwargs': {}}
