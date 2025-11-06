from nicegui import ui

from . import doc


@doc.demo(ui.date_input)
def main_demo() -> None:
    date = ui.date_input('Date', value='2025-05-31')
    ui.label().bind_text_from(date, 'value', lambda v: f'date: {v}')


@doc.demo('Date Range Input', '''
    This demo shows how to use the date input with a range selection.

    To respect the input which expects a string, the value is a string formatted as 'start_date - end_date'.
''')
def date_range_input_demo():
    date = ui.date_input('Range', value='2025-05-01 - 2025-05-31', range_input=True)
    date.classes('w-60')
    ui.label().bind_text_from(date, 'value', lambda v: f'range: {v}')


@doc.demo('Date Input with Date Filter', '''
    This demo shows how to use the date input with a date filter by customizing `.picker`, the underlying `ui.date` element.

    Read more about the date filter in the [`ui.date` documentation](date).
''')
def date_input_with_filter_demo():
    date = ui.date_input('Date', value='2025-11-15')
    date.picker.props[':options'] = 'date => date >= "2025/11/10"'
    ui.label().bind_text_from(date, 'value', lambda v: f'date: {v}')


doc.reference(ui.date_input)
