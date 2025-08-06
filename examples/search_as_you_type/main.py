#!/usr/bin/env python3
import asyncio
from typing import Optional

import httpx

from nicegui import events, ui

api = httpx.AsyncClient()
running_query: Optional[asyncio.Task] = None


async def search(e: events.ValueChangeEventArguments) -> None:
    """Search for cocktails as you type."""
    global running_query  # pylint: disable=global-statement # noqa: PLW0603
    if running_query:
        running_query.cancel()  # cancel the previous query; happens when you type fast
    search_field.classes('mt-2', remove='mt-24')  # move the search field up
    results.clear()
    # store the http coroutine in a task so we can cancel it later if needed
    running_query = asyncio.create_task(api.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={e.value}'))
    response = await running_query
    if response.text == '':
        return
    with results:  # enter the context of the results row
        for drink in response.json()['drinks'] or []:  # iterate over the response data of the api
            with ui.image(drink['strDrinkThumb']).classes('w-64'):
                ui.label(drink['strDrink']).classes('absolute-bottom text-subtitle2 text-center')
    running_query = None

# create a search field which is initially focused and leaves space at the top
search_field = ui.input(on_change=search) \
    .props('autofocus outlined rounded item-aligned input-class="ml-3"') \
    .classes('w-96 self-center mt-24 transition-all')
results = ui.row()

ui.run()
