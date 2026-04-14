from ..element import Element


class Lazy(Element, component='lazy.js'):
    """Lazy element that defers rendering of its children until mounted.

    Child elements are only rendered after the component is mounted and the next Vue tick,
    which can improve initial page load performance for complex UIs.
    """

    def __init__(self) -> None:
        super().__init__()
