from typing import List, Tuple

from nicegui import ui

from ..content.sections.controls import ControlsDocumentation
from ..content.sections.text_elements import TextElementsDocumentation
from ..model import Documentation, SectionDocumentation


class Overview(Documentation):

    def __init__(self) -> None:
        super().__init__('/documentation/', subtitle='Reference, Demos and more', title='*NiceGUI* Documentation')

    def content(self) -> None:
        self.add_markdown('Overview', '''
            NiceGUI is an open-source Python library to write graphical user interfaces which run in the browser.
            It has a very gentle learning curve while still offering the option for advanced customizations.
            NiceGUI follows a backend-first philosophy:
            It handles all the web development details.
            You can focus on writing Python code. 
            This makes it ideal for a wide range of projects including short 
            scripts, dashboards, robotics projects, IoT solutions, smart home automation, and machine learning.
        ''')

        self.add_markdown('How to use this guide', '''
            This documentation explains how to use NiceGUI.
            Each of the tiles covers a NiceGUI topic in detail.
            It is recommended to start by reading this entire introduction page, then refer to other sections as needed.
        ''')

        self.add_markdown('Basic concepts', '''
            NiceGUI provides UI _components_ (or _elements_) such as buttons, sliders, text, images, charts, and more.
            Your app assembles these components into _pages_.
            When the user interacts with an item on a page, NiceGUI triggers an _event_ (or _action_).
            You define code to _handle_ each event, such as what to do when a user clicks a button named "Go".

            Components are arranged on a page using _layouts_.
            Layouts provide things like grids, tabs, carousels, expansions, menus, and other tools to arrange your components.
            Many components are linked to a _model_ (data object) in your code, which automatically updates the user interface when the value changes.

            Styling and appearance can be controlled in several ways.
            NiceGUI accepts optional arguments for certain styling, such as icons on buttons.
            Other styling can be set with functions such as `.styles`, `.classes`, or `.props` that you'll learn about later.
            Global styles like colors and fonts can be set with dedicated properties.
            Or if you prefer, almost anything can be styled with CSS.
        ''')

        tiles: List[Tuple[SectionDocumentation, str]] = [
            (TextElementsDocumentation(), '''
                Elements like `ui.label`, `ui.markdown` and `ui.html` can be used to display text and other content.
            '''),
            (ControlsDocumentation(), '''
                NiceGUI provides a variety of elements for user interaction, e.g. `ui.button`, `ui.slider`, `ui.inputs`, etc.
            '''),
        ]

        @self.add_raw_nicegui
        def create_tiles():
            with ui.grid().classes('grid-cols-[1fr] md:grid-cols-[1fr_1fr] xl:grid-cols-[1fr_1fr_1fr]'):
                for documentation, description in tiles:
                    with ui.link(target=documentation.route) \
                            .classes('bg-[#5898d420] p-4 self-stretch rounded flex flex-col gap-2') \
                            .style('box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1)'):
                        if documentation.title:
                            ui.label(documentation.title.replace('*', '')).classes(replace='text-2xl')
                        ui.markdown(description).classes(replace='bold-links arrow-links')

        self.add_markdown('Actions', '''
            NiceGUI runs an event loop to handle user input and other events like timers and keyboard bindings.
            You can write asynchronous functions for long-running tasks to keep the UI responsive.
            The _Actions_ section covers how to work with events.
        ''')

        self.add_markdown('Implementation', '''
            NiceGUI is implemented with HTML components served by an HTTP server (FastAPI), even for native windows.
            If you already know HTML, everything will feel very familiar.
            If you don't know HTML, that's fine too!
            NiceGUI abstracts away the details, so you can focus on creating beautiful interfaces without worrying about how they are implemented.
        ''')

        self.add_markdown('Running NiceGUI Apps', '''
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

        self.add_markdown('Customization', '''
            If you want more customization in your app, you can use the underlying Tailwind classes and Quasar components
            to control the style or behavior of your components.
            You can also extend the available components by subclassing existing NiceGUI components or importing new ones from Quasar.
            All of this is optional.
            Out of the box, NiceGUI provides everything you need to make modern, stylish, responsive user interfaces.
        ''')
