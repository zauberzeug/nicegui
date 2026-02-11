import textwrap
from typing import TYPE_CHECKING

from lazy_imports import LazyModule, load

__all__ = [
    'add_body_html',
    'add_css',
    'add_head_html',
    'add_sass',
    'add_scss',
    'aggrid',
    'altair',
    'anywidget',
    'audio',
    'avatar',
    'badge',
    'button',
    'button_group',
    'card',
    'card_actions',
    'card_section',
    'carousel',
    'carousel_slide',
    'chat_message',
    'checkbox',
    'chip',
    'circular_progress',
    'clipboard',
    'code',
    'codemirror',
    'color_input',
    'color_picker',
    'colors',
    'column',
    'context',
    'context_menu',
    'dark_mode',
    'date',
    'date_input',
    'dialog',
    'download',
    'drawer',
    'dropdown_button',
    'echart',
    'editor',
    'element',
    'expansion',
    'fab',
    'fab_action',
    'footer',
    'fullscreen',
    'grid',
    'header',
    'highchart',
    'html',
    'icon',
    'image',
    'input',
    'input_chips',
    'interactive_image',
    'item',
    'item_label',
    'item_section',
    'joystick',
    'json_editor',
    'keyboard',
    'knob',
    'label',
    'leaflet',
    'left_drawer',
    'line_plot',
    'linear_progress',
    'link',
    'link_target',
    'list',
    'log',
    'markdown',
    'matplotlib',
    'menu',
    'menu_item',
    'mermaid',
    'navigate',
    'notification',
    'notify',
    'number',
    'on',
    'on_exception',
    'page',
    'page_scroller',
    'page_sticky',
    'page_title',
    'pagination',
    'plotly',
    'pyplot',
    'query',
    'radio',
    'range',
    'rating',
    'refreshable',
    'refreshable_method',
    'restructured_text',
    'right_drawer',
    'row',
    'run',
    'run_javascript',
    'run_with',
    'scene',
    'scene_view',
    'scroll_area',
    'select',
    'separator',
    'skeleton',
    'slide_item',
    'slider',
    'space',
    'spinner',
    'splitter',
    'state',
    'step',
    'stepper',
    'stepper_navigation',
    'sub_pages',
    'switch',
    'tab',
    'tab_panel',
    'tab_panels',
    'table',
    'tabs',
    'teleport',
    'textarea',
    'time',
    'time_input',
    'timeline',
    'timeline_entry',
    'timer',
    'toggle',
    'tooltip',
    'tree',
    'update',
    'upload',
    'video',
    'xterm',
]

# Create a lazy module that imports all the necessary components when accessed
_module = LazyModule(textwrap.dedent('''
    from nicegui.context import context
    from nicegui.element import Element as element
    from nicegui.elements.aggrid import AgGrid as aggrid
    from nicegui.elements.altair import Altair as altair
    from nicegui.elements.anywidget import AnyWidget as anywidget
    from nicegui.elements.audio import Audio as audio
    from nicegui.elements.avatar import Avatar as avatar
    from nicegui.elements.badge import Badge as badge
    from nicegui.elements.button import Button as button
    from nicegui.elements.button_dropdown import DropdownButton as dropdown_button
    from nicegui.elements.button_group import ButtonGroup as button_group
    from nicegui.elements.card import Card as card
    from nicegui.elements.card import CardActions as card_actions
    from nicegui.elements.card import CardSection as card_section
    from nicegui.elements.carousel import Carousel as carousel
    from nicegui.elements.carousel import CarouselSlide as carousel_slide
    from nicegui.elements.chat_message import ChatMessage as chat_message
    from nicegui.elements.checkbox import Checkbox as checkbox
    from nicegui.elements.chip import Chip as chip
    from nicegui.elements.code import Code as code
    from nicegui.elements.codemirror import CodeMirror as codemirror
    from nicegui.elements.color_input import ColorInput as color_input
    from nicegui.elements.color_picker import ColorPicker as color_picker
    from nicegui.elements.colors import Colors as colors
    from nicegui.elements.column import Column as column
    from nicegui.elements.context_menu import ContextMenu as context_menu
    from nicegui.elements.dark_mode import DarkMode as dark_mode
    from nicegui.elements.date import Date as date
    from nicegui.elements.date_input import DateInput as date_input
    from nicegui.elements.dialog import Dialog as dialog
    from nicegui.elements.drawer import Drawer as drawer
    from nicegui.elements.drawer import LeftDrawer as left_drawer
    from nicegui.elements.drawer import RightDrawer as right_drawer
    from nicegui.elements.echart import EChart as echart
    from nicegui.elements.editor import Editor as editor
    from nicegui.elements.expansion import Expansion as expansion
    from nicegui.elements.fab import Fab as fab
    from nicegui.elements.fab import FabAction as fab_action
    from nicegui.elements.footer import Footer as footer
    from nicegui.elements.fullscreen import Fullscreen as fullscreen
    from nicegui.elements.grid import Grid as grid
    from nicegui.elements.header import Header as header
    from nicegui.elements.highchart import highchart
    from nicegui.elements.html import Html as html
    from nicegui.elements.icon import Icon as icon
    from nicegui.elements.image import Image as image
    from nicegui.elements.input import Input as input  # pylint: disable=redefined-builtin
    from nicegui.elements.input_chips import InputChips as input_chips
    from nicegui.elements.interactive_image import InteractiveImage as interactive_image
    from nicegui.elements.item import Item as item
    from nicegui.elements.item import ItemLabel as item_label
    from nicegui.elements.item import ItemSection as item_section
    from nicegui.elements.joystick import Joystick as joystick
    from nicegui.elements.json_editor import JsonEditor as json_editor
    from nicegui.elements.keyboard import Keyboard as keyboard
    from nicegui.elements.knob import Knob as knob
    from nicegui.elements.label import Label as label
    from nicegui.elements.leaflet import Leaflet as leaflet
    from nicegui.elements.line_plot import LinePlot as line_plot
    from nicegui.elements.link import Link as link
    from nicegui.elements.link import LinkTarget as link_target
    from nicegui.elements.list import List as list  # pylint: disable=redefined-builtin
    from nicegui.elements.log import Log as log
    from nicegui.elements.markdown import Markdown as markdown
    from nicegui.elements.menu import Menu as menu
    from nicegui.elements.menu import MenuItem as menu_item
    from nicegui.elements.mermaid import Mermaid as mermaid
    from nicegui.elements.notification import Notification as notification
    from nicegui.elements.number import Number as number
    from nicegui.elements.page_scroller import PageScroller as page_scroller
    from nicegui.elements.page_sticky import PageSticky as page_sticky
    from nicegui.elements.pagination import Pagination as pagination
    from nicegui.elements.plotly import Plotly as plotly
    from nicegui.elements.progress import CircularProgress as circular_progress
    from nicegui.elements.progress import LinearProgress as linear_progress
    from nicegui.elements.pyplot import Matplotlib as matplotlib
    from nicegui.elements.pyplot import Pyplot as pyplot
    from nicegui.elements.query import Query as query
    from nicegui.elements.radio import Radio as radio
    from nicegui.elements.range import Range as range  # pylint: disable=redefined-builtin
    from nicegui.elements.rating import Rating as rating
    from nicegui.elements.restructured_text import ReStructuredText as restructured_text
    from nicegui.elements.row import Row as row
    from nicegui.elements.scene import Scene as scene
    from nicegui.elements.scene import SceneView as scene_view
    from nicegui.elements.scroll_area import ScrollArea as scroll_area
    from nicegui.elements.select import Select as select
    from nicegui.elements.separator import Separator as separator
    from nicegui.elements.skeleton import Skeleton as skeleton
    from nicegui.elements.slide_item import SlideItem as slide_item
    from nicegui.elements.slider import Slider as slider
    from nicegui.elements.space import Space as space
    from nicegui.elements.spinner import Spinner as spinner
    from nicegui.elements.splitter import Splitter as splitter
    from nicegui.elements.stepper import Step as step
    from nicegui.elements.stepper import Stepper as stepper
    from nicegui.elements.stepper import StepperNavigation as stepper_navigation
    from nicegui.elements.sub_pages import SubPages as sub_pages
    from nicegui.elements.switch import Switch as switch
    from nicegui.elements.table import Table as table
    from nicegui.elements.tabs import Tab as tab
    from nicegui.elements.tabs import TabPanel as tab_panel
    from nicegui.elements.tabs import TabPanels as tab_panels
    from nicegui.elements.tabs import Tabs as tabs
    from nicegui.elements.teleport import Teleport as teleport
    from nicegui.elements.textarea import Textarea as textarea
    from nicegui.elements.time import Time as time
    from nicegui.elements.time_input import TimeInput as time_input
    from nicegui.elements.timeline import Timeline as timeline
    from nicegui.elements.timeline import TimelineEntry as timeline_entry
    from nicegui.elements.timer import Timer as timer
    from nicegui.elements.toggle import Toggle as toggle
    from nicegui.elements.tooltip import Tooltip as tooltip
    from nicegui.elements.tree import Tree as tree
    from nicegui.elements.upload import Upload as upload
    from nicegui.elements.video import Video as video
    from nicegui.elements.xterm import Xterm as xterm
    from nicegui.functions.clipboard import clipboard
    from nicegui.functions.download import download
    from nicegui.functions.html import add_body_html, add_head_html
    from nicegui.functions.javascript import run_javascript
    from nicegui.functions.navigate import navigate
    from nicegui.functions.notify import notify
    from nicegui.functions.on import on
    from nicegui.functions.on_exception import on_exception
    from nicegui.functions.page_title import page_title
    from nicegui.functions.refreshable import refreshable, refreshable_method, state
    from nicegui.functions.style import add_css, add_sass, add_scss
    from nicegui.functions.update import update
    from nicegui.page import page
    from nicegui.ui_run import run
    from nicegui.ui_run_with import run_with
'''), name=__name__, doc=__doc__)

if TYPE_CHECKING:
    from .context import context
    from .element import Element as element
    from .elements.aggrid import AgGrid as aggrid
    from .elements.altair import Altair as altair
    from .elements.anywidget import AnyWidget as anywidget
    from .elements.audio import Audio as audio
    from .elements.avatar import Avatar as avatar
    from .elements.badge import Badge as badge
    from .elements.button import Button as button
    from .elements.button_dropdown import DropdownButton as dropdown_button
    from .elements.button_group import ButtonGroup as button_group
    from .elements.card import Card as card
    from .elements.card import CardActions as card_actions
    from .elements.card import CardSection as card_section
    from .elements.carousel import Carousel as carousel
    from .elements.carousel import CarouselSlide as carousel_slide
    from .elements.chat_message import ChatMessage as chat_message
    from .elements.checkbox import Checkbox as checkbox
    from .elements.chip import Chip as chip
    from .elements.code import Code as code
    from .elements.codemirror import CodeMirror as codemirror
    from .elements.color_input import ColorInput as color_input
    from .elements.color_picker import ColorPicker as color_picker
    from .elements.colors import Colors as colors
    from .elements.column import Column as column
    from .elements.context_menu import ContextMenu as context_menu
    from .elements.dark_mode import DarkMode as dark_mode
    from .elements.date import Date as date
    from .elements.date_input import DateInput as date_input
    from .elements.dialog import Dialog as dialog
    from .elements.drawer import Drawer as drawer
    from .elements.drawer import LeftDrawer as left_drawer
    from .elements.drawer import RightDrawer as right_drawer
    from .elements.echart import EChart as echart
    from .elements.editor import Editor as editor
    from .elements.expansion import Expansion as expansion
    from .elements.fab import Fab as fab
    from .elements.fab import FabAction as fab_action
    from .elements.footer import Footer as footer
    from .elements.fullscreen import Fullscreen as fullscreen
    from .elements.grid import Grid as grid
    from .elements.header import Header as header
    from .elements.highchart import highchart
    from .elements.html import Html as html
    from .elements.icon import Icon as icon
    from .elements.image import Image as image
    from .elements.input import Input as input  # pylint: disable=redefined-builtin
    from .elements.input_chips import InputChips as input_chips
    from .elements.interactive_image import InteractiveImage as interactive_image
    from .elements.item import Item as item
    from .elements.item import ItemLabel as item_label
    from .elements.item import ItemSection as item_section
    from .elements.joystick import Joystick as joystick
    from .elements.json_editor import JsonEditor as json_editor
    from .elements.keyboard import Keyboard as keyboard
    from .elements.knob import Knob as knob
    from .elements.label import Label as label
    from .elements.leaflet import Leaflet as leaflet
    from .elements.line_plot import LinePlot as line_plot
    from .elements.link import Link as link
    from .elements.link import LinkTarget as link_target
    from .elements.list import List as list  # pylint: disable=redefined-builtin
    from .elements.log import Log as log
    from .elements.markdown import Markdown as markdown
    from .elements.menu import Menu as menu
    from .elements.menu import MenuItem as menu_item
    from .elements.mermaid import Mermaid as mermaid
    from .elements.notification import Notification as notification
    from .elements.number import Number as number
    from .elements.page_scroller import PageScroller as page_scroller
    from .elements.page_sticky import PageSticky as page_sticky
    from .elements.pagination import Pagination as pagination
    from .elements.plotly import Plotly as plotly
    from .elements.progress import CircularProgress as circular_progress
    from .elements.progress import LinearProgress as linear_progress
    from .elements.pyplot import Matplotlib as matplotlib
    from .elements.pyplot import Pyplot as pyplot
    from .elements.query import Query as query
    from .elements.radio import Radio as radio
    from .elements.range import Range as range  # pylint: disable=redefined-builtin
    from .elements.rating import Rating as rating
    from .elements.restructured_text import ReStructuredText as restructured_text
    from .elements.row import Row as row
    from .elements.scene import Scene as scene
    from .elements.scene import SceneView as scene_view
    from .elements.scroll_area import ScrollArea as scroll_area
    from .elements.select import Select as select
    from .elements.separator import Separator as separator
    from .elements.skeleton import Skeleton as skeleton
    from .elements.slide_item import SlideItem as slide_item
    from .elements.slider import Slider as slider
    from .elements.space import Space as space
    from .elements.spinner import Spinner as spinner
    from .elements.splitter import Splitter as splitter
    from .elements.stepper import Step as step
    from .elements.stepper import Stepper as stepper
    from .elements.stepper import StepperNavigation as stepper_navigation
    from .elements.sub_pages import SubPages as sub_pages
    from .elements.switch import Switch as switch
    from .elements.table import Table as table
    from .elements.tabs import Tab as tab
    from .elements.tabs import TabPanel as tab_panel
    from .elements.tabs import TabPanels as tab_panels
    from .elements.tabs import Tabs as tabs
    from .elements.teleport import Teleport as teleport
    from .elements.textarea import Textarea as textarea
    from .elements.time import Time as time
    from .elements.time_input import TimeInput as time_input
    from .elements.timeline import Timeline as timeline
    from .elements.timeline import TimelineEntry as timeline_entry
    from .elements.timer import Timer as timer
    from .elements.toggle import Toggle as toggle
    from .elements.tooltip import Tooltip as tooltip
    from .elements.tree import Tree as tree
    from .elements.upload import Upload as upload
    from .elements.video import Video as video
    from .elements.xterm import Xterm as xterm
    from .functions.clipboard import clipboard
    from .functions.download import download
    from .functions.html import add_body_html, add_head_html
    from .functions.javascript import run_javascript
    from .functions.navigate import navigate
    from .functions.notify import notify
    from .functions.on import on
    from .functions.on_exception import on_exception
    from .functions.page_title import page_title
    from .functions.refreshable import refreshable, refreshable_method, state
    from .functions.style import add_css, add_sass, add_scss
    from .functions.update import update
    from .page import page
    from .ui_run import run
    from .ui_run_with import run_with
else:
    # Register the lazy module in sys.modules to enable proper caching
    load(_module)
