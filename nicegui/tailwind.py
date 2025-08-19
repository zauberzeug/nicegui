# pylint: disable=too-many-lines
from __future__ import annotations

import weakref
from typing import TYPE_CHECKING, overload

if TYPE_CHECKING:
    from .element import Element
    from .tailwind_types.accent_color import AccentColor
    from .tailwind_types.align_content import AlignContent
    from .tailwind_types.align_items import AlignItems
    from .tailwind_types.align_self import AlignSelf
    from .tailwind_types.animation import Animation
    from .tailwind_types.appearance import Appearance
    from .tailwind_types.aspect_ratio import AspectRatio
    from .tailwind_types.backdrop_filter import BackdropFilter
    from .tailwind_types.backdrop_filter_blur import BackdropFilterBlur
    from .tailwind_types.backdrop_filter_grayscale import BackdropFilterGrayscale
    from .tailwind_types.backdrop_filter_invert import BackdropFilterInvert
    from .tailwind_types.backdrop_filter_sepia import BackdropFilterSepia
    from .tailwind_types.backface_visibility import BackfaceVisibility
    from .tailwind_types.background_attachment import BackgroundAttachment
    from .tailwind_types.background_blend_mode import BackgroundBlendMode
    from .tailwind_types.background_clip import BackgroundClip
    from .tailwind_types.background_color import BackgroundColor
    from .tailwind_types.background_image import BackgroundImage
    from .tailwind_types.background_origin import BackgroundOrigin
    from .tailwind_types.background_position import BackgroundPosition
    from .tailwind_types.background_repeat import BackgroundRepeat
    from .tailwind_types.background_size import BackgroundSize
    from .tailwind_types.border_collapse import BorderCollapse
    from .tailwind_types.border_color import BorderColor
    from .tailwind_types.border_radius import BorderRadius
    from .tailwind_types.border_style import BorderStyle
    from .tailwind_types.border_width import BorderWidth
    from .tailwind_types.box_decoration_break import BoxDecorationBreak
    from .tailwind_types.box_shadow import BoxShadow
    from .tailwind_types.box_sizing import BoxSizing
    from .tailwind_types.break_after import BreakAfter
    from .tailwind_types.break_before import BreakBefore
    from .tailwind_types.break_inside import BreakInside
    from .tailwind_types.caption_side import CaptionSide
    from .tailwind_types.caret_color import CaretColor
    from .tailwind_types.clear import Clear
    from .tailwind_types.color import Color
    from .tailwind_types.color_scheme import ColorScheme
    from .tailwind_types.columns import Columns
    from .tailwind_types.content import Content
    from .tailwind_types.cursor import Cursor
    from .tailwind_types.display import Display
    from .tailwind_types.field_sizing import FieldSizing
    from .tailwind_types.fill import Fill
    from .tailwind_types.filter import Filter
    from .tailwind_types.filter_blur import FilterBlur
    from .tailwind_types.filter_drop_shadow import FilterDropShadow
    from .tailwind_types.filter_grayscale import FilterGrayscale
    from .tailwind_types.filter_invert import FilterInvert
    from .tailwind_types.filter_sepia import FilterSepia
    from .tailwind_types.flex import Flex
    from .tailwind_types.flex_basis import FlexBasis
    from .tailwind_types.flex_direction import FlexDirection
    from .tailwind_types.flex_grow import FlexGrow
    from .tailwind_types.flex_shrink import FlexShrink
    from .tailwind_types.flex_wrap import FlexWrap
    from .tailwind_types.float import Float
    from .tailwind_types.font_family import FontFamily
    from .tailwind_types.font_size import FontSize
    from .tailwind_types.font_smoothing import FontSmoothing
    from .tailwind_types.font_stretch import FontStretch
    from .tailwind_types.font_style import FontStyle
    from .tailwind_types.font_variant_numeric import FontVariantNumeric
    from .tailwind_types.font_weight import FontWeight
    from .tailwind_types.forced_color_adjust import ForcedColorAdjust
    from .tailwind_types.grid_auto_columns import GridAutoColumns
    from .tailwind_types.grid_auto_flow import GridAutoFlow
    from .tailwind_types.grid_auto_rows import GridAutoRows
    from .tailwind_types.grid_column import GridColumn
    from .tailwind_types.grid_row import GridRow
    from .tailwind_types.grid_template_columns import GridTemplateColumns
    from .tailwind_types.grid_template_rows import GridTemplateRows
    from .tailwind_types.height import Height
    from .tailwind_types.hyphens import Hyphens
    from .tailwind_types.isolation import Isolation
    from .tailwind_types.justify_content import JustifyContent
    from .tailwind_types.justify_items import JustifyItems
    from .tailwind_types.justify_self import JustifySelf
    from .tailwind_types.letter_spacing import LetterSpacing
    from .tailwind_types.line_clamp import LineClamp
    from .tailwind_types.line_height import LineHeight
    from .tailwind_types.list_style_image import ListStyleImage
    from .tailwind_types.list_style_position import ListStylePosition
    from .tailwind_types.list_style_type import ListStyleType
    from .tailwind_types.margin import Margin
    from .tailwind_types.mask_clip import MaskClip
    from .tailwind_types.mask_composite import MaskComposite
    from .tailwind_types.mask_image import MaskImage
    from .tailwind_types.mask_mode import MaskMode
    from .tailwind_types.mask_origin import MaskOrigin
    from .tailwind_types.mask_position import MaskPosition
    from .tailwind_types.mask_repeat import MaskRepeat
    from .tailwind_types.mask_size import MaskSize
    from .tailwind_types.mask_type import MaskType
    from .tailwind_types.max_height import MaxHeight
    from .tailwind_types.max_width import MaxWidth
    from .tailwind_types.min_height import MinHeight
    from .tailwind_types.min_width import MinWidth
    from .tailwind_types.mix_blend_mode import MixBlendMode
    from .tailwind_types.object_fit import ObjectFit
    from .tailwind_types.object_position import ObjectPosition
    from .tailwind_types.order import Order
    from .tailwind_types.outline_color import OutlineColor
    from .tailwind_types.outline_style import OutlineStyle
    from .tailwind_types.outline_width import OutlineWidth
    from .tailwind_types.overflow import Overflow
    from .tailwind_types.overflow_wrap import OverflowWrap
    from .tailwind_types.overscroll_behavior import OverscrollBehavior
    from .tailwind_types.padding import Padding
    from .tailwind_types.perspective import Perspective
    from .tailwind_types.perspective_origin import PerspectiveOrigin
    from .tailwind_types.place_content import PlaceContent
    from .tailwind_types.place_items import PlaceItems
    from .tailwind_types.place_self import PlaceSelf
    from .tailwind_types.pointer_events import PointerEvents
    from .tailwind_types.position import Position
    from .tailwind_types.resize import Resize
    from .tailwind_types.rotate import Rotate
    from .tailwind_types.scale import Scale
    from .tailwind_types.scroll_behavior import ScrollBehavior
    from .tailwind_types.scroll_snap_align import ScrollSnapAlign
    from .tailwind_types.scroll_snap_stop import ScrollSnapStop
    from .tailwind_types.scroll_snap_type import ScrollSnapType
    from .tailwind_types.stroke import Stroke
    from .tailwind_types.table_layout import TableLayout
    from .tailwind_types.text_align import TextAlign
    from .tailwind_types.text_decoration_color import TextDecorationColor
    from .tailwind_types.text_decoration_line import TextDecorationLine
    from .tailwind_types.text_decoration_style import TextDecorationStyle
    from .tailwind_types.text_decoration_thickness import TextDecorationThickness
    from .tailwind_types.text_indent import TextIndent
    from .tailwind_types.text_overflow import TextOverflow
    from .tailwind_types.text_shadow import TextShadow
    from .tailwind_types.text_transform import TextTransform
    from .tailwind_types.text_underline_offset import TextUnderlineOffset
    from .tailwind_types.text_wrap import TextWrap
    from .tailwind_types.top_right_bottom_left import TopRightBottomLeft
    from .tailwind_types.touch_action import TouchAction
    from .tailwind_types.transform import Transform
    from .tailwind_types.transform_origin import TransformOrigin
    from .tailwind_types.transform_style import TransformStyle
    from .tailwind_types.transition_behavior import TransitionBehavior
    from .tailwind_types.transition_duration import TransitionDuration
    from .tailwind_types.transition_property import TransitionProperty
    from .tailwind_types.transition_timing_function import TransitionTimingFunction
    from .tailwind_types.translate import Translate
    from .tailwind_types.user_select import UserSelect
    from .tailwind_types.vertical_align import VerticalAlign
    from .tailwind_types.visibility import Visibility
    from .tailwind_types.white_space import WhiteSpace
    from .tailwind_types.width import Width
    from .tailwind_types.will_change import WillChange
    from .tailwind_types.word_break import WordBreak
    from .tailwind_types.z_index import ZIndex


class PseudoElement:

    def __init__(self) -> None:
        self._classes: list[str] = []

    def classes(self, add: str) -> None:
        """Add the given classes to the element."""
        self._classes.append(add)


class Tailwind:

    def __init__(self, _element: Element | None = None) -> None:
        self._element: PseudoElement | weakref.ref[Element] = \
            PseudoElement() if _element is None else weakref.ref(_element)

    @property
    def element(self) -> PseudoElement | Element:
        """The element or pseudo element this Tailwind object belongs to."""
        element = self._element if isinstance(self._element, PseudoElement) else self._element()
        if element is None:
            raise RuntimeError('The element this Tailwind object belongs to has been deleted.')
        return element

    @overload
    def __call__(self, tailwind: Tailwind) -> Tailwind:
        ...

    @overload
    def __call__(self, *classes: str) -> Tailwind:
        ...

    def __call__(self, *args) -> Tailwind:  # type: ignore
        if not args:
            return self
        if isinstance(args[0], Tailwind):
            args[0].apply(self.element)  # type: ignore
        else:
            self.element.classes(' '.join(args))
        return self

    def apply(self, element: Element) -> None:
        """Apply the tailwind classes to the given element."""
        element._classes.extend(self.element._classes)  # pylint: disable=protected-access
        element.update()

    def aspect_ratio(self, value: AspectRatio) -> Tailwind:
        """Utilities for controlling the aspect ratio of an element."""
        self.element.classes('aspect-' + value)
        return self

    def columns(self, value: Columns) -> Tailwind:
        """Utilities for controlling the number of columns within an element."""
        self.element.classes('columns-' + value)
        return self

    def break_after(self, value: BreakAfter) -> Tailwind:
        """Utilities for controlling how a column or page should break after an element."""
        self.element.classes('break-after-' + value)
        return self

    def break_before(self, value: BreakBefore) -> Tailwind:
        """Utilities for controlling how a column or page should break before an element."""
        self.element.classes('break-before-' + value)
        return self

    def break_inside(self, value: BreakInside) -> Tailwind:
        """Utilities for controlling how a column or page should break within an element."""
        self.element.classes('break-inside-' + value)
        return self

    def box_decoration_break(self, value: BoxDecorationBreak) -> Tailwind:
        """Utilities for controlling how element fragments should be rendered across multiple lines, columns, or pages."""
        self.element.classes('box-decoration-' + value)
        return self

    def box_sizing(self, value: BoxSizing) -> Tailwind:
        """Utilities for controlling how the browser should calculate an element's total size."""
        self.element.classes('box-' + value)
        return self

    def display(self, value: Display) -> Tailwind:
        """Utilities for controlling the display box type of an element."""
        self.element.classes('' + value)
        return self

    def float(self, value: Float) -> Tailwind:
        """Utilities for controlling the wrapping of content around an element."""
        self.element.classes('float-' + value)
        return self

    def clear(self, value: Clear) -> Tailwind:
        """Utilities for controlling the wrapping of content around an element."""
        self.element.classes('clear-' + value)
        return self

    def isolation(self, value: Isolation) -> Tailwind:
        """Utilities for controlling whether an element should explicitly create a new stacking context."""
        self.element.classes('' + value)
        return self

    def object_fit(self, value: ObjectFit) -> Tailwind:
        """Utilities for controlling how a replaced element's content should be resized."""
        self.element.classes('object-' + value)
        return self

    def object_position(self, value: ObjectPosition) -> Tailwind:
        """Utilities for controlling how a replaced element's content should be positioned within its container."""
        self.element.classes('object-' + value)
        return self

    def overflow(self, value: Overflow) -> Tailwind:
        """Utilities for controlling how an element handles content that is too large for the container."""
        self.element.classes('overflow-' + value)
        return self

    def overscroll_behavior(self, value: OverscrollBehavior) -> Tailwind:
        """Utilities for controlling how the browser behaves when reaching the boundary of a scrolling area."""
        self.element.classes('overscroll-' + value)
        return self

    def position(self, value: Position) -> Tailwind:
        """Utilities for controlling how an element is positioned in the document."""
        self.element.classes('' + value)
        return self

    def top_right_bottom_left(self, value: TopRightBottomLeft) -> Tailwind:
        """Utilities for controlling the placement of positioned elements."""
        self.element.classes('' + value)
        return self

    def visibility(self, value: Visibility) -> Tailwind:
        """Utilities for controlling the visibility of an element."""
        self.element.classes('' + value)
        return self

    def z_index(self, value: ZIndex) -> Tailwind:
        """Utilities for controlling the stack order of an element."""
        self.element.classes('z-auto-' + value if value else 'z-auto')
        return self

    def flex_basis(self, value: FlexBasis) -> Tailwind:
        """Utilities for controlling the initial size of flex items."""
        self.element.classes('basis-' + value)
        return self

    def flex_direction(self, value: FlexDirection) -> Tailwind:
        """Utilities for controlling the direction of flex items."""
        self.element.classes('flex-' + value)
        return self

    def flex_wrap(self, value: FlexWrap) -> Tailwind:
        """Utilities for controlling how flex items wrap."""
        self.element.classes('flex-' + value)
        return self

    def flex(self, value: Flex) -> Tailwind:
        """Utilities for controlling how flex items both grow and shrink."""
        self.element.classes('flex-' + value)
        return self

    def flex_grow(self, value: FlexGrow) -> Tailwind:
        """Utilities for controlling how flex items grow."""
        self.element.classes('grow-' + value if value else 'grow')
        return self

    def flex_shrink(self, value: FlexShrink) -> Tailwind:
        """Utilities for controlling how flex items shrink."""
        self.element.classes('shrink-' + value if value else 'shrink')
        return self

    def order(self, value: Order) -> Tailwind:
        """Utilities for controlling the order of flex and grid items."""
        self.element.classes('order-' + value)
        return self

    def grid_template_columns(self, value: GridTemplateColumns) -> Tailwind:
        """Utilities for specifying the columns in a grid layout."""
        self.element.classes('grid-cols-' + value)
        return self

    def grid_column(self, value: GridColumn) -> Tailwind:
        """Utilities for controlling how elements are sized and placed across grid columns."""
        self.element.classes('col-' + value)
        return self

    def grid_template_rows(self, value: GridTemplateRows) -> Tailwind:
        """Utilities for specifying the rows in a grid layout."""
        self.element.classes('grid-rows-' + value)
        return self

    def grid_row(self, value: GridRow) -> Tailwind:
        """Utilities for controlling how elements are sized and placed across grid rows."""
        self.element.classes('row-' + value)
        return self

    def grid_auto_flow(self, value: GridAutoFlow) -> Tailwind:
        """Utilities for controlling how elements in a grid are auto-placed."""
        self.element.classes('grid-flow-' + value)
        return self

    def grid_auto_columns(self, value: GridAutoColumns) -> Tailwind:
        """Utilities for controlling the size of implicitly-created grid columns."""
        self.element.classes('auto-cols-' + value)
        return self

    def grid_auto_rows(self, value: GridAutoRows) -> Tailwind:
        """Utilities for controlling the size of implicitly-created grid rows."""
        self.element.classes('auto-rows-' + value)
        return self

    def justify_content(self, value: JustifyContent) -> Tailwind:
        """Utilities for controlling how flex and grid items are positioned along a container's main axis."""
        self.element.classes('justify-' + value)
        return self

    def justify_items(self, value: JustifyItems) -> Tailwind:
        """Utilities for controlling how grid items are aligned along their inline axis."""
        self.element.classes('justify-items-' + value)
        return self

    def justify_self(self, value: JustifySelf) -> Tailwind:
        """Utilities for controlling how an individual grid item is aligned along its inline axis."""
        self.element.classes('justify-self-' + value)
        return self

    def align_content(self, value: AlignContent) -> Tailwind:
        """Utilities for controlling how rows are positioned in multi-row flex and grid containers."""
        self.element.classes('content-' + value)
        return self

    def align_items(self, value: AlignItems) -> Tailwind:
        """Utilities for controlling how flex and grid items are positioned along a container's cross axis."""
        self.element.classes('items-' + value)
        return self

    def align_self(self, value: AlignSelf) -> Tailwind:
        """Utilities for controlling how an individual flex or grid item is positioned along its container's cross axis."""
        self.element.classes('self-' + value)
        return self

    def place_content(self, value: PlaceContent) -> Tailwind:
        """Utilities for controlling how content is justified and aligned at the same time."""
        self.element.classes('place-content-' + value)
        return self

    def place_items(self, value: PlaceItems) -> Tailwind:
        """Utilities for controlling how items are justified and aligned at the same time."""
        self.element.classes('place-items-' + value)
        return self

    def place_self(self, value: PlaceSelf) -> Tailwind:
        """Utilities for controlling how an individual item is justified and aligned at the same time."""
        self.element.classes('place-self-' + value)
        return self

    def padding(self, value: Padding) -> Tailwind:
        """Utilities for controlling an element's padding."""
        self.element.classes('' + value)
        return self

    def margin(self, value: Margin) -> Tailwind:
        """Utilities for controlling an element's margin."""
        self.element.classes('' + value)
        return self

    def width(self, value: Width) -> Tailwind:
        """Utilities for setting the width of an element."""
        self.element.classes('' + value)
        return self

    def min_width(self, value: MinWidth) -> Tailwind:
        """Utilities for setting the minimum width of an element."""
        self.element.classes('min-w-' + value)
        return self

    def max_width(self, value: MaxWidth) -> Tailwind:
        """Utilities for setting the maximum width of an element."""
        self.element.classes('' + value)
        return self

    def height(self, value: Height) -> Tailwind:
        """Utilities for setting the height of an element."""
        self.element.classes('' + value)
        return self

    def min_height(self, value: MinHeight) -> Tailwind:
        """Utilities for setting the minimum height of an element."""
        self.element.classes('min-h-' + value)
        return self

    def max_height(self, value: MaxHeight) -> Tailwind:
        """Utilities for setting the maximum height of an element."""
        self.element.classes('max-h-' + value)
        return self

    def font_family(self, value: FontFamily) -> Tailwind:
        """Utilities for controlling the font family of an element."""
        self.element.classes('font-' + value)
        return self

    def font_size(self, value: FontSize) -> Tailwind:
        """Utilities for controlling the font size of an element."""
        self.element.classes('text-' + value)
        return self

    def font_smoothing(self, value: FontSmoothing) -> Tailwind:
        """Utilities for controlling the font smoothing of an element."""
        self.element.classes('' + value)
        return self

    def font_style(self, value: FontStyle) -> Tailwind:
        """Utilities for controlling the style of text."""
        self.element.classes('' + value)
        return self

    def font_weight(self, value: FontWeight) -> Tailwind:
        """Utilities for controlling the font weight of an element."""
        self.element.classes('font-' + value)
        return self

    def font_stretch(self, value: FontStretch) -> Tailwind:
        """Utilities for selecting the width of a font face."""
        self.element.classes('font-stretch-' + value)
        return self

    def font_variant_numeric(self, value: FontVariantNumeric) -> Tailwind:
        """Utilities for controlling the variant of numbers."""
        self.element.classes('' + value)
        return self

    def letter_spacing(self, value: LetterSpacing) -> Tailwind:
        """Utilities for controlling the tracking, or letter spacing, of an element."""
        self.element.classes('tracking-' + value)
        return self

    def line_clamp(self, value: LineClamp) -> Tailwind:
        """Utilities for clamping text to a specific number of lines."""
        self.element.classes('line-clamp-none-' + value if value else 'line-clamp-none')
        return self

    def line_height(self, value: LineHeight) -> Tailwind:
        """Utilities for controlling the leading, or line height, of an element."""
        self.element.classes('leading-none-' + value if value else 'leading-none')
        return self

    def list_style_image(self, value: ListStyleImage) -> Tailwind:
        """Utilities for controlling the marker images for list items."""
        self.element.classes('list-image-none-' + value if value else 'list-image-none')
        return self

    def list_style_position(self, value: ListStylePosition) -> Tailwind:
        """Utilities for controlling the position of bullets and numbers in lists."""
        self.element.classes('list-' + value)
        return self

    def list_style_type(self, value: ListStyleType) -> Tailwind:
        """Utilities for controlling the marker style of a list."""
        self.element.classes('list-' + value)
        return self

    def text_align(self, value: TextAlign) -> Tailwind:
        """Utilities for controlling the alignment of text."""
        self.element.classes('text-' + value)
        return self

    def color(self, value: Color) -> Tailwind:
        """Utilities for controlling the text color of an element."""
        self.element.classes('text-' + value)
        return self

    def text_decoration_line(self, value: TextDecorationLine) -> Tailwind:
        """Utilities for controlling the decoration of text."""
        self.element.classes('' + value)
        return self

    def text_decoration_color(self, value: TextDecorationColor) -> Tailwind:
        """Utilities for controlling the color of text decorations."""
        self.element.classes('decoration-' + value)
        return self

    def text_decoration_style(self, value: TextDecorationStyle) -> Tailwind:
        """Utilities for controlling the style of text decorations."""
        self.element.classes('decoration-' + value)
        return self

    def text_decoration_thickness(self, value: TextDecorationThickness) -> Tailwind:
        """Utilities for controlling the thickness of text decorations."""
        self.element.classes('decoration-' + value)
        return self

    def text_underline_offset(self, value: TextUnderlineOffset) -> Tailwind:
        """Utilities for controlling the offset of a text underline."""
        self.element.classes('underline-offset-auto-' + value if value else 'underline-offset-auto')
        return self

    def text_transform(self, value: TextTransform) -> Tailwind:
        """Utilities for controlling the capitalization of text."""
        self.element.classes('' + value)
        return self

    def text_overflow(self, value: TextOverflow) -> Tailwind:
        """Utilities for controlling how the text of an element overflows."""
        self.element.classes('' + value)
        return self

    def text_wrap(self, value: TextWrap) -> Tailwind:
        """Utilities for controlling how text wraps within an element."""
        self.element.classes('text-' + value)
        return self

    def text_indent(self, value: TextIndent) -> Tailwind:
        """Utilities for controlling the amount of empty space shown before text in a block."""
        self.element.classes('' + value)
        return self

    def vertical_align(self, value: VerticalAlign) -> Tailwind:
        """Utilities for controlling the vertical alignment of an inline or table-cell box."""
        self.element.classes('align-' + value)
        return self

    def white_space(self, value: WhiteSpace) -> Tailwind:
        """Utilities for controlling an element's white-space property."""
        self.element.classes('whitespace-' + value)
        return self

    def word_break(self, value: WordBreak) -> Tailwind:
        """Utilities for controlling word breaks in an element."""
        self.element.classes('break-' + value)
        return self

    def overflow_wrap(self, value: OverflowWrap) -> Tailwind:
        """Utilities for controlling line breaks within words in an overflowing element."""
        self.element.classes('wrap-' + value)
        return self

    def hyphens(self, value: Hyphens) -> Tailwind:
        """Utilities for controlling how words should be hyphenated."""
        self.element.classes('hyphens-' + value)
        return self

    def content(self, value: Content) -> Tailwind:
        """Utilities for controlling the content of the before and after pseudo-elements."""
        self.element.classes('content-none-' + value if value else 'content-none')
        return self

    def background_attachment(self, value: BackgroundAttachment) -> Tailwind:
        """Utilities for controlling how a background image behaves when scrolling."""
        self.element.classes('bg-' + value)
        return self

    def background_clip(self, value: BackgroundClip) -> Tailwind:
        """Utilities for controlling the bounding box of an element's background."""
        self.element.classes('bg-clip-' + value)
        return self

    def background_color(self, value: BackgroundColor) -> Tailwind:
        """Utilities for controlling an element's background color."""
        self.element.classes('bg-' + value)
        return self

    def background_image(self, value: BackgroundImage) -> Tailwind:
        """Utilities for controlling an element's background image."""
        self.element.classes('bg-' + value)
        return self

    def background_origin(self, value: BackgroundOrigin) -> Tailwind:
        """Utilities for controlling how an element's background is positioned relative to borders, padding, and content."""
        self.element.classes('bg-origin-' + value)
        return self

    def background_position(self, value: BackgroundPosition) -> Tailwind:
        """Utilities for controlling the position of an element's background image."""
        self.element.classes('bg-' + value)
        return self

    def background_repeat(self, value: BackgroundRepeat) -> Tailwind:
        """Utilities for controlling the repetition of an element's background image."""
        self.element.classes('bg-' + value)
        return self

    def background_size(self, value: BackgroundSize) -> Tailwind:
        """Utilities for controlling the background size of an element's background image."""
        self.element.classes('bg-' + value)
        return self

    def border_radius(self, value: BorderRadius) -> Tailwind:
        """Utilities for controlling the border radius of an element."""
        self.element.classes('rounded-' + value)
        return self

    def border_width(self, value: BorderWidth) -> Tailwind:
        """Utilities for controlling the width of an element's borders."""
        self.element.classes('' + value)
        return self

    def border_color(self, value: BorderColor) -> Tailwind:
        """Utilities for controlling the color of an element's borders."""
        self.element.classes('' + value)
        return self

    def border_style(self, value: BorderStyle) -> Tailwind:
        """Utilities for controlling the style of an element's borders."""
        self.element.classes('' + value)
        return self

    def outline_width(self, value: OutlineWidth) -> Tailwind:
        """Utilities for controlling the width of an element's outline."""
        self.element.classes('outline-' + value if value else 'outline')
        return self

    def outline_color(self, value: OutlineColor) -> Tailwind:
        """Utilities for controlling the color of an element's outline."""
        self.element.classes('outline-' + value)
        return self

    def outline_style(self, value: OutlineStyle) -> Tailwind:
        """Utilities for controlling the style of an element's outline."""
        self.element.classes('outline-' + value)
        return self

    def box_shadow(self, value: BoxShadow) -> Tailwind:
        """Utilities for controlling the box shadow of an element."""
        self.element.classes('' + value)
        return self

    def text_shadow(self, value: TextShadow) -> Tailwind:
        """Utilities for controlling the shadow of a text element."""
        self.element.classes('text-shadow-' + value)
        return self

    def mix_blend_mode(self, value: MixBlendMode) -> Tailwind:
        """Utilities for controlling how an element should blend with the background."""
        self.element.classes('mix-blend-' + value)
        return self

    def background_blend_mode(self, value: BackgroundBlendMode) -> Tailwind:
        """Utilities for controlling how an element's background image should blend with its background color."""
        self.element.classes('bg-blend-' + value)
        return self

    def mask_clip(self, value: MaskClip) -> Tailwind:
        """Utilities for controlling the bounding box of an element's mask."""
        self.element.classes('mask-' + value)
        return self

    def mask_composite(self, value: MaskComposite) -> Tailwind:
        """Utilities for controlling how multiple masks are combined together."""
        self.element.classes('mask-' + value)
        return self

    def mask_image(self, value: MaskImage) -> Tailwind:
        """Utilities for controlling an element's mask image."""
        self.element.classes('mask-' + value)
        return self

    def mask_mode(self, value: MaskMode) -> Tailwind:
        """Utilities for controlling an element's mask mode."""
        self.element.classes('mask-' + value)
        return self

    def mask_origin(self, value: MaskOrigin) -> Tailwind:
        """Utilities for controlling how an element's mask image is positioned relative to borders, padding, and content."""
        self.element.classes('mask-origin-' + value)
        return self

    def mask_position(self, value: MaskPosition) -> Tailwind:
        """Utilities for controlling the position of an element's mask image."""
        self.element.classes('mask-' + value)
        return self

    def mask_repeat(self, value: MaskRepeat) -> Tailwind:
        """Utilities for controlling the repetition of an element's mask image."""
        self.element.classes('mask-' + value)
        return self

    def mask_size(self, value: MaskSize) -> Tailwind:
        """Utilities for controlling the size of an element's mask image."""
        self.element.classes('mask-' + value)
        return self

    def mask_type(self, value: MaskType) -> Tailwind:
        """Utilities for controlling how an SVG mask is interpreted."""
        self.element.classes('mask-type-' + value)
        return self

    def filter(self, value: Filter) -> Tailwind:
        """Utilities for applying filters to an element."""
        self.element.classes('filter-none-' + value if value else 'filter-none')
        return self

    def filter_blur(self, value: FilterBlur) -> Tailwind:
        """Utilities for applying blur filters to an element."""
        self.element.classes('blur-' + value)
        return self

    def filter_drop_shadow(self, value: FilterDropShadow) -> Tailwind:
        """Utilities for applying drop-shadow filters to an element."""
        self.element.classes('drop-shadow-' + value)
        return self

    def filter_grayscale(self, value: FilterGrayscale) -> Tailwind:
        """Utilities for applying grayscale filters to an element."""
        self.element.classes('grayscale-' + value if value else 'grayscale')
        return self

    def filter_invert(self, value: FilterInvert) -> Tailwind:
        """Utilities for applying invert filters to an element."""
        self.element.classes('invert-' + value if value else 'invert')
        return self

    def filter_sepia(self, value: FilterSepia) -> Tailwind:
        """Utilities for applying sepia filters to an element."""
        self.element.classes('sepia-' + value if value else 'sepia')
        return self

    def backdrop_filter(self, value: BackdropFilter) -> Tailwind:
        """Utilities for applying backdrop filters to an element."""
        self.element.classes('backdrop-filter-none-' + value if value else 'backdrop-filter-none')
        return self

    def backdrop_filter_blur(self, value: BackdropFilterBlur) -> Tailwind:
        """Utilities for applying backdrop blur filters to an element."""
        self.element.classes('backdrop-blur-' + value)
        return self

    def backdrop_filter_grayscale(self, value: BackdropFilterGrayscale) -> Tailwind:
        """Utilities for applying backdrop grayscale filters to an element."""
        self.element.classes('backdrop-grayscale-' + value if value else 'backdrop-grayscale')
        return self

    def backdrop_filter_invert(self, value: BackdropFilterInvert) -> Tailwind:
        """Utilities for applying backdrop invert filters to an element."""
        self.element.classes('backdrop-invert-' + value if value else 'backdrop-invert')
        return self

    def backdrop_filter_sepia(self, value: BackdropFilterSepia) -> Tailwind:
        """Utilities for applying backdrop sepia filters to an element."""
        self.element.classes('backdrop-sepia-' + value if value else 'backdrop-sepia')
        return self

    def border_collapse(self, value: BorderCollapse) -> Tailwind:
        """Utilities for controlling whether table borders should collapse or be separated."""
        self.element.classes('border-' + value)
        return self

    def table_layout(self, value: TableLayout) -> Tailwind:
        """Utilities for controlling the table layout algorithm."""
        self.element.classes('table-' + value)
        return self

    def caption_side(self, value: CaptionSide) -> Tailwind:
        """Utilities for controlling the alignment of a caption element inside of a table."""
        self.element.classes('caption-' + value)
        return self

    def transition_property(self, value: TransitionProperty) -> Tailwind:
        """Utilities for controlling which CSS properties transition."""
        self.element.classes('transition-' + value if value else 'transition')
        return self

    def transition_behavior(self, value: TransitionBehavior) -> Tailwind:
        """Utilities to control the behavior of CSS transitions."""
        self.element.classes('transition-' + value)
        return self

    def transition_duration(self, value: TransitionDuration) -> Tailwind:
        """Utilities for controlling the duration of CSS transitions."""
        self.element.classes('duration-initial-' + value if value else 'duration-initial')
        return self

    def transition_timing_function(self, value: TransitionTimingFunction) -> Tailwind:
        """Utilities for controlling the easing of CSS transitions."""
        self.element.classes('ease-' + value)
        return self

    def animation(self, value: Animation) -> Tailwind:
        """Utilities for animating elements with CSS animations."""
        self.element.classes('animate-' + value)
        return self

    def backface_visibility(self, value: BackfaceVisibility) -> Tailwind:
        """Utilities for controlling if an element's backface is visible."""
        self.element.classes('backface-' + value)
        return self

    def perspective(self, value: Perspective) -> Tailwind:
        """Utilities for controlling an element's perspective when placed in 3D space."""
        self.element.classes('perspective-' + value)
        return self

    def perspective_origin(self, value: PerspectiveOrigin) -> Tailwind:
        """Utilities for controlling an element's perspective origin when placed in 3D space."""
        self.element.classes('perspective-origin-' + value)
        return self

    def rotate(self, value: Rotate) -> Tailwind:
        """Utilities for rotating elements."""
        self.element.classes('rotate-none-' + value if value else 'rotate-none')
        return self

    def scale(self, value: Scale) -> Tailwind:
        """Utilities for scaling elements."""
        self.element.classes('scale-' + value)
        return self

    def transform(self, value: Transform) -> Tailwind:
        """Utilities for transforming elements."""
        self.element.classes('transform-' + value)
        return self

    def transform_origin(self, value: TransformOrigin) -> Tailwind:
        """Utilities for specifying the origin for an element's transformations."""
        self.element.classes('origin-' + value)
        return self

    def transform_style(self, value: TransformStyle) -> Tailwind:
        """Utilities for controlling if an elements children are placed in 3D space."""
        self.element.classes('transform-' + value)
        return self

    def translate(self, value: Translate) -> Tailwind:
        """Utilities for translating elements."""
        self.element.classes('' + value)
        return self

    def accent_color(self, value: AccentColor) -> Tailwind:
        """Utilities for controlling the accented color of a form control."""
        self.element.classes('accent-' + value)
        return self

    def appearance(self, value: Appearance) -> Tailwind:
        """Utilities for suppressing native form control styling."""
        self.element.classes('appearance-' + value)
        return self

    def caret_color(self, value: CaretColor) -> Tailwind:
        """Utilities for controlling the color of the text input cursor."""
        self.element.classes('caret-' + value)
        return self

    def color_scheme(self, value: ColorScheme) -> Tailwind:
        """Utilities for controlling the color scheme of an element."""
        self.element.classes('scheme-' + value)
        return self

    def cursor(self, value: Cursor) -> Tailwind:
        """Utilities for controlling the cursor style when hovering over an element."""
        self.element.classes('cursor-' + value)
        return self

    def field_sizing(self, value: FieldSizing) -> Tailwind:
        """Utilities for controlling the sizing of form controls."""
        self.element.classes('field-sizing-' + value)
        return self

    def pointer_events(self, value: PointerEvents) -> Tailwind:
        """Utilities for controlling whether an element responds to pointer events."""
        self.element.classes('pointer-events-' + value)
        return self

    def resize(self, value: Resize) -> Tailwind:
        """Utilities for controlling how an element can be resized."""
        self.element.classes('resize-' + value if value else 'resize')
        return self

    def scroll_behavior(self, value: ScrollBehavior) -> Tailwind:
        """Utilities for controlling the scroll behavior of an element."""
        self.element.classes('scroll-' + value)
        return self

    def scroll_snap_align(self, value: ScrollSnapAlign) -> Tailwind:
        """Utilities for controlling the scroll snap alignment of an element."""
        self.element.classes('snap-' + value)
        return self

    def scroll_snap_stop(self, value: ScrollSnapStop) -> Tailwind:
        """Utilities for controlling whether you can skip past possible snap positions."""
        self.element.classes('snap-' + value)
        return self

    def scroll_snap_type(self, value: ScrollSnapType) -> Tailwind:
        """Utilities for controlling how strictly snap points are enforced in a snap container."""
        self.element.classes('snap-' + value)
        return self

    def touch_action(self, value: TouchAction) -> Tailwind:
        """Utilities for controlling how an element can be scrolled and zoomed on touchscreens."""
        self.element.classes('touch-' + value)
        return self

    def user_select(self, value: UserSelect) -> Tailwind:
        """Utilities for controlling whether the user can select text in an element."""
        self.element.classes('select-' + value)
        return self

    def will_change(self, value: WillChange) -> Tailwind:
        """Utilities for optimizing upcoming animations of elements that are expected to change."""
        self.element.classes('will-change-' + value)
        return self

    def fill(self, value: Fill) -> Tailwind:
        """Utilities for styling the fill of SVG elements."""
        self.element.classes('fill-' + value)
        return self

    def stroke(self, value: Stroke) -> Tailwind:
        """Utilities for styling the stroke of SVG elements."""
        self.element.classes('stroke-' + value)
        return self

    def forced_color_adjust(self, value: ForcedColorAdjust) -> Tailwind:
        """Utilities for opting in and out of forced colors."""
        self.element.classes('forced-color-adjust-' + value)
        return self
