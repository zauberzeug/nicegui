from nicegui import binding, ui
from nicegui.testing import User


@binding.bindable_dataclass
class _Price:
    price: float = 10.0


async def test_computed_keeps_tracking_after_ui_input_edit(user: User):
    """A computed recomputed from inside a UI element -> model propagation must keep its dependencies."""
    p = _Price()
    sub = binding.computed(lambda: p.price * 2)

    @ui.page('/')
    def page():
        ui.number('price').bind_value(p, 'price')

    await user.open('/')
    user.find(ui.number).type('5')  # element -> model write goes through _propagate
    assert sub.value == p.price * 2
    p.price = 7  # a later programmatic write must still be tracked
    assert sub.value == 14
