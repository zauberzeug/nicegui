from nicegui import ui

from . import doc


@doc.demo(ui.rating)
def main_demo() -> None:
    ui.rating(value=4)


@doc.demo('Customize icons', '''
    You can customize the icons and size.
    The icon for the selected state can also be customised.
''')
def customize_icons():
    ui.label('Change the icon and size')
    ui.rating(value=4, icon='mood', size='lg')

    ui.label('Change the selected icon to differ the un-selected')
    ui.rating(value=4, icon='sentiment_neutral', icon_selected='mood')



@doc.demo('Change rating color', '''
    You can change the color of the rating.
    This can be a single color or a range of different colors.
''')
def rating_color():
    ui.label('Change icons to a single color')
    ui.rating(value=3, color='red-10')

    ui.label('Change icons to a range of colors')
    colors = ['green-1', 'green-3', 'green-5', 'green-7', 'green-10']
    
    rating = ui.range(value=5)
    rating.props(f':color-selected="{colors}"')



@doc.demo('Change rating scale', '''
    This demo shows how to change the maximum rating allowed and
    how to include an additional icon for partial values.
''')
def rating_scale():
    rating = ui.rating(value=6.5, icon='star_outline', icon_selected='star', max=10)
    rating.props('icon-half="star_half"')



    


doc.reference(ui.range)