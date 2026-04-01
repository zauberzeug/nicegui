from nicegui import ui

from . import doc
from ... import design as d

doc.title('Technological *Foundations*', 'Built on giants')

doc.text('', '''
    NiceGUI follows a backend-first philosophy:
    All UI logic lives in Python while the framework handles all the web development details.
    Under the hood, a carefully chosen stack of open-source technologies makes this possible.
''')


@doc.part('UI Framework')
def _():
    with ui.grid().classes('grid-cols-[2fr_1fr] max-xl:grid-cols-1 w-full gap-8 items-start'):
        ui.markdown('''
            ##### Vue.js

            Inspired by [JustPy](https://justpy.io/),
            every [UI element](/documentation/element) you create in Python maps to a
            [Vue](https://vuejs.org/) component in the browser.
            Vue's reactive model enables seamless real-time updates —
            when your Python code changes a property, the browser updates instantly.

            And if the built-in elements aren't enough, you can
            [create your own Vue components](/documentation/section_configuration_deployment#custom_vue_components)
            (see the [example](https://github.com/zauberzeug/nicegui/tree/main/examples/custom_vue_component)).

            There is also experimental support for plugging in
            [other Vue UI frameworks](/documentation/section_styling_appearance#using_other_vue_ui_frameworks)
            like Element Plus or Vuetify, though this requires hands-on work
            since all native NiceGUI elements expect Quasar.
        ''')
        ui.mermaid('''
            graph TD
                N["NiceGUI Element"] -- "props & slots" --> V["Vue Component"] -- "reactive render" --> D["Browser DOM"]
        ''').classes(d.MERMAID_CLASSES)


@doc.part('Component Library')
def _():
    with ui.grid().classes('grid-cols-[2fr_1fr] max-xl:grid-cols-1 w-full gap-8 items-start'):
        ui.markdown('''
            ##### Quasar

            [Quasar](https://quasar.dev/) provides 70+ production-ready, Material Design UI components —
            from [buttons](/documentation/button) and [inputs](/documentation/input)
            to [dialogs](/documentation/dialog) and [tables](/documentation/table).
            NiceGUI wraps these as Python elements, giving you a polished interface out of the box.

            Each NiceGUI element exposes the most commonly used options as `__init__` parameters.
            Names mostly match their Quasar counterparts, though NiceGUI occasionally renames
            for clarity (e.g. `ui.switch` wraps `q-toggle`).
            The full set of Quasar props is always available via
            [`.props()`](/documentation/section_styling_appearance#styling).

            Explore the rich set of [icons](/documentation/icon), [layouts](/documentation/page_layout),
            and interactive widgets.

            Quasar was chosen because it offers a comprehensive, batteries-included component library built on Vue —
            so NiceGUI can provide high-level Python elements without reinventing every widget from scratch.
        ''')
        ui.markdown('''
            | NiceGUI       | Quasar       | Example `.props()`           |
            | ------------- | ------------ | ---------------------------- |
            | `ui.button`   | `q-btn`      | `'flat color=red icon=star'` |
            | `ui.slider`   | `q-slider`   | `'label-always snap'`        |
            | `ui.checkbox` | `q-checkbox` | `'keep-color'`               |
            | `ui.switch`   | `q-toggle`   | `'icon=alarm'`               |
            | `ui.card`     | `q-card`     | `'bordered flat'`            |
            | `ui.badge`    | `q-badge`    | `'floating color=negative'`  |
            | `ui.tabs`     | `q-tabs`     | `'dense inline-label'`       |
        ''')


@doc.part('Backend')
def _():
    with ui.grid().classes('grid-cols-[2fr_1fr] max-xl:grid-cols-1 w-full gap-8 items-start'):
        ui.markdown('''
            ##### FastAPI

            NiceGUI is built on [FastAPI](https://fastapi.tiangolo.com/),
            chosen for its outstanding performance and developer experience.
            The entire ASGI stack — FastAPI on [Starlette](https://www.starlette.io/),
            served by [Uvicorn](https://www.uvicorn.org/) — keeps everything fast and fully async.

            Because NiceGUI sits on a real web framework, you can freely mix UI pages with
            [REST API endpoints](/documentation/section_pages_routing#api_responses),
            use FastAPI's
            [parameter injection](/documentation/section_pages_routing#parameter_injection),
            or run NiceGUI
            [on top of your own FastAPI app](/documentation/section_pages_routing#api_responses)
            via `ui.run_with()`.
            You can also mount additional ASGI apps alongside NiceGUI on the same Uvicorn server.
        ''')
        ui.mermaid('''
            graph TD
                N["NiceGUI"] --> F["FastAPI"]
                R["Other Routes"] -. "REST / API" .-> F
                F --> U["Uvicorn"]
                A["Other ASGI Apps"] -. "mount" .-> U
        ''').classes(d.MERMAID_CLASSES)


@doc.part('Real-Time Communication')
def _():
    with ui.grid().classes('grid-cols-[2fr_1fr] max-xl:grid-cols-1 w-full gap-8 items-start'):
        ui.markdown('''
            ##### Socket.IO

            NiceGUI uses [Socket.IO](https://socket.io/) for all real-time communication
            between the Python backend and the browser.
            Socket.IO builds on [Engine.IO](https://socket.io/docs/v4/engine-io-protocol/)
            and adds features that a plain WebSocket connection cannot provide:

            - **Transport fallback** — Socket.IO connects via WebSocket by default
              but falls back to HTTP long-polling when WebSocket is unavailable
              (e.g. behind restrictive proxies or firewalls).
              The `socket_io_js_transports` config controls which transports are offered.
            - **Automatic reconnection** — on disconnect, Socket.IO reconnects
              with exponential backoff and jitter, avoiding thundering-herd problems.
            - **Rooms** — the server can target messages to individual clients
              by placing each socket in a room keyed by its client ID.

            ##### The Outbox

            Every client has an outbox that batches element updates and messages in an async loop.
            Rather than emitting each property change immediately,
            the outbox collects all pending updates and sends them together via `sio.emit()` to the client's room.

            Each message gets a sequential ID and is stored in a history buffer.
            When a client reconnects after a brief drop, it reports the last message ID it received,
            and the outbox **rewinds** and replays everything since — no full page reload needed.
            Clients acknowledge received messages so the server can prune old history.
        ''')
        ui.mermaid('''
            graph TD
                N["NiceGUI"] --> O["Outbox"]
                O -- "batch & emit" --> S["Socket.IO"]
                S -- "room: client_id" --> B["Browser"]
                B -- "user event" --> S
                S -- "event handler" --> N
                B -. "ack" .-> S
                S -. "prune history" .-> O
        ''').classes(d.MERMAID_CLASSES)


@doc.part('Styling')
def _():
    with ui.grid().classes('grid-cols-[2fr_1fr] max-xl:grid-cols-1 w-full gap-8 items-start'):
        ui.markdown('''
            NiceGUI supports three CSS engines.
            All of them work through the [`.classes()`](/documentation/section_styling_appearance#styling) method —
            apply classes like "bg-blue-500 text-white p-4" directly in Python,
            no separate CSS files, no context switching.

            ##### Tailwind CSS

            [Tailwind CSS](https://tailwindcss.com/) is the most feature-complete option,
            with thousands of utility classes covering layout, typography, colors, animations, and more.
            NiceGUI uses the Tailwind CDN (runtime) rather than precompiled CSS,
            since running the Tailwind build toolchain in a Python environment is impractical,
            so the footprint is larger.

            ##### UnoCSS

            [UnoCSS](/documentation/section_styling_appearance#unocss) is a lighter alternative
            that is largely Tailwind-compatible while being more resource-friendly.
            Use the "mini" preset for the smallest bundle.

            ##### Quasar CSS

            [Quasar](https://quasar.dev/) ships its own CSS helper classes out of the box —
            the most resource-friendly option since no extra JS engine is loaded.

            With [CSS layers](/documentation/section_styling_appearance#tailwind_css_layers),
            you can override Quasar's defaults for full control over your design.

            Try the interactive styling playground in the
            [Styling & Appearance](/documentation/section_styling_appearance#styling) section.
        ''')
        with ui.column().classes('w-full gap-4'):
            for name, features, lightweight in [
                ('Tailwind CSS', 1.0, 0.2),
                ('UnoCSS', 0.7, 0.6),
                ('Quasar CSS', 0.3, 1.0),
            ]:
                with ui.column().classes('w-full gap-1'):
                    ui.label(name).classes('font-bold text-sm')
                    with ui.row(wrap=False).classes('w-full items-center gap-2'):
                        ui.label('Features').classes('text-xs min-w-18')
                        ui.linear_progress(value=features, show_value=False).classes('flex-grow').props('color=primary')
                    with ui.row(wrap=False).classes('w-full items-center gap-2'):
                        ui.label('Lightweight').classes('text-xs min-w-18')
                        ui.linear_progress(value=lightweight, show_value=False).classes(
                            'flex-grow').props('color=green')


doc.text('How It All Fits Together', '''
    The architecture is intentionally simple:

    - **Python** defines your UI using NiceGUI elements
    - **Vue** renders each element reactively in the browser
    - **Quasar** provides the Material Design component library
    - **Socket.IO** keeps Python and the browser in sync via the outbox
    - **FastAPI** serves pages and REST endpoints on **Uvicorn**
    - **Tailwind CSS** / **UnoCSS** / **Quasar CSS** handle styling

    A single Uvicorn worker handles everything — no multi-process synchronization needed, thanks to full async support.
    UI events flow from the browser through Socket.IO to Python handlers, which push updates back via the outbox
    that batches and tracks messages for seamless reconnection.

    For more details, see the [overview](/documentation)
    and the [configuration & deployment](/documentation/section_configuration_deployment) section.
''')
