from nicegui import binding, ui
from nicegui.testing import Screen


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
