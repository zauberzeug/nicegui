#!/usr/bin/env python3
from openai import AsyncOpenAI

from nicegui import ui

client = AsyncOpenAI(api_key='provide your OpenAI API key here')


async def root():
    messages = []

    async def send() -> None:
        messages.append({'role': 'user', 'content': question.value})

        response.content = ''
        spinner = ui.spinner(size='5em', type='comment').classes('mx-auto')

        stream = await client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {
                    'role': 'system',
                    'content': '''
                        You are a personal assistant for NiceGUI developers.
                        Your sole focus is to help with questions about the NiceGUI framework.
                        You are precise and concise.
                        Stay on the topic.
                        Very short answers are preferred, but always be friendly and polite.
                    ''',
                },
                *messages,
            ],
            stream=True,
        )

        spinner.delete()
        assistant_message = ''

        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                assistant_message += content
                response.content += content

        messages.append({'role': 'assistant', 'content': assistant_message})

    with ui.column().classes('mx-auto w-full max-w-xl my-16'):
        ui.label('NiceGUI Assistant').classes('text-2xl font-bold mx-auto')
        question = ui.input(value='Why does NiceGUI use async/await?') \
            .classes('w-full self-center mt-4').props('hint="Ask your question" dense') \
            .on('keydown.enter', send)
        response = ui.markdown().classes('mx-4 mt-2')
        ui.timer(0, send, once=True)  # NOTE: we send the prepared demo question immediately

ui.run(root=root)
