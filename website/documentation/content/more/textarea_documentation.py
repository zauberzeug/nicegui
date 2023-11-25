from nicegui import ui

from ...model import UiElementDocumentation


class TextareaDocumentation(UiElementDocumentation, element=ui.textarea):

    def main_demo(self) -> None:
        ui.textarea(label='Text', placeholder='start typing',
                    on_change=lambda e: result.set_text('you typed: ' + e.value))
        result = ui.label()

    def more(self) -> None:
        @self.demo('Clearable', '''
            The `clearable` prop from [Quasar](https://quasar.dev/) adds a button to the input that clears the text.    
        ''')
        def clearable():
            i = ui.textarea(value='some text').props('clearable')
            ui.label().bind_text_from(i, 'value')
