from nicegui import ui


def setup() -> None:
    """Prevent the page from scrolling when closing a dialog."""
    # HACK (issue #1404)
    # pylint: disable=protected-access
    def _handle_value_change(sender, value, on_value_change=ui.dialog._handle_value_change) -> None:
        ui.query('html').classes(**{'add' if value else 'remove': 'has-dialog'})
        on_value_change(sender, value)

    # pylint: disable=method-assign
    ui.dialog._handle_value_change = _handle_value_change  # type: ignore
