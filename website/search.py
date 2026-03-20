from nicegui import __version__, background_tasks, events, ui

from . import design as d
from .documentation import CustomRestructuredText as custom_restructured_text
from .documentation.search import search_index
from .utils import phosphor_icon


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
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', loadSearchData);
            } else {
                loadSearchData();
            }
            </script>
        ''')
        with ui.dialog() as self.dialog, ui.card().tight().classes(f'w-[800px] h-[600px] {d.BG_SURFACE} {d.BORDER}'):
            with ui.row().classes(f'w-full items-center gap-3 px-4 py-3 {d.BORDER_B}'):
                phosphor_icon('ph-magnifying-glass').classes(f'text-xl {d.TEXT_MUTED}')
                self.input = ui.input(placeholder='Search documentation', on_change=self._handle_input) \
                    .classes('flex-grow').props('borderless autofocus')
                ui.button('ESC', on_click=self.dialog.close) \
                    .props('padding="2px 8px" outline size=sm').classes(f'shadow {d.TEXT_MUTED}')
            self.results = ui.element('q-list').classes('w-full overflow-auto').props('separator')
        ui.keyboard().on('key', self.open_dialog, js_handler='''(e) => {
            if (e.action !== 'keydown') return;
            if (e.key === '/' || (e.key === 'k' && (e.ctrlKey || e.metaKey))) {
                emit(e);
                e.event.preventDefault();
            }
        }''')

    def _handle_input(self, e: events.ValueChangeEventArguments) -> None:
        async def handle_input() -> None:
            with self.results:
                indices = await ui.run_javascript(f'''
                    const isMobile = window.innerWidth < 610;
                    const limit = isMobile ? 25 : 100;
                    return window.fuse.search("{e.value}", {{ limit }}).map(result => result.refIndex);
                ''', timeout=6)
                self.results.clear()
                for index in indices:
                    if not 0 <= index < len(search_index):
                        continue
                    result_item = search_index[index]
                    if not result_item['content']:
                        continue
                    with ui.link(target=result_item['url']).on('click', self.dialog.close) \
                            .classes(f'block px-4 py-3 no-underline {d.BORDER_B} hover:opacity-80'):
                        ui.label(result_item['title']).classes('font-medium')
                        intro = result_item['content'].split(':param')[0]
                        if result_item['format'] == 'md':
                            element = ui.markdown(intro)
                        else:
                            element = custom_restructured_text(intro)
                        element.classes(f'line-clamp-1 {d.TEXT_MUTED}')
        background_tasks.create_lazy(handle_input(), name='handle_search_input')

    def open_dialog(self) -> None:
        self.input.run_method('select')
        self.dialog.open()
