# isort:skip_file
import os


class Ui:
    from .config import config  # NOTE: before run
    from .run import run  # NOTE: before justpy

    _excludes = [word.strip().lower() for word in config.exclude.split(',')]
    _excludes = [e[:-3] if e.endswith('.js') else e for e in _excludes]  # NOTE: for python <3.9 without removesuffix
    os.environ['HIGHCHARTS'] = str('highcharts' not in _excludes)
    os.environ['AGGRID'] = str('aggrid' not in _excludes)

    from .elements.button import Button as button
    from .elements.card import Card as card
    from .elements.card import CardSection as card_section
    from .elements.checkbox import Checkbox as checkbox
    from .elements.color_input import ColorInput as color_input
    from .elements.color_picker import ColorPicker as color_picker
    from .elements.column import Column as column
    from .elements.dialog import Dialog as dialog
    from .elements.expansion import Expansion as expansion
    from .elements.html import Html as html
    from .elements.icon import Icon as icon
    from .elements.image import Image as image
    from .elements.input import Input as input
    from .elements.label import Label as label
    from .elements.link import Link as link
    from .elements.markdown import Markdown as markdown
    from .elements.menu import Menu as menu
    from .elements.menu_item import MenuItem as menu_item
    from .elements.menu_separator import MenuSeparator as menu_separator
    from .elements.notify import Notify as notify
    from .elements.number import Number as number
    from .elements.open import open, open_async
    from .elements.page import Page as page, add_head_html, add_body_html
    from .elements.radio import Radio as radio
    from .elements.row import Row as row
    from .elements.select import Select as select
    from .elements.slider import Slider as slider
    from .elements.svg import Svg as svg
    from .elements.switch import Switch as switch
    from .elements.table import Table as table
    from .elements.toggle import Toggle as toggle
    from .elements.tree import Tree as tree
    from .elements.update import update
    from .elements.upload import Upload as upload
    from .lifecycle import on_connect, on_disconnect, on_shutdown, on_startup
    from .routes import add_route, add_static_files, get
    from .timer import Timer as timer

    if 'colors' not in _excludes:
        from .elements.colors import Colors as colors

    if 'custom_example' not in _excludes:
        from .elements.custom_example import CustomExample as custom_example

    if 'highcharts' not in _excludes:
        from .elements.chart import Chart as chart

    if 'interactive_image' not in _excludes:
        from .elements.interactive_image import InteractiveImage as interactive_image

    if 'keyboard' not in _excludes:
        from .elements.keyboard import Keyboard as keyboard

    if 'log' not in _excludes:
        from .elements.log import Log as log

    if 'matplotlib' not in _excludes:
        from .elements.line_plot import LinePlot as line_plot
        from .elements.plot import Plot as plot

    if 'nipple' not in _excludes:
        from .elements.joystick import Joystick as joystick

    if 'three' not in _excludes:
        from .elements.scene import Scene as scene
