import pytest

from nicegui import Event, ui
from nicegui.testing.general import nicegui_reset_globals as reset_globals


# NOTE: ignore warnings because the reset drops the script client's deferred outbox loop without closing it
@pytest.mark.filterwarnings('ignore:coroutine .Outbox.loop. was never awaited:RuntimeWarning')
def test_reset_after_ui_outside_page(nicegui_reset_globals):
    """UI outside a page enters script mode; a reset must not leave its slot behind (#6314)."""
    ui.label('outside a page')
    with reset_globals():
        Event().subscribe(lambda: None)  # must not fail with "parent element has been deleted"
