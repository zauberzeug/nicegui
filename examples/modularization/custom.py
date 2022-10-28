from nicegui import ui

from navbar import navbar


class page(ui.page):

    def __init__(self, route: str, **kwargs) -> None:
        '''Custom page decorator to share the same styling and behavior across all pages'''
        super().__init__(route, classes='fit column items-start', title='Modularization Demo')
        self.kwargs = kwargs

    async def before_content(self) -> None:
        await super().before_content()
        navbar(**self.kwargs)
        # enter a ui.row to center all content
        self.content = ui.row().classes('justify-center fit mt-10').__enter__()

    async def after_content(self) -> None:
        await super().after_content()
        # close the row which was opened in before_content()
        self.content.__exit__(None, None, None)


def headline(text: str) -> ui.label:
    return ui.label(text).classes('text-h4 text-weight-bold text-grey-8')
