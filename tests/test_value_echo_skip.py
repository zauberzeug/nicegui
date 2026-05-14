"""Tests for the client-value echo skip optimization in ValueElement (see #5933)."""

from collections.abc import Callable

import pytest

from nicegui import ui
from nicegui.elements.mixins.value_element import ValueElement
from nicegui.helpers import event_type_to_camel_case
from nicegui.testing import User


class PlainValue(ValueElement[str]):

    def __init__(self, *, value: str = '', on_change: Callable | None = None) -> None:
        super().__init__(tag='div', value=value, on_value_change=on_change)


class TruncatingValue(ValueElement[str]):

    def __init__(self, *, value: str = '') -> None:
        super().__init__(tag='div', value=value)

    def _value_to_model_value(self, value):  # type: ignore[override]
        return (value or '')[:3]


def _outbox_has_update_for(element) -> bool:
    return element.id in element.client.outbox.updates


def _simulate_client_change(element, value) -> None:
    event_name = event_type_to_camel_case(f'update:{element.VALUE_PROP}')
    listeners = element._event_listeners  # pylint: disable=protected-access
    try:
        listener_id = next(lid for lid, listener in listeners.items() if listener.type == event_name)
    except StopIteration:
        types = sorted({listener.type for listener in listeners.values()})
        raise AssertionError(f'no {event_name!r} listener on {element!r}; have: {types}') from None
    element._handle_event({'listener_id': listener_id, 'args': value})  # pylint: disable=protected-access


def _single(user: User, kind):
    return next(iter(user.find(kind=kind).elements))


async def test_pure_echo_is_skipped(user: User):
    @ui.page('/')
    def page():
        PlainValue(value='')

    await user.open('/')
    elem = _single(user, PlainValue)
    elem.client.outbox.updates.clear()
    _simulate_client_change(elem, 'hello')
    assert elem.value == 'hello'
    assert not _outbox_has_update_for(elem)


async def test_server_transform_is_echoed(user: User):
    @ui.page('/')
    def page():
        TruncatingValue(value='')

    await user.open('/')
    elem = _single(user, TruncatingValue)
    elem.client.outbox.updates.clear()
    _simulate_client_change(elem, 'abcdef')
    assert elem._props[elem.VALUE_PROP] == 'abc'  # pylint: disable=protected-access
    assert _outbox_has_update_for(elem)


async def test_on_change_correction_is_echoed(user: User):
    @ui.page('/')
    def page():
        PlainValue(value='', on_change=lambda e: setattr(e.sender, 'value', str(e.value).upper()))

    await user.open('/')
    elem = _single(user, PlainValue)
    elem.client.outbox.updates.clear()
    _simulate_client_change(elem, 'hello')
    assert elem.value == 'HELLO'
    assert _outbox_has_update_for(elem)


async def test_side_effect_update_in_handler_flows_through(user: User):
    @ui.page('/')
    def page():
        PlainValue(value='', on_change=lambda e: e.sender.classes('error'))

    await user.open('/')
    elem = _single(user, PlainValue)
    elem.client.outbox.updates.clear()
    _simulate_client_change(elem, 'x')
    assert _outbox_has_update_for(elem)


async def test_loopback_false_still_skips(user: User):
    @ui.page('/')
    def page():
        ui.input(value='')

    await user.open('/')
    inp = _single(user, ui.input)
    inp.client.outbox.updates.clear()
    _simulate_client_change(inp, 'hello')
    assert inp.value == 'hello'
    assert not _outbox_has_update_for(inp)


async def test_to_dict_still_carries_value(user: User):
    @ui.page('/')
    def page():
        PlainValue(value='initial')

    await user.open('/')
    elem = _single(user, PlainValue)
    _simulate_client_change(elem, 'client_typed')
    assert elem._to_dict()['props'][elem.VALUE_PROP] == 'client_typed'  # pylint: disable=protected-access


@pytest.mark.parametrize('factory, kind, emit', [
    (lambda: ui.checkbox('cb'), ui.checkbox, True),
    (lambda: ui.switch('sw'), ui.switch, True),
    (lambda: ui.dialog(), ui.dialog, True),
    (lambda: ui.menu(), ui.menu, True),
    (lambda: ui.expansion('exp'), ui.expansion, True),
    (lambda: ui.select(options=['a', 'b'], value='a'), ui.select, {'value': 1, 'label': 'b'}),
])
async def test_real_loopback_true_elements_skip_echo(user: User, factory, kind, emit):
    @ui.page('/')
    def page():
        factory()

    await user.open('/')
    elem = _single(user, kind)
    elem.client.outbox.updates.clear()
    _simulate_client_change(elem, emit)
    assert not _outbox_has_update_for(elem)


async def test_rapid_toggles_do_not_enqueue_outbox_update(user: User):
    @ui.page('/')
    def page():
        ui.checkbox('cb')

    await user.open('/')
    cb = _single(user, ui.checkbox)
    cb.client.outbox.updates.clear()
    for i in range(50):
        _simulate_client_change(cb, bool(i % 2))
    assert cb.id not in cb.client.outbox.updates


async def test_set_value_exception_does_not_leak_suppression(user: User, caplog: pytest.LogCaptureFixture):
    class Raising(ValueElement[str]):
        def __init__(self) -> None:
            super().__init__(tag='div', value='')

        def _value_to_model_value(self, value):  # type: ignore[override]
            if value == 'BOOM':
                raise ValueError('nope')
            return value

    @ui.page('/')
    def page():
        Raising()

    await user.open('/')
    elem = _single(user, Raising)
    _simulate_client_change(elem, 'BOOM')  # handle_event swallows + logs the ValueError
    caplog.clear()
    elem.client.outbox.updates.clear()
    elem.value = 'legit'  # server-driven change must still flow
    assert _outbox_has_update_for(elem)
