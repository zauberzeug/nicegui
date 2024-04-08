from collections import Counter
from datetime import datetime

from nicegui import ui

from . import doc

counter = Counter()  # type: ignore
start = datetime.now().strftime(r'%H:%M, %d %B %Y')

doc.title('Storage')


@doc.demo('Storage', '''
    NiceGUI offers a straightforward method for data persistence within your application. 
    It features four built-in storage types:

    - `app.storage.client`:
        Stored server-side in memory, this dictionary is unique to each client connection and can hold arbitrary 
        objects. Data will be lost when the page is reloaded or the user navigates to another page.
        Unlike data stored in  `app.storage.tab` which can be persisted on the server even for days, 
        `app.storage.client` helps caching resource-intensive objects such as a streaming or database connection you 
        need to keep alive for dynamic site updates but would like to close as soon as the user leaves the page or 
        closes the browser. This storage is only available within [page builder functions](/documentation/page).
    - `app.storage.user`:
        Stored server-side, each dictionary is associated with a unique identifier held in a browser session cookie.
        Unique to each user, this storage is accessible across all their browser tabs.
        `app.storage.browser['id']` is used to identify the user.
    - `app.storage.general`:
        Also stored server-side, this dictionary provides a shared storage space accessible to all users.
    - `app.storage.browser`:
        Unlike the previous types, this dictionary is stored directly as the browser session cookie, shared among all browser tabs for the same user.
        However, `app.storage.user` is generally preferred due to its advantages in reducing data payload, enhancing security, and offering larger storage capacity.
        By default, NiceGUI holds a unique identifier for the browser session in `app.storage.browser['id']`.

    The user storage and browser storage are only available within `page builder functions </documentation/page>`_
    because they are accessing the underlying `Request` object from FastAPI.
    Additionally these two types require the `storage_secret` parameter in`ui.run()` to encrypt the browser session cookie.
''')
def storage_demo():
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


@doc.demo('Counting page visits', '''
    Here we are using the automatically available browser-stored session ID to count the number of unique page visits.
''')
def page_visits():
    from collections import Counter
    from datetime import datetime

    from nicegui import app

    # counter = Counter()
    # start = datetime.now().strftime('%H:%M, %d %B %Y')
    #
    # @ui.page('/')
    # def index():
    #     counter[app.storage.browser['id']] += 1
    #     ui.label(f'{len(counter)} unique views ({sum(counter.values())} overall) since {start}')
    #
    # ui.run(storage_secret='private key to secure the browser session cookie')
    # END OF DEMO
    counter[app.storage.browser['id']] += 1
    ui.label(f'{len(counter)} unique views ({sum(counter.values())} overall) since {start}')


@doc.demo('Storing UI state', '''
    Storage can also be used in combination with [`bindings`](/documentation/bindings).
    Here we are storing the value of a textarea between visits.
    The note is also shared between all tabs of the same user.
''')
def ui_state():
    from nicegui import app

    # @ui.page('/')
    # def index():
    #     ui.textarea('This note is kept between visits') \
    #         .classes('w-full').bind_value(app.storage.user, 'note')
    # END OF DEMO
    ui.textarea('This note is kept between visits').classes('w-full').bind_value(app.storage.user, 'note')


@doc.demo('Short-term memory', '''
          The goal of `app.storage.client` is to store data only for the duration of the current page visit.
          In difference to data stored in `app.storage.tab` - which is persisted between page changes and even 
          browser restarts as long as the tab is kept open - the data in `app.storage.client` will be discarded 
          if the user closes the browser, reloads the page or navigates to another page.
          This is may be beneficial for resource hungry or intentionally very short lived data such as a database 
          connection which should be closed as soon as the user leaves the page, sensitive data or if you on purpose
          want to return a page with the default settings every time the user reloads the page while keeping the
          data alive during in-page navigation or when updating elements on the site in intervals such as a live feed.
          ''')
def short_term_memory():
    from nicegui import app

    # @ui.page('/')
    # async def index(client):
    with ui.column():  # HIDE
        app.storage.client['counter'] = 0
        ui.label().bind_text_from(app.storage.client, 'counter',
                                  backward=lambda n: f'Updates: {n}')
        ui.button('Update content',
                  on_click=lambda: app.storage.client.update(
                      {"counter": app.storage.client["counter"] + 1}))
        ui.button("Reload page", on_click=lambda: ui.navigate.reload())
