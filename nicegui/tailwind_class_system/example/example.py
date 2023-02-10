from Typography import Typography
from Backgrounds import Backgrounds
from Sizing import Sizing
from nicegui import ui

# STYLE LIB

s_title = (
    Typography()
    .text_color("text-teal-600")
    .font_size("text-6xl")
    .text_transform("uppercase")
    .text_align("text-center")
)

s_full_width = Sizing().width("w-full")

# PROG


@ui.page("/")
async def page():
    with ui.left_drawer() as sidebar:
        page_title = ui.label("Title")

    with ui.card() as main:
        ui.label("Lorem Ipsum")
        ui.separator()

        with ui.row() as btns:
            btn1 = (
                Typography(ui.button("btn1"))
                .text_color("text-amber-700")
                .element.tooltip("btn1")
            )
            btn2 = (
                Typography(ui.button("btn2"))
                .text_color("text-orange-900")
                .element.tooltip("btn2")
            )

    # Aplying styles
    s_title.apply(page_title)

    s_full_width.apply(main)
    s_full_width.apply(btns)

    Backgrounds(main).background_color("bg-lime-300")
    Backgrounds(sidebar).background_color("bg-orange-300")


ui.run()
