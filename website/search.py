from nicegui import events, ui


class Search:

    def __init__(self) -> None:
        ui.add_head_html(r'''
            <script>
            async function loadSearchData() {
                const response = await fetch("/static/search_index.json");
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
                ui.button('ESC').props('padding="2px 8px" outline size=sm color=grey-5').classes('shadow')
            ui.separator()
            self.results = ui.element('q-list').classes('w-full').props('separator')
        ui.keyboard(self.handle_keypress)

    def create_button(self) -> ui.button:
        return ui.button(on_click=self.dialog.open).props('flat icon=search color=white')

    def handle_keypress(self, e: events.KeyEventArguments) -> None:
        if not e.action.keydown:
            return
        if e.key == '/':
            self.dialog.open()
        if e.key == 'k' and (e.modifiers.ctrl or e.modifiers.meta):
            self.dialog.open()

    async def handle_input(self, e: events.ValueChangeEventArguments) -> None:
        self.results.clear()
        with self.results:
            for result in await ui.run_javascript(f'return window.fuse.search("{e.value}").slice(0, 50)'):
                href: str = result['item']['url']
                with ui.element('q-item').props(f'clickable').on('click', lambda href=href: self.clicked(href)):
                    with ui.element('q-item-section'):
                        ui.label(result['item']['title'])

    async def clicked(self, url: str) -> None:
        await ui.run_javascript(f'''
            const url = "{url}"
            if (url.startsWith("http"))
                window.open(url, "_blank");
            else
                window.location.href = url;
      ''', respond=False)
        self.dialog.close()
        print(url, flush=True)
