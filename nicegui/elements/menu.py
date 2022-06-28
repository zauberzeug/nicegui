import justpy as jp

from ..task_logger import create_task
from .group import Group


class Menu(Group):

    def __init__(self, *, value: bool = False):
        """Menu

        Creates a menu.

        :param value: whether the menu is already opened (default: `False`)
        """
        view = jp.QMenu(value=value, temp=False, no_parent_event=True)

        super().__init__(view)

    def open(self):
        self.view.value = True
        create_task(self.view.update())

    def close(self):
        self.view.value = False
        create_task(self.view.update())
