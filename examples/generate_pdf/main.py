#!/usr/bin/env python3
from io import BytesIO

import cairo

from nicegui import ui


def generate_svg() -> str:
    """
    Generate an SVG image using the Cairo library.

    This function creates an SVG image with a size of 300x200 pixels using the Cairo library.
    The image is drawn using the `draw` function, and the resulting SVG data is returned as a string.

    Returns:
        str: The SVG data as a string.

    Example:
        >>> svg_data = generate_svg()
        >>> print(svg_data)
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<svg width="300" height="200" ...'

    Note:
        This function requires the Cairo library to be installed.
    """
    output = BytesIO()
    surface = cairo.SVGSurface(output, 300, 200)
    draw(surface)
    surface.finish()
    return output.getvalue().decode('utf-8')

def generate_pdf() -> bytes:
    """
    Generates a PDF document and returns it as bytes.

    This function creates a PDF document using the Cairo library. It initializes a PDF surface with a width of 300
    units and a height of 200 units. It then calls the `draw` function to draw on the surface. Finally, it finishes
    the surface and returns the PDF document as bytes.

    Returns:
        bytes: The generated PDF document.

    Example:
        >>> pdf = generate_pdf()
        >>> with open('output.pdf', 'wb') as f:
        ...     f.write(pdf)
    """
    output = BytesIO()
    surface = cairo.PDFSurface(output, 300, 200)
    draw(surface)
    surface.finish()
    return output.getvalue()


def draw(surface: cairo.Surface) -> None:
    """
    Draw text on a Cairo surface.

    Args:
        surface (cairo.Surface): The Cairo surface to draw on.

    Returns:
        None

    Raises:
        None

    Usage:
        1. Create a Cairo surface to draw on.
        2. Call the draw function, passing in the surface as an argument.
        3. The function will draw text on the surface using the specified font, size, and position.
    """
    context = cairo.Context(surface)
    context.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    context.set_font_size(20)
    context.move_to(10, 40)
    context.show_text(name.value)
    context.move_to(10, 80)
    context.show_text(email.value)


def update() -> None:
    """
    Update the preview content by generating an SVG.

    This function calls the generate_svg() function to generate an SVG content
    and assigns it to the preview.content variable.

    Returns:
        None
    """
    preview.content = generate_svg()


with ui.row():
    with ui.column():
        name = ui.input('Name', placeholder='Enter your name', on_change=update)
        email = ui.input('E-Mail', placeholder='Enter your E-Mail address', on_change=update)
    preview = ui.html().classes('border-2 border-gray-500')
    update()
    ui.button('PDF', on_click=lambda: ui.download(generate_pdf(), 'output.pdf')).bind_visibility_from(name, 'value')

ui.run()
