"""NiceGUI Pyodide Demo - runs entirely in the browser via PyScript."""
from nicegui import Client, binding, ui
from nicegui.page_pyodide import page

# ── Page builders ─────────────────────────────────────────────────────


def page_home():
    ui.label('This app runs entirely in your browser — no server needed.').classes('text-gray-500')
    with ui.card().classes('w-full'):
        ui.label('Navigate using the links above to explore each demo section.')


def page_basics():
    # Counter with binding
    with ui.card().classes('w-full'):
        ui.label('Counter with data binding').classes('text-lg font-semibold')

        @binding.bindable_dataclass
        class Counter:
            count: int = 0
        counter = Counter()

        ui.label().bind_text_from(counter, 'count', lambda n: f'Count: {n}')
        with ui.row():
            ui.button('-', on_click=lambda: setattr(counter, 'count', counter.count - 1))
            ui.button('+', on_click=lambda: setattr(counter, 'count', counter.count + 1))

    # Timer
    with ui.card().classes('w-full'):
        ui.label('Live timer').classes('text-lg font-semibold')
        elapsed = {'s': 0}
        timer_label = ui.label('Elapsed: 0s')

        def tick():
            elapsed['s'] += 1
            timer_label.text = f'Elapsed: {elapsed["s"]}s'

        ui.timer(1.0, tick)

    # run_javascript
    with ui.card().classes('w-full'):
        ui.label('run_javascript (await)').classes('text-lg font-semibold')
        js_result = ui.label('Result: ...')

        async def eval_js():
            result = await ui.run_javascript('navigator.userAgent')
            js_result.text = f'Result: {result[:80]}...'

        ui.button('Get user agent', on_click=eval_js)

    # Notification
    with ui.card().classes('w-full'):
        ui.label('Notifications').classes('text-lg font-semibold')
        ui.button('Show notification', on_click=lambda: ui.notify('Hello from Pyodide!'))

    # Async background task
    with ui.card().classes('w-full'):
        ui.label('Async task').classes('text-lg font-semibold')
        async_result = ui.label('Async: not started')

        async def run_async_task():
            import asyncio
            async_result.text = 'Async: running...'
            await asyncio.sleep(1)
            async_result.text = 'Async: done!'

        ui.button('Run async task', on_click=run_async_task)

    # Refreshable
    with ui.card().classes('w-full'):
        ui.label('ui.refreshable').classes('text-lg font-semibold')
        color_idx = {'i': 0}
        colors = ['red', 'green', 'blue', 'orange', 'purple']

        @ui.refreshable
        def color_display():
            c = colors[color_idx['i'] % len(colors)]
            ui.label(c).classes(f'text-{c}-500 text-xl font-bold')

        color_display()

        def next_color():
            color_idx['i'] += 1
            color_display.refresh()

        ui.button('Next color', on_click=next_color)


def page_forms():
    # Basic form elements
    with ui.card().classes('w-full'):
        ui.label('Form elements').classes('text-lg font-semibold')
        form_result = ui.label('Form: ...')

        name_input = ui.input('Name', value='World')
        slider = ui.slider(min=0, max=100, value=50)
        checkbox = ui.checkbox('Agree to terms')
        select = ui.select(['Option A', 'Option B', 'Option C'], value='Option A', label='Pick one')

        def update_form_result():
            form_result.text = (
                f'Form: name={name_input.value!r}, '
                f'slider={slider.value}, '
                f'check={checkbox.value}, '
                f'select={select.value!r}'
            )

        ui.button('Show form values', on_click=update_form_result)

    # Extra form elements
    with ui.card().classes('w-full'):
        ui.label('Textarea / Number / Switch / Radio / Toggle').classes('text-lg font-semibold')
        extra_form_result = ui.label('Extra form: ...')

        textarea = ui.textarea('Notes', value='Hello')
        number_input = ui.number('Pick a number', value=42, min=0, max=100)
        switch = ui.switch('Dark mode')
        radio = ui.radio(['X', 'Y', 'Z'], value='X')
        toggle = ui.toggle(['One', 'Two', 'Three'], value='One')

        def show_extra_form():
            extra_form_result.text = (
                f'Extra form: textarea={textarea.value!r}, '
                f'number={number_input.value}, '
                f'switch={switch.value}, '
                f'radio={radio.value!r}, '
                f'toggle={toggle.value!r}'
            )

        ui.button('Show extra form values', on_click=show_extra_form)


def page_content():
    # Markdown
    with ui.card().classes('w-full'):
        ui.label('Markdown').classes('text-lg font-semibold')
        ui.markdown('''
**Bold** and *italic* text.

```python
def hello():
    print("Hello from Pyodide!")
```

- Item 1
- Item 2
        ''')

    # Table
    with ui.card().classes('w-full'):
        ui.label('Table').classes('text-lg font-semibold')
        ui.table(
            columns=[
                {'name': 'name', 'label': 'Name', 'field': 'name'},
                {'name': 'age', 'label': 'Age', 'field': 'age'},
            ],
            rows=[
                {'name': 'Alice', 'age': 30},
                {'name': 'Bob', 'age': 25},
                {'name': 'Carol', 'age': 35},
            ],
        )

    # Tabs
    with ui.card().classes('w-full'):
        ui.label('Tabs').classes('text-lg font-semibold')
        tab_result = ui.label('Tab: none')
        with ui.tabs() as tabs:
            tab_a = ui.tab('Tab A')
            tab_b = ui.tab('Tab B')
        with ui.tab_panels(tabs, value=tab_a):
            with ui.tab_panel(tab_a):
                ui.label('Content of Tab A')
            with ui.tab_panel(tab_b):
                ui.label('Content of Tab B')
        tabs.on_value_change(lambda e: setattr(tab_result, 'text', f'Tab: {e.value}'))

    # Dialog
    with ui.card().classes('w-full'):
        ui.label('Dialog').classes('text-lg font-semibold')
        dialog_result = ui.label('Dialog: not opened yet')

        with ui.dialog() as dialog:
            with ui.card():
                ui.label('Hello from dialog!')
                ui.button('Close', on_click=dialog.close)

        def open_dialog():
            dialog_result.text = 'Dialog: opened'
            dialog.open()

        ui.button('Open dialog', on_click=open_dialog)

    # Expansion / Tooltip / Badge
    with ui.card().classes('w-full'):
        ui.label('Expansion / Tooltip / Badge').classes('text-lg font-semibold')
        with ui.expansion('Click to expand', icon='info'):
            ui.label('Hidden content revealed!')
        with ui.row():
            ui.button('Hover me').tooltip('Tooltip text here')
            ui.badge('3', color='red')

    # Image
    with ui.card().classes('w-full'):
        ui.label('Image (data URI)').classes('text-lg font-semibold')
        # 1x1 red PNG as base64 data URI
        ui.image('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==').classes('w-16 h-16')

    # Mermaid diagram (ESM element)
    with ui.card().classes('w-full'):
        ui.label('Mermaid diagram (ESM)').classes('text-lg font-semibold')
        mermaid_click_label = ui.label('Click a node...')

        def on_node_click(e):
            mermaid_click_label.text = f'Clicked: {e.node_id}'

        ui.mermaid('''
        graph LR
            A[Browser] --> B[Pyodide/WASM]
            B --> C[NiceGUI Python]
            C --> D[Vue.js UI]
        ''', on_node_click=on_node_click)


def page_io():
    # Download
    with ui.card().classes('w-full'):
        ui.label('File download (bytes)').classes('text-lg font-semibold')

        def do_download():
            ui.download(b'Hello from NiceGUI Pyodide!\n', 'hello.txt', 'text/plain')

        ui.button('Download hello.txt', on_click=do_download)

    # Upload
    with ui.card().classes('w-full'):
        ui.label('File upload').classes('text-lg font-semibold')
        upload_info = ui.label('No file uploaded yet')

        async def handle_upload(e):
            data = await e.file.read()
            upload_info.text = f'Received "{e.file.name}" ({len(data)} bytes)'

        ui.upload(on_upload=handle_upload, auto_upload=True).classes('w-full')


# ── Build the UI ──────────────────────────────────────────────────────

with Client(page('')) as client:
    dark = ui.dark_mode(False)

    with ui.row().classes('w-full max-w-lg items-center'):
        ui.label('NiceGUI + Pyodide').classes('text-3xl font-bold')
        ui.space()
        ui.button(icon='dark_mode', on_click=dark.toggle).props('flat round')

    with ui.row().classes('w-full max-w-lg gap-4'):
        ui.link('Home', '/').classes('text-blue-500')
        ui.link('Basics', '/basics').classes('text-blue-500')
        ui.link('Forms', '/forms').classes('text-blue-500')
        ui.link('Content', '/content').classes('text-blue-500')
        ui.link('I/O', '/io').classes('text-blue-500')

    ui.separator()

    with ui.column().classes('w-full max-w-lg'):
        ui.sub_pages({
            '/': page_home,
            '/basics': page_basics,
            '/forms': page_forms,
            '/content': page_content,
            '/io': page_io,
        })
