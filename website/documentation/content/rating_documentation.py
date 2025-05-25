from nicegui import ui

from . import doc


@doc.demo(ui.rating)
def main_demo() -> None:
    ui.rating(value=4)


@doc.demo('Customize icons', '''
    You can customize name and size of the icons.
    Optionally, unselected, selected or half-selected values can have different icons.
''')
def customize_icons():
    ui.rating(
        value=3.5,
        size='lg',
        icon='sentiment_dissatisfied',
        icon_selected='sentiment_satisfied',
        icon_half='sentiment_neutral',
    )
    ui.rating(
        value=3.5,
        size='lg',
        icon='star',
        icon_selected='star',
        icon_half='star_half',
    )


@doc.demo('Customize color', '''
    You can customize the color of the rating either by providing a single color or a range of different colors.
''')
def rating_color():
    ui.rating(value=3, color='red-10')
    ui.rating(value=5, color=['green-2', 'green-4', 'green-6', 'green-8', 'green-10'])


@doc.demo('Maximum rating', '''
    This demo shows how to change the maximum possible rating
    as well as binding the value to a slider.
''')
def rating_scale():
    slider = ui.slider(value=5, min=0, max=10)
    ui.rating(max=10, icon='circle').bind_value(slider)


doc.reference(ui.rating)
