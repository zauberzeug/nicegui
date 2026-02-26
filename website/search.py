import asyncio

from nicegui import background_tasks, events, ui

from .documentation import CustomRestructuredText as custom_restructured_text
from .documentation.search import search


class Search:

    def __init__(self, window_state: dict) -> None:
        self.window_state = window_state
        with ui.dialog() as self.dialog, ui.card().tight().classes('w-[800px] h-[600px]'):
            with ui.row().classes('w-full items-center px-4'):
                ui.icon('search', size='2em')
                self.input = ui.input(placeholder='Search documentation', on_change=self.handle_input) \
                    .classes('flex-grow').props('borderless autofocus')
                ui.button('ESC', on_click=self.dialog.close) \
                    .props('padding="2px 8px" outline size=sm color=grey-5').classes('shadow')
            ui.separator()
            self.results = ui.element('q-list').classes('w-full').props('separator')
        ui.keyboard().on('key', self.open_dialog, js_handler='''(e) => {
            if (e.action !== 'keydown') return;
            if (e.key === '/' || (e.key === 'k' && (e.ctrlKey || e.metaKey))) {
                emit(e);
                e.event.preventDefault();
            }
        }''')

    def create_button(self) -> ui.button:
        return ui.button(on_click=self.open_dialog, icon='search').props('flat color=white') \
            .tooltip('Press Ctrl+K or / to search the documentation')

    def handle_input(self, e: events.ValueChangeEventArguments) -> None:
        async def handle_input() -> None:
            with self.results:
                limit = 100 if self.window_state.get('is_desktop') else 25
                results = search(e.value, limit=limit)
                self.results.clear()
                with ui.list().props('bordered separator'):
                    for result_item in results:
                        if not result_item['content']:
                            continue
                        with ui.item().props('clickable'):
                            with ui.item_section():
                                with ui.link(target=result_item['url']).on('click', self.dialog.close):
                                    ui.item_label(result_item['title'])
                                    with ui.item_label().props('caption'):
                                        intro = result_item['content'].split(':param')[0]
                                        if result_item['format'] == 'md':
                                            element = ui.markdown(intro)
                                        else:
                                            element = custom_restructured_text(intro)
                                        element.classes('text-grey line-clamp-1')
            await asyncio.sleep(0.2)  # debounce
        background_tasks.create_lazy(handle_input(), name=f'handle_search_input_{ui.context.client.id}')

    def open_dialog(self) -> None:
        self.input.run_method('select')
        self.dialog.open()
