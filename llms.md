# NiceGUI – LLM Reference

> Concise, opinionated guide for AI assistants working with NiceGUI.
> The single most important rule: **everything is Python**. Reach for `ui.*` before CSS, Quasar, or JavaScript.

---

## Architecture

- **Backend-first**: All UI logic lives in Python. The framework handles web details automatically.
- **Stack**: Python/FastAPI backend → WebSocket (socket.io) → Vue 3 / Quasar frontend
- **Single worker**: One uvicorn worker with full async support; no multiprocessing needed.
- **Outbox**: UI updates are accumulated and sent in batches to the client over the persistent WebSocket.
- **Element lifecycle**: Python `Element` objects mirror Vue components on the client. Creating an element registers it immediately; calling `.update()` pushes changes.

---

## Mental Models — The "Why" Behind NiceGUI

Understanding these mental models prevents the most common LLM mistakes. They explain *why* the API is shaped the way it is.

### 1. There is no virtual DOM — understand what "rebuilding" costs

React and similar frameworks diff a virtual DOM and patch only what changed. NiceGUI has no such diffing. When you delete and recreate elements, NiceGUI literally destroys Vue components on the client and creates new ones. This means:

- Rebuilding a subtree loses focus, scroll position, animation state, and any client-side state
- Use `@ui.refreshable` for sections that need to update — it handles clearing and rebuilding safely
- For simple value changes, update **in place** via bindings or `.set_text()` / `.set_value()` instead of recreating elements

```python
# BAD: destroys and recreates on every data change
def show_count():
    container.clear()
    ui.label(f'Count: {count}')

# GOOD: updates the existing element in place
label = ui.label('Count: 0')
# then: label.set_text(f'Count: {count}') or bind_text_from
```

### 2. Module-level state is shared across ALL users

NiceGUI runs as a single Python process. Module-level variables are shared between every connected browser tab and every user. This is the most common source of subtle multi-user bugs:

```python
# BUG: all users see the same data, last writer wins
items = []

@ui.page('/')
def index():
    ui.button('Add', on_click=lambda: items.append('x'))  # shared!
    ui.label(str(items))

# CORRECT: per-user state in app.storage or local variables inside @ui.page
@ui.page('/')
def index():
    items = []  # local to this page invocation = per user
    # or: app.storage.user['items'] for persistence across reloads
```

### 3. `@ui.page` creates a new Python scope per visitor — but only once per page load

Each time a user navigates to a `@ui.page` route, the decorated function runs exactly once, building the page. It is **not** called again on state changes. All subsequent UI updates happen through:
- Bindings (automatic)
- `@ui.refreshable` (explicit rebuild of a subtree)
- Direct element mutation (`.set_text()`, `.visible = False`, etc.)
- Timers

Understanding this prevents the mistake of trying to "re-run the page function" to update the UI.

### 4. The slot stack — why context managers place elements automatically

When you write `with ui.row(): ui.label('x')`, the label automatically becomes a child of the row. This works via a thread-local slot stack:

- `with element:` pushes the element's default slot onto the stack
- Any element created inside the `with` block is registered as a child of that slot
- `__exit__` pops the slot off the stack

Consequence: **element creation order matters**, and you cannot place an element in a different parent after creation. If you need to move elements, delete and recreate them (within a `@ui.refreshable`).

```python
row = ui.row()
# Too late to add to row here without entering its context:
with row:
    ui.label('This works')
# ui.label('This would go to page root, NOT inside row')
```

### 5. The binding system is pull-based, not push-based

NiceGUI bindings use two complementary mechanisms:

- **Push**: assigning to a `BindableProperty` (the descriptor used on element attributes like `value`, `text`, `visible`) propagates synchronously through all linked bindings immediately.
- **Pull**: a refresh loop runs every `binding_refresh_interval` (default 0.1s) and re-checks `active_links` — this is what makes bindings work against plain `dict` keys and ordinary object attributes that have no setter to hook into.

In practice:
- Binding a `ui.input` value to a plain dataclass attribute → the refresh loop picks up changes (~100ms)
- Binding between two NiceGUI elements (both use `BindableProperty`) → propagation is synchronous
- You usually don't need to call `.update()` after a bound assignment; either the descriptor or the refresh loop handles it
- Bindings work on any Python object — no special base class required

### 6. Why Python-first is a hard rule, not just style

When you bypass NiceGUI's Python API and manipulate the DOM directly via JavaScript:
- NiceGUI's Python-side model diverges from the client DOM (they are out of sync)
- The next time NiceGUI sends an update for that element, it overwrites your JS change
- Bindings and refreshables don't know about changes made outside the Python model

Use `ui.run_javascript()` only for things that are truly impossible via the Python API (e.g., reading `window.innerWidth`). Never use it to style, show/hide, or update content.

### 7. Async in NiceGUI: the event loop is shared

NiceGUI runs in a single asyncio event loop. Every page, every user, every timer shares it. Blocking the loop (with `time.sleep()`, `requests.get()`, heavy CPU work) freezes the **entire application** for all users. Rules:

- All I/O must be async (`httpx`, `aiofiles`, `asyncio.sleep()`)
- CPU-heavy work must run in a thread: `await asyncio.to_thread(cpu_func)` (Python 3.9+, simpler than `run_in_executor`; use `run_in_executor` when you need a custom executor like `ProcessPoolExecutor`)
- `background_tasks.create()` for fire-and-forget coroutines — wraps `create_task` but keeps a reference (so the GC won't cancel it) and routes exceptions through NiceGUI's exception handler. Avoid bare `asyncio.create_task()` or `asyncio.ensure_future()` for this reason.
- Timers (`ui.timer()`) are safe: they schedule callbacks without blocking

### 8. Why `ui.storage.user` and not a global dict

`app.storage.user` is per-user (session-scoped) and persistent across page reloads. A module-level `dict` is per-process (shared across all users) and lost on server restart. Always ask: "Should this be per-user, per-session, or global?" and pick accordingly:

| Storage | Scope | Persistence |
|---|---|---|
| local variable in `@ui.page` | per page load | until page reload |
| `app.storage.client` | per browser connection | until tab closes |
| `app.storage.tab` | per browser tab | until tab closes |
| `app.storage.user` | per user (session cookie) | until cookie expires |
| `app.storage.general` | all users | persistent on disk |
| module-level variable | entire server | server restart |

### 9. The Outbox — why you don't need to batch updates manually

NiceGUI accumulates all element changes within a single event handler execution and sends them in one WebSocket message. You don't need to worry about "sending too many updates" within a single callback — they are automatically batched. However, updates from **different** async callbacks or timer ticks are sent separately.

### 10. Why `response_timeout` matters for `@ui.page`

The page builder function has a 3-second default timeout. If it takes longer, the client gets an error. Heavy work (DB queries, API calls, file loading) must be done via background tasks launched from within the page builder — the page delivers the skeleton UI immediately, then populates data asynchronously.

```python
@ui.page('/')
async def index():
    spinner = ui.spinner()
    label = ui.label()

    async def load():
        data = await slow_database_query()
        spinner.delete()
        label.set_text(data)

    background_tasks.create(load())
    # Page is delivered immediately; load() runs in background
```

---

## The Golden Rule – Python First

**Never reach for raw CSS, Quasar props, or JavaScript unless NiceGUI's Python API is insufficient.**

| Situation | WRONG | RIGHT |
|---|---|---|
| Change background color | `ui.add_head_html('<style>body{background:blue}</style>')` | `ui.query('body').classes('bg-blue')` |
| Hide an element | `element.run_method('hide')` | `element.visible = False` |
| Style a button | `ui.button(...).style('background-color: green')` | `ui.button(..., color='green')` |
| Center content | raw flexbox CSS | `with ui.row().classes('justify-center'):` |
| React to input | JS event listener | `ui.input(on_change=handler)` |
| Repeat an action | `asyncio.create_task(loop())` | `ui.timer(interval, callback)` |
| Navigate | `ui.run_javascript('window.location = ...')` | `ui.navigate.to(url)` |
| Show a message | custom HTML overlay | `ui.notify('message')` |
| Copy to clipboard | `ui.run_javascript("navigator.clipboard.writeText(...)")` | `await ui.clipboard.write(text)` |
| Styled download link | `ui.html('<a href=... style=...>')` | `ui.button('Download').props('href=... tag=a')` |
| CPU work in thread | `asyncio.get_event_loop().run_in_executor(None, fn)` | `await asyncio.to_thread(fn)` (3.9+; use `run_in_executor` for custom executors) |

---

## Styling API

Every element exposes three orthogonal styling methods that return `Self` (chainable):

### `.classes(add, *, remove, toggle, replace)`
Apply **Tailwind CSS** or **Quasar utility classes**. This is the primary styling tool.

```python
ui.label('Hello').classes('text-xl font-bold text-red-500')
ui.card().classes('shadow-lg p-4 bg-grey-2')
# remove a class
element.classes(remove='bg-red-500')
# toggle
element.classes(toggle='hidden')
```

### `.style(add, *, remove, replace)`
Inline CSS as a **semicolon-separated string**. Use only when no Tailwind/Quasar class fits.

```python
ui.label('Hi').style('font-size: 2rem; color: #333')
```

### `.props(add, *, remove)`
**Quasar component props** as space-separated `key` or `key=value` pairs.
Boolean props are `True` if no value is given.

```python
ui.button('Send').props('unelevated rounded color=positive')
ui.input('Name').props('outlined dense clearable')
ui.table(...).props('flat bordered')
```

### `ui.query(selector)`
Style arbitrary DOM elements (e.g. the page body):

```python
ui.query('body').classes('bg-grey-1')
ui.query('.nicegui-content').style('max-width: 960px; margin: auto')
```

### Color values
The `color` parameter (on button, badge, chip, etc.) accepts, in priority order:
1. Quasar color names (`primary`, `secondary`, `positive`, `negative`, `warning`, `info`, `dark`, `grey-5`, …)
2. Tailwind color names (`red-500`, `blue-200`, …)
3. CSS color values (`#ff0000`, `rgb(255,0,0)`, `red`)

---

## Layout Elements (Context Managers)

All layout elements are used as context managers. Children are automatically placed inside them.

```python
with ui.row():               # horizontal flex row (wrapping by default)
    ui.button('A')
    ui.button('B')

with ui.column():            # vertical flex column
    ui.label('Top')
    ui.label('Bottom')

with ui.card():              # Quasar QCard with shadow
    with ui.card_section():
        ui.label('Title')

with ui.grid(columns=3):    # CSS grid
    for i in range(9):
        ui.label(str(i))

with ui.row().classes('w-full justify-between items-center'):
    ui.label('Left')
    ui.label('Right')

with ui.expansion('Details', icon='info'):
    ui.label('Hidden content')

with ui.scroll_area().classes('h-64'):
    for i in range(50):
        ui.label(f'Row {i}')

with ui.splitter() as splitter:
    with splitter.before:
        ui.label('Left pane')
    with splitter.after:
        ui.label('Right pane')
```

### Page structure elements
```python
with ui.header():
    ui.label('My App')

with ui.left_drawer():
    ui.label('Sidebar')

with ui.footer():
    ui.label('Footer')

ui.page_sticky('bottom-right', x_offset=20, y_offset=20)  # floating content
```

---

## Input Elements

```python
ui.input('Name', value='Alice', on_change=handler)
ui.textarea('Notes', rows=5)
ui.number('Age', min=0, max=120, step=1)
ui.select(['a', 'b', 'c'], value='a', on_change=handler)
ui.select({'Option A': 1, 'Option B': 2}, value=1)  # dict: label→value
ui.checkbox('Agree', value=False, on_change=handler)
ui.switch('Dark mode', value=False)
ui.radio(['Yes', 'No', 'Maybe'], value='Yes')
ui.toggle(['Left', 'Center', 'Right'], value='Left')
ui.slider(min=0, max=100, step=1, value=50)
ui.range(min=0, max=100, value={'min': 20, 'max': 80})
ui.knob(value=0.5, min=0, max=1, step=0.01)
ui.rating(max=5, value=3)
ui.color_input('Color', value='#ff0000')
ui.date(value='2024-01-01')              # returns ISO string
ui.time(value='12:00')
ui.date_input('Birthday')               # combined date picker + text input
ui.time_input('Time')
ui.upload(on_upload=handler, multiple=True)
ui.input_chips('Tags')                  # chip-based multi-value input
```

---

## Display Elements

```python
ui.label('Hello World')
ui.markdown('**Bold** and *italic*')
ui.code('print("hello")', language='python')
ui.image('/path/to/image.png')          # or URL or base64
ui.audio('/path/to/audio.mp3')
ui.video('/path/to/video.mp4')
ui.icon('thumb_up', size='2rem', color='green')   # Material Design icons
ui.avatar('JD', color='blue')           # initials or image
ui.badge('3', color='red')
ui.chip('Tag', icon='label', color='primary')
ui.separator()
ui.space()                              # flexible spacer (flex: 1)
ui.spinner(size='lg', color='primary')
ui.skeleton(type='rect', height='2rem')
ui.link('Click here', target='https://example.com')
ui.html('<b>raw</b> HTML')             # use sparingly
ui.chat_message('Hello!', name='Alice', stamp='now', avatar='...')
ui.log(max_lines=100)                  # live-updating log display
```

---

## Data Display

```python
# Table (Quasar QTable)
columns = [
    {'name': 'name', 'label': 'Name', 'field': 'name', 'sortable': True},
    {'name': 'age', 'label': 'Age', 'field': 'age'},
]
rows = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
ui.table(columns=columns, rows=rows, row_key='name')

# AG Grid (advanced grid)
ui.aggrid({
    'columnDefs': [{'field': 'name'}, {'field': 'age'}],
    'rowData': rows,
})

# Tree
ui.tree([
    {'id': 'root', 'label': 'Root', 'children': [
        {'id': 'child1', 'label': 'Child 1'},
    ]}
], label_key='label', node_key='id')

# JSON editor
ui.json_editor({'content': {'json': {'key': 'value'}}})
```

---

## Charts & Visualization

```python
# ECharts (recommended for most charts)
ui.echart({
    'xAxis': {'type': 'category', 'data': ['Mon', 'Tue', 'Wed']},
    'yAxis': {'type': 'value'},
    'series': [{'type': 'bar', 'data': [120, 200, 150]}],
})

# Plotly
import plotly.graph_objects as go
fig = go.Figure(go.Bar(x=['A', 'B'], y=[1, 2]))
ui.plotly(fig)

# Matplotlib / pyplot
with ui.pyplot(figsize=(6, 4)) as plot:
    import matplotlib.pyplot as plt
    plt.plot([1, 2, 3], [4, 5, 6])

# Live line plot (efficient for streaming data)
with ui.line_plot(n=50, update_every=5) as plot:
    plot.push(x_value, [y1, y2])

# 3D Scene (Three.js)
with ui.scene() as scene:
    scene.sphere().move(x=1)
    scene.box().material('#ff0000')
```

---

## Navigation & Dialogs

```python
# Tabs
with ui.tabs() as tabs:
    ui.tab('home', label='Home', icon='home')
    ui.tab('settings', label='Settings', icon='settings')
with ui.tab_panels(tabs, value='home'):
    with ui.tab_panel('home'):
        ui.label('Home content')
    with ui.tab_panel('settings'):
        ui.label('Settings content')

# Dialog
with ui.dialog() as dialog:
    with ui.card():
        ui.label('Are you sure?')
        with ui.row():
            ui.button('Yes', on_click=dialog.close)
            ui.button('No', on_click=dialog.close)
ui.button('Open', on_click=dialog.open)

# Menu
with ui.button('Menu'):
    with ui.menu():
        ui.menu_item('Option 1', on_click=handler)
        ui.menu_item('Option 2', on_click=handler)

# Context menu
with ui.label('Right-click me'):
    with ui.context_menu():
        ui.menu_item('Action', on_click=handler)

# Stepper
with ui.stepper() as stepper:
    with ui.step('Step 1'):
        ui.label('First step')
        with ui.stepper_navigation():
            ui.button('Next', on_click=stepper.next)
    with ui.step('Step 2'):
        ui.label('Second step')
        with ui.stepper_navigation():
            ui.button('Back', on_click=stepper.previous)
            ui.button('Finish')

# Carousel
with ui.carousel(animated=True) as carousel:
    with ui.carousel_slide():
        ui.label('Slide 1')
    with ui.carousel_slide():
        ui.label('Slide 2')

# Pagination
ui.pagination(min=1, max=10, direction_links=True)
```

---

## Binding System

Bind element properties to Python objects reactively. Changes propagate automatically — no manual `.update()` needed.

```python
class State:
    name = 'Alice'
    visible = True

state = State()

# Two-way binding (element ↔ object)
ui.input('Name').bind_value(state, 'name')

# One-way: object → element (read-only display)
ui.label().bind_text_from(state, 'name')

# One-way: element → object
ui.input().bind_value_to(state, 'name')

# Visibility binding
ui.label('Hello').bind_visibility_from(state, 'visible')

# With value transformation
ui.label().bind_text_from(state, 'name', backward=lambda v: f'Hello, {v}!')

# Bind to dict key
data = {'count': 0}
ui.label().bind_text_from(data, 'count', backward=str)

# Bind to nested key (tuple path, since v3.10)
ui.label().bind_text_from(state, ('nested', 'key'))
```

Available bind methods (all support `forward`/`backward` transform functions):
- `bind_value` / `bind_value_from` / `bind_value_to`
- `bind_text` / `bind_text_from` / `bind_text_to`
- `bind_visibility` / `bind_visibility_from` / `bind_visibility_to`
- `bind_content` / `bind_content_from` / `bind_content_to` (for `ui.html`, `ui.markdown`)
- `bind_source` / `bind_source_from` / `bind_source_to` (for `ui.image`, `ui.audio`, etc.)

---

## Refreshable UI

Use `@ui.refreshable` to rebuild a section of the UI on demand:

```python
items = ['Apple', 'Banana']

@ui.refreshable
def item_list():
    for item in items:
        ui.label(item)

item_list()  # initial render

def add_item():
    items.append('Cherry')
    item_list.refresh()  # clears and rebuilds

ui.button('Add', on_click=add_item)
```

Use `ui.state()` for local state within a refreshable (React-style):

```python
@ui.refreshable
def counter():
    count, set_count = ui.state(0)
    ui.label(f'Count: {count}')
    ui.button('+1', on_click=lambda: set_count(count + 1))
```

Use `@ui.refreshable_method` for methods in classes:

```python
class MyView:
    def __init__(self):
        self.data = []

    @ui.refreshable_method
    def render(self):
        for item in self.data:
            ui.label(item)
```

---

## Timer

```python
# Repeating timer
ui.timer(1.0, lambda: label.set_text(str(datetime.now())))

# Run once after delay
ui.timer(5.0, callback, once=True)

# Timer with activation control
t = ui.timer(0.1, callback, active=False)
t.activate()
t.deactivate()
t.cancel()

# Async callback
async def update():
    data = await fetch_data()
    label.set_text(data)

ui.timer(5.0, update)
```

---

## Pages & Routing

```python
# Per-user private page (each visitor gets their own instance)
@ui.page('/dashboard')
def dashboard():
    ui.label('Welcome!')

# With path parameter (FastAPI style)
@ui.page('/item/{item_id}')
def item_page(item_id: int):
    ui.label(f'Item {item_id}')

# Shared page (all users see the same elements — rare, usually not desired)
# Just put ui.* calls at module level (outside @ui.page)

# Navigation
ui.navigate.to('/dashboard')
ui.navigate.to('https://example.com', new_tab=True)
ui.navigate.back()
ui.navigate.forward()
ui.navigate.reload()

# Page title
ui.page_title('My App')
```

---

## Storage

Requires `ui.run(storage_secret='...')` for `user` and `browser`.

```python
from nicegui import app

# Per-user persistent storage (survives page reload, browser-session scoped)
app.storage.user['username'] = 'Alice'
name = app.storage.user.get('username', 'Guest')

# Global shared storage (all users, persistent)
app.storage.general['visit_count'] = app.storage.general.get('visit_count', 0) + 1

# Per-connection in-memory (lost on page reload)
app.storage.client['temp'] = 'value'

# Per-browser-tab in-memory
app.storage.tab['step'] = 2

# Read-only browser session data
session_id = app.storage.browser.get('id')
```

---

## Events

```python
# Constructor callbacks (most common)
ui.button('Click', on_click=handler)
ui.input('Name', on_change=handler, on_focus=handler, on_blur=handler)
ui.upload(on_upload=handler, on_rejected=handler)
ui.keyboard(on_key=handler)

# .on() for any DOM/Vue event
ui.label('Hover me').on('mouseover', handler)
ui.image(...).on('click', handler, ['offsetX', 'offsetY'])  # pass specific args

# Throttle high-frequency events
ui.input().on('keydown', handler, throttle=0.1)

# Client-side only (no server round-trip)
ui.button().on('click', js_handler='() => alert("hello")')

# await a one-time event
btn = ui.button('Click me')
await btn.clicked()
```

Event argument objects have `.sender` (the element) and `.client` attributes.
Input/value events have `.value` and `.previous_value`.

---

## Notifications & Feedback

```python
ui.notify('Saved!', type='positive')
ui.notify('Error!', type='negative', position='top')
ui.notify('Warning', type='warning', close_button='Dismiss')
ui.notify('Loading…', type='ongoing')

# Persistent notification object
n = ui.notification('Processing…', spinner=True)
# later:
n.message = 'Done!'
n.spinner = False
n.type = 'positive'
n.dismiss()
```

---

## JavaScript Interop

Only use when no Python API exists:

```python
# Run JS and ignore result (fire-and-forget)
ui.run_javascript('document.title = "New Title"')

# Run JS and await result
result = await ui.run_javascript('return window.innerWidth')

# Call a method on a specific element's Vue component
await element.run_method('methodName', arg1, arg2)

# Get a computed Vue prop
value = await element.get_computed_prop('propName')

# Add global CSS
ui.add_css('body { font-family: monospace; }')
ui.add_scss('$primary: blue; body { color: $primary; }')

# Add raw HTML to <head> or <body> (last resort)
ui.add_head_html('<link rel="preconnect" href="...">')
ui.add_body_html('<script src="..."></script>')
```

---

## Global App & Lifecycle

```python
from nicegui import app, ui

# Startup / shutdown hooks
app.on_startup(async_function)
app.on_shutdown(async_function)
app.on_connect(handler)     # new client connects
app.on_disconnect(handler)  # client disconnects
app.on_exception(handler)   # unhandled exceptions

# Custom FastAPI routes alongside NiceGUI
@app.get('/api/data')
async def get_data():
    return {'value': 42}

# Serve static files
app.mount('/static', StaticFiles(directory='static'))

# Run
ui.run(
    host='0.0.0.0',
    port=8080,
    title='My App',
    favicon='🚀',
    dark=None,           # None = follow system
    storage_secret='my-secret',
    reload=True,         # auto-reload on file change (dev only)
    show=False,          # don't open browser automatically
)
```

---

## Background Tasks (Async)

```python
from nicegui import background_tasks

# NEVER use asyncio.create_task() — the GC may cancel it
# ALWAYS use background_tasks.create()
background_tasks.create(my_coroutine(), name='my-task')

# Inside a @ui.page handler, run something after the page is built
async def long_work():
    await asyncio.sleep(5)
    label.set_text('Done')

@ui.page('/')
async def index():
    label = ui.label('Working…')
    background_tasks.create(long_work())
```

---

## Element Reference

### Text & Media
| Element | Description |
|---|---|
| `ui.label(text)` | Plain text |
| `ui.markdown(content)` | Markdown with auto-dedent |
| `ui.html(content)` | Raw HTML |
| `ui.code(content, language)` | Syntax-highlighted code block |
| `ui.codemirror(value, language)` | Editable code editor |
| `ui.mermaid(content)` | Mermaid diagram |
| `ui.restructured_text(content)` | RST content |
| `ui.image(source)` | Image (path, URL, or base64) |
| `ui.interactive_image(source)` | Image with click/hover events |
| `ui.audio(source)` | Audio player |
| `ui.video(source)` | Video player |
| `ui.icon(name)` | Material Design icon |
| `ui.avatar(text_or_icon)` | Avatar (initials or icon) |
| `ui.badge(text)` | Small badge label |
| `ui.chip(text)` | Chip / tag |
| `ui.link(text, target)` | Hyperlink |
| `ui.chat_message(text, name)` | Chat bubble |
| `ui.log(max_lines)` | Auto-scrolling log |

### Input
| Element | Description |
|---|---|
| `ui.input(label)` | Text input |
| `ui.textarea(label)` | Multi-line text |
| `ui.number(label)` | Numeric input |
| `ui.select(options)` | Dropdown select |
| `ui.radio(options)` | Radio group |
| `ui.toggle(options)` | Toggle button group |
| `ui.checkbox(text)` | Checkbox |
| `ui.switch(text)` | Toggle switch |
| `ui.slider(min, max)` | Range slider |
| `ui.range(min, max)` | Dual-handle range |
| `ui.knob(value)` | Rotary knob |
| `ui.rating(max)` | Star rating |
| `ui.color_input(label)` | Color picker input |
| `ui.color_picker()` | Standalone color picker |
| `ui.date(value)` | Date picker |
| `ui.time(value)` | Time picker |
| `ui.date_input(label)` | Date input with picker |
| `ui.time_input(label)` | Time input with picker |
| `ui.upload()` | File upload |
| `ui.input_chips(label)` | Multi-value chip input |
| `ui.editor(value)` | WYSIWYG rich text editor |

### Layout & Structure
| Element | Description |
|---|---|
| `ui.row()` | Horizontal flex row |
| `ui.column()` | Vertical flex column |
| `ui.grid(columns)` | CSS grid |
| `ui.card()` | Card container |
| `ui.card_section()` | Card section |
| `ui.card_actions()` | Card action bar |
| `ui.expansion(label)` | Collapsible section |
| `ui.scroll_area()` | Scrollable container |
| `ui.splitter()` | Resizable split panes |
| `ui.separator()` | Horizontal divider |
| `ui.space()` | Flexible spacer |
| `ui.header()` | Page header |
| `ui.footer()` | Page footer |
| `ui.left_drawer()` | Left sidebar drawer |
| `ui.right_drawer()` | Right sidebar drawer |
| `ui.page_sticky(position)` | Fixed-position overlay |
| `ui.page_scroller()` | Scroll-to-top button |
| `ui.teleport(to)` | Render child in different DOM location |

### Navigation
| Element | Description |
|---|---|
| `ui.tabs()` + `ui.tab_panels()` | Tab navigation |
| `ui.stepper()` | Step-by-step wizard |
| `ui.carousel()` | Image/slide carousel |
| `ui.pagination(min, max)` | Page number controls |
| `ui.sub_pages()` | Nested sub-page routing |

### Overlay & Feedback
| Element | Description |
|---|---|
| `ui.dialog()` | Modal dialog |
| `ui.menu()` | Dropdown menu |
| `ui.context_menu()` | Right-click menu |
| `ui.tooltip(text)` | Hover tooltip |
| `ui.notification(msg)` | Persistent notification |
| `ui.spinner()` | Loading spinner |
| `ui.skeleton()` | Placeholder skeleton |
| `ui.fab(icon)` | Floating action button |
| `ui.fab_action(icon)` | FAB sub-action |

### Data & Charts
| Element | Description |
|---|---|
| `ui.table(columns, rows)` | Quasar data table |
| `ui.aggrid(options)` | AG Grid |
| `ui.tree(nodes)` | Foldable tree |
| `ui.json_editor(content)` | JSON editor |
| `ui.echart(options)` | Apache ECharts |
| `ui.plotly(figure)` | Plotly chart |
| `ui.matplotlib()` / `ui.pyplot()` | Matplotlib figure |
| `ui.altair(chart)` | Vega-Altair chart |
| `ui.highchart(options)` | Highcharts (requires license) |
| `ui.line_plot(n)` | Efficient streaming line chart |

### Advanced / Specialized
| Element | Description |
|---|---|
| `ui.scene()` | Interactive 3D (Three.js) |
| `ui.leaflet()` | Interactive map (Leaflet.js) |
| `ui.interactive_image()` | Image with SVG overlays |
| `ui.joystick()` | Virtual joystick |
| `ui.keyboard(on_key)` | Global keyboard listener |
| `ui.xterm()` | Terminal emulator |
| `ui.anywidget(widget)` | Embed anywidget |
| `ui.timer(interval, cb)` | Repeating/one-shot timer |
| `ui.dark_mode()` | Dark mode toggle |
| `ui.colors(primary, ...)` | Global theme colors |
| `ui.query(selector)` | Style arbitrary DOM elements |

### Global Functions
| Function | Description |
|---|---|
| `ui.notify(msg)` | Toast notification |
| `ui.navigate.to(url)` | Navigate to URL |
| `ui.navigate.back/forward/reload()` | Browser history navigation |
| `ui.run_javascript(code)` | Execute JS (await for result) |
| `ui.download(src)` | Trigger file download |
| `ui.clipboard.write(text)` | Write to clipboard |
| `ui.clipboard.read()` | Read from clipboard (await) |
| `ui.update(element)` | Force push element update |
| `ui.refreshable` | Decorator for rebuilding UI sections |
| `ui.refreshable_method` | Same, for class methods |
| `ui.state(value)` | Local state inside `@ui.refreshable` |
| `ui.page_title(title)` | Set browser tab title |
| `ui.add_css/add_scss/add_sass(code)` | Global styles |
| `ui.add_head_html(html)` | Inject into `<head>` |
| `ui.add_body_html(html)` | Inject into `<body>` |
| `ui.on(event, handler)` | Global app event listener |
| `ui.on_exception(handler)` | Global exception handler |
| `ui.status_code(code)` | Set HTTP response status |

---

## Named Slots

Most elements have only a `default` slot. Complex elements (table, drawer, etc.) have named slots
for injecting custom content into specific areas:

```python
# Table header slot
table = ui.table(columns=columns, rows=rows)
with table.add_slot('header'):
    with table.add_slot('header-cell-name'):
        ui.label('NAME').classes('font-bold')

# Drawer toggle slot
with ui.header():
    with ui.button(icon='menu').props('flat'):
        pass  # default
    ui.label('My App')

# Dialog default slot is just 'with dialog:'
with ui.dialog() as dialog:
    ui.label('Content goes in default slot')
```

---

## Element Markers (Testing & Querying)

Use `.mark()` to tag elements for testing and `ElementFilter`:

```python
# Mark elements
ui.button('Submit').mark('submit-btn')
ui.input('Email').mark('email-input')
ui.label().mark('result-label')

# In tests (User fixture):
async def test_form(user: User):
    await user.open('/')
    await user.type('test@example.com', marker='email-input')
    await user.click('submit-btn')
    await user.should_see(marker='result-label')

# ElementFilter in app code (for reducing global vars):
from nicegui.element_filter import ElementFilter
labels = ElementFilter(marker='result-label')
for label in labels:
    label.set_text('Updated')
```

---

## Common Patterns

### Dynamic list
```python
names = ['Alice', 'Bob']

@ui.refreshable
def name_list():
    for name in names:
        with ui.row().classes('items-center'):
            ui.label(name)
            ui.button(icon='delete', on_click=lambda n=name: remove(n)).props('flat dense')

def remove(name):
    names.remove(name)
    name_list.refresh()

name_list()
ui.button('Add', on_click=lambda: (names.append('New'), name_list.refresh()))
```

### Reactive form with validation
```python
ui.input('Email', validation={'Must contain @': lambda v: '@' in v})
ui.number('Age', min=0, max=150, validation={'Too young': lambda v: v >= 18})
```

### Async data loading
```python
@ui.page('/')
async def index():
    spinner = ui.spinner()
    async def load():
        data = await fetch_data()
        spinner.delete()
        ui.label(str(data))
    background_tasks.create(load())
```

### Card grid layout
```python
with ui.grid(columns=3).classes('w-full gap-4'):
    for item in items:
        with ui.card().classes('cursor-pointer hover:shadow-lg') \
                .on('click', lambda i=item: select(i)):
            ui.image(item.image).classes('w-full')
            ui.label(item.title).classes('font-bold')
            ui.label(item.description).classes('text-sm text-grey')
```

### Bind label to slider value
```python
slider = ui.slider(min=0, max=100, value=50)
ui.label().bind_text_from(slider, 'value', backward=lambda v: f'Value: {v}')
```

---

## Anti-Patterns to Avoid

```python
# BAD: raw JS for styling
ui.run_javascript("document.querySelector('.my-class').style.color = 'red'")
# GOOD:
ui.query('.my-class').style('color: red')

# BAD: asyncio.create_task() or asyncio.ensure_future() — bare task references
#      may be GC-cancelled, and exceptions are silently swallowed unless awaited
asyncio.create_task(my_coro())
asyncio.ensure_future(my_coro())
# GOOD: keeps a reference + routes exceptions through NiceGUI's exception handler
background_tasks.create(my_coro())

# BAD: run_javascript for clipboard
await ui.run_javascript("navigator.clipboard.writeText('https://example.com')")
# GOOD:
await ui.clipboard.write('https://example.com')

# BAD: raw HTML for a styled download link
ui.html('<a href="/download" style="color: white; background: green; padding: 8px">Download</a>')
# GOOD: ui.button with tag=a renders as an <a> element with full Quasar styling
ui.button('Download', icon='download') \
    .props('href="/download" tag=a unelevated color=primary')

# BAD: blocking I/O in async handler
async def on_click():
    data = requests.get(url).json()  # blocks the event loop!
# GOOD:
async def on_click():
    async with httpx.AsyncClient() as client:
        data = (await client.get(url)).json()

# BAD: rebuilding entire page on every change
@ui.page('/')
def index():
    ...  # all dynamic content here, triggers full reload
# GOOD: use @ui.refreshable for the dynamic sections only

# BAD: inline style for something Tailwind/Quasar already provides
ui.label('Big').style('font-size: 1.5rem; font-weight: bold')
# GOOD:
ui.label('Big').classes('text-2xl font-bold')

# BAD: add_head_html for page background
ui.add_head_html('<style>body { background: #f0f0f0 }</style>')
# GOOD:
ui.query('body').classes('bg-grey-2')

# BAD: passing Quasar-specific values to .style()
ui.button().style('background-color: var(--q-primary)')
# GOOD: let NiceGUI handle Quasar theme
ui.button(color='primary')
```

---

## Testing

Prefer `User` fixture (no browser, fast, same async context):

```python
async def test_counter(user: User) -> None:
    await user.open('/')
    await user.click('Increment')
    await user.should_see('Count: 1')
```

Use `Screen` fixture only when JavaScript or real browser rendering is required:

```python
def test_chart(screen: Screen) -> None:
    screen.open('/')
    screen.should_contain('canvas')  # chart rendered
```

---

## Project Structure (Recommended)

```
my_app/
├── main.py           # ui.run() entry point, top-level shared UI
├── pages/
│   ├── dashboard.py  # @ui.page('/dashboard') def dashboard(): ...
│   └── settings.py
├── components/       # Reusable @ui.refreshable functions or classes
│   └── navbar.py
└── models/           # Plain Python data classes / state objects
    └── state.py
```

**Key rules for project structure:**
- Keep files under 200–300 lines; refactor when exceeding this
- `@ui.page` functions are free functions or static methods (not instance methods)
- Put high-level/interesting code at the top of files; helper functions below their usage
- Shared UI that every page uses (header, nav) lives at module level or in a shared `@ui.refreshable`

---

## Multi-Page App Pattern

```python
# main.py
from nicegui import app, ui
from pages import dashboard, settings  # imports trigger @ui.page registration

@ui.page('/')
def index():
    ui.navigate.to('/dashboard')

ui.run(storage_secret='my-secret', title='My App')
```

```python
# pages/dashboard.py
from nicegui import ui

@ui.page('/dashboard')
def dashboard():
    with ui.header():
        ui.label('Dashboard').classes('text-xl font-bold')
    with ui.column().classes('p-4'):
        ui.label('Welcome!')
```

---

## Coding Standards

These follow NiceGUI project conventions and work well for NiceGUI-based apps:

### Python Style
- **Single quotes** for strings: `'hello'` not `"hello"` (in Python code)
- **f-strings** preferred over `.format()` or `%`
- **`# NOTE:`** prefix for non-obvious implementation details
- **No mutable defaults**: use `None` instead of `[]` or `{}`
- **`contextlib.suppress()`** instead of `try: ... except: pass`
- **`background_tasks.create()`** instead of `asyncio.create_task()`
- **`ImportError`** (not `ModuleNotFoundError`) when catching optional dependency errors

### Async Rules
```python
# NEVER block the event loop
import time
time.sleep(5)             # blocks everything — never do this in async context
requests.get(url)         # synchronous HTTP — use httpx or aiohttp instead

# ALWAYS use background_tasks for fire-and-forget coroutines
from nicegui import background_tasks
background_tasks.create(my_coroutine(), name='descriptive-name')

# Handle exceptions in background tasks
from nicegui import core
async def safe_task():
    try:
        await do_work()
    except Exception as e:
        core.app.handle_exception(e)
```

### Fluent Interface Formatting
When chaining methods, use backslash continuation:
```python
ui.button('Click me') \
    .classes('bg-green text-white') \
    .props('rounded') \
    .on('click', handler)
```

---

## What to Avoid (Summary)

- **Global mutable state** in shared module scope (use `app.storage` instead)
- **Blocking I/O** in async handlers or WebSocket paths
- **`asyncio.create_task()` / `asyncio.ensure_future()`** — use `background_tasks.create()` (keeps a reference so GC won't cancel it, and routes exceptions through NiceGUI's handler)
- **Broad `except:`** without re-raise or proper context
- **Debug `print()`** — use Python `logging` module
- **Raw CSS/JS** when a NiceGUI Python API exists
- **`ui.add_head_html` / `ui.add_body_html`** for things `.classes()`, `.style()`, or `ui.query()` can handle
- **`ui.run_javascript()`** for styling or visibility (use Python API)
- **Creating new files** when editing existing ones suffices
- **Over-engineering**: three similar lines beat a premature abstraction

---

## Core Principles for AI Assistants

1. **Python first**: Never reach for CSS, Quasar, or JS unless the Python API is insufficient
2. **Simplicity first**: Prefer simple, direct solutions; avoid over-engineering
3. **Search before inventing**: Look for existing patterns in the codebase before creating new ones
4. **API stability**: New parameters need sensible defaults; avoid breaking changes
5. **Requirements first**: Verify the goal before implementing, especially for tests
6. **Think from first principles**: Question assumptions; find the true nature of the problem

---

*This file is intended for AI assistants working with NiceGUI projects.*
*For full API docs see https://nicegui.io/documentation.*
*Source: NiceGUI repository — https://github.com/zauberzeug/nicegui*
