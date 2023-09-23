from nicegui import Tailwind, ui

heading_style = 'color: blue; font-size: 200%; font-weight: 500'

ui.markdown("""## NiceGui Style""")
# Issue:
# pygments.util.ClassNotFound: Could not find style module 'github-dark'.
# Fix: 
# https://github.com/zauberzeug/nicegui/issues/1595
# upgrade pygments to 2.16.1 (was 2.11.2)

ui.markdown("""### How to simplify styling
[PR #362: TailwindCSS class manager](https://github.com/zauberzeug/nicegui/pull/362)
""")


with ui.row():
    with ui.card():
        ui.label("Styling ").style(heading_style)

        ui.radio(['x', 'y', 'z'], value='x').props('color=red inline ' )
        # inline to align radio buttons horizontally

        ui.button(icon='touch_app').props('outline round').classes('shadow-lg')
        ui.label('props, classes, style').style('color: red; font-size: 150%; font-weight: 400')


    with ui.card():
        ui.label("Tailwind CSS").style(heading_style)

        ui.label('Label A').tailwind.font_weight('extrabold').text_color('blue-600').background_color('orange-200')
        ui.label('Label B').tailwind('drop-shadow', 'font-bold', 'text-green-600')

        red_style = Tailwind().text_color('red-600').font_weight('bold')
        label_c = ui.label('Label C')
        red_style.apply(label_c)

        ui.label('Label D').tailwind(red_style)
        ui.label('Label E').tailwind.font_weight('extrabold').text_color('red-200')

    with ui.card():
        ui.label("Query selector").style(heading_style)

        def set_background(color: str) -> None:
            ui.query('body').style(f'background-color: {color}')

        ui.button('Green', icon='warning', on_click=lambda: set_background('green'))
        ui.button('Black', icon='today', on_click=lambda: set_background('#000'))        
        ui.button('White', icon='format_size', on_click=lambda: set_background('#FFF'))        

    with ui.card():
        ui.label("Switch mode").style(heading_style)

        dark = ui.dark_mode()
        ui.button('Dark', icon='font_download', on_click=dark.enable)
        ui.button('Light', icon='print', on_click=dark.disable)

ui.run()