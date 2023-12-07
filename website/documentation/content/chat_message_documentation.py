from nicegui import ui

from . import doc


@doc.demo(ui.chat_message)
def main_demo() -> None:
    ui.chat_message('Hello NiceGUI!',
                    name='Robot',
                    stamp='now',
                    avatar='https://robohash.org/ui')


@doc.demo('HTML text', '''
    Using the `text_html` parameter, you can send HTML text to the chat.
''')
def html_text():
    ui.chat_message('Without <strong>HTML</strong>')
    ui.chat_message('With <strong>HTML</strong>', text_html=True)


@doc.demo('Newline', '''
    You can use newlines in the chat message.
''')
def newline():
    ui.chat_message('This is a\nlong line!')


@doc.demo('Multi-part messages', '''
    You can send multiple message parts by passing a list of strings.
''')
def multiple_messages():
    ui.chat_message(['Hi! 😀', 'How are you?']
                    )


@doc.demo('Chat message with child elements', '''
    You can add child elements to a chat message.
''')
def child_elements():
    with ui.chat_message():
        ui.label('Guess where I am!')
        ui.image('https://picsum.photos/id/249/640/360').classes('w-64')


doc.reference(ui.chat_message)
