#!/usr/bin/env python3
import asyncio
from typing import Optional

import httpx

from nicegui import events, ui
from nicegui.page import page


class Results:
    """
    Component class to pass references to NiceGUI objects
    but build them explicitly when needed
    """
    def __init__(self, ui_row):
        self._row = ui_row
        self.row: Optional[ui.row] = None

    def build(self):
        self.row = self._row()


class Search:
    """
    Component class to receive other Components (like Result class above)
    to operate on them, but not bind UI building when initialized
    """
    def __init__(self, results: Results):
        self.results = results
        self.search_field = None
        self.api = httpx.AsyncClient()
        self.running_query: Optional[asyncio.Task] = None

    def build(self):
        self.search_field = ui.input(on_change=self.search) \
            .props('autofocus outlined rounded item-aligned input-class="ml-3"') \
            .classes('w-96 self-center mt-24 transition-all')

    async def search(self, e: events.ValueChangeEventArguments) -> None:
        """Search for cocktails as you type."""
        if self.running_query:
            self.running_query.cancel()  # cancel the previous query; happens when you type fast
        self.search_field.classes('mt-2', remove='mt-24')  # move the search field up
        self.results.row.clear()
        # store the http coroutine in a task, so we can cancel it later if needed
        self.running_query = asyncio.create_task(
            self.api.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={e.value}'))
        response = await self.running_query
        if response.text == '':
            return
        with self.results.row:  # enter the context of the results row
            for drink in response.json()['drinks'] or []:  # iterate over the response data of the api
                with ui.image(drink['strDrinkThumb']).classes('w-64'):
                    ui.label(drink['strDrink']).classes('absolute-bottom text-subtitle2 text-center')
        self.running_query = None


@page("/")
async def my_page():
    # initialization of objects (for future reference) but not creating ui itself inplace
    results = Results(ui.row)
    search = Search(results)
    # actual UI building
    with ui.row().classes("fit"):
        with ui.column().classes("col"):
            search.build()  # invoke build method to actually create wanted component
        with ui.column().classes("col"):
            results.build()


if __name__ in {"__main__", "__mp_main__"}:
    ui.run()
