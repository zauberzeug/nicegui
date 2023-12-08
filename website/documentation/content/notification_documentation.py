from nicegui import ui

from . import doc


@doc.demo(ui.notification)
def main_demo() -> None:
    import asyncio

    async def compute():
        n = ui.notification()
        for i in range(10):
            n.message = f'Computing {i/10:.0%}'
            n.spinner = True
            await asyncio.sleep(0.2)
        n.message = 'Done!'
        n.spinner = False

    ui.button('Compute', on_click=compute)


doc.reference(ui.notification)
