from collections import Counter
from datetime import datetime

from nicegui import ui

from . import doc

counter = Counter()  # type: ignore
start = datetime.now().strftime(r'%H:%M, %d %B %Y')


doc.title('Storage')


@doc.demo('Storage', '''
    NiceGUI offers a straightforward mechanism for data persistence within your application.
    It features five built-in storage types:

    - `app.storage.tab`:
        Stored server-side in memory, this dictionary is unique to each non-duplicated tab session and can hold arbitrary objects.
        Data will be lost when restarting the server until <https://github.com/zauberzeug/nicegui/discussions/2841> is implemented.
        This storage is only available within [page builder functions](/documentation/page)
        and requires an established connection, obtainable via [`await client.connected()`](/documentation/page#wait_for_client_connection).
    - `app.storage.client`:
        Also stored server-side in memory, this dictionary is unique to each client connection and can hold arbitrary objects.
        Data will be discarded when the page is reloaded or the user navigates to another page.
        Unlike data stored in `app.storage.tab` which can be persisted on the server even for days,
        `app.storage.client` helps caching resource-hungry objects such as a streaming or database connection you need to keep alive
        for dynamic site updates but would like to discard as soon as the user leaves the page or closes the browser.
        This storage is only available within [page builder functions](/documentation/page).
    - `app.storage.user`:
        Stored server-side, each dictionary is associated with a unique identifier held in a browser session cookie.
        Unique to each user, this storage is accessible across all their browser tabs.
        `app.storage.browser['id']` is used to identify the user.
        This storage is only available within [page builder functions](/documentation/page)
        and requires the `storage_secret` parameter in`ui.run()` to sign the browser session cookie.
    - `app.storage.general`:
        Also stored server-side, this dictionary provides a shared storage space accessible to all users.
    - `app.storage.browser`:
        Unlike the previous types, this dictionary is stored directly as the browser session cookie, shared among all browser tabs for the same user.
        However, `app.storage.user` is generally preferred due to its advantages in reducing data payload, enhancing security, and offering larger storage capacity.
        By default, NiceGUI holds a unique identifier for the browser session in `app.storage.browser['id']`.
        This storage is only available within [page builder functions](/documentation/page)
        and requires the `storage_secret` parameter in `ui.run()` to sign the browser session cookie.

    The following table will help you to choose storage.

    | Storage type                | `client` | `tab`  | `browser` | `user` | `general` |
    |-----------------------------|----------|--------|-----------|--------|-----------|
    | Location                    | Server   | Server | Browser   | Server | Server    |
    | Across tabs                 | No       | No     | Yes       | Yes    | Yes       |
    | Across browsers             | No       | No     | No        | No     | Yes       |
    | Across server restarts      | No       | Yes    | No        | Yes    | Yes       |
    | Across page reloads         | No       | Yes    | Yes       | Yes    | Yes       |
    | Needs page builder function | Yes      | Yes    | Yes       | Yes    | No        |
    | Needs client connection     | No       | Yes    | No        | No     | No        |
    | Write only before response  | No       | No     | Yes       | No     | No        |
    | Needs serializable data     | No       | No     | Yes       | Yes    | Yes       |
    | Needs `storage_secret`      | No       | No     | Yes       | Yes    | No        |
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
    Storage can also be used in combination with [`bindings`](/documentation/section_binding_properties).
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


@doc.demo('Storing data per browser tab', '''
    When storing data in `app.storage.tab`, a single user can open multiple tabs of the same app, each with its own storage data.
    This may be beneficial in certain scenarios like search or when performing data analysis.
    It is also more secure to use such a volatile storage for scenarios like logging into a bank account or accessing a password manager.
''')
def tab_storage():
    from nicegui import app

    # @ui.page('/')
    # async def index():
    #     await ui.context.client.connected()
    with ui.column():  # HIDE
        app.storage.tab['count'] = app.storage.tab.get('count', 0) + 1
        ui.label(f'Tab reloaded {app.storage.tab["count"]} times')
        ui.button('Reload page', on_click=ui.navigate.reload)


@doc.demo('Maximum age of tab storage', '''
    By default, the tab storage is kept for 30 days.
    You can change this by setting `app.storage.max_tab_storage_age`.

    *Added in version 2.10.0*
''')
def max_tab_storage_age():
    from nicegui import app
    from datetime import timedelta
    # app.storage.max_tab_storage_age = timedelta(minutes=1).total_seconds()
    ui.label(f'Tab storage age: {timedelta(minutes=1).total_seconds()} seconds')  # HIDE

    @ui.page('/')
    def index():
        # ui.label(f'Tab storage age: {app.storage.max_tab_storage_age} seconds')
        pass  # HIDE


@doc.demo('Short-term memory', '''
    The goal of `app.storage.client` is to store data only for the duration of the current page visit.
    In difference to data stored in `app.storage.tab`
    - which is persisted between page changes and even browser restarts as long as the tab is kept open -
    the data in `app.storage.client` will be discarded if the user closes the browser, reloads the page or navigates to another page.
    This is beneficial for resource-hungry, intentionally short-lived or sensitive data.
    An example is a database connection, which should be closed as soon as the user leaves the page.
    Additionally, this storage useful if you want to return a page with default settings every time a user reloads.
    Meanwhile, it keeps the data alive during in-page navigation.
    This is also helpful when updating elements on the site at intervals, such as a live feed.
''')
def short_term_memory():
    from nicegui import app

    # @ui.page('/')
    # async def index():
    with ui.column():  # HIDE
        cache = app.storage.client
        cache['count'] = 0
        ui.label().bind_text_from(cache, 'count', lambda n: f'Updated {n} times')
        ui.button('Update content',
                  on_click=lambda: cache.update(count=cache['count'] + 1))
        ui.button('Reload page', on_click=ui.navigate.reload)


doc.text('Indentation', '''
    By default, the general and user storage data is stored in JSON format without indentation.
    You can change this to an indentation of 2 spaces by setting
    `app.storage.general.indent = True` or `app.storage.user.indent = True`.
''')


doc.text('Redis storage', '''
    You can use [Redis](https://redis.io/) for storage as an alternative to the default file storage.
    This is useful if you have multiple NiceGUI instances and want to share data across them.

    To activate this feature install the `redis` package (`pip install nicegui[redis]`)
    and provide the `NICEGUI_REDIS_URL` environment variable to point to your Redis server.
    Our [Redis storage example](https://github.com/zauberzeug/nicegui/tree/main/examples/redis_storage) shows
    how you can setup it up with a reverse proxy or load balancer.

    Please note that the Redis sync always contains all the data, not only the changed values.

    - For `app.storage.general` this is the whole dictionary.
    - For `app.storage.user` it's all the data of the user.
    - For `app.storage.tab` it's all the data stored for this specific tab.

    If you have large data sets, we suggest to use a database instead.
    See our [database example](https://github.com/zauberzeug/nicegui/blob/main/examples/sqlite_database/main.py) for a demo with SQLite.
    But of course to sync between multiple instances you should replace SQLite with PostgreSQL or similar.

    *Added in version 2.10.0*
''')
