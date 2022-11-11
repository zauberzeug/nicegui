import justpy as jp

from .group import Group


class Card(Group):

    def __init__(self):
        """Card

        Provides a container with a dropped shadow.
        """
        view = jp.QCard(classes='column items-start q-pa-md gap-4', delete_flag=False, temp=False)
        super().__init__(view)


class CardSection(Group):

    def __init__(self):
        view = jp.QCardSection(delete_flag=False, temp=False)
        super().__init__(view)
