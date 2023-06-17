import os

__all__ = [
    'deprecated',
    'element',
    'aggrid',
    'audio',
    'avatar',
    'badge',
    'button',
    'card',
    'card_actions',
    'card_section',
    'chart',
    'chat_message',
    'checkbox',
    'color_input',
    'color_picker',
    'colors',
    'column',
    'dark_mode',
    'date',
    'dialog',
    'expansion',
    'grid',
    'html',
    'icon',
    'image',
    'input',
    'interactive_image',
    'joystick',
    'keyboard',
    'knob',
    'label',
    'link',
    'link_target',
    'log',
    'markdown',
    'menu',
    'menu_item',
    'mermaid',
    'number',
    'plotly',
    'circular_progress',
    'linear_progress',
    'query',
    'radio',
    'row',
    'scene',
    'select',
    'separator',
    'slider',
    'spinner',
    'splitter',
    'step',
    'stepper',
    'stepper_navigation',
    'switch',
    'table',
    'tab',
    'tab_panel',
    'tab_panels',
    'tabs',
    'textarea',
    'time',
    'toggle',
    'tooltip',
    'tree',
    'upload',
    'video',
    'download',
    'add_body_html',
    'add_head_html',
    'run_javascript',
    'notify',
    'open',
    'refreshable',
    'timer',
    'update',
    'page',
    'drawer',
    'footer',
    'header',
    'left_drawer',
    'page_sticky',
    'right_drawer',
    'run',
    'run_with',
]

from .deprecation import deprecated
from .element import Element as element
from .elements.aggrid import AgGrid as aggrid
from .elements.audio import Audio as audio
from .elements.avatar import Avatar as avatar
from .elements.badge import Badge as badge
from .elements.button import Button as button
from .elements.card import Card as card
from .elements.card import CardActions as card_actions
from .elements.card import CardSection as card_section
from .elements.chart import Chart as chart
from .elements.chat_message import ChatMessage as chat_message
from .elements.checkbox import Checkbox as checkbox
from .elements.color_input import ColorInput as color_input
from .elements.color_picker import ColorPicker as color_picker
from .elements.colors import Colors as colors
from .elements.column import Column as column
from .elements.dark_mode import DarkMode as dark_mode
from .elements.date import Date as date
from .elements.dialog import Dialog as dialog
from .elements.expansion import Expansion as expansion
from .elements.grid import Grid as grid
from .elements.html import Html as html
from .elements.icon import Icon as icon
from .elements.image import Image as image
from .elements.input import Input as input
from .elements.interactive_image import InteractiveImage as interactive_image
from .elements.joystick import Joystick as joystick
from .elements.keyboard import Keyboard as keyboard
from .elements.knob import Knob as knob
from .elements.label import Label as label
from .elements.link import Link as link
from .elements.link import LinkTarget as link_target
from .elements.log import Log as log
from .elements.markdown import Markdown as markdown
from .elements.menu import Menu as menu
from .elements.menu import MenuItem as menu_item
from .elements.mermaid import Mermaid as mermaid
from .elements.number import Number as number
from .elements.plotly import Plotly as plotly
from .elements.progress import CircularProgress as circular_progress
from .elements.progress import LinearProgress as linear_progress
from .elements.query import query
from .elements.radio import Radio as radio
from .elements.row import Row as row
from .elements.scene import Scene as scene
from .elements.select import Select as select
from .elements.separator import Separator as separator
from .elements.slider import Slider as slider
from .elements.spinner import Spinner as spinner
from .elements.splitter import Splitter as splitter
from .elements.stepper import Step as step
from .elements.stepper import Stepper as stepper
from .elements.stepper import StepperNavigation as stepper_navigation
from .elements.switch import Switch as switch
from .elements.table import Table as table
from .elements.tabs import Tab as tab
from .elements.tabs import TabPanel as tab_panel
from .elements.tabs import TabPanels as tab_panels
from .elements.tabs import Tabs as tabs
from .elements.textarea import Textarea as textarea
from .elements.time import Time as time
from .elements.toggle import Toggle as toggle
from .elements.tooltip import Tooltip as tooltip
from .elements.tree import Tree as tree
from .elements.upload import Upload as upload
from .elements.video import Video as video
from .functions.download import download
from .functions.html import add_body_html, add_head_html
from .functions.javascript import run_javascript
from .functions.notify import notify
from .functions.open import open
from .functions.refreshable import refreshable
from .functions.timer import Timer as timer
from .functions.update import update
from .page import page
from .page_layout import Drawer as drawer
from .page_layout import Footer as footer
from .page_layout import Header as header
from .page_layout import LeftDrawer as left_drawer
from .page_layout import PageSticky as page_sticky
from .page_layout import RightDrawer as right_drawer
from .run import run
from .run_with import run_with

if os.environ.get('MATPLOTLIB', 'true').lower() == 'true':
    from .elements.line_plot import LinePlot as line_plot
    from .elements.pyplot import Pyplot as pyplot
    plot = deprecated(pyplot, 'ui.plot', 'ui.pyplot', 317)
    __all__.extend(['line_plot', 'pyplot', 'plot'])
