from ..tools import load_demo

name = 'binding_properties'
title = 'Binding Properties'
description = '''
    To update UI elements automatically, you can bind them to each other or to your data model.
'''


def content() -> None:
    load_demo('bindings')
