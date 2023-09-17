from nicegui import ui
from fontColor import FontColor

ui.markdown("""### Any easy way to import a style file on every page
[discussion thread with code snippet](https://github.com/zauberzeug/nicegui/discussions/1631)
""")

with FontColor():
    ui.markdown("""
        ## Home page
        bg color is red
    """)


@ui.page("/other")
def index():
    # this page not work
    with FontColor():
        ui.markdown("""
            ## Other page
            bg color is also red
        """)

ui.run()