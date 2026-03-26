"""Design constants and helpers for the NiceGUI website."""

import re

from nicegui import ui

SPECIAL_CHARACTERS = re.compile('[^(a-z)(A-Z)(0-9)-]')

# --- Raw color values ---

BLUE = '#5898d4'
BLUE_LIGHT = '#7ab4e4'
ACCENT = '#f0a050'

_BG_LIGHT = '#fafbfc'  # defined in style.css as well; keep in sync
_BG_DARK = '#0f1117'  # defined in style.css as well; keep in sync
_BG_SURFACE_LIGHT = '#ffffff'
_BG_SURFACE_DARK = '#181b23'
_BG_CODE_LIGHT = '#f0f4f8'
_BG_CODE_DARK = '#1e222c'
_BG_FOOTER_LIGHT = '#edf0f3'
_BG_FOOTER_DARK = f'color-mix(in_srgb,{_BG_DARK}_70%,black)'

_TEXT_PRIMARY_LIGHT = '#1a1d26'  # defined in style.css as well; keep in sync
_TEXT_PRIMARY_DARK = '#edeff3'  # defined in style.css as well; keep in sync
_TEXT_SECONDARY_LIGHT = '#4a4f5a'
_TEXT_SECONDARY_DARK = '#9ba2ae'
_TEXT_MUTED_LIGHT = '#7d8590'
_TEXT_MUTED_DARK = '#6b737e'

_BORDER_LIGHT = 'rgba(0,0,0,0.06)'
_BORDER_DARK = 'rgba(255,255,255,0.08)'

# --- Tailwind class fragments ---

# Backgrounds
BG = f'bg-[{_BG_LIGHT}] dark:bg-[{_BG_DARK}]'
BG_SURFACE = f'bg-[{_BG_SURFACE_LIGHT}] dark:bg-[{_BG_SURFACE_DARK}]'
BG_CODE = f'bg-[{_BG_CODE_LIGHT}] dark:bg-[{_BG_CODE_DARK}]'
BG_FOOTER = f'bg-[{_BG_FOOTER_LIGHT}] dark:bg-[{_BG_FOOTER_DARK}]'
BG_BLUE = f'bg-[{BLUE}]'
BG_ACCENT = f'bg-[{ACCENT}]'
BG_BORDER = f'bg-[{_BORDER_LIGHT}] dark:bg-[{_BORDER_DARK}]'

# Text
TEXT_PRIMARY = f'text-[{_TEXT_PRIMARY_LIGHT}] dark:text-[{_TEXT_PRIMARY_DARK}]'
TEXT_PRIMARY_IMPORTANT = f'!text-[{_TEXT_PRIMARY_LIGHT}] dark:!text-[{_TEXT_PRIMARY_DARK}]'
TEXT_SECONDARY = f'text-[{_TEXT_SECONDARY_LIGHT}] dark:text-[{_TEXT_SECONDARY_DARK}]'
TEXT_MUTED = f'text-[{_TEXT_MUTED_LIGHT}] dark:text-[{_TEXT_MUTED_DARK}]'
TEXT_BLUE = f'text-[{BLUE}]'
TEXT_ACCENT = f'text-[{ACCENT}]'

# Borders
BORDER = f'border border-[{_BORDER_LIGHT}] dark:border-[{_BORDER_DARK}]'
BORDER_B = f'border-b border-b-[{_BORDER_LIGHT}] dark:border-b-[{_BORDER_DARK}]'
BORDER_T = f'border-t border-t-[{_BORDER_LIGHT}] dark:border-t-[{_BORDER_DARK}]'
BORDER_2 = f'border-2 border-[{_BORDER_LIGHT}] dark:border-[{_BORDER_DARK}]'
BORDER_BLUE = f'border-[1.5px] border-[{BLUE}]'
BORDER_ACCENT = f'border-[{ACCENT}]'
BORDER_SUBTLE = f'border-[1.5px] border-[{_BORDER_LIGHT}] dark:border-[{_BORDER_DARK}]'
RING = f'ring-1 ring-[{_BORDER_LIGHT}] dark:ring-[{_BORDER_DARK}]'

# Shadows
SHADOW_BLUE = f'shadow-[0_2px_8px_color-mix(in_srgb,{BLUE}_30%,transparent)]'
SHADOW_CARD = 'shadow-[0_4px_24px_rgba(0,0,0,0.08)]'

# Font sizes
TEXT_13PX = 'text-[0.8125rem]'
TEXT_13PX_MONO = 'text-[0.8rem] font-mono'  # section label (slightly smaller for mono)
TEXT_15PX = 'text-[0.9375rem]'
TEXT_19PX = 'text-[1.1875rem]'
TEXT_24PX = 'text-[1.5rem]'
TEXT_32PX = 'text-[2rem]'
TEXT_HERO = 'text-[clamp(2.5rem,5vw,4.5rem)]'
TEXT_SECTION_TITLE = 'text-[clamp(1.8rem,3vw,3rem)]'
TEXT_CTA_TITLE = 'text-[clamp(1.5rem,2.5vw,2.25rem)]'


# --- Helpers ---

def section_heading(subtitle_: str, title_: str) -> None:
    """Render a section heading with a subtitle."""
    ui.label(subtitle_).classes(f'{TEXT_19PX} font-medium {TEXT_SECONDARY}')
    ui.markdown(title_).classes(f'{TEXT_SECTION_TITLE} font-medium mt-[-12px] [&_em]:not-italic [&_em]:{TEXT_BLUE}')


def subheading(text: str, *, link: str | None = None, major: bool = False, anchor_name: str | None = None) -> None:
    """Render a subheading with an anchor that can be linked to with a hash."""
    name = anchor_name or create_anchor_name(text)
    ui.html(f'<div id="{name}"></div>', sanitize=False).style('position: relative; top: -90px')
    with ui.row().classes('group gap-2 items-center relative'):
        classes = TEXT_32PX if major else TEXT_24PX
        if link:
            ui.link(text, link).classes(classes)
        else:
            ui.label(text).classes(classes)
        with ui.link(target=f'#{name}').classes('absolute').style('transform: translateX(-150%)'):
            phosphor_icon('ph-link').classes('opacity-0 group-hover:opacity-50 transition-opacity')


def create_anchor_name(text: str) -> str:
    """Create an anchor name that can be linked to with a hash."""
    return SPECIAL_CHARACTERS.sub('_', text).lower()


def phosphor_icon(name: str) -> ui.html:
    """Render a Phosphor duotone icon, e.g. ``phosphor_icon('ph-code')``."""
    return ui.html(f'<i class="ph-duotone {name}"></i>', sanitize=False).classes('-mb-1')


def themed_image(src: str, *, classes: str = '') -> None:
    """Show one image in light mode and another in dark mode."""
    ui.interactive_image(src.replace('THEME', 'light')).classes(f'block dark:!hidden {classes}')
    ui.interactive_image(src.replace('THEME', 'dark')).classes(f'hidden dark:!block {classes}')


def tooltip(text: str) -> ui.tooltip:
    """Create a tooltip with consistent styling."""
    return ui.tooltip(text).classes(f'rounded-xl {BG} {BORDER} {TEXT_SECONDARY} {TEXT_13PX}')
