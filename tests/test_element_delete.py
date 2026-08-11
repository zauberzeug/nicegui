import asyncio
import weakref

import pytest

from nicegui import binding, ui
from nicegui.testing import Screen, User


def test_remove_element_by_reference(screen: Screen):
    texts = {'a': 'Label A', 'b': 'Label B', 'c': 'Label C'}
    b = row = None

    @ui.page('/')
    def page():
        nonlocal b, row
        with ui.row() as row:
            ui.label().bind_text_from(texts, 'a')
            b = ui.label().bind_text_from(texts, 'b')
            ui.label().bind_text_from(texts, 'c')

        ui.button('Remove', on_click=lambda: row.remove(b))

    screen.open('/')
    screen.click('Remove')
    screen.wait(0.5)
    screen.should_contain('Label A')
    screen.should_not_contain('Label B')
    screen.should_contain('Label C')
    assert b.is_deleted
    assert b.id not in row.client.elements
    assert len(row.default_slot.children) == 2
    assert len(binding.active_links) == 2


def test_remove_element_by_index(screen: Screen):
    texts = {'a': 'Label A', 'b': 'Label B', 'c': 'Label C'}
    b = row = None

    @ui.page('/')
    def page():
        nonlocal b, row
        with ui.row() as row:
            ui.label().bind_text_from(texts, 'a')
            b = ui.label().bind_text_from(texts, 'b')
            ui.label().bind_text_from(texts, 'c')

        ui.button('Remove', on_click=lambda: row.remove(1))

    screen.open('/')
    screen.click('Remove')
    screen.wait(0.5)
    screen.should_contain('Label A')
    screen.should_not_contain('Label B')
    screen.should_contain('Label C')
    assert b.is_deleted
    assert b.id not in row.client.elements
    assert len(row.default_slot.children) == 2
    assert len(binding.active_links) == 2


def test_clear(screen: Screen):
    texts = {'a': 'Label A', 'b': 'Label B', 'c': 'Label C'}
    a = b = c = row = None

    @ui.page('/')
    def page():
        nonlocal a, b, c, row
        with ui.row() as row:
            a = ui.label().bind_text_from(texts, 'a')
            b = ui.label().bind_text_from(texts, 'b')
            c = ui.label().bind_text_from(texts, 'c')

        ui.button('Clear', on_click=row.clear)

    screen.open('/')
    screen.click('Clear')
    screen.wait(0.5)
    screen.should_not_contain('Label A')
    screen.should_not_contain('Label B')
    screen.should_not_contain('Label C')
    assert a.is_deleted
    assert b.is_deleted
    assert c.is_deleted
    assert b.id not in row.client.elements
    assert len(row.default_slot.children) == 0
    assert len(binding.active_links) == 0


def test_remove_parent(screen: Screen):
    texts = {'a': 'Label A', 'b': 'Label B', 'c': 'Label C'}
    a = b = c = row = container = None

    @ui.page('/')
    def page():
        nonlocal a, b, c, row, container
        with ui.element() as container:
            with ui.row() as row:
                a = ui.label().bind_text_from(texts, 'a')
                b = ui.label().bind_text_from(texts, 'b')
                c = ui.label().bind_text_from(texts, 'c')

        ui.button('Remove parent', on_click=lambda: container.remove(row))

    screen.open('/')
    screen.click('Remove parent')
    screen.wait(0.5)
    screen.should_not_contain('Label A')
    screen.should_not_contain('Label B')
    screen.should_not_contain('Label C')
    assert row.is_deleted
    assert a.is_deleted
    assert b.is_deleted
    assert c.is_deleted
    assert a.id not in container.client.elements
    assert b.id not in container.client.elements
    assert c.id not in container.client.elements
    assert len(container.default_slot.children) == 0
    assert len(binding.active_links) == 0


def test_delete_element(screen: Screen):
    texts = {'a': 'Label A', 'b': 'Label B', 'c': 'Label C'}
    b = row = None

    @ui.page('/')
    def page():
        nonlocal b, row
        with ui.row() as row:
            ui.label().bind_text_from(texts, 'a')
            b = ui.label().bind_text_from(texts, 'b')
            ui.label().bind_text_from(texts, 'c')

        ui.button('Delete', on_click=b.delete)

    screen.open('/')
    screen.click('Delete')
    screen.wait(0.5)
    screen.should_contain('Label A')
    screen.should_not_contain('Label B')
    screen.should_contain('Label C')
    assert b.is_deleted
    assert b.id not in row.client.elements
    assert len(row.default_slot.children) == 2
    assert len(binding.active_links) == 2


def test_on_delete(screen: Screen):
    deleted_labels = []

    class CustomLabel(ui.label):

        def __init__(self, text: str) -> None:
            super().__init__(text)

        def _handle_delete(self) -> None:
            deleted_labels.append(self.text)
            super()._handle_delete()

    b = row = None

    @ui.page('/')
    def page():
        nonlocal b, row
        with ui.row() as row:
            CustomLabel('Label A')
            b = CustomLabel('Label B')
            CustomLabel('Label C')

        ui.button('Delete C', on_click=lambda: row.remove(2))
        ui.button('Delete B', on_click=lambda: row.remove(b))
        ui.button('Clear row', on_click=row.clear)

    screen.open('/')
    screen.click('Delete C')
    screen.click('Delete B')
    screen.click('Clear row')
    screen.wait(0.5)
    assert deleted_labels == ['Label C', 'Label B', 'Label A']


def test_slot_children_cleared_on_delete(screen: Screen):
    """Slot children are cleared when parent is deleted and no cyclic references are left behind (issue #5110)."""
    labels = weakref.WeakSet[ui.label]()

    @ui.page('/')
    def page():
        with ui.splitter() as splitter:
            labels.add(ui.label('Default'))
            with splitter.before:
                labels.add(ui.label('Before'))
            with splitter.after:
                labels.add(ui.label('After'))
        ui.button('Delete', on_click=splitter.delete).on_click(lambda: ui.notify('Deleted'))

    screen.open('/')
    screen.click('Delete')
    screen.should_contain('Deleted')
    assert len(labels) == 0, 'all labels should be deleted immediately'


@pytest.mark.parametrize('deletion_method', ['client_delete', 'element_delete'])
async def test_usage_after_delete(user: User, caplog: pytest.LogCaptureFixture, deletion_method: str):
    """Using an element or head functions after deletion is silent when the client is gone (benign reload race)
    but warns once when only the element was deleted (a user bug). See issue #6058."""
    label = None

    @ui.page('/')
    def page():
        nonlocal label
        label = ui.label('hi')

    await user.open('/')
    assert isinstance(label, ui.label)
    (label.client if deletion_method == 'client_delete' else label).delete()
    assert label.client.is_deleted == (deletion_method == 'client_delete')
    assert label.is_deleted

    label.run_method('foo')
    label.update()
    label.get_computed_prop('bar')
    with label.client:
        ui.page_title('late title')
        ui.add_head_html('<meta name="late">')
        ui.add_body_html('<span>late</span>')
        ui.add_css('body {color: red}')
    await asyncio.sleep(0)  # let the fire-and-forget tasks of run_javascript run
    expected_warnings = 0 if deletion_method == 'client_delete' else 1
    assert len([record for record in caplog.records if 'still being used' in record.message]) == expected_warnings


async def test_parent_slot_error(user: User):
    label = card = None

    @ui.page('/')
    def page():
        nonlocal label, card
        with ui.card() as card:
            label = ui.label('hi').mark('my_label')

    await user.open('/')
    card.delete()
    del card  # drop the last strong reference to the card and its slots
    with pytest.raises(RuntimeError, match=r'The parent slot of Label\(id=5, markers=my_label\) has been deleted\.'):
        _ = label.parent_slot


def test_event_listeners_cleared_on_delete(screen: Screen):
    """Event listeners are cleared when element is deleted and no cyclic references are left behind (issue #5110)."""
    buttons = weakref.WeakSet[ui.button]()

    @ui.page('/')
    def page():
        with ui.card() as card:
            button = ui.button('Click me')
            button.on('click', lambda: button.set_text('clicked'))  # cycle: button → listener → lambda → button
            buttons.add(button)
        ui.button('Delete', on_click=card.clear).on_click(lambda: ui.notify('Deleted'))

    screen.open('/')
    screen.click('Delete')
    screen.should_contain('Deleted')
    assert len(buttons) == 0, 'all buttons should be deleted immediately'
