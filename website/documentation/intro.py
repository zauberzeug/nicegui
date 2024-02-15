from typing import Callable

from nicegui import ui

from ..style import subheading
from .demo import demo


def create_intro() -> None:
    """
    Creates the introduction section of the NiceGUI documentation website.

    This function defines three demo functions: formatting_demo, common_elements_demo, and binding_demo.
    Each demo function showcases different features and functionalities of NiceGUI.

    The formatting_demo function demonstrates how to modify the look of an app using CSS, Tailwind, and Quasar classes.
    It displays an icon, Markdown text, HTML code, and labels styled with CSS, Tailwind, and Quasar classes.
    It also includes a link to the NiceGUI GitHub repository.

    The common_elements_demo function showcases a collection of commonly used UI elements provided by NiceGUI.
    It includes a button, checkbox, switch, radio buttons, text input, select dropdown, and a link to more elements.

    The binding_demo function demonstrates how to bind values between UI elements and data models in NiceGUI.
    It creates a Demo class with a number attribute and showcases how to bind the visibility of UI elements to a checkbox value.
    It also demonstrates binding the value of a slider, toggle, and number input to the number attribute of the Demo class.

    This function does not return any value.
    """
    @_main_page_demo('Styling', '''
        While having reasonable defaults, you can still modify the look of your app with CSS as well as Tailwind and Quasar classes.
    ''')
    def formatting_demo():
        ui.icon('thumb_up')
        ui.markdown('This is **Markdown**.')
        ui.html('This is <strong>HTML</strong>.')
        with ui.row():
            ui.label('CSS').style('color: #888; font-weight: bold')
            ui.label('Tailwind').classes('font-serif')
            ui.label('Quasar').classes('q-ml-xl')
        ui.link('NiceGUI on GitHub', 'https://github.com/zauberzeug/nicegui')

    @_main_page_demo('Common UI Elements', '''
        NiceGUI comes with a collection of commonly used UI elements.
    ''')
    def common_elements_demo():
        from nicegui.events import ValueChangeEventArguments

        def show(event: ValueChangeEventArguments):
            name = type(event.sender).__name__
            ui.notify(f'{name}: {event.value}')

        ui.button('Button', on_click=lambda: ui.notify('Click'))
        with ui.row():
            ui.checkbox('Checkbox', on_change=show)
            ui.switch('Switch', on_change=show)
        ui.radio(['A', 'B', 'C'], value='A', on_change=show).props('inline')
        with ui.row():
            ui.input('Text input', on_change=show)
            ui.select(['One', 'Two'], value='One', on_change=show)
        ui.link('And many more...', '/documentation').classes('mt-8')

    @_main_page_demo('Value Binding', '''
        Binding values between UI elements and data models is built into NiceGUI.
    ''')
    def binding_demo():
        class Demo:
            def __init__(self):
                self.number = 1

        demo = Demo()
        v = ui.checkbox('visible', value=True)
        with ui.column().bind_visibility_from(v, 'value'):
            ui.slider(min=1, max=3).bind_value(demo, 'number')
            ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')
            ui.number().bind_value(demo, 'number')


def _main_page_demo(title: str, explanation: str) -> Callable:
    """
    Decorator function for creating a main page demo.

    This decorator function is used to create a main page demo by providing a title and an explanation.
    It returns a decorator that can be applied to a function.

    Parameters:
    - title (str): The title of the main page demo.
    - explanation (str): The explanation of the main page demo.

    Returns:
    - Callable: A decorator function that can be applied to a function.

    Example usage:
    ```
    @_main_page_demo("My Demo", "This is a demo of my code.")
    def my_demo_function():
        # Code for the demo
        pass
    ```
    """
    def decorator(f: Callable) -> Callable:
        subheading(title)
        ui.markdown(explanation).classes('bold-links arrow-links')
        return demo(f)
    return decorator
