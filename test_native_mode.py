
from nicegui import Client, ui


@ui.page('/')
async def page(client: Client):
    await client.connected()
    result = await ui.run_javascript('return "Roundtrip works!"')
    with open('result', 'w') as f:
        f.write(result)

ui.run(reload=False)
