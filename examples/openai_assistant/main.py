#!/usr/bin/env python3
from openai import AsyncOpenAI
from openai.types.beta.assistant_stream_event import ThreadMessageInProgress
from openai.types.beta.threads import MessageDeltaEvent, TextDeltaBlock

from nicegui import ui

client = AsyncOpenAI(api_key='provide your OpenAI API key here')


@ui.page('/')
async def main():
    assistant = await client.beta.assistants.create(
        name='NiceGUI Assistant',
        instructions='''
            You are a personal assistant for NiceGUI developers.
            Your sole focus is to help with questions about the NiceGUI framework.
            You are precise and concise.
            Stay on the topic.
            Very short answers are preferred, but always be friendly and polite.
        ''',
        tools=[{'type': 'code_interpreter'}],
        model='gpt-4o-mini',
    )

    thread = await client.beta.threads.create()

    async def send() -> None:
        response.content = ''
        spinner = ui.spinner(size='5em', type='comment').classes('mx-auto')
        await client.beta.threads.messages.create(
            thread_id=thread.id,
            role='user',
            content=question.value,
        )
        stream = await client.beta.threads.runs.create(
            assistant_id=assistant.id,
            thread_id=thread.id,
            stream=True,
        )
        async for chunk in stream:
            if isinstance(chunk, ThreadMessageInProgress):
                spinner.delete()
            # NOTE: the stream contains a lot of different types so we need to filter out the ones we don't need
            if not isinstance(chunk.data, MessageDeltaEvent) or not chunk.data.delta.content:
                continue
            content = chunk.data.delta.content[0]
            if not isinstance(content, TextDeltaBlock) or content.text is None or content.text.value is None:
                continue
            response.content += content.text.value

    with ui.column().classes('mx-auto w-full max-w-xl my-16'):
        ui.label('NiceGUI Assistant').classes('text-2xl font-bold mx-auto')
        question = ui.input(value='Why does NiceGUI use async/await?') \
            .classes('w-full self-center mt-4').props('hint="Ask your question" dense') \
            .on('keydown.enter', send)
        response = ui.markdown().classes('mx-4 mt-2')
        ui.timer(0, send, once=True)  # NOTE: we send the prepared demo question immediately

ui.run()
