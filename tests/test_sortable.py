from nicegui import ui
from nicegui.testing import Screen


def _dispatch_sortend(screen: Screen, element_id: int, item_id: int, *,
                      from_id: int | None = None, to_id: int | None = None,
                      old_index: int, new_index: int) -> None:
    """Dispatch a synthetic sortend CustomEvent on the element DOM node.

    NOTE: The client-side tree-sync logic here must mirror the onEnd handler in sortable.py's _INIT_JS.
    """
    from_id = from_id or element_id
    to_id = to_id or element_id
    screen.selenium.execute_script(f'''
        const dom = document.getElementById('c' + {element_id});
        // update client-side element tree to prevent snap-back
        const fromSlot = window.mounted_app?.elements?.[{from_id}]?.slots?.default;
        const toSlot = window.mounted_app?.elements?.[{to_id}]?.slots?.default;
        if (fromSlot && fromSlot.ids) {{
            const itemId = fromSlot.ids.splice({old_index}, 1)[0];
            if ({from_id} === {to_id}) {{
                fromSlot.ids.splice({new_index}, 0, itemId);
            }} else if (toSlot && toSlot.ids) {{
                toSlot.ids.splice({new_index}, 0, itemId);
            }}
        }}
        dom.dispatchEvent(new CustomEvent('sortend', {{
            detail: {{
                item_id: {item_id},
                from_id: {from_id},
                to_id: {to_id},
                old_index: {old_index},
                new_index: {new_index},
            }},
            bubbles: false,
        }}));
    ''')


def test_basic_reorder(screen: Screen):
    events = []
    children_order = []
    col_ref = None

    @ui.page('/')
    def page():
        nonlocal col_ref
        with ui.column() as col:
            a = ui.label('A')
            b = ui.label('B')
            c = ui.label('C')
        col_ref = col

        def on_end(e):
            events.append((e.old_index, e.new_index))
            children_order.clear()
            children_order.extend(child.text for child in col_ref)

        col.make_sortable(on_end=on_end)
        ui.label(f'ids:{a.id},{b.id},{c.id},{col.id}')

    screen.open('/')
    screen.wait(0.5)

    # extract IDs from the page
    text = screen.find('ids:').text
    ids = text.replace('ids:', '').split(',')
    a_id, col_id = int(ids[0]), int(ids[3])

    # simulate moving A (index 0) to index 2
    _dispatch_sortend(screen, col_id, a_id, old_index=0, new_index=2)
    screen.wait(0.5)

    # verify callback fired
    assert len(events) == 1
    assert events[0] == (0, 2)

    # verify server-side children order: B, C, A
    assert children_order == ['B', 'C', 'A']


def test_cross_container(screen: Screen):
    events = []

    @ui.page('/')
    def page():
        with ui.row():
            with ui.column() as col1:
                a = ui.label('A')
                b = ui.label('B')
            with ui.column() as col2:
                c = ui.label('C')
        col1.make_sortable(group='shared', on_end=lambda e: events.append(('col1', e.old_index, e.new_index)))
        col2.make_sortable(group='shared', on_end=lambda e: events.append(('col2', e.old_index, e.new_index)))
        ui.label(f'ids:{a.id},{b.id},{c.id},{col1.id},{col2.id}')

    screen.open('/')
    screen.wait(0.5)

    text = screen.find('ids:').text
    ids = text.replace('ids:', '').split(',')
    a_id, col1_id, col2_id = int(ids[0]), int(ids[3]), int(ids[4])

    # simulate moving A from col1 (index 0) to col2 (index 1)
    _dispatch_sortend(screen, col1_id, a_id, from_id=col1_id, to_id=col2_id, old_index=0, new_index=1)
    screen.wait(0.5)

    # verify callback on col1 fired
    assert len(events) == 1
    assert events[0] == ('col1', 0, 1)


def test_enable_disable(screen: Screen):
    @ui.page('/')
    def page():
        with ui.column() as col:
            ui.label('A')
            ui.label('B')
        sortable = col.make_sortable()
        ui.button('Disable', on_click=sortable.disable)
        ui.button('Enable', on_click=sortable.enable)

    screen.open('/')
    screen.wait(0.5)

    # verify disable/enable don't raise errors
    screen.click('Disable')
    screen.wait(0.3)
    screen.click('Enable')
    screen.wait(0.3)


def test_destroy(screen: Screen):
    @ui.page('/')
    def page():
        with ui.column() as col:
            ui.label('A')
            ui.label('B')
        sortable = col.make_sortable()
        ui.button('Destroy', on_click=sortable.destroy)

    screen.open('/')
    screen.wait(0.5)

    screen.click('Destroy')
    screen.wait(0.3)


def test_multiple_handlers(screen: Screen):
    events1 = []
    events2 = []

    @ui.page('/')
    def page():
        with ui.column() as col:
            a = ui.label('A')
            b = ui.label('B')
        sortable = col.make_sortable(on_end=lambda e: events1.append(e.new_index))
        sortable.on_end(lambda e: events2.append(e.new_index))
        ui.label(f'ids:{a.id},{b.id},{col.id}')

    screen.open('/')
    screen.wait(0.5)

    text = screen.find('ids:').text
    ids = text.replace('ids:', '').split(',')
    a_id, col_id = int(ids[0]), int(ids[2])

    _dispatch_sortend(screen, col_id, a_id, old_index=0, new_index=1)
    screen.wait(0.5)

    assert events1 == [1]
    assert events2 == [1]


def test_element_references(screen: Screen):
    results = {}

    @ui.page('/')
    def page():
        with ui.column() as col:
            a = ui.label('A')
            b = ui.label('B')

        def on_end(e):
            results['item_id'] = e.item.id
            results['source_id'] = e.source.id
            results['target_id'] = e.target.id

        col.make_sortable(on_end=on_end)
        ui.label(f'ids:{a.id},{b.id},{col.id}')

    screen.open('/')
    screen.wait(0.5)

    text = screen.find('ids:').text
    ids = text.replace('ids:', '').split(',')
    a_id, col_id = int(ids[0]), int(ids[2])

    _dispatch_sortend(screen, col_id, a_id, old_index=0, new_index=1)
    screen.wait(0.5)

    assert results['item_id'] == a_id
    assert results['source_id'] == col_id
    assert results['target_id'] == col_id
