#!/usr/bin/env python3
"""Offline-capable NiceGUI app.

This example shows how to keep parts of a NiceGUI app usable without a network
connection, the way YouTube still shows your downloads when you are offline.

NiceGUI is server-driven: the browser loads an HTML shell and then a WebSocket
connection lets the *server* build and update the UI.
When the device is offline that connection cannot be established, so NiceGUI's
normal live rendering is unavailable.
The trick is therefore not a single caching header but a combination of two
browser features:

* a **service worker** (a small script the browser keeps running in the
  background) that intercepts requests and can answer them from a cache, and
* **client-side storage** (here ``localStorage``) that holds the content the
  user chose to keep.

While **online** the full NiceGUI app runs as usual and "Save for offline"
writes an article into ``localStorage`` via ``ui.run_javascript``.
The service worker pre-caches a standalone ``/offline`` page.
While **offline** the navigation to the server fails, so the service worker
serves that cached ``/offline`` page instead.
That page is plain HTML/JavaScript: it reads the saved articles back from
``localStorage`` and renders them without ever touching the server.
"""
import json
from pathlib import Path

from fastapi.responses import FileResponse

from nicegui import app, ui

HERE = Path(__file__).parent

# A few demo articles. In a real app these would come from a database or an API.
ARTICLES = [
    {
        'id': 'service-workers',
        'title': 'What is a service worker?',
        'body': 'A service worker is a script the browser runs in the background, separate from the page. '
                'It can intercept network requests and answer them from a cache, which is what lets a web '
                'app keep working when the network (or the server) is unavailable.',
    },
    {
        'id': 'client-storage',
        'title': 'Where do offline downloads live?',
        'body': 'Content you keep for offline use is stored on the device, typically in localStorage or '
                'IndexedDB. This example uses localStorage for simplicity; reach for IndexedDB when you need '
                'to store larger blobs such as images or audio.',
    },
    {
        'id': 'nicegui-and-offline',
        'title': 'How does this fit NiceGUI?',
        'body': 'NiceGUI builds the UI on the server and streams updates over a WebSocket, so the live app '
                'needs a connection. The offline page is deliberately plain HTML/JS: it renders the saved '
                'articles on its own, so it works even when the server is unreachable.',
    },
]


class ArticleCard:
    """A card that shows an article and lets the user keep it for offline reading."""

    def __init__(self, article: dict) -> None:
        self.article = article
        self.saved = False
        with ui.card().classes('w-full'):
            ui.label(article['title']).classes('text-lg font-semibold')
            ui.label(article['body']).classes('text-gray-600 whitespace-pre-line')
            self.button = ui.button(on_click=self.toggle)
        self._refresh()

    def toggle(self) -> None:
        """Add or remove the article from the browser's offline storage."""
        self.saved = not self.saved
        key = json.dumps(f'article:{self.article["id"]}')
        if self.saved:
            # Store the article as a JSON string so the offline page can parse it back.
            value = json.dumps(json.dumps(self.article))
            ui.run_javascript(f'localStorage.setItem({key}, {value})')
            ui.notify(f'Saved "{self.article["title"]}" for offline reading')
        else:
            ui.run_javascript(f'localStorage.removeItem({key})')
            ui.notify(f'Removed "{self.article["title"]}" from offline storage')
        self._refresh()

    def set_saved(self, saved: bool) -> None:
        self.saved = saved
        self._refresh()

    def _refresh(self) -> None:
        if self.saved:
            self.button.props('color=positive icon=check').set_text('Saved for offline')
        else:
            self.button.props('color=primary icon=download').set_text('Save for offline')


# Register the service worker and link the web app manifest on every page.
ui.add_head_html('''
    <link rel="manifest" href="/manifest.webmanifest">
    <meta name="theme-color" content="#1976d2">
    <script>
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/service_worker.js').catch(console.error);
            });
        }
    </script>
''', shared=True)


@app.get('/service_worker.js')
def service_worker() -> FileResponse:
    # Served from the root so its scope covers the whole app.
    return FileResponse(HERE / 'service_worker.js', media_type='application/javascript',
                        headers={'Service-Worker-Allowed': '/'})


@app.get('/offline')
def offline_page() -> FileResponse:
    return FileResponse(HERE / 'offline.html', media_type='text/html')


@app.get('/manifest.webmanifest')
def manifest() -> FileResponse:
    return FileResponse(HERE / 'manifest.webmanifest', media_type='application/manifest+json')


@ui.page('/')
async def index() -> None:
    with ui.column().classes('mx-auto max-w-2xl p-4 gap-4'):
        with ui.row().classes('w-full items-center justify-between'):
            ui.label('Offline-ready reading list').classes('text-2xl font-bold')
            ui.button('Offline page', icon='cloud_off',
                      on_click=lambda: ui.navigate.to('/offline')).props('outline')
        ui.label('Save articles while online, then read them even without a connection. '
                 'Try it: save a few, stop the server (or switch to offline in the browser dev tools), '
                 'and reload.').classes('text-gray-600')
        cards = {article['id']: ArticleCard(article) for article in ARTICLES}

    # Once the client is connected, reflect which articles this browser already has stored.
    await ui.context.client.connected()
    saved_ids = await ui.run_javascript(
        'Object.keys(localStorage).filter(k => k.startsWith("article:")).map(k => k.slice(8))'
    )
    for article_id in saved_ids:
        if article_id in cards:
            cards[article_id].set_saved(True)


ui.run()
