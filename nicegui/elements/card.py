from nicegui.elements.element import Design
import justpy as jp
from .group import Group

class Card(Group):
    def __init__(self, design: Design = Design.default):
        if design == design.default:
            view = jp.QCard(classes='column items-start q-pa-md', style='gap: 1em', delete_flag=False)
        elif design == design.plain:
            view = jp.QCard(delete_flag=False)
        else:
            raise Exception(f'unsupported design: {design}')
        super().__init__(view)

class CardSection(Group):
    def __init__(self):
        view = jp.QCardSection(delete_flag=False)
        super().__init__(view)
