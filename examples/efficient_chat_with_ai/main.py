#!/usr/bin/env python3
from typing import List, Tuple

from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from nicegui import context, ui
OPENAI_API_KEY = 'not-set'  # TODO: set your OpenAI API key here


class CustomChatMessage:
    def __init__(self, cls):
        self.pointer = 0
        self.last_message = None
        self.spinner = None
        self.cls = cls

    def chat(self, name, text):
        with self.container:
            self.last_message = ui.chat_message(text=text, name=name, sent=name == 'You')
            self.spinner = ui.spinner(size='3rem').classes('self-center')
            self.spinner.bind_visibility_from(self.cls, "thinking")
            ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')

    def add_container(self, container):
        self.container = container

    def refresh(self, messeges):
        if len(messeges):
            name, text = messeges[-1]
            if self.spinner:
                self.spinner.delete()
            if len(messeges) > self.pointer:
                self.chat(name, text)
                self.pointer += 1
            else:
                if self.last_message:
                    self.last_message.delete()
                self.chat(name, text)

class Page:
    def __init__(self) -> None:
        self.llm=ChatOpenAI(model_name='gpt-3.5-turbo', openai_api_key=OPENAI_API_KEY)
        self.messages: List[Tuple[str, str]] = []
        self.thinking: bool = False
        self.chat_messages = CustomChatMessage(self)
    
    async def send(self) -> None:
        message = self.text.value
        self.messages.append(['You', self.text.value])
        self.thinking = True
        self.text.value = ''
        self.chat_messages.refresh(self.messages)
        self.messages.append(['Bot', ""])
        async for chunk in self.llm.astream(message):
            self.messages[-1][-1] += chunk.content
            self.thinking = False
            self.chat_messages.refresh(self.messages)
    
    def main(self):
        anchor_style = r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}'
        ui.add_head_html(f'<style>{anchor_style}</style>')

        # the queries below are used to expand the contend down to the footer (content can then use flex-grow to expand)
        ui.query('.q-page').classes('flex')
        ui.query('.nicegui-content').classes('w-full')

        with ui.tabs().classes('w-full') as tabs:
            chat_tab = ui.tab('Chat')
        with ui.tab_panels(tabs, value=chat_tab).classes('w-full max-w-2xl mx-auto flex-grow items-stretch'):
            container = ui.tab_panel(chat_tab).classes('items-stretch')
            self.chat_messages.add_container(container)

        with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
            with ui.row().classes('w-full no-wrap items-center'):
                placeholder = 'message' if OPENAI_API_KEY != 'not-set' else \
                    'Please provide your OPENAI key in the Python script first!'
                self.text = ui.input(placeholder=placeholder).props('rounded outlined input-class=mx-3') \
                    .classes('w-full self-center').on('keydown.enter', self.send)
            ui.markdown('simple chat app built with [NiceGUI](https://nicegui.io)') \
                .classes('text-xs self-end mr-8 m-[-1em] text-primary')

@ui.page('/')
def main():
    Page().main()


ui.run(title='Chat with GPT-3 (example)', reload=False)