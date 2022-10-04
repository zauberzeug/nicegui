from nicegui import ui

from navbar import navbar


class page(ui.page):

    def __init__(self, route: str, **kwargs) -> None:
        '''Custom page decorator to share the same styling and behavior across all pages'''
        super().__init__(route, classes='fit column items-start', title='Modularization Demo')
        self.kwargs = kwargs

    async def header(self) -> None:
        await super().header()
        navbar(**self.kwargs)
        # start using a ui row to let all content between header and footer be centered
        self.content = ui.row().classes('justify-center fit mt-10').__enter__()

    async def footer(self) -> None:
        await super().footer()
        # closing the row which was opened in header
        self.content.__exit__(None, None, None)


def headline(text: str) -> ui.label:
    return ui.label(text).classes('text-h4 text-weight-bold text-grey-8')
