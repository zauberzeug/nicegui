from nicegui import ui


def phosphor_icon(name: str) -> ui.html:
    """Render a Phosphor duotone icon, e.g. ``phosphor_icon('ph-code')``."""
    return ui.html(f'<i class="ph-duotone {name}"></i>', sanitize=False).classes('-mb-1')
