from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    ui.chat_message('Hello NiceGUI!',
                    name='Robot',
                    stamp='now',
                    avatar='https://robohash.org/ui')


def more() -> None:
    @text_demo('HTML text', '''
        Using the `text_html` parameter, you can send HTML text to the chat.
    ''')
    def html_text():
        ui.chat_message('Without <strong>HTML</strong>')
        ui.chat_message('With <strong>HTML</strong>', text_html=True)

    @text_demo('Newline', '''
        You can use newlines in the chat message.
    ''')
    def newline():
        ui.chat_message('This is a\nlong line!')

    @text_demo('Multi-part messages', '''
        You can send multiple message parts by passing a list of strings.
    ''')
    def multiple_messages():
        ui.chat_message(['Hi! 😀', 'How are you?'])
