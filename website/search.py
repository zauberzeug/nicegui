from nicegui import __version__, background_tasks, events, ui


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
        ui.keyboard(self.handle_keypress)

    def create_button(self) -> ui.button:
        return ui.button(on_click=self.dialog.open, icon='search').props('flat color=white') \
            .tooltip('Press Ctrl+K or / to search the documentation')

    def handle_keypress(self, e: events.KeyEventArguments) -> None:
        if not e.action.keydown:
            return
        if e.key == '/':
            self.dialog.open()
        if e.key == 'k' and (e.modifiers.ctrl or e.modifiers.meta):
            self.dialog.open()

    def handle_input(self, e: events.ValueChangeEventArguments) -> None:
        async def handle_input() -> None:
            with self.results:
                results = await ui.run_javascript(f'return window.fuse.search("{e.value}").slice(0, 100)', timeout=6)
                self.results.clear()
                with ui.list().props('bordered separator'):
                    for result in results:
                        if not result['item']['content']:
                            continue
                        with ui.item().props('clickable'):
                            with ui.item_section():
                                with ui.link(target=result['item']['url']):
                                    ui.item_label(result['item']['title'])
                                    with ui.item_label().props('caption'):
                                        intro = result['item']['content'].split(':param')[0]
                                        if result['item']['format'] == 'md':
                                            element = ui.markdown(intro)
                                        else:
                                            element = ui.restructured_text(intro)
                                        element.classes('text-grey line-clamp-1')
        background_tasks.create_lazy(handle_input(), name='handle_search_input')

    def open_url(self, url: str) -> None:
        ui.run_javascript(f'''
            const url = "{url}"
            if (url.startsWith("http"))
                window.open(url, "_blank");
            else
                window.location.href = url;
        ''')
        self.dialog.close()
