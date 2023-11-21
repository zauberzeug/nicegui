from typing import Dict

from nicegui import ui

from .section import Section
from .sections import (action_events, audiovisual_elements, binding_properties, configuration_deployment, controls,
                       data_elements, page_layout, pages_routing, styling_appearance, text_elements)
from .tools import heading

SECTIONS: Dict[str, Section] = {
    section.name: section
    for section in [
        text_elements,
        controls,
        audiovisual_elements,
        data_elements,
        binding_properties,
        page_layout,
        styling_appearance,
        action_events,
        pages_routing,
        configuration_deployment,
    ]
}


def create_overview() -> None:
    ui.markdown('''
        ### Overview
                                
        NiceGUI is an open-source Python library to write graphical user interfaces which run in the browser.
        It has a very gentle learning curve while still offering the option for advanced customizations.
        NiceGUI follows a backend-first philosophy: it handles all the web development details.
        You can focus on writing Python code. 
        This makes it ideal for a wide range of projects including short 
        scripts, dashboards, robotics projects, IoT solutions, smart home automation, and machine learning.

        ### How to use this guide

        This documentation explains how to use nicegui.
        Each of the tiles sections cover a NiceGUI topic in detail.
        It is recommended to start by reading this entire introduction page, then refer to other sections as needed.

        ### Basic concepts

        NiceGUI provides UI _components_ (or _elements_) such as buttons, sliders, text, images, charts, and more.
        Your app assembles these components into _pages_.
        When the user interacts with an item on a page, nicegui triggers an _event_ (or _action_).
        You define code to _handle_ each event, such as what to do when a user clicks a button named `Go`.

        Components are arranged on a page using _layouts_.
        Layouts provide things like grids, tabs, carousels, expansions, menus, and other tools to arrange your components.
        Many components are linked to a _model_ (data object) in your code, which automatically updates the user interface when the value changes.

        Styling and appearance can be controlled in several ways.
        Nicegui accepts optional arguments for certain styling, such as icons on buttons.
        Other styling can be set with functions such as .styles, .classes, or .props that you'll learn about later.
        Global styles like colors and fonts can be set with dedicated properties.
        Or if you prefer, almost anything can be styled with css.
    ''')
    with ui.grid().classes('grid-cols-[1fr] md:grid-cols-[1fr_1fr] xl:grid-cols-[1fr_1fr_1fr]'):
        for section in SECTIONS.values():
            with ui.link(target=f'/documentation/section_{section.name}/') \
                    .classes('bg-[#5898d420] p-4 self-stretch rounded flex flex-col gap-2') \
                    .style('box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1)'):
                ui.label(section.title).classes(replace='text-2xl')
                ui.markdown(section.description).classes(replace='bold-links arrow-links')

    ui.markdown('''### Actions

    Nicegui runs an event loop to handle user input and other events like timers and keyboard bindings.
    You can write asynchronous functions for long-running tasks to keep the UI responsive.
    The _Actions_ section covers how to work with events.

    ### Implementation
    
    NiceGUI is implemented with html components served by an http server (FastAPI), even for native windows.
    If you already know html, everything will feel very familiar.
    If you don't know html, that's fine too!
    Nicegui abstracts away the details, so you can focus on creating beautiful interfaces without worrying about how they are implemented.

    ### Running Nicegui Apps

    There are several options for deploying NiceGUI.
    By default, NiceGUI runs a server on localhost and runs your app as a private web page on the local machine.
    When run this way, your app appears in a web browser window.
    You can also run NiceGUI in a native window separate from a web browser.
    Or you can run NiceGUI on a server that handles many clients - the website you're reading right now is served from NiceGUI.

    After creating your app pages with components, you call `ui.run()` to start the nicegui server.
    Optional parameters to `ui.run` set things like the network address and port the server binds to, 
    whether the app runs in native mode, initial window size, and many other options.
    The section _Configuration and Deployment_ covers the options to the `ui.run()` function and the FastAPI framework its based on.

    ### Customization

    If you want more customization in your app, you can use the underlying Tailwind classes and Quasar components
    to control the style or behavior of your components.
    You can also extend the available components by subclassing existing nicegui components or importing new ones from Quasar.
    All of this is optional.
    Out of the box, NiceGUI provides everything you need to make modern, stylish, responsive user interfaces.
    ''')


def create_section(name: str) -> None:
    section = SECTIONS[name]
    heading(section.title)
    section.content()
