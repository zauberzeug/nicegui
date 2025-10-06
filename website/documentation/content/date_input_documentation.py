from nicegui import ui

from . import doc


@doc.demo(ui.date_input)
def main_demo() -> None:
    label = ui.label('date: 2025-05-31')
    ui.date_input(label='Date', value='2025-05-31',
                  on_change=lambda e: label.set_text(f'date: {e.value}'))


@doc.demo('Date Range Input', '''
    This demo shows how to use the date input with a range selection.

    To respect the input which expects a string, the value is a string formatted as 'start_date - end_date'.
''')
def date_range_input_demo():
    label = ui.label('date range: 2025-05-01 - 2025-05-31')
    ui.date_input('Date range', value='2025-05-01 - 2025-05-31', range_input=True,
                  on_change=lambda e: label.set_text(f'date range: {e.value}'))


@doc.demo('Date Input with Date Filter', '''
    This demo shows how to use the date input with a date filter by customizing `.picker`, the underlying `ui.date` element.

    Read more about the date filter in the [`ui.date` documentation](date).
''')
def date_input_with_filter_demo():
    label = ui.label('date: 2023-01-01')
    date_input = ui.date_input(label='Date', value='2023-01-01',
                               on_change=lambda e: label.set_text(f'date: {e.value}'))
    date_input.picker.props('''default-year-month=2023/01 :options="date => date <= '2023/01/15'"''')


doc.reference(ui.date_input)
