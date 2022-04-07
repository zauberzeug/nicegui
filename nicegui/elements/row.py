import justpy as jp

from .group import Group


class Row(Group):

    def __init__(self):
        '''Row Element

        Provides a container which arranges its child in a row.
        '''
        view = jp.QDiv(classes='row items-start', style='gap: 1em', delete_flag=False, temp=False)
        super().__init__(view)
