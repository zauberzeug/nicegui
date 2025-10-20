#!/usr/bin/env python3
from html_sanitizer import Sanitizer
from langchain_openai import ChatOpenAI

from nicegui import ui

OPENAI_API_KEY = 'not-set'  # TODO: set your OpenAI API key here


def root():
    llm = ChatOpenAI(model_name='gpt-4o-mini', streaming=True, openai_api_key=OPENAI_API_KEY)

    async def send() -> None:
        question = text.value
        text.value = ''

        with message_container:
            ui.chat_message(text=question, name='You', sent=True)
            response_message = ui.chat_message(name='Bot', sent=False)
            spinner = ui.spinner(type='dots')

        response = ''
        async for chunk in llm.astream(question):
            response += chunk.content
            response_message.clear()
            with response_message:
                ui.html(response, sanitize=Sanitizer().sanitize)
            ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        message_container.remove(spinner)

    message_container = ui.column().classes('w-full max-w-2xl mx-auto flex-grow items-stretch')

    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            placeholder = 'message' if OPENAI_API_KEY != 'not-set' else \
                'Please provide your OPENAI key in the Python script first!'
            text = ui.input(placeholder=placeholder).props('rounded outlined input-class=mx-3') \
                .classes('w-full self-center').on('keydown.enter', send)
        ui.markdown('simple chat app built with [NiceGUI](https://nicegui.io)') \
            .classes('text-xs self-end mr-8 m-[-1em] text-primary') \
            .classes('[&_a]:text-inherit [&_a]:no-underline [&_a]:font-medium')


ui.run(root, title='Chat with GPT-4o-mini')
