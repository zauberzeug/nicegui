import pytest

from nicegui import Event, ui
from nicegui.slot import Slot
from nicegui.testing import general


@pytest.mark.filterwarnings('ignore:coroutine .Outbox.loop. was never awaited:RuntimeWarning')
def test_reset_globals_clears_dangling_script_mode_slot(nicegui_reset_globals) -> None:
    """Bare UI outside a page leaves Slot.stacks[0]; reset must drop it.

    Otherwise a later Event.subscribe() with no active task hits a deleted parent (#6314).
    """
    ui.card()
    assert Slot.stacks.get(0)

    with general.nicegui_reset_globals():
        pass

    Event().subscribe(lambda: None)
