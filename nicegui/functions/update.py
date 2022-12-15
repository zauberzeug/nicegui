from ..element import Element


def update(*elements: Element) -> None:
    for element in elements:
        element.update()
