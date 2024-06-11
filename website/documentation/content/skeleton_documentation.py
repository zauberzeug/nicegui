from nicegui import ui

from . import doc


@doc.demo(ui.skeleton)
def skeleton():
    ui.skeleton('QBtn').props("bordered square").classes("bg-slate-300")


@doc.demo("Animations",
           """How to define custom animations for a skeleton.

The `animation` prop can be set to any of the following values:

- pulse
- wave
- pulse-x
- pulse-y
- fade
- blink
- none

The default value is `wave`.
            
           """)
def custom_animations():
    ui.skeleton('QToolbar').props("animation='pulse'").classes("bg-slate-300 w-full")
    

@doc.demo("Youtube Skeleton", """
          A skeleton for a Youtube video, modified to fit the NiceGUI framework.
""")
def youtube_skeleton():
    with ui.card().props("flat").style("width: 100%;"):
        ui.skeleton("square").style("height: 150px; width: 100%;").classes("bg-slate-300").props("animation='fade'")

        with ui.card_section().style("width: 100%;"):
            ui.skeleton("text").classes("text-subtitle1 bg-slate-300")
            ui.skeleton("text").classes("text-subtitle1 w-1/2 bg-slate-300")
            ui.skeleton("text").classes("text-caption bg-slate-300")