#!/usr/bin/env python3
from langchain_google_genai import ChatGoogleGenerativeAI

from nicegui import ui

GOOGLE_API_KEY = 'not-set'  # TODO: set your GEMINI API key here


@ui.page('/')
def main():
    llm = ChatGoogleGenerativeAI(
        api_key=GOOGLE_API_KEY, model="gemini-2.5-flash", temperature=0, max_retries=10
    )


    async def send() -> None:
        question = text.value
        text.value = ''

        with message_container:
            ui.chat_message(text=question, name='You', sent=True)
            response_message = ui.chat_message(name='Bot', sent=False)
            spinner = ui.spinner(type='dots')

        data = {'response': ''}
        async for chunk in llm.astream(question):
            data['response'] += chunk.content
            response_message.clear()
            with response_message:
                ui.markdown().bind_content(data, 'response')
            ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        message_container.remove(spinner)

    ui.add_css(r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}')

    # the queries below are used to expand the contend down to the footer (content can then use flex-grow to expand)
    ui.query('.q-page').classes('flex')
    ui.query('.nicegui-content').classes('w-full')

    with ui.tabs().classes('w-full') as tabs:
        chat_tab = ui.tab('Chat')
    with ui.tab_panels(tabs, value=chat_tab).classes('w-full max-w-2xl mx-auto flex-grow items-stretch'):
        message_container = ui.tab_panel(chat_tab).classes('items-stretch')

    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            placeholder = 'message' if GOOGLE_API_KEY != 'not-set' else \
                'Please provide your Gemini key in the Python script first!'
            text = ui.input(placeholder=placeholder).props('rounded outlined input-class=mx-3') \
                .classes('w-full self-center').on('keydown.enter', send)
        ui.markdown('simple chat app built with [NiceGUI](https://nicegui.io)') \
            .classes('text-xs self-end mr-8 m-[-1em] text-primary')


ui.run(title='Chat with Gemini (example)')
