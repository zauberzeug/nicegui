from nicegui import ui
from nicegui.testing import Screen, User


def test_carousel(screen: Screen):
    @ui.page('/')
    def page():
        with ui.carousel(arrows=True).props('control-color=primary'):
            for name in ['Alice', 'Bob', 'Carol']:
                with ui.carousel_slide():
                    ui.label(name).classes('w-32')

    screen.open('/')
    screen.should_contain('Alice')

    screen.click('chevron_right')
    screen.should_contain('Bob')

    screen.click('chevron_right')
    screen.should_contain('Carol')

    screen.click('chevron_left')
    screen.should_contain('Bob')

    screen.click('chevron_left')
    screen.should_contain('Alice')


async def test_no_done_prop_on_slides(user: User):
    slides = []

    @ui.page('/')
    def page():
        with ui.carousel() as carousel:
            slides.extend([ui.carousel_slide('a'), ui.carousel_slide('b'), ui.carousel_slide('c')])
        carousel.value = 'b'

    await user.open('/')
    assert not any(':done' in slide._props for slide in slides)
