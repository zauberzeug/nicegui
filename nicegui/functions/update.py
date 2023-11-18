from ..element import Element


def update(*elements: Element) -> None:
    """Update the given elements."""
    for element in elements:
        element.update()
