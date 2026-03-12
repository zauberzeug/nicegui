#!/usr/bin/env python3
import random

import httpx

from nicegui import ui


async def show_new_quote():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://zenquotes.io/api/quotes')
        quote = random.choice(response.json())['q']
    label.text = f'“{quote}”'

with ui.card().classes('max-w-md mx-auto mt-20 p-12 gap-12 rounded-2xl shadow-lg border border-gray-100 items-center'):
    label = ui.label('Click on "Next Quote" to get a quote') \
        .classes('text-gray-700 italic text-lg text-center font-serif')

    ui.button('Next Quote', on_click=show_new_quote) \
        .classes('bg-gray-800 hover:bg-gray-900 text-sm px-4 py-2 rounded-xl shadow-md transition duration-200')

ui.run()
