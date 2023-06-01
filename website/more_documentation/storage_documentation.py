import logging

from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    """Storage
    With `app.storage` you can easily persist data.
    By default there are three types of storage. 
    `app.storage.user` is a dictionary stored on the server and identified by a generated id in a browser session cookie.
    That means each user gets their own storage which is shared between all browser tabs.
    `app.storage.general` is a dictionary stored on the server and shared between all users.

    Lastly `app.storage.browser` is a dictionary directly stored as the browser session cookie and shared between all browser tabs.
    It is normally better to use `app.storage.user` instead to reduce payload, gain improved security and have larger storage capacity).
    """
    from nicegui import app

    # @ui.page('/')
    # def index():
    #     app.storage.user['count'] = app.storage.user.get('count', 0) + 1
    #     with ui.row():
    #        ui.label('your own page visits:')
    #        ui.label().bind_text_from(app.storage.user, 'count')
    #
    # ui.run(storage_secret='private key to secure the browser session cookie')
    # END OF DEMO
    app.storage.user['count'] = app.storage.user.get('count', 0) + 1
    with ui.row():
        ui.label('your own page visits:')
        ui.label().bind_text_from(app.storage.user, 'count')


def more() -> None:
    @text_demo('Counting page visits', '''
        Here we are using the automatically available browser stored session id to count the number of unique page visits.
    ''')
    def page_visits():
        from collections import Counter
        from datetime import datetime

        from nicegui import app

        counter = Counter()
        start = datetime.now().strftime('%H:%M, %d %B %Y')

        @ui.page('/')
        def index():
            counter[app.storage.session.browser[id]] += 1
            ui.label(f'{len(counter)} unique views ({sum(counter.values())} overall) since {start}')

        # ui.run(storage_secret='private key to secure the browser session cookie')
