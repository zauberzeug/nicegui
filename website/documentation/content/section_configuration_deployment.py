from nicegui import ui

from ..windows import bash_window, python_window
from . import doc, run_documentation

doc.title('Configuration & Deployment')


@doc.demo('URLs', '''
    You can access the list of all URLs on which the NiceGUI app is available via `app.urls`.
    The URLs are not available in `app.on_startup` because the server is not yet running.
    Instead, you can access them in a page function or register a callback with `app.urls.on_change`.
''')
def urls_demo():
    from nicegui import app

    # @ui.page('/')
    # def index():
    #     for url in app.urls:
    #         ui.link(url, target=url)
    # END OF DEMO
    ui.link('https://nicegui.io', target='https://nicegui.io')


doc.intro(run_documentation)


@doc.demo('Native Mode', '''
    You can enable native mode for NiceGUI by specifying `native=True` in the `ui.run` function.
    To customize the initial window size and display mode, use the `window_size` and `fullscreen` parameters respectively.
    Additionally, you can provide extra keyword arguments via `app.native.window_args` and `app.native.start_args`.
    Pick any parameter as it is defined by the internally used [pywebview module](https://pywebview.flowrl.com/guide/api.html)
    for the `webview.create_window` and `webview.start` functions.
    Note that these keyword arguments will take precedence over the parameters defined in `ui.run`.

    Additionally, you can change `webview.settings` via `app.native.settings`.

    In native mode the `app.native.main_window` object allows you to access the underlying window.
    It is an async version of [`Window` from pywebview](https://pywebview.flowrl.com/guide/api.html#window-object).
''', tab=lambda: ui.label('NiceGUI'))
def native_mode_demo():
    from nicegui import app

    app.native.window_args['resizable'] = False
    app.native.start_args['debug'] = True
    app.native.settings['ALLOW_DOWNLOADS'] = True

    ui.label('app running in native mode')
    # ui.button('enlarge', on_click=lambda: app.native.main_window.resize(1000, 700))
    #
    # ui.run(native=True, window_size=(400, 300), fullscreen=False)
    # END OF DEMO
    ui.button('enlarge', on_click=lambda: ui.notify('window will be set to 1000x700 in native mode'))


# Show a helpful workaround until issue is fixed upstream.
# For more info see: https://github.com/r0x0r/pywebview/issues/1078
doc.text('', '''
    If webview has trouble finding required libraries, you may get an error relating to "WebView2Loader.dll".
    To work around this issue, try moving the DLL file up a directory, e.g.:

    * from `.venv/Lib/site-packages/webview/lib/x64/WebView2Loader.dll`
    * to `.venv/Lib/site-packages/webview/lib/WebView2Loader.dll`
''')


@doc.demo('Environment Variables', '''
    You can set the following environment variables to configure NiceGUI:

    - `MATPLOTLIB` (default: true) can be set to `false` to avoid the potentially costly import of Matplotlib.
        This will make `ui.pyplot` and `ui.line_plot` unavailable.
    - `NICEGUI_STORAGE_PATH` (default: local ".nicegui") can be set to change the location of the storage files.
    - `MARKDOWN_CONTENT_CACHE_SIZE` (default: 1000): The maximum number of Markdown content snippets that are cached in memory.
    - `RST_CONTENT_CACHE_SIZE` (default: 1000): The maximum number of ReStructuredText content snippets that are cached in memory.
    - `NICEGUI_REDIS_URL` (default: None, means local file storage): The URL of the Redis server to use for shared persistent storage.
    - `NICEGUI_REDIS_KEY_PREFIX` (default: "nicegui:"): The prefix for Redis keys.
''')
def env_var_demo():
    from nicegui.elements import markdown

    ui.label(f'Markdown content cache size is {markdown.prepare_content.cache_info().maxsize}')


doc.text('Custom Vue Components', '''
    You can create custom components by subclassing `ui.element` and implementing a corresponding Vue component.
    The ["Custom Vue components" example](https://github.com/zauberzeug/nicegui/tree/main/examples/custom_vue_component)
    demonstrates how to create a custom counter component which emits events and receives updates from the server.

    The ["Signature pad" example](https://github.com/zauberzeug/nicegui/blob/main/examples/signature_pad)
    shows how to define dependencies for a custom component using a `package.json` file.
    This allows you to use third-party libraries via NPM in your component.

    Last but not least, the ["Node module integration" example](https://github.com/zauberzeug/nicegui/blob/main/examples/node_module_integration)
    demonstrates how to create a package.json file and a webpack.config.js file to bundle a custom Vue component with its dependencies.
''')

doc.text('Server Hosting', '''
    To deploy your NiceGUI app on a server, you will need to execute your `main.py` (or whichever file contains your `ui.run(...)`) on your cloud infrastructure.
    You can, for example, just install the [NiceGUI python package via pip](https://pypi.org/project/nicegui/) and use systemd or similar service to start the main script.
    In most cases, you will set the port to 80 (or 443 if you want to use HTTPS) with the `ui.run` command to make it easily accessible from the outside.

    A convenient alternative is the use of our [pre-built multi-arch Docker image](https://hub.docker.com/r/zauberzeug/nicegui) which contains all necessary dependencies.
    With this command you can launch the script `main.py` in the current directory on the public port 80:
''')


@doc.ui
def docker_run():
    with bash_window(classes='max-w-lg w-full h-44'):
        ui.markdown('''
            ```bash
            docker run -it --restart always \\
            -p 80:8080 \\
            -e PUID=$(id -u) \\
            -e PGID=$(id -g) \\
            -v $(pwd)/:/app/ \\
            zauberzeug/nicegui:latest
            ```
        ''')


doc.text('', '''
    The demo assumes `main.py` uses the port 8080 in the `ui.run` command (which is the default).
    The `-d` tells docker to run in background and `--restart always` makes sure the container is restarted if the app crashes or the server reboots.
    Of course this can also be written in a Docker compose file:
''')


@doc.ui
def docker_compose():
    with python_window('docker-compose.yml', classes='max-w-lg w-full h-60'):
        ui.markdown('''
            ```yaml
            app:
                image: zauberzeug/nicegui:latest
                restart: always
                ports:
                    - 80:8080
                environment:
                    - PUID=1000 # change this to your user id
                    - PGID=1000 # change this to your group id
                volumes:
                    - ./:/app/
            ```
        ''')


doc.text('', '''
    There are other handy features in the Docker image like non-root user execution and signal pass-through.
    For more details we recommend to have a look at our [Docker example](https://github.com/zauberzeug/nicegui/tree/main/examples/docker_image).

    To serve your application with [HTTPS](https://fastapi.tiangolo.com/deployment/https/) encryption, you can provide SSL certificates in multiple ways.
    For instance, you can directly provide your certificates to [Uvicorn](https://www.uvicorn.org/), which NiceGUI is based on, by passing the
    relevant [options](https://www.uvicorn.org/#command-line-options) to `ui.run()`:
''')


@doc.ui
def uvicorn_ssl():
    with python_window('main.py', classes='max-w-lg w-full'):
        ui.markdown('''
            ```python
            from nicegui import ui

            ui.run(
                port=443,
                ssl_certfile="<path_to_certfile>",
                ssl_keyfile="<path_to_keyfile>",
            )
            ```
        ''')


doc.text('', '''
    In production we also like using reverse proxies like [Traefik](https://doc.traefik.io/traefik/) or [NGINX](https://www.nginx.com/) to handle these details for us.
    See our development [docker-compose.yml](https://github.com/zauberzeug/nicegui/blob/main/docker-compose.yml) as an example based on traefik or
    [this example nginx.conf file](https://github.com/zauberzeug/nicegui/blob/main/examples/nginx_https/nginx.conf) showing how NGINX can be used to handle the SSL certificates and
    reverse proxy to your NiceGUI app.

    You may also have a look at [our demo for using a custom FastAPI app](https://github.com/zauberzeug/nicegui/tree/main/examples/fastapi).
    This will allow you to do very flexible deployments as described in the [FastAPI documentation](https://fastapi.tiangolo.com/deployment/).
    Note that there are additional steps required to allow multiple workers.
''')

doc.text('Package for Installation', '''
    NiceGUI apps can also be bundled into an executable with `nicegui-pack` which is based on [PyInstaller](https://www.pyinstaller.org/).
    This allows you to distribute your app as a single file that can be executed on any computer.

    Just make sure to call `ui.run` with `reload=False` in your main script to disable the auto-reload feature.
    Running the `nicegui-pack` command below will create an executable `myapp` in the `dist` folder:
''')


@doc.ui
def pyinstaller():
    with ui.row().classes('w-full items-stretch'):
        with python_window(classes='max-w-lg w-full'):
            ui.markdown('''
                ```python
                from nicegui import native, ui

                ui.label('Hello from PyInstaller')

                ui.run(reload=False, port=native.find_open_port())
                ```
            ''')
        with bash_window(classes='max-w-lg w-full'):
            ui.markdown('''
                ```bash
                nicegui-pack --onefile --name "myapp" main.py
                ```
            ''')


doc.text('', '''
    **Packaging Tips:**

    - When building a PyInstaller app, your main script can use a native window (rather than a browser window) by
    using `ui.run(reload=False, native=True)`.
    The `native` parameter can be `True` or `False` depending on whether you want a native window or to launch a
    page in the user's browser - either will work in the PyInstaller generated app.

    - Specifying `--windowed` to `nicegui-pack` will prevent a terminal console from appearing.
    However you should only use this option if you have also specified `native=True` in your `ui.run` command.
    Without a terminal console the user won't be able to exit the app by pressing Ctrl-C.
    With the `native=True` option, the app will automatically close when the window is closed, as expected.

    - Specifying `--windowed` to `nicegui-pack` will create an `.app` file on Mac which may be more convenient to distribute.
    When you double-click the app to run it, it will not show any console output.
    You can also run the app from the command line with `./myapp.app/Contents/MacOS/myapp` to see the console output.

    - Specifying `--onefile` to `nicegui-pack` will create a single executable file.
    Whilst convenient for distribution, it will be slower to start up.
    This is not NiceGUI's fault but just the way Pyinstaller zips things into a single file, then unzips everything
    into a temporary directory before running.
    You can mitigate this by removing `--onefile` from the `nicegui-pack` command,
    and zip up the generated `dist` directory yourself, distribute it,
    and your end users can unzip once and be good to go,
    without the constant expansion of files due to the `--onefile` flag.

    - Summary of user experience for different options:

        | `nicegui-pack`           | `ui.run(...)`  | Explanation |
        | :---                     | :---           | :---        |
        | `onefile`                | `native=False` | Single executable generated in `dist/`, runs in browser |
        | `onefile`                | `native=True`  | Single executable generated in `dist/`, runs in popup window |
        | `onefile` and `windowed` | `native=True`  | Single executable generated in `dist/` (on Mac a proper `dist/myapp.app` generated incl. icon), runs in popup window, no console appears |
        | `onefile` and `windowed` | `native=False` | Avoid (no way to exit the app) |
        | Specify neither          |                | A `dist/myapp` directory created which can be zipped manually and distributed; run with `dist/myapp/myapp` |

    - If you are using a Python virtual environment, ensure you `pip install pyinstaller` within your virtual environment
    so that the correct PyInstaller is used, or you may get broken apps due to the wrong version of PyInstaller being picked up.
    That is why the `nicegui-pack` invokes PyInstaller using `python -m PyInstaller` rather than just `pyinstaller`.
''')


@doc.ui
def install_pyinstaller():
    with bash_window(classes='max-w-lg w-full h-42 self-center'):
        ui.markdown('''
            ```bash
            python -m venv venv
            source venv/bin/activate
            pip install nicegui
            pip install pyinstaller
            ```
        ''')


doc.text('', '''
    Note:
    If you're getting an error "TypeError: a bytes-like object is required, not 'str'", try adding the following lines to the top of your `main.py` file:
    ```py
    import sys
    sys.stdout = open('logs.txt', 'w')
    ```
    See <https://github.com/zauberzeug/nicegui/issues/681> for more information.
''')

doc.text('', '''
    **macOS Packaging**

    Add the following snippet before anything else in your main app's file, to prevent new processes from being spawned in an endless loop:

    ```python
    # macOS packaging support
    from multiprocessing import freeze_support  # noqa
    freeze_support()  # noqa

    # all your other imports and code
    ```

    The `# noqa` comment instructs Pylance or autopep8 to not apply any PEP rule on those two lines, guaranteeing they remain on top of anything else.
    This is key to prevent process spawning.
''')

doc.text('NiceGUI On Air', '''
    By using `ui.run(on_air=True)` you can share your local app with others over the internet 🧞.

    When accessing the on-air URL, all libraries (like Vue, Quasar, ...) are loaded from our CDN.
    Thereby only the raw content and events need to be transmitted by your local app.
    This makes it blazing fast even if your app only has a poor internet connection (e.g. a mobile robot in the field).

    By setting `on_air=True` you will get a random URL which is valid for 1 hour.
    If you sign-up at <https://on-air.nicegui.io>, you can setup an organization and device name to get a fixed URL:
    `https://on-air.nicegui.io/<my-org>/<my_device_name>`.
    The device is then identified by a unique, private token which you can use instead of a boolean flag: `ui.run(on_air='<your token>')`.
    If you [sponsor us](https://github.com/sponsors/zauberzeug),
    we will enable multi-device management and provide built-in passphrase protection for each device.

    Currently On Air is available as a tech preview and can be used free of charge.
    We will gradually improve stability and extend the service with usage statistics, remote terminal access and more.
    Please let us know your feedback on [GitHub](https://github.com/zauberzeug/nicegui/discussions),
    [Reddit](https://www.reddit.com/r/nicegui/), or [Discord](https://discord.gg/TEpFeAaF4f).

    **Data Privacy:**
    We take your privacy very serious.
    NiceGUI On Air does not log or store any content of the relayed data.
''')
