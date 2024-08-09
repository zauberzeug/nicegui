from nicegui import context
from nicegui import ui
from nicegui.anchor import bottom
from nicegui.anchor import parent
from nicegui.anchor import previous
from nicegui.anchor import right
from nicegui.anchor import width

context.client.content.classes("h-[100vh]")

ui.page_title("Anchor demo")

def main():
    with ui.element().classes("w-full h-full"):
        with ui.element().classes("bg-primary").at.top.fit_height as top_bar:
            ui.icon("home", size="lg", color="white").at.top_left
            ui.label("SAMPLE APP").style("margin: 10px").at.center.tailwind.text_color("white")
            ui.button(icon="menu").at.top_right
        with ui.element().at.bottom_left.a(top=bottom(top_bar)).classes("bg-primary") as drawer:
            add_left_drawer_items()
        with ui.element().at.bottom_right.a(top=bottom(top_bar), left=right(drawer)) as content_area:
            with ui.element().at.center.fit_height.a(width=max(width(parent)/3, 200)):
                input_with_id(placeholder="Username").at.top
                input_with_id(placeholder="Password").at.below(previous).a(width=width(previous))
                ui.button("Login").at.below(previous)
        ui.button(icon="add").at.bottom_right.props("fab")


def add_left_drawer_items():
    with ui.list().props("separator").classes("text-white").style("margin: 10px"):
        ui.item("Sections").props("header").classes("text-bold")
        for i in range(1, 5):
            with ui.item():
                with ui.item_section().props("avatar"):
                    ui.icon("chevron_right")
                with ui.item_section():
                    ui.item_label(f"Section {i}")

def input_with_id(*args, **kwargs):
    with ui.element() as wrapper:
        ui.input(*args, **kwargs).classes("w-full")
    return wrapper


main()

ui.run()
