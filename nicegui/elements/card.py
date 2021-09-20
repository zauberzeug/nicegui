import justpy as jp
from .element import Design
from .group import Group

class Card(Group):

    def __init__(self, design: Design = Design.default):
        """Card Element

        Provides a container with a dropped shadow.

        :param design: `Design.plain` does not apply any stylings to the underlying Quasar card.
            If ommitted, `Design.default` configures padding and spacing.
            When using `Design.plain`, content expands to the edges.
            To provide margins for other content you can use `ui.card_section`.
        """
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
