from nicegui import ui

from . import doc


@doc.demo(ui.range)
def main_demo() -> None:
    min_max_range = ui.range(min=0, max=100, value={'min': 20, 'max': 80})
    ui.label().bind_text_from(min_max_range, 'value',
                              backward=lambda v: f'min: {v["min"]}, max: {v["max"]}')


@doc.demo('Customize labels', '''
        You can customize the colors of the range and its labels by setting them individually or for the range in total.
''')
def customize_labels():
    ui.label('Color the entire range')
    ui.range(min=0, max=100, value={'min': 20, 'max': 80}) \
        .props('label snap color="secondary"')

    ui.label('Customize the color of the labels')
    ui.range(min=0, max=100, value={'min': 40, 'max': 80}) \
        .props('label-always snap label-color="secondary" right-label-text-color="black"')


doc.reference(ui.range)
