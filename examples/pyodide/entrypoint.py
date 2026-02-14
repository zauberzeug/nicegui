"""Pyodide/PyScript bootstrap - installs NiceGUI, launches the app, and mounts the runtime.

This is the PyScript entry point referenced by index.html.
Users should edit app.py to build their UI.
"""
import micropip  # type: ignore
from js import window  # type: ignore

window.console.log('Python: Installing NiceGUI and dependencies...')
await micropip.install('nicegui-0.0.0-py3-none-any.whl', deps=False)  # type: ignore  # noqa: F704, PLE1142
await micropip.install(['typing-extensions', 'markdown2', 'Pygments', 'docutils'])  # type: ignore  # noqa: F704, PLE1142
window.console.log('Python: NiceGUI installed')

# Import app.py — this builds the UI
from app import client  # noqa: E402, I001
from nicegui.pyodide import PyodideRuntime  # noqa: E402

# Hide loading indicator
loading = window.document.getElementById('loading')
if loading:
    loading.style.display = 'none'

# Mount the NiceGUI Pyodide runtime
runtime = PyodideRuntime(client)
try:
    await runtime.mount()  # type: ignore  # noqa: F704, PLE1142
    window.console.log('Python: mount() completed')
except Exception as e:
    window.console.log(f'Python: mount() error: {e}')

window.__pyodide_ready = True  # type: ignore
window.console.log('Python: Ready!')
