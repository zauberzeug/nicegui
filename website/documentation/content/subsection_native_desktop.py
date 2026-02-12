from nicegui import ui

from ..windows import python_window
from . import doc

doc.title('Native Mode')


@doc.demo('Native Mode', '''
    You can enable native mode for NiceGUI by specifying `native=True` in the `ui.run` function.
    To customize the initial window size and display mode, use the `window_size` and `fullscreen` parameters respectively.
    Additionally, you can provide extra keyword arguments via `app.native.window_args` and `app.native.start_args`.
    Pick any parameter as it is defined by the internally used [pywebview module](https://pywebview.flowrl.com/api)
    for the `webview.create_window` and `webview.start` functions.
    Note that these keyword arguments will take precedence over the parameters defined in `ui.run`.

    Additionally, you can change `webview.settings` via `app.native.settings`.

    In native mode the `app.native.main_window` object allows you to access the underlying window.
    It is an async version of [`Window` from pywebview](https://pywebview.flowrl.com/api/#webview-window).

    On Windows, native mode requires the .NET Framework to be installed,
    as pywebview uses it for the EdgeChromium backend.
    This is typically pre-installed on standard Windows installations,
    but may be missing on minimal or freshly installed systems.
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


doc.text('', '''
    Note that the native app is run in a separate
    [process](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process).
    Therefore any configuration changes from code run under a
    [main guard](https://docs.python.org/3/library/__main__.html#idiomatic-usage) is ignored by the native app.
    The following examples show the difference between a working and a non-working configuration.

    For packaged apps (nicegui-pack, PyInstaller, etc.), also see the "Packaging with Native Mode" section below
    regarding the correct placement of `freeze_support()`.
''')


@doc.ui
def native_main_guard():
    with ui.row().classes('w-full items-stretch'):
        with python_window('good_example.py', classes='max-w-lg w-full'):
            ui.markdown('''
                ```python
                from nicegui import app, ui

                app.native.window_args['resizable'] = False  # works

                if __name__ == '__main__':
                    ui.run(native=True, reload=False)
                ```
            ''')
        with python_window('bad_example.py', classes='max-w-lg w-full'):
            ui.markdown('''
                ```python
                from nicegui import app, ui

                if __name__ == '__main__':
                    app.native.window_args['resizable'] = False  # ignored

                    ui.run(native=True, reload=False)
                ```
            ''')


# Show a helpful workaround until issue is fixed upstream.
# For more info see: https://github.com/r0x0r/pywebview/issues/1078
doc.text('', '''
    If webview has trouble finding required libraries, you may get an error relating to "WebView2Loader.dll".
    To work around this issue, try moving the DLL file up a directory, e.g.:

    * from `.venv/Lib/site-packages/webview/lib/x64/WebView2Loader.dll`
    * to `.venv/Lib/site-packages/webview/lib/WebView2Loader.dll`
''')
