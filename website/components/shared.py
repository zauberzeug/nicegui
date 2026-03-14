"""Shared helper functions for consistent section structure across main page components."""

from collections.abc import Iterator
from contextlib import contextmanager

from nicegui import ui

from ..style import link_target

# ---------------------------------------------------------------------------
# Section container
# ---------------------------------------------------------------------------

@contextmanager
def section(anchor: str = '', *, classes: str = '', offset: str = '0') -> Iterator[None]:
    """Consistent full-width section wrapper with max-width inner container.

    Every page section should use this to guarantee identical padding and
    max-width.  Extra *classes* are appended to the outer ``<section>`` element
    (useful for custom backgrounds like ``mo-sponsors-bg``).

    Usage::

        with section('features'):
            section_heading('features', 'Code nicely.', 'Everything you need …')
            ...
    """
    with ui.element('section').classes(f'mo-section-outer {classes}'):
        if anchor:
            link_target(anchor, offset)
        with ui.column().classes('mo-section-inner'):
            yield


# ---------------------------------------------------------------------------
# Section heading helpers
# ---------------------------------------------------------------------------

def section_label(text: str) -> ui.label:
    """Render a monospace section label like ``# get_started``.

    The ``#`` prefix is added via CSS ``::before``.
    """
    return ui.label(text).classes('mo-section-label')


def section_title(text: str) -> ui.label:
    """Render a large section title."""
    return ui.label(text).classes('mo-section-title')


def section_desc(text: str) -> ui.label:
    """Render a section description paragraph."""
    return ui.label(text).classes('mo-section-desc')


def section_heading(label: str, title: str, description: str = '', *, center: bool = False) -> None:
    """Render a grouped section heading (label + title + optional description)."""
    extra = ' items-center text-center' if center else ''
    with ui.column().classes(f'mo-reveal gap-0{extra}'):
        section_label(label)
        section_title(title)
        if description:
            section_desc(description)


# ---------------------------------------------------------------------------
# Code / browser window helpers
# ---------------------------------------------------------------------------

def code_window(filename: str, icon: str, code_html: str) -> None:
    """Render a styled code window with filename header and syntax-highlighted body."""
    with ui.column().classes('mo-code-window gap-0'):
        with ui.row().classes('mo-code-header items-center'):
            ui.icon(icon).classes('text-base')
            ui.label(filename).classes('mo-code-filename')
        ui.html(f'<div class="mo-code-body">{code_html}</div>', sanitize=False)


def browser_window(url: str = 'localhost:8080') -> ui.column:
    """Render a styled browser preview window.  Use as context manager to add content."""
    col = ui.column().classes('mo-browser-window gap-0')
    with col:
        with ui.row().classes('mo-browser-header items-center'):
            ui.icon('language').classes('text-base')
            ui.label(url).classes('mo-browser-tab')
    return col
