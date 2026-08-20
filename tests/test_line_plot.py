from nicegui import ui
from nicegui.testing import User


async def test_push_empty_data_is_noop(user: User) -> None:
    @ui.page('/')
    def page():
        plot = ui.line_plot(n=1)
        plot.push([], [[]])
        plot.push([1], [[]])
        ui.label('rendered')

    await user.open('/')
    await user.should_see('rendered')
