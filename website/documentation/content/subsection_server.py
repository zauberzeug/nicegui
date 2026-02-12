from nicegui import ui

from . import (
    doc,
    run_documentation,
)

doc.title('Server')


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


@doc.demo('Background Tasks', '''
    `background_tasks.create()` allows you to run an async function in the background and return a task object.
    By default the task will be automatically cancelled during shutdown.
    You can prevent this by using the `@background_tasks.await_on_shutdown` decorator (added in version 2.16.0).
    This is useful for tasks that need to be completed even when the app is shutting down.
''')
def background_tasks_demo():
    # import aiofiles
    import asyncio

    from nicegui import background_tasks

    results = {'answer': '?'}

    async def compute() -> None:
        await asyncio.sleep(1)
        results['answer'] = 42

    @background_tasks.await_on_shutdown
    async def backup() -> None:
        await asyncio.sleep(1)
        # async with aiofiles.open('backup.json', 'w') as f:
        #     await f.write(f'{results["answer"]}')
        # print('backup.json written', flush=True)

    ui.label().bind_text_from(results, 'answer', lambda x: f'answer: {x}')
    ui.button('Compute', on_click=lambda: background_tasks.create(compute()))
    ui.button('Backup', on_click=lambda: background_tasks.create(backup()))


doc.text('Custom Vue Components', '''
    You can create custom components by subclassing `ui.element` and implementing a corresponding Vue component.
    The ["Custom Vue components" example](https://github.com/zauberzeug/nicegui/tree/main/examples/custom_vue_component)
    demonstrates how to create a custom counter component which emits events and receives updates from the server.

    The ["Signature pad" example](https://github.com/zauberzeug/nicegui/blob/main/examples/signature_pad) and
    the ["Node module integration" example](https://github.com/zauberzeug/nicegui/blob/main/examples/node_module_integration)
    demonstrate how to bundle a custom Vue component with its dependencies defined in a `package.json` file.
    In Python we can use the `esm` parameter when subclassing `ui.element`
    to specify the ESM module name and the path to the bundled component.
    This adds the ESM module to the import map of the page and makes it available in the Vue component.
''')
