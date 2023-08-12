from io import BytesIO
from pathlib import Path

import cairo

from nicegui import ui


def generate_svg() -> str:
    output = BytesIO()
    surface = cairo.SVGSurface(output, 200, 150)
    draw(surface)
    surface.finish()
    return output.getvalue().decode('utf-8')


def generate_pdf() -> bytes:
    output = BytesIO()
    surface = cairo.PDFSurface(output, 200, 150)
    draw(surface)
    surface.finish()
    return output.getvalue()


def draw(surface: cairo.SVGSurface):
    context = cairo.Context(surface)

    context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    context.set_font_size(20)
    context.move_to(10, 40)
    context.show_text(f"{name_input.value}")
    context.move_to(10, 80)
    context.show_text(f"{email_input.value}")


def update():
    preview.content = generate_svg()
    Path('output.pdf').write_bytes(generate_pdf())


with ui.row().classes('items-stretch gap-12'):
    with ui.column():
        name_input = ui.input("Name", placeholder="Enter your name", on_change=update)
        email_input = ui.input("E-Mail", placeholder="Enter your E-Mail address", on_change=update)
    with ui.column():
        preview = ui.html().classes('w-[400px] h-[300px] border-2 border-gray-500')
    with ui.column():
        ui.button("Download PDF", on_click=lambda: ui.download('output.pdf'))\
            .bind_visibility_from(preview, 'content')

ui.run()
