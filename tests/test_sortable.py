from nicegui import events, ui
from nicegui.testing import Screen


def _simulate_sortend_event(screen: Screen, item: ui.element, *,
                            source: ui.element | None = None, target: ui.element | None = None,
                            old_index: int, new_index: int) -> None:
    assert item.parent_slot is not None
    source = source or item.parent_slot.parent
    target = target or item.parent_slot.parent
    screen.selenium.execute_script(f'''
        // Mirrors the slot manipulation in sortable.js onEnd handler — keep in sync.
        const fromSlot = window.mounted_app?.elements?.[{source.id}]?.slots?.default;
        const toSlot = window.mounted_app?.elements?.[{target.id}]?.slots?.default;
        if (fromSlot && fromSlot.ids) {{
            const itemId = fromSlot.ids.splice({old_index}, 1)[0];
            if ({source.id} === {target.id}) {{
                fromSlot.ids.splice({new_index}, 0, itemId);
            }} else if (toSlot && toSlot.ids) {{
                toSlot.ids.splice({new_index}, 0, itemId);
            }}
        }}
        {source.html_id}.dispatchEvent(new CustomEvent('sortend', {{
            detail: {{
                item_id: {item.id},
                from_id: {source.id},
                to_id: {target.id},
                old_index: {old_index},
                new_index: {new_index},
            }},
            bubbles: false,
        }}));
    ''')


def test_basic_reorder(screen: Screen):
    sort_events: list[tuple[ui.element, ui.element, ui.element, int, int]] = []
    item = None

    @ui.page('/')
    def page():
        nonlocal item
        with ui.column() as col:
            item = ui.label('A')
            ui.label('B')
            ui.label('C')
        order = ui.label()

        def handle_end(e: events.SortableEventArguments):
            sort_events.append((e.item, e.source, e.target, e.old_index, e.new_index))
            order.text = f'col: {",".join(child._text or "" for child in col)}'  # pylint: disable=protected-access
        col.make_sortable(on_end=handle_end)

    screen.open('/')
    screen.should_contain('A')
    assert isinstance(item, ui.label)

    _simulate_sortend_event(screen, item, old_index=0, new_index=2)
    screen.should_contain('col: B,C,A')
    assert item.parent_slot is not None
    assert sort_events == [(item, item.parent_slot.parent, item.parent_slot.parent, 0, 2)]


def test_cross_container(screen: Screen):
    sort_events: list[tuple[str, int, int]] = []
    item, column1, column2 = None, None, None

    @ui.page('/')
    def page():
        nonlocal item, column1, column2
        with ui.row():
            with ui.column() as column1:
                item = ui.label('A')
                ui.label('B')
            with ui.column() as column2:
                ui.label('C')
        order1 = ui.label()
        order2 = ui.label()

        def handle_end_col1(e: events.SortableEventArguments):
            sort_events.append(('col1', e.old_index, e.new_index))
            order1.text = f'col1: {",".join(child._text or "" for child in column1)}'  # pylint: disable=protected-access
            order2.text = f'col2: {",".join(child._text or "" for child in column2)}'  # pylint: disable=protected-access
        column1.make_sortable(group='shared', on_end=handle_end_col1)
        column2.make_sortable(group='shared', on_end=lambda e: sort_events.append(('col2', e.old_index, e.new_index)))

    screen.open('/')
    screen.should_contain('A')
    assert isinstance(item, ui.label)
    assert isinstance(column1, ui.column)
    assert isinstance(column2, ui.column)

    _simulate_sortend_event(screen, item, source=column1, target=column2, old_index=0, new_index=1)
    screen.should_contain('col1: B')
    screen.should_contain('col2: C,A')
    assert sort_events == [('col1', 0, 1)]


def test_multiple_handlers(screen: Screen):
    events1: list[tuple[int, int]] = []
    events2: list[tuple[int, int]] = []
    item = None

    @ui.page('/')
    def page():
        nonlocal item
        with ui.column() as col:
            item = ui.label('A')
            ui.label('B')
        order = ui.label()

        def handle_end(e: events.SortableEventArguments):
            events1.append((e.old_index, e.new_index))
            order.text = f'col: {",".join(child._text or "" for child in col)}'  # pylint: disable=protected-access
        sortable = col.make_sortable(on_end=handle_end)
        sortable.on_end(lambda e: events2.append((e.old_index, e.new_index)))

    screen.open('/')
    screen.should_contain('A')
    assert isinstance(item, ui.label)

    _simulate_sortend_event(screen, item, old_index=0, new_index=1)
    screen.should_contain('col: B,A')
    assert events1 == [(0, 1)]
    assert events2 == [(0, 1)]
