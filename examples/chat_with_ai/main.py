#!/usr/bin/env python3
from typing import List, Tuple

from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from log_callback_handler import NiceGuiLogElementCallbackHandler

from nicegui import context, ui

OPENAI_API_KEY = 'not-set'  # TODO: set your OpenAI API key here


@ui.page('/')
def main():
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

    ui.add_style(r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}')

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
