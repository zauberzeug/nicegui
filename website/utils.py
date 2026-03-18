from nicegui import ui


def phosphor_icon(name: str) -> ui.html:
    """Render a Phosphor duotone icon, e.g. ``phosphor_icon('ph-code')``."""
    return ui.html(f'<i class="ph-duotone {name}"></i>', sanitize=False).classes('-mb-1')


def themed_image(src: str, *, classes: str = '') -> None:
    """Show one image in light mode and another in dark mode."""
    ui.interactive_image(src.replace('THEME', 'light')).classes(f'block dark:!hidden {classes}')
    ui.interactive_image(src.replace('THEME', 'dark')).classes(f'hidden dark:!block {classes}')
