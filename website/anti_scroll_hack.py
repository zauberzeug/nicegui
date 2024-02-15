from nicegui import ui


def setup() -> None:
    """Prevent the page from scrolling when closing a dialog.

    This function modifies the behavior of the NiceGUI library to prevent the page from scrolling
    when a dialog is closed. It achieves this by overriding the internal `_handle_value_change`
    method of the `ui.dialog` module.

    Usage:
        Call this function once at the beginning of your program to enable the anti-scroll hack.

    Note:
        This code includes a hack to modify the behavior of the NiceGUI library. Hacks like this
        should be used with caution and may not be future-proof. It is recommended to keep an eye
        on updates to the NiceGUI library and adjust this code accordingly if necessary.
    """
    # HACK (issue #1404)
    # pylint: disable=protected-access
    def _handle_value_change(sender, value, on_value_change=ui.dialog._handle_value_change) -> None:
        ui.query('html').classes(**{'add' if value else 'remove': 'has-dialog'})
        on_value_change(sender, value)

    # pylint: disable=method-assign
    ui.dialog._handle_value_change = _handle_value_change  # type: ignore
