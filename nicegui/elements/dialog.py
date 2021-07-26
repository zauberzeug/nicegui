import justpy as jp
from .group import Group

class Dialog(Group):

    def __init__(self,
                 *,
                 value: bool = False
                 ):
        """Dialog

        Creates a modal dialog.

        :param value: whether the dialog is already opened (default: False)
        """

        view = jp.QDialog(
            value=value,
            classes='row items-start bg-red-400',
            style='gap: 1em',
        )

        super().__init__(view)

    def open(self):

        self.view.value = True

    def close(self):

        self.view.value = False
