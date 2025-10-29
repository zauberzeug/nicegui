from nicegui import __version__, background_tasks, events, ui

from .documentation import CustomRestructuredText as custom_restructured_text
from .documentation.search import search_index


class Search:

    def __init__(self) -> None:
        ui.add_head_html(r'''
            <script>
            async function loadSearchData() {
                const response = await fetch("/static/search_index.json?version=''' + __version__ + r'''");
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const searchData = await response.json();
                const options = {
                    keys: [
                        { name: "title", weight: 0.7 },
                        { name: "content", weight: 0.3 },
                    ],
                    tokenize: true, // each word is ranked individually
                    threshold: 0.3,
                    location: 0,
                    distance: 10000,
                };
                window.fuse = new Fuse(searchData, options);
            }
            loadSearchData();
            </script>
        ''')
        with ui.dialog() as self.dialog, ui.card().tight().classes('w-[800px] h-[600px]'):
            with ui.row().classes('w-full items-center px-4'):
                ui.icon('search', size='2em')
                ui.input(placeholder='Search documentation', on_change=self.handle_input) \
                    .classes('flex-grow').props('borderless autofocus')
                ui.button('ESC', on_click=self.dialog.close) \
                    .props('padding="2px 8px" outline size=sm color=grey-5').classes('shadow')
            ui.separator()
            self.results = ui.element('q-list').classes('w-full').props('separator')
        ui.keyboard().on('key', self.dialog.open, js_handler='''(e) => {
            if (e.action !== 'keydown') return;
            if (e.key === '/' || (e.key === 'k' && (e.ctrlKey || e.metaKey))) {
                emit(e);
                e.event.preventDefault();
            }
        }''')

    def create_button(self) -> ui.button:
        return ui.button(on_click=self.dialog.open, icon='search').props('flat color=white') \
            .tooltip('Press Ctrl+K or / to search the documentation')

    def handle_input(self, e: events.ValueChangeEventArguments) -> None:
        async def handle_input() -> None:
            with self.results:
                indices = await ui.run_javascript(f'''
                    const isMobile = window.innerWidth < 610;
                    const limit = isMobile ? 25 : 100;
                    return window.fuse.search("{e.value}", {{ limit }}).map(result => result.refIndex);
                ''', timeout=6)
                self.results.clear()
                with ui.list().props('bordered separator'):
                    for index in indices:
                        if not 0 <= index < len(search_index):
                            continue
                        result_item = search_index[index]
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
        background_tasks.create_lazy(handle_input(), name='handle_search_input')
