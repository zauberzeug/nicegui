import justpy as jp

from .group import Group


class Column(Group):

    def __init__(self):
        '''Column Element

        Provides a container which arranges its child in a row.
        '''
        view = jp.QDiv(classes='column items-start gap-4', delete_flag=False, temp=False)
        super().__init__(view)
