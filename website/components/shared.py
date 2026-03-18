from collections.abc import Iterator
from contextlib import contextmanager

from nicegui import ui

from ..style import link_target


@contextmanager
def section(anchor: str, *, classes: str = '') -> Iterator[None]:
    """Full-width section wrapper with max-width inner container."""
    with ui.element('section').classes(f'w-full py-20 first:pt-[120px] px-6 {classes}'):
        link_target(anchor)
        with ui.column().classes('max-w-[1280px] mx-auto w-full gap-0'):
            yield


def section_label(text: str) -> ui.label:
    """Monospace section label like ``# get_started``."""
    return ui.label(f'# {text}').classes('font-mono text-[0.8rem] font-medium tracking-wide text-(--mo-text-muted)')


def section_title(text: str) -> ui.label:
    """Large section title."""
    return ui.label(text) \
        .classes('text-[clamp(1.8rem,3vw,3rem)] font-semibold tracking-tight leading-tight mb-3 text-(--mo-text-primary)')


def section_desc(text: str) -> ui.label:
    """Section description paragraph."""
    return ui.label(text) \
        .classes('text-[1.0625rem] max-w-[640px] leading-relaxed mb-12 text-(--mo-text-secondary)')


def section_heading(label: str, title: str, description: str = '', *, center: bool = False) -> None:
    """Grouped section heading (label + title + optional description)."""
    extra = 'items-center text-center' if center else ''
    with ui.column().classes(f'mo-reveal gap-0 w-full {extra}'):
        section_label(label)
        section_title(title)
        if description:
            section_desc(description)
