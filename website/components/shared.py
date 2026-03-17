"""Shared helper functions and reusable UI components for the main page."""

from collections.abc import Iterator
from contextlib import contextmanager

from nicegui import ui

from ..style import link_target

# ---------------------------------------------------------------------------
# Section container
# ---------------------------------------------------------------------------


@contextmanager
def section(anchor: str = '', *, classes: str = '', offset: str = '0') -> Iterator[None]:
    """Full-width section wrapper with max-width inner container.

    *classes* are appended to the outer ``<section>`` (for custom backgrounds).
    """
    with ui.element('section').classes(f'w-full py-20 first:pt-[120px] px-6 {classes}'):
        if anchor:
            link_target(anchor, offset)
        with ui.column().classes('max-w-[1280px] mx-auto w-full gap-0'):
            yield


# ---------------------------------------------------------------------------
# Section heading helpers
# ---------------------------------------------------------------------------

def section_label(text: str) -> ui.label:
    """Monospace section label like ``# get_started``."""
    return ui.label(text).classes(
        'mo-section-label font-mono text-[0.8rem] font-medium tracking-wide'
    ).style('color: var(--mo-text-muted)')


def section_title(text: str) -> ui.label:
    """Large section title."""
    return ui.label(text).classes(
        'text-[clamp(1.8rem,3vw,3rem)] font-semibold tracking-tight leading-tight mb-3'
    ).style('color: var(--mo-text-primary)')


def section_desc(text: str) -> ui.label:
    """Section description paragraph."""
    return ui.label(text).classes(
        'text-[1.0625rem] max-w-[640px] leading-relaxed mb-12'
    ).style('color: var(--mo-text-secondary)')


def section_heading(label: str, title: str, description: str = '', *, center: bool = False) -> None:
    """Grouped section heading (label + title + optional description)."""
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
    """Styled code window with filename header and syntax-highlighted body."""
    with ui.column().classes('rounded-xl overflow-hidden font-mono text-sm leading-relaxed gap-0') \
            .style('background: var(--mo-code-bg)'):
        with ui.row().classes('items-center justify-between px-4 py-2.5') \
                .style('border-bottom: 1px solid var(--mo-border)'):
            with ui.row().classes('items-center gap-2 text-[0.8125rem]') \
                    .style('color: var(--mo-text-muted)'):
                ui.icon(icon).classes('text-base')
                ui.label(filename)
        ui.html(f'<div class="mo-code-body" style="padding: 16px 20px; overflow-x: auto; white-space: pre; color: var(--mo-text-primary)">{code_html}</div>', sanitize=False)


def browser_window(url: str = 'localhost:8080') -> ui.column:
    """Styled browser preview window. Use as context manager to add content."""
    col = ui.column().classes(
        'rounded-xl overflow-hidden gap-0'
    ).style('background: var(--mo-surface); border: 1px solid var(--mo-border)')
    with col:
        with ui.row().classes('items-center px-4 py-2.5') \
                .style('border-bottom: 1px solid var(--mo-border)'):
            with ui.row().classes('items-center gap-2 text-[0.8125rem]') \
                    .style('color: var(--mo-text-muted)'):
                ui.icon('language').classes('text-base')
                ui.label(url)
    return col
