from typing import Optional, Type

from nicegui import context
from nicegui.element import Element


class elements:

    def __init__(self, *, type: Optional[Type] = None):
        self.type = type

    def __iter__(self):
        client = context.get_client()
        return self.iterate(client.layout)

    def iterate(self, parent: Element):
        for element in parent:
            if self.type is None or isinstance(element, self.type):
                yield element
            yield from self.iterate(element)

    def __len__(self):
        return len(list(iter(self)))

    def __getitem__(self, index):
        return list(iter(self))[index]


get = elements
