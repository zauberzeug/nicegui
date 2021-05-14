import justpy as jp
from .group import Group

class Row(Group):

    def __init__(self):

        view = jp.QDiv(classes='row items-start', style='gap: 1em', delete_flag=False)

        super().__init__(view)
