import justpy as jp

from .group import Group


class Container(Group):

    def __init__(self, **kwargs):
        """QDiv Container"""
        view = jp.QDiv(temp=True, **kwargs)
        super().__init__(view)
