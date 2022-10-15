# isort:skip_file
import os


class Ui:
    from .run import run  # NOTE: before justpy

    from .page import page, add_head_html, add_body_html, run_javascript
    from .update import update

    from .elements.button import Button as button
    from .elements.card import Card as card
    from .elements.card import CardSection as card_section
    from .elements.chart import Chart as chart
    from .elements.checkbox import Checkbox as checkbox
    from .elements.color_input import ColorInput as color_input
    from .elements.color_picker import ColorPicker as color_picker
    from .elements.colors import Colors as colors
    from .elements.column import Column as column
    from .elements.dialog import Dialog as dialog
    from .elements.expansion import Expansion as expansion
    from .elements.html import Html as html
    from .elements.icon import Icon as icon
    from .elements.image import Image as image
    from .elements.input import Input as input
    from .elements.interactive_image import InteractiveImage as interactive_image
    from .elements.joystick import Joystick as joystick
    from .elements.keyboard import Keyboard as keyboard
    from .elements.label import Label as label
    from .elements.link import Link as link
    from .elements.log import Log as log
    from .elements.markdown import Markdown as markdown
    from .elements.menu import Menu as menu
    from .elements.menu_item import MenuItem as menu_item
    from .elements.menu_separator import MenuSeparator as menu_separator
    from .elements.notify import Notify as notify
    from .elements.number import Number as number
    from .elements.open import open, open_async
    from .elements.radio import Radio as radio
    from .elements.row import Row as row
    from .elements.scene import Scene as scene
    from .elements.select import Select as select
    from .elements.slider import Slider as slider
    from .elements.switch import Switch as switch
    from .elements.table import Table as table
    from .elements.toggle import Toggle as toggle
    from .elements.tree import Tree as tree
    from .elements.upload import Upload as upload
    from .lifecycle import on_connect, on_disconnect, on_shutdown, on_startup, shutdown
    from .routes import add_route, add_static_files, get
    from .timer import Timer as timer

    if os.environ.get('MATPLOTLIB', 'true').lower() == 'true':
        from .elements.line_plot import LinePlot as line_plot
        from .elements.plot import Plot as plot
