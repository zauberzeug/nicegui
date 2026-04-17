import pytest

from nicegui import app, ui


def test_run_with_rejects_self_mount():
    """Passing nicegui.app to ui.run_with() would mount it into itself and cause infinite recursion on unmatched paths."""
    with pytest.raises(ValueError, match='must be called with your own FastAPI app'):
        ui.run_with(app)
