from typing import Union, Callable
from nicegui import ui


class PageBuilder:
    def __init__(self, router: Union["PageRouter", None] = None):
        self._router = router

    def build(self):
        pass


class PageRouter:
    def __init__(self):
        self.routes = {}
        self.element = ui.column()
        self._page_name: Union[str, None] = None
        self._page_builder: Union[PageBuilder, None] = None

    def add(self, name: str, page: Union[PageBuilder, Callable, type],
            default: bool = True) -> None:
        self.routes[name] = page
        if default:
            self.page = name

    @property
    def page(self):
        return self._page_name

    @page.setter
    def page(self, name: str):
        if self._page_name == name:
            return
        if name not in self.routes:
            raise ValueError(f'Page "{name}" not found')
        self._page_name = name
        self.element.clear()
        self._page_builder = None
        with self.element:
            new_page = self.routes[name]
            if isinstance(new_page, PageBuilder):  # an already configured page
                self._page_builder = new_page
            elif issubclass(new_page,
                            PageBuilder):  # a class of which an instance is created
                self._page_builder = new_page(router=self)
            elif callable(new_page):  # a call which builds the ui dynamically
                new_page()
            else:
                raise ValueError(f'Invalid page type: {new_page}')
            if self._page_builder:
                self._page_builder.build()
