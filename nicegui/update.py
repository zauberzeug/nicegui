from .elements.element import Element


def update(self, *elements: Element) -> None:
    for element in elements:
        element.update()
