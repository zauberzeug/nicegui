#!/usr/bin/env python3
from io import BytesIO
from pathlib import Path

import cairo

from nicegui import ui

PDF_PATH = Path('output.pdf')


def generate_svg() -> str:
    output = BytesIO()
    surface = cairo.SVGSurface(output, 300, 200)
    draw(surface)
    surface.finish()
    return output.getvalue().decode('utf-8')


def generate_pdf() -> bytes:
    output = BytesIO()
    surface = cairo.PDFSurface(output, 300, 200)
    draw(surface)
    surface.finish()
    return output.getvalue()


def draw(surface: cairo.SVGSurface) -> None:
    context = cairo.Context(surface)
    context.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    context.set_font_size(20)
    context.move_to(10, 40)
    context.show_text(name.value)
    context.move_to(10, 80)
    context.show_text(email.value)


def update() -> None:
    preview.content = generate_svg()
    PDF_PATH.write_bytes(generate_pdf())


with ui.row():
    with ui.column():
        name = ui.input('Name', placeholder='Enter your name', on_change=update)
        email = ui.input('E-Mail', placeholder='Enter your E-Mail address', on_change=update)
    preview = ui.html().classes('border-2 border-gray-500')
    update()
    ui.button('Download PDF', on_click=lambda: ui.download(PDF_PATH)).bind_visibility_from(name, 'value')

ui.run()
