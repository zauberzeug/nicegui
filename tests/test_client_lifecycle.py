from nicegui import Client, ui
from nicegui.testing import Screen


def test_no_double_delete(screen: Screen):
    @ui.page('/', reconnect_timeout=3)
    def page():
        pass

    screen.open('/')
    screen.wait(1)
    screen.close()  # self-delete 1+3 = 4 second mark
    Client.prune_instances(client_age_threshold=0)  # should do nothing
    screen.wait(4)  # should not raise KeyError at 5 second mark
