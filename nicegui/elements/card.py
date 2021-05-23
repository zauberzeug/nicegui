import justpy as jp
from .group import Group

class Card(Group):

    def __init__(self):

        view = jp.QCard(classes='column items-start q-pa-md', style='gap: 1em', delete_flag=False)

        super().__init__(view)
