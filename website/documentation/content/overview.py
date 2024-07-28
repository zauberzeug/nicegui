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
    section_text_elements,
)

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
    Elements can also be bound to a _model_ (data object), which automatically updates the user interface when the value changes.

    Elements are arranged on a page using a "declarative UI" or "code-based UI".
    That means that you also write structures like grids, cards, tabs, carousels, expansions, menus, and other layout elements directly in code.
    This concept has been made popular with Flutter and SwiftUI.
    For readability, NiceGUI utilizes Pythons `with ...` statement.
    This context mangers provides a nice way to indent the code to resemble the layout of the UI.

    Styling and appearance can be controlled in several ways.
    Most elements accepts optional arguments for common styling and behavior changes, such as icons on buttons or color of a text.
    Because NiceGUI is a web framework, you can change almost any appearance of an element with CSS.
    But elements also provide `.classes` and `.props` methods to apply Tailwind CSS and Quasar properties
    which are more high level and simpler to use day-to-day after you get the hang of it.
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
