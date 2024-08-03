from nicegui import ui

from . import doc


@doc.demo(ui.teleport)
def main_demo() -> None:
    markdown = ui.markdown('Enter your **name**!')

    def inject_input():
        with ui.teleport(f'#c{markdown.id} strong'):
            ui.input('name').classes('inline-flex').props('dense outlined')

    ui.button('inject input', on_click=inject_input)


@doc.demo('Radio element with arbitrary content', '''
    With the right CSS selector, you can place any content inside a standard radio element.
''')
def arbitrary_content():
    options = ['Star', 'Thump Up', 'Heart']
    radio = ui.radio({x: '' for x in options}, value='Star').props('inline')
    with ui.teleport(f'#c{radio.id} > div:nth-child(1) .q-radio__label'):
        ui.icon('star', size='md')
    with ui.teleport(f'#c{radio.id} > div:nth-child(2) .q-radio__label'):
        ui.icon('thumb_up', size='md')
    with ui.teleport(f'#c{radio.id} > div:nth-child(3) .q-radio__label'):
        ui.icon('favorite', size='md')
    ui.label().bind_text_from(radio, 'value')


@doc.demo('Injecting a graph into a table cell', '''
    This demo shows how to inject ECharts graphs into table cells.
''')
def graph_in_table():
    columns = [
        {'name': 'name', 'label': 'Product', 'field': 'name', 'align': 'center'},
        {'name': 'sales', 'label': 'Sales', 'field': 'sales', 'align': 'center'},
    ]
    rows = [
        {'name': 'A', 'data': [10, 8, 2, 4]},
        {'name': 'B', 'data': [3, 5, 7, 8]},
        {'name': 'C', 'data': [2, 1, 3, 7]},
    ]
    table = ui.table(columns=columns, rows=rows, row_key='name').classes('w-72')
    for r, row in enumerate(rows):
        with ui.teleport(f'#c{table.id} tr:nth-child({r+1}) td:nth-child(2)'):
            ui.echart({
                'xAxis': {'type': 'category', 'show': False},
                'yAxis': {'type': 'value', 'show': False},
                'series': [{'type': 'line', 'data': row['data']}],
            }).classes('w-44 h-20')


doc.reference(ui.teleport)
