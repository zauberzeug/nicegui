from nicegui import ui

from . import (
    doc,
    section_action_events,
    section_audiovisual_elements,
    section_binding_properties,
    section_configuration_deployment,
    section_controls,
    section_data_elements,
    section_page_layout,
    section_pages_routing,
    section_styling_appearance,
    section_testing,
    section_text_elements,
)
from ...style import subheading

doc.title('*NiceGUI* Documentation', 'Reference, Demos and more')

doc.text('Overview', '''
    NiceGUI is an open-source Python library to write graphical user interfaces which run in the browser.
    It has a very gentle learning curve while still offering the option for advanced customizations.
    NiceGUI follows a backend-first philosophy:
    It handles all the web development details.
    You can focus on writing Python code.
    This makes it ideal for a wide range of projects including short
    scripts, dashboards, robotics projects, IoT solutions, smart home automation, and machine learning.
''')

doc.text('How to use this guide', '''
    This documentation explains how to use NiceGUI.
    Each of the tiles covers a NiceGUI topic in detail.
    It is recommended to start by reading this entire introduction page, then refer to other sections as needed.
''')

doc.text('Basic concepts', '''
    NiceGUI provides UI _elements_ such as buttons, sliders, text, images, charts, and more.
    Your app assembles these components into _pages_.
    When the user interacts with an item on a page, NiceGUI triggers an _event_ (or _action_).
    You define code to _handle_ each event, such as what to do when a user clicks a button, modifies a value or operates a slider.
    Elements can also be bound to a _model_ (data object), which automatically updates the user interface when the model value changes.

    Elements are arranged on a page using a "declarative UI" or "code-based UI".
    That means that you also write structures like grids, cards, tabs, carousels, expansions, menus, and other layout elements directly in code.
    This concept has been made popular with Flutter and SwiftUI.
    For readability, NiceGUI utilizes Python's `with ...` statement.
    This context manager provides a nice way to indent the code to resemble the layout of the UI.

    Styling and appearance can be controlled in several ways.
    Most elements accept optional arguments for common styling and behavior changes, such as button icons or text color.
    Because NiceGUI is a web framework, you can change almost any appearance of an element with CSS.
    But elements also provide `.classes` and `.props` methods to apply Tailwind CSS and Quasar properties
    which are more high-level and simpler to use day-to-day after you get the hang of it.
''')

doc.text('Actions, Events and Tasks', '''
    NiceGUI uses an async/await event loop for concurrency which is resource-efficient and has the great benefit of not having to worry about thread safety.
    This section shows how to handle user input and other events like timers and keyboard bindings.
    It also describes helper functions to wrap long-running tasks in asynchronous functions to keep the UI responsive.
    Keep in mind that all UI updates must happen on the main thread with its event loop.
''')

doc.text('Implementation', '''
    NiceGUI is implemented with HTML components served by an HTTP server (FastAPI), even for native windows.
    If you already know HTML, everything will feel very familiar.
    If you don't know HTML, that's fine too!
    NiceGUI abstracts away the details, so you can focus on creating beautiful interfaces without worrying about how they are implemented.
''')

doc.text('Running NiceGUI Apps', '''
    There are several options for deploying NiceGUI.
    By default, NiceGUI runs a server on localhost and runs your app as a private web page on the local machine.
    When run this way, your app appears in a web browser window.
    You can also run NiceGUI in a native window separate from a web browser.
    Or you can run NiceGUI on a server that handles many clients - the website you're reading right now is served from NiceGUI.

    After creating your app pages with components, you call `ui.run()` to start the NiceGUI server.
    Optional parameters to `ui.run` set things like the network address and port the server binds to,
    whether the app runs in native mode, initial window size, and many other options.
    The section _Configuration and Deployment_ covers the options to the `ui.run()` function and the FastAPI framework it is based on.
''')

doc.text('Customization', '''
    If you want more customization in your app, you can use the underlying Tailwind classes and Quasar components
    to control the style or behavior of your components.
    You can also extend the available components by subclassing existing NiceGUI components or importing new ones from Quasar.
    All of this is optional.
    Out of the box, NiceGUI provides everything you need to make modern, stylish, responsive user interfaces.
''')

doc.text('Testing', '''
    NiceGUI provides a comprehensive testing framework based on [pytest](https://docs.pytest.org/)
    which allows you to automate the testing of your user interface.
    You can utilize the `screen` fixture which starts a real (headless) browser to interact with your application.
    This is great if you have browser-specific behavior to test.

    But most of the time, NiceGUI's newly introduced `user` fixture is more suited:
    It only simulates the user interaction on a Python level and, hence, is blazing fast.
    That way the classical [test pyramid](https://martinfowler.com/bliki/TestPyramid.html),
    where UI tests are considered slow and expensive, does not apply anymore.
    This can have a huge impact on your development speed, quality and confidence.
''')

tiles = [
    (section_text_elements, '''
        Elements like `ui.label`, `ui.markdown`, `ui.restructured_text` and `ui.html` can be used to display text and other content.
    '''),
    (section_controls, '''
        NiceGUI provides a variety of elements for user interaction, e.g. `ui.button`, `ui.slider`, `ui.inputs`, etc.
    '''),
    (section_audiovisual_elements, '''
        You can use elements like `ui.image`, `ui.audio`, `ui.video`, etc. to display audiovisual content.
    '''),
    (section_data_elements, '''
        There are several elements for displaying data, e.g. `ui.table`, `ui.aggrid`, `ui.highchart`, `ui.echart`, etc.
    '''),
    (section_binding_properties, '''
        To update UI elements automatically, you can bind them to each other or to your data model.
    '''),
    (section_page_layout, '''
        This section covers fundamental techniques as well as several elements to structure your UI.
    '''),
    (section_styling_appearance, '''
        NiceGUI allows to customize the appearance of UI elements in various ways, including CSS, Tailwind CSS and Quasar properties.
    '''),
    (section_action_events, '''
        This section covers timers, UI events, and the lifecycle of NiceGUI apps.
    '''),
    (section_pages_routing, '''
        A NiceGUI app can consist of multiple pages and other FastAPI endpoints.
    '''),
    (section_configuration_deployment, '''
        Whether you want to run your app locally or on a server, native or in a browser, we got you covered.
    '''),
    (section_testing, '''
        Write automated UI tests which run in a headless browser (slow) or fully simulated in Python (fast).
     '''),
]


@doc.extra_column
def create_tiles():
    with ui.row().classes('items-center content-between'):
        ui.label('If you like NiceGUI, go and become a')
        ui.html('<iframe src="https://github.com/sponsors/zauberzeug/button" title="Sponsor zauberzeug" height="32" width="114" style="border: 0; border-radius: 6px;"></iframe>')
    for documentation, description in tiles:
        page = doc.get_page(documentation)
        with ui.link(target=f'/documentation/{page.name}') \
                .classes('bg-[#5898d420] p-4 self-stretch rounded flex flex-col gap-2') \
                .style('box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1)'):
            if page.title:
                ui.label(page.title.replace('*', '')).classes(replace='text-2xl')
            ui.markdown(description).classes(replace='bold-links arrow-links')


@doc.ui
def map_of_nicegui():
    ui.separator().classes('mt-6')
    subheading('Map of NiceGUI', anchor_name='map-of-nicegui')
    ui.add_css('''
        .map-of-nicegui a code {
            font-weight: bold;
        }
    ''')
    ui.markdown('''
        This overview shows the structure of NiceGUI.
        It is a map of the NiceGUI namespace and its contents.
        It is not exhaustive, but it gives you a good idea of what is available.
        An ongoing goal is to make this map more complete and to add missing links to the documentation.

        #### `ui`

        UI elements and other essentials to run a NiceGUI app.

        - [`ui.element`](/documentation/element): base class for all UI elements
            - customization:
                - `.props()` and [`.default_props()`](/documentation/element#default_props): add Quasar props and regular HTML attributes
                - `.classes()` and [`.default_classes()`](/documentation/element#default_classes): add Quasar, Tailwind and custom HTML classes
                - [`.tailwind`](/documentation/section_styling_appearance#tailwind_css): convenience API for adding Tailwind classes
                - `.style()` and [`.default_style()`](/documentation/element#default_style): add CSS style definitions
                - [`.tooltip()`](/documentation/tooltip): add a tooltip to an element
                - [`.mark()`](/documentation/element_filter#markers): mark an element for querying with an [ElementFilter](/documentation/element_filter)
            - interaction:
                - [`.on()`](/documentation/generic_events): add Python and JavaScript event handlers
                - `.update()`: send an update to the client (mostly done automatically)
                - `.run_method()`: run a method on the client side
                - `.get_computed_prop()`: get the value of a property that is computed on the client side
            - hierarchy:
                - `with ...:` nesting elements in a declarative way
                - `__iter__`: an iterator over all child elements
                - `ancestors`: an iterator over the element's parent, grandparent, etc.
                - `descendants`: an iterator over all child elements, grandchildren, etc.
                - `slots`: a dictionary of named slots
                - `add_slot`: fill a new slot with NiceGUI elements or a scoped slot with template strings
                - [`clear`](/documentation/section_page_layout#clear_containers): remove all child elements
                - [`move`](/documentation/element#move_elements): move an element to a new parent
                - `remove`: remove a child element
                - `delete`: delete an element and all its children
                - `is_deleted`: whether an element has been deleted
        - elements:
            - [`ui.aggrid`](/documentation/aggrid)
            - [`ui.audio`](/documentation/audio)
            - [`ui.avatar`](/documentation/avatar)
            - [`ui.badge`](/documentation/badge)
            - [`ui.button`](/documentation/button)
            - [`ui.button_group`](/documentation/button_group)
            - [`ui.card`](/documentation/card), `ui.card_actions`, `ui.card_section`
            - [`ui.carousel`](/documentation/carousel), `ui.carousel_slide`
            - [`ui.chat_message`](/documentation/chat_message)
            - [`ui.checkbox`](/documentation/checkbox)
            - [`ui.chip`](/documentation/chip)
            - [`ui.circular_progress`](/documentation/circular_progress)
            - [`ui.code`](/documentation/code)
            - [`ui.codemirror`](/documentation/codemirror)
            - [`ui.color_input`](/documentation/color_input)
            - [`ui.color_picker`](/documentation/color_picker)
            - [`ui.column`](/documentation/column)
            - [`ui.context_menu`](/documentation/context_menu)
            - [`ui.date`](/documentation/date)
            - [`ui.dialog`](/documentation/dialog)
            - [`ui.dropdown_button`](/documentation/button_dropdown)
            - [`ui.echart`](/documentation/echart)
            - [`ui.editor`](/documentation/editor)
            - [`ui.expansion`](/documentation/expansion)
            - [`ui.grid`](/documentation/grid)
            - [`ui.highchart`](/documentation/highchart)
            - [`ui.html`](/documentation/html)
            - [`ui.icon`](/documentation/icon)
            - [`ui.image`](/documentation/image)
            - [`ui.input`](/documentation/input)
            - [`ui.interactive_image`](/documentation/interactive_image)
            - `ui.item`, `ui.item_label`, `ui.item_section`
            - [`ui.joystick`](/documentation/joystick)
            - [`ui.json_editor`](/documentation/json_editor)
            - [`ui.knob`](/documentation/knob)
            - [`ui.label`](/documentation/label)
            - [`ui.leaflet`](/documentation/leaflet)
            - [`ui.line_plot`](/documentation/line_plot)
            - [`ui.linear_progress`](/documentation/linear_progress)
            - [`ui.link`](/documentation/link), `ui.link_target`
            - [`ui.list`](/documentation/list)
            - [`ui.log`](/documentation/log)
            - [`ui.markdown`](/documentation/markdown)
            - [`ui.matplotlib`](/documentation/matplotlib)
            - [`ui.menu`](/documentation/menu), `ui.menu_item`
            - [`ui.mermaid`](/documentation/mermaid)
            - [`ui.notification`](/documentation/notification)
            - [`ui.number`](/documentation/number)
            - [`ui.pagination`](/documentation/pagination)
            - [`ui.plotly`](/documentation/plotly)
            - [`ui.pyplot`](/documentation/pyplot)
            - [`ui.radio`](/documentation/radio)
            - [`ui.range`](/documentation/range)
            - [`ui.restructured_text`](/documentation/restructured_text)
            - [`ui.row`](/documentation/row)
            - [`ui.scene`](/documentation/scene), [`ui.scene_view`](/documentation/scene#scene_view)
            - [`ui.scroll_area`](/documentation/scroll_area)
            - [`ui.select`](/documentation/select)
            - [`ui.separator`](/documentation/separator)
            - [`ui.skeleton`](/documentation/skeleton)
            - [`ui.slider`](/documentation/slider)
            - [`ui.space`](/documentation/space)
            - [`ui.spinner`](/documentation/spinner)
            - [`ui.splitter`](/documentation/splitter)
            - [`ui.stepper`](/documentation/stepper), `ui.step`, `ui.stepper_navigation`
            - [`ui.switch`](/documentation/switch)
            - [`ui.tabs`](/documentation/tabs), `ui.tab`, `ui.tab_panels`, `ui.tab_panel`
            - [`ui.table`](/documentation/table)
            - [`ui.textarea`](/documentation/textarea)
            - [`ui.time`](/documentation/time)
            - [`ui.timeline`](/documentation/timeline), `ui.timeline_entry`
            - [`ui.toggle`](/documentation/toggle)
            - [`ui.tooltip`](/documentation/tooltip)
            - [`ui.tree`](/documentation/tree)
            - [`ui.upload`](/documentation/upload)
            - [`ui.video`](/documentation/video)
        - special layout [elements](/documentation/page_layout):
            - `ui.header`
            - `ui.footer`
            - `ui.drawer`, `ui.left_drawer`, `ui.right_drawer`
            - `ui.page_sticky`
        - special functions and objects:
            - [`ui.add_body_html`](/documentation/section_pages_routing#add_html_to_the_page) and
                [`ui.add_head_html`](/documentation/section_pages_routing#add_html_to_the_page): add HTML to the body and head of the page
            - [`ui.add_css`](/documentation/add_style#add_css_style_definitions_to_the_page),
                [`ui.add_sass`](/documentation/add_style#add_sass_style_definitions_to_the_page) and
                [`ui.add_scss`](/documentation/add_style#add_scss_style_definitions_to_the_page): add CSS, SASS and SCSS to the page
            - [`ui.clipboard`](/documentation/clipboard): interact with the browser's clipboard
            - [`ui.colors`](/documentation/colors): define the main color theme for a page
            - `ui.context`: get the current UI context including the `client` and `request` objects
            - [`ui.dark_mode`](/documentation/dark_mode): get and set the dark mode on a page
            - [`ui.download`](/documentation/download): download a file to the client
            - [`ui.keyboard`](/documentation/keyboard): define keyboard event handlers
            - [`ui.navigate`](/documentation/navigate): let the browser navigate to another location
            - [`ui.notify`](/documentation/notification): show a notification
            - [`ui.on`](/documentation/generic_events#custom_events): register an event handler
            - [`ui.page_title`](/documentation/page_title): change the current page title
            - [`ui.query`](/documentation/query): query HTML elements on the client side to modify props, classes and style definitions
            - [`ui.run`](/documentation/run) and `ui.run_with`: run the app (standalone or attached to a FastAPI app)
            - [`ui.run_javascript`](/documentation/run#run_custom_javascript_on_the_client_side): run custom JavaScript on the client side (can use `getElement()`, `getHtmlElement()`, and `emitEvent()`)
            - [`ui.teleport`](/documentation/teleport): teleport an element to a different location in the HTML DOM
            - [`ui.timer`](/documentation/timer): run a function periodically or once after a delay
            - `ui.update`: send updates of multiple elements to the client
        - decorators:
            - [`ui.page`](/documentation/page): define a page (in contrast to the automatically generated "auto-index page")
            - [`ui.refreshable`](/documentation/refreshable), `ui.refreshable_method`: define refreshable UI containers
                (can use [`ui.state`](/documentation/refreshable#refreshable_ui_with_reactive_state))

        #### `app`

        App-wide storage, mount points and lifecycle hooks.

        - [`app.storage`](/documentation/storage):
            - `app.storage.tab`: stored in memory on the server, unique per tab
            - `app.storage.client`: stored in memory on the server, unique per client connected to a page
            - `app.storage.user`: stored in a file on the server, unique per browser
            - `app.storage.general`: stored in a file on the server, shared across the entire app
            - `app.storage.browser`: stored in the browser's local storage, unique per browser
        - [lifecycle hooks](/documentation/section_action_events#events):
            - `app.on_connect()`: called when a client connects
            - `app.on_disconnect()`: called when a client disconnects
            - `app.on_startup()`: called when the app starts
            - `app.on_shutdown()`: called when the app shuts down
            - `app.on_exception()`: called when an exception occurs
        - [`app.shutdown()`](/documentation/section_action_events#shut_down_nicegui): shut down the app
        - static files:
            - [`app.add_static_files()`](/documentation/section_pages_routing#add_a_directory_of_static_files),
                `app.add_static_file()`: serve static files
            - [`app.add_media_files()`](/documentation/section_pages_routing#add_directory_of_media_files),
                `app.add_media_file()`: serve media files (supports streaming)
        - [`app.native`](/documentation/section_configuration_deployment#native_mode): configure the app when running in native mode

        #### `html`

        [Pure HTML elements](/documentation/html#other_html_elements):

        `a`,
        `abbr`,
        `acronym`,
        `address`,
        `area`,
        `article`,
        `aside`,
        `audio`,
        `b`,
        `basefont`,
        `bdi`,
        `bdo`,
        `big`,
        `blockquote`,
        `br`,
        `button`,
        `canvas`,
        `caption`,
        `cite`,
        `code`,
        `col`,
        `colgroup`,
        `data`,
        `datalist`,
        `dd`,
        `del_`,
        `details`,
        `dfn`,
        `dialog`,
        `div`,
        `dl`,
        `dt`,
        `em`,
        `embed`,
        `fieldset`,
        `figcaption`,
        `figure`,
        `footer`,
        `form`,
        `h1`,
        `header`,
        `hgroup`,
        `hr`,
        `i`,
        `iframe`,
        `img`,
        `input_`,
        `ins`,
        `kbd`,
        `label`,
        `legend`,
        `li`,
        `main`,
        `map_`,
        `mark`,
        `menu`,
        `meter`,
        `nav`,
        `object_`,
        `ol`,
        `optgroup`,
        `option`,
        `output`,
        `p`,
        `param`,
        `picture`,
        `pre`,
        `progress`,
        `q`,
        `rp`,
        `rt`,
        `ruby`,
        `s`,
        `samp`,
        `search`,
        `section`,
        `select`,
        `small`,
        `source`,
        `span`,
        `strong`,
        `sub`,
        `summary`,
        `sup`,
        `svg`,
        `table`,
        `tbody`,
        `td`,
        `template`,
        `textarea`,
        `tfoot`,
        `th`,
        `thead`,
        `time`,
        `tr`,
        `track`,
        `u`,
        `ul`,
        `var`,
        `video`,
        `wbr`

        #### `background_tasks`

        Run async functions in the background.

        - `create()`: create a background task
        - `create_lazy()`: prevent two tasks with the same name from running at the same time

        #### `run`

        Run IO and CPU bound functions in separate threads and processes.

        - [`run.cpu_bound()`](/documentation/section_action_events#running_cpu-bound_tasks): run a CPU-bound function in a separate process
        - [`run.io_bound()`](/documentation/section_action_events#running_i_o-bound_tasks): run an IO-bound function in a separate thread

        #### `binding`

        [Bind properties of objects to each other](/documentation/section_binding_properties).

        - [`binding.BindableProperty`](/documentation/section_binding_properties#bindable_properties_for_maximum_performance): bindable properties for maximum performance
        - [`binding.bindable_dataclass()`](/documentation/section_binding_properties#bindable_dataclass): create a dataclass with bindable properties
        - `binding.bind()`, `binding.bind_from()`, `binding.bind_to()`: methods to bind two properties

        #### `observables`

        Observable collections that notify observers when their contents change.

        - `ObservableCollection`: base class
        - `ObservableDict`: an observable dictionary
        - `ObservableList`: an observable list
        - `ObservableSet`: an observable set

        #### `testing`

        Write automated UI tests which run in a headless browser (slow) or fully simulated in Python (fast).

        - [`Screen`](/documentation/section_testing#screen_fixture) fixture: start a real (headless) browser to interact with your application
        - [`User`](/documentation/section_testing#user_fixture) fixture: simulate user interaction on a Python level (fast)
    ''').classes('map-of-nicegui arrow-links bold-links')
