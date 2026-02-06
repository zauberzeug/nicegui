import weakref

from nicegui import binding, ui
from nicegui.testing import SharedScreen


def test_remove_element_by_reference(shared_screen: SharedScreen):
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

    shared_screen.open('/')
    shared_screen.click('Remove')
    shared_screen.wait(0.5)
    shared_screen.should_contain('Label A')
    shared_screen.should_not_contain('Label B')
    shared_screen.should_contain('Label C')
    assert b.is_deleted
    assert b.id not in row.client.elements
    assert len(row.default_slot.children) == 2
    assert len(binding.active_links) == 2


def test_remove_element_by_index(shared_screen: SharedScreen):
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

    shared_screen.open('/')
    shared_screen.click('Remove')
    shared_screen.wait(0.5)
    shared_screen.should_contain('Label A')
    shared_screen.should_not_contain('Label B')
    shared_screen.should_contain('Label C')
    assert b.is_deleted
    assert b.id not in row.client.elements
    assert len(row.default_slot.children) == 2
    assert len(binding.active_links) == 2


def test_clear(shared_screen: SharedScreen):
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

    shared_screen.open('/')
    shared_screen.click('Clear')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('Label A')
    shared_screen.should_not_contain('Label B')
    shared_screen.should_not_contain('Label C')
    assert a.is_deleted
    assert b.is_deleted
    assert c.is_deleted
    assert b.id not in row.client.elements
    assert len(row.default_slot.children) == 0
    assert len(binding.active_links) == 0


def test_remove_parent(shared_screen: SharedScreen):
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

    shared_screen.open('/')
    shared_screen.click('Remove parent')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('Label A')
    shared_screen.should_not_contain('Label B')
    shared_screen.should_not_contain('Label C')
    assert row.is_deleted
    assert a.is_deleted
    assert b.is_deleted
    assert c.is_deleted
    assert a.id not in container.client.elements
    assert b.id not in container.client.elements
    assert c.id not in container.client.elements
    assert len(container.default_slot.children) == 0
    assert len(binding.active_links) == 0


def test_delete_element(shared_screen: SharedScreen):
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

    shared_screen.open('/')
    shared_screen.click('Delete')
    shared_screen.wait(0.5)
    shared_screen.should_contain('Label A')
    shared_screen.should_not_contain('Label B')
    shared_screen.should_contain('Label C')
    assert b.is_deleted
    assert b.id not in row.client.elements
    assert len(row.default_slot.children) == 2
    assert len(binding.active_links) == 2


def test_on_delete(shared_screen: SharedScreen):
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

    shared_screen.open('/')
    shared_screen.click('Delete C')
    shared_screen.click('Delete B')
    shared_screen.click('Clear row')
    shared_screen.wait(0.5)
    assert deleted_labels == ['Label C', 'Label B', 'Label A']


def test_slot_children_cleared_on_delete(shared_screen: SharedScreen):
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

    shared_screen.open('/')
    shared_screen.click('Delete')
    shared_screen.should_contain('Deleted')
    assert len(labels) == 0, 'all labels should be deleted immediately'


def test_event_listeners_cleared_on_delete(shared_screen: SharedScreen):
    """Event listeners are cleared when element is deleted and no cyclic references are left behind (issue #5110)."""
    buttons = weakref.WeakSet[ui.button]()

    @ui.page('/')
    def page():
        with ui.card() as card:
            button = ui.button('Click me')
            button.on('click', lambda: button.set_text('clicked'))  # cycle: button → listener → lambda → button
            buttons.add(button)
        ui.button('Delete', on_click=card.clear).on_click(lambda: ui.notify('Deleted'))

    shared_screen.open('/')
    shared_screen.click('Delete')
    shared_screen.should_contain('Deleted')
    assert len(buttons) == 0, 'all buttons should be deleted immediately'
