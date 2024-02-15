#!/usr/bin/env python3
import asyncio
from typing import Optional

import httpx

from nicegui import events, ui

api = httpx.AsyncClient()
running_query: Optional[asyncio.Task] = None


async def search(e: events.ValueChangeEventArguments) -> None:
    '''
    Search for cocktails as you type.

    This function is responsible for performing a search for cocktails based on the user's input. It utilizes an API to retrieve the search results and displays them in a graphical user interface.

    Parameters:
    - e (events.ValueChangeEventArguments): The event arguments containing the value of the search input.

    Returns:
    - None

    Usage:
    - Call this function when the user types in the search field to initiate a search for cocktails. The search results will be displayed in the graphical user interface.
    '''
    global running_query
    if running_query:
        running_query.cancel()  # cancel the previous query; happens when you type fast
    search_field.classes('mt-2', remove='mt-24')  # move the search field up
    results.clear()
    # store the http coroutine in a task so we can cancel it later if needed
    running_query = asyncio.create_task(api.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={e.value}'))
    response = await running_query
    if response.text == '':
        return
    with results:  # enter the context of the the results row
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
