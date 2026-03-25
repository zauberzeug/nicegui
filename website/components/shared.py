from collections.abc import Callable, Iterator
from contextlib import contextmanager

from nicegui import ui

from .. import design as d
from ..design import phosphor_icon


@contextmanager
def section(anchor: str) -> Iterator[None]:
    """Full-width section wrapper with max-width inner container."""
    with ui.element('section').classes('w-full py-20 max-sm:px-6 min-sm:px-16'):
        ui.link_target(anchor).classes('scroll-mt-32')
        with ui.column().classes('max-w-[1280px] mx-auto w-full gap-0'):
            yield


def section_label(text: str) -> ui.label:
    """Monospace section label like ``# get_started``."""
    return ui.label(f'# {text}').classes(f'{d.TEXT_13PX_MONO} font-medium tracking-wide {d.TEXT_MUTED}')


def section_title(text: str) -> ui.label:
    """Large section title."""
    return ui.label(text) \
        .classes(f'{d.TEXT_SECTION_TITLE} font-semibold tracking-tight leading-tight mb-3 {d.TEXT_PRIMARY}')


def section_desc(text: str) -> ui.label:
    """Section description paragraph."""
    return ui.label(text) \
        .classes(f'{d.TEXT_19PX} max-w-[640px] leading-relaxed mb-12 {d.TEXT_SECONDARY}')


def cta_button(
    title: str, *,
    left_icon: str = '',
    right_icon: str = '',
    filled: bool = True,
    blue: bool = True,
    mono: bool = False,
    on_click: Callable,
) -> ui.button:
    """Styled CTA button with optional Phosphor icons."""
    with ui.button(on_click=on_click) \
            .props('unelevated no-caps rounded size=1rem') \
            .classes('px-7 py-2.5 transition-all duration-150 hover:-translate-y-px') as button:
        with ui.row(align_items='center').classes('gap-2'):
            if left_icon:
                phosphor_icon(left_icon)
            ui.label(title)
            if right_icon:
                phosphor_icon(right_icon).classes(d.TEXT_MUTED if not filled and not blue else '')

    if filled:
        button.classes(f'text-white {d.SHADOW_BLUE} {d.BG_BLUE if blue else d.BG_ACCENT}')
    else:
        button.classes(f'bg-transparent {d.TEXT_PRIMARY_IMPORTANT} {d.BORDER_BLUE if blue else d.BORDER_SUBTLE}')

    if mono:
        button.classes(d.TEXT_13PX_MONO)

    return button


def section_heading(label: str, title: str, description: str = '', *, center: bool = False) -> None:
    """Grouped section heading (label + title + optional description)."""
    extra = 'items-center text-center' if center else ''
    with ui.column().classes(f'reveal gap-0 w-full {extra}'):
        section_label(label)
        section_title(title)
        if description:
            section_desc(description)
