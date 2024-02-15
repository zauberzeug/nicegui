#!/usr/bin/env python3
from typing import List, Tuple

from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from log_callback_handler import NiceGuiLogElementCallbackHandler

from nicegui import context, ui

OPENAI_API_KEY = 'not-set'  # TODO: set your OpenAI API key here


@ui.page('/')
def main():
    """
    Entry point function for the chat application.

    This function sets up the chat interface using NiceGUI library and handles user interactions.
    It initializes a ConversationChain object with a ChatOpenAI instance as the language model.
    The messages exchanged between the user and the bot are stored in the `messages` list.
    The `thinking` flag is used to indicate whether the bot is processing a message.

    The function defines a `chat_messages` refreshable function that displays the chat messages
    and the thinking spinner. It also scrolls to the bottom of the chat window if there is a socket connection.

    The `send` async function is called when the user sends a message. It adds the user's message to the `messages`
    list, sets the `thinking` flag to True, clears the input field, and refreshes the chat messages. It then calls
    the `arun` method of the ConversationChain object to generate a response from the bot. The response is added
    to the `messages` list, the `thinking` flag is set to False, and the chat messages are refreshed again.

    The function sets the anchor style for the chat interface and adds it to the head of the HTML document.

    The chat interface is created using NiceGUI tabs. The first tab is for the chat messages and the second tab
    is for the logs. The chat messages are displayed using the `chat_messages` function. The logs are displayed
    using the `log` UI component.

    The function also creates a footer with an input field for the user to enter messages. If the OPENAI_API_KEY
    is not set, a placeholder message is displayed instead. The user can send a message by pressing the Enter key.

    Note: This code assumes that the NiceGUI library and the required dependencies are installed.

    Usage:
    - Ensure that the NiceGUI library and the required dependencies are installed.
    - Set the OPENAI_API_KEY variable with your OpenAI API key.
    - Run the `main` function to start the chat application.
    """
    llm = ConversationChain(llm=ChatOpenAI(model_name='gpt-3.5-turbo', openai_api_key=OPENAI_API_KEY))

    messages: List[Tuple[str, str]] = []
    thinking: bool = False

    @ui.refreshable
    def chat_messages() -> None:
        for name, text in messages:
            ui.chat_message(text=text, name=name, sent=name == 'You')
        if thinking:
            ui.spinner(size='3rem').classes('self-center')
        if context.get_client().has_socket_connection:
            ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')

    async def send() -> None:
        nonlocal thinking
        message = text.value
        messages.append(('You', text.value))
        thinking = True
        text.value = ''
        chat_messages.refresh()

        response = await llm.arun(message, callbacks=[NiceGuiLogElementCallbackHandler(log)])
        messages.append(('Bot', response))
        thinking = False
        chat_messages.refresh()

    anchor_style = r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}'
    ui.add_head_html(f'<style>{anchor_style}</style>')

    # the queries below are used to expand the contend down to the footer (content can then use flex-grow to expand)
    ui.query('.q-page').classes('flex')
    ui.query('.nicegui-content').classes('w-full')

    with ui.tabs().classes('w-full') as tabs:
        chat_tab = ui.tab('Chat')
        logs_tab = ui.tab('Logs')
    with ui.tab_panels(tabs, value=chat_tab).classes('w-full max-w-2xl mx-auto flex-grow items-stretch'):
        with ui.tab_panel(chat_tab).classes('items-stretch'):
            chat_messages()
        with ui.tab_panel(logs_tab):
            log = ui.log().classes('w-full h-full')

    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            placeholder = 'message' if OPENAI_API_KEY != 'not-set' else \
                'Please provide your OPENAI key in the Python script first!'
            text = ui.input(placeholder=placeholder).props('rounded outlined input-class=mx-3') \
                .classes('w-full self-center').on('keydown.enter', send)
        ui.markdown('simple chat app built with [NiceGUI](https://nicegui.io)') \
            .classes('text-xs self-end mr-8 m-[-1em] text-primary')


ui.run(title='Chat with GPT-3 (example)')
