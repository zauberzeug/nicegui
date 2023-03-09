#!/usr/bin/env python3
import asyncio
from typing import Optional

import httpx

from nicegui import events, ui
from nicegui.page import page


class Search:
    def __init__(self, results: ui.row):
        self.results = results
        self.search_field = ui.input(on_change=self.search) \
            .props('autofocus outlined rounded item-aligned input-class="ml-3"') \
            .classes('w-96 self-center mt-24 transition-all')
        self.api = httpx.AsyncClient()
        self.running_query: Optional[asyncio.Task] = None

    async def search(self, e: events.ValueChangeEventArguments) -> None:
        """Search for cocktails as you type."""
        if self.running_query:
            self.running_query.cancel()  # cancel the previous query; happens when you type fast
        self.search_field.classes('mt-2', remove='mt-24')  # move the search field up
        self.results.clear()
        # store the http coroutine in a task, so we can cancel it later if needed
        self.running_query = asyncio.create_task(
            self.api.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={e.value}'))
        response = await self.running_query
        if response.text == '':
            return
        with self.results:  # enter the context of the results row
            for drink in response.json()['drinks'] or []:  # iterate over the response data of the api
                with ui.image(drink['strDrinkThumb']).classes('w-64'):
                    ui.label(drink['strDrink']).classes('absolute-bottom text-subtitle2 text-center')
        self.running_query = None


@page("/")
async def my_page():
    results = ui.row()
    Search(results)


if __name__ in {"__main__", "__mp_main__"}:
    ui.run()
