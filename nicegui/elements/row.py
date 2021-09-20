import justpy as jp
from .element import Design
from .group import Group

class Row(Group):

    def __init__(self, design: Design = Design.default):
        '''Row Element

        Provides a container which arranges its child in a row.

        :param design: `Design.plain` does not apply any stylings.
            If ommitted, `Design.default` configures padding and spacing.
        '''
        if design == design.default:
            view = jp.QDiv(classes='row items-start', style='gap: 1em', delete_flag=False)
        elif design == design.plain:
            view = jp.QDiv(classes='row', delete_flag=False)
        else:
            raise Exception(f'unsupported design: {design}')

        super().__init__(view)
