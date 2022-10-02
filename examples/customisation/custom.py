from typing import Optional

from nicegui import ui

from examples.customisation.data import Data
from examples.customisation.elements import Footer, LinearProgress, Badge, Layout, Header, PageContainer, Div
from examples.customisation.navbar import navbar


class page(ui.page):
    def __init__(self, route: str, step: int = 1, **kwargs):
        '''Custom page decorator to share the same styling and behavior across all pages'''
        super().__init__(route, classes='fit column items-start', title='Modularization Demo')
        self.kwargs = kwargs
        self.layout: Layout  # Quasar layout
        self.content: Optional[ui.page] = None
        self.step = step
        self.bound_data = Data()

    async def header(self) -> None:
        await super().header()

        with Layout() as self.layout:
            with Header():
                navbar(**self.kwargs)
            with PageContainer():
                # start using a ui row to let all content between header and footer be centered
                ui.row().classes('justify-center fit mt-10').__enter__()

    async def footer(self) -> None:
        await super().footer()

        with self.layout:
            with Footer():
                with LinearProgress(value=0, target_object=self.bound_data, target_name='progress_float'):
                    with Div() as progress_lbl:
                        progress_lbl.classes(add='absolute-full flex flex-center')
                        Badge(target_object=self.bound_data, target_name='progress_str')
        # closing the row which was opened in header
        if self.content:
            self.content.__exit__(None, None, None)

        # start a timer for demoing progress on each page
        ui.timer(1.0, self.progress)

    async def progress(self):
        self.bound_data.progress = (self.bound_data.progress + self.step) % 100


def headline(text: str) -> ui.label:
    return ui.label(text).classes('text-h4 text-weight-bold text-grey-8')
