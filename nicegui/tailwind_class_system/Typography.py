
from typing import Literal

from nicegui.element import Element

FontFamily = Literal[
    'font-sans',
    'font-serif',
    'font-mono'
]

FontSize = Literal[
    'text-xs',
    'text-sm',
    'text-base',
    'text-lg',
    'text-xl',
    'text-2xl',
    'text-3xl',
    'text-4xl',
    'text-5xl',
    'text-6xl',
    'text-7xl',
    'text-8xl',
    'text-9xl'
]

FontSmoothing = Literal[
    'antialiased',
    'subpixel-antialiased'
]

FontStyle = Literal[
    'italic',
    'not-italic'
]

FontWeight = Literal[
    'font-thin',
    'font-extralight',
    'font-light',
    'font-normal',
    'font-medium',
    'font-semibold',
    'font-bold',
    'font-extrabold',
    'font-black'
]

FontVariantNumeric = Literal[
    'normal-nums',
    'ordinal',
    'slashed-zero',
    'lining-nums',
    'oldstyle-nums',
    'proportional-nums',
    'tabular-nums',
    'diagonal-fractions',
    'stacked-fractions'
]

LetterSpacing = Literal[
    'tracking-tighter',
    'tracking-tight',
    'tracking-normal',
    'tracking-wide',
    'tracking-wider',
    'tracking-widest'
]

LineHeight = Literal[
    'leading-3',
    'leading-4',
    'leading-5',
    'leading-6',
    'leading-7',
    'leading-8',
    'leading-9',
    'leading-10',
    'leading-none',
    'leading-tight',
    'leading-snug',
    'leading-normal',
    'leading-relaxed',
    'leading-loose'
]

ListStyleType = Literal[
    'list-none',
    'list-disc',
    'list-decimal'
]

ListStylePosition = Literal[
    'list-inside',
    'list-outside'
]

TextAlign = Literal[
    'text-left',
    'text-center',
    'text-right',
    'text-justify',
    'text-start',
    'text-end'
]

TextColor = Literal[
    'text-inherit',
    'text-current',
    'text-transparent',
    'text-black',
    'text-white',
    'text-slate-50',
    'text-slate-100',
    'text-slate-200',
    'text-slate-300',
    'text-slate-400',
    'text-slate-500',
    'text-slate-600',
    'text-slate-700',
    'text-slate-800',
    'text-slate-900',
    'text-gray-50',
    'text-gray-100',
    'text-gray-200',
    'text-gray-300',
    'text-gray-400',
    'text-gray-500',
    'text-gray-600',
    'text-gray-700',
    'text-gray-800',
    'text-gray-900',
    'text-zinc-50',
    'text-zinc-100',
    'text-zinc-200',
    'text-zinc-300',
    'text-zinc-400',
    'text-zinc-500',
    'text-zinc-600',
    'text-zinc-700',
    'text-zinc-800',
    'text-zinc-900',
    'text-neutral-50',
    'text-neutral-100',
    'text-neutral-200',
    'text-neutral-300',
    'text-neutral-400',
    'text-neutral-500',
    'text-neutral-600',
    'text-neutral-700',
    'text-neutral-800',
    'text-neutral-900',
    'text-stone-50',
    'text-stone-100',
    'text-stone-200',
    'text-stone-300',
    'text-stone-400',
    'text-stone-500',
    'text-stone-600',
    'text-stone-700',
    'text-stone-800',
    'text-stone-900',
    'text-red-50',
    'text-red-100',
    'text-red-200',
    'text-red-300',
    'text-red-400',
    'text-red-500',
    'text-red-600',
    'text-red-700',
    'text-red-800',
    'text-red-900',
    'text-orange-50',
    'text-orange-100',
    'text-orange-200',
    'text-orange-300',
    'text-orange-400',
    'text-orange-500',
    'text-orange-600',
    'text-orange-700',
    'text-orange-800',
    'text-orange-900',
    'text-amber-50',
    'text-amber-100',
    'text-amber-200',
    'text-amber-300',
    'text-amber-400',
    'text-amber-500',
    'text-amber-600',
    'text-amber-700',
    'text-amber-800',
    'text-amber-900',
    'text-yellow-50',
    'text-yellow-100',
    'text-yellow-200',
    'text-yellow-300',
    'text-yellow-400',
    'text-yellow-500',
    'text-yellow-600',
    'text-yellow-700',
    'text-yellow-800',
    'text-yellow-900',
    'text-lime-50',
    'text-lime-100',
    'text-lime-200',
    'text-lime-300',
    'text-lime-400',
    'text-lime-500',
    'text-lime-600',
    'text-lime-700',
    'text-lime-800',
    'text-lime-900',
    'text-green-50',
    'text-green-100',
    'text-green-200',
    'text-green-300',
    'text-green-400',
    'text-green-500',
    'text-green-600',
    'text-green-700',
    'text-green-800',
    'text-green-900',
    'text-emerald-50',
    'text-emerald-100',
    'text-emerald-200',
    'text-emerald-300',
    'text-emerald-400',
    'text-emerald-500',
    'text-emerald-600',
    'text-emerald-700',
    'text-emerald-800',
    'text-emerald-900',
    'text-teal-50',
    'text-teal-100',
    'text-teal-200',
    'text-teal-300',
    'text-teal-400',
    'text-teal-500',
    'text-teal-600',
    'text-teal-700',
    'text-teal-800',
    'text-teal-900',
    'text-cyan-50',
    'text-cyan-100',
    'text-cyan-200',
    'text-cyan-300',
    'text-cyan-400',
    'text-cyan-500',
    'text-cyan-600',
    'text-cyan-700',
    'text-cyan-800',
    'text-cyan-900',
    'text-sky-50',
    'text-sky-100',
    'text-sky-200',
    'text-sky-300',
    'text-sky-400',
    'text-sky-500',
    'text-sky-600',
    'text-sky-700',
    'text-sky-800',
    'text-sky-900',
    'text-blue-50',
    'text-blue-100',
    'text-blue-200',
    'text-blue-300',
    'text-blue-400',
    'text-blue-500',
    'text-blue-600',
    'text-blue-700',
    'text-blue-800',
    'text-blue-900',
    'text-indigo-50',
    'text-indigo-100',
    'text-indigo-200',
    'text-indigo-300',
    'text-indigo-400',
    'text-indigo-500',
    'text-indigo-600',
    'text-indigo-700',
    'text-indigo-800',
    'text-indigo-900',
    'text-violet-50',
    'text-violet-100',
    'text-violet-200',
    'text-violet-300',
    'text-violet-400',
    'text-violet-500',
    'text-violet-600',
    'text-violet-700',
    'text-violet-800',
    'text-violet-900',
    'text-purple-50',
    'text-purple-100',
    'text-purple-200',
    'text-purple-300',
    'text-purple-400',
    'text-purple-500',
    'text-purple-600',
    'text-purple-700',
    'text-purple-800',
    'text-purple-900',
    'text-fuchsia-50',
    'text-fuchsia-100',
    'text-fuchsia-200',
    'text-fuchsia-300',
    'text-fuchsia-400',
    'text-fuchsia-500',
    'text-fuchsia-600',
    'text-fuchsia-700',
    'text-fuchsia-800',
    'text-fuchsia-900',
    'text-pink-50',
    'text-pink-100',
    'text-pink-200',
    'text-pink-300',
    'text-pink-400',
    'text-pink-500',
    'text-pink-600',
    'text-pink-700',
    'text-pink-800',
    'text-pink-900',
    'text-rose-50',
    'text-rose-100',
    'text-rose-200',
    'text-rose-300',
    'text-rose-400',
    'text-rose-500',
    'text-rose-600',
    'text-rose-700',
    'text-rose-800',
    'text-rose-900'
]

TextDecoration = Literal[
    'underline',
    'overline',
    'line-through',
    'no-underline'
]

TextDecorationColor = Literal[
    'decoration-inherit',
    'decoration-current',
    'decoration-transparent',
    'decoration-black',
    'decoration-white',
    'decoration-slate-50',
    'decoration-slate-100',
    'decoration-slate-200',
    'decoration-slate-300',
    'decoration-slate-400',
    'decoration-slate-500',
    'decoration-slate-600',
    'decoration-slate-700',
    'decoration-slate-800',
    'decoration-slate-900',
    'decoration-gray-50',
    'decoration-gray-100',
    'decoration-gray-200',
    'decoration-gray-300',
    'decoration-gray-400',
    'decoration-gray-500',
    'decoration-gray-600',
    'decoration-gray-700',
    'decoration-gray-800',
    'decoration-gray-900',
    'decoration-zinc-50',
    'decoration-zinc-100',
    'decoration-zinc-200',
    'decoration-zinc-300',
    'decoration-zinc-400',
    'decoration-zinc-500',
    'decoration-zinc-600',
    'decoration-zinc-700',
    'decoration-zinc-800',
    'decoration-zinc-900',
    'decoration-neutral-50',
    'decoration-neutral-100',
    'decoration-neutral-200',
    'decoration-neutral-300',
    'decoration-neutral-400',
    'decoration-neutral-500',
    'decoration-neutral-600',
    'decoration-neutral-700',
    'decoration-neutral-800',
    'decoration-neutral-900',
    'decoration-stone-50',
    'decoration-stone-100',
    'decoration-stone-200',
    'decoration-stone-300',
    'decoration-stone-400',
    'decoration-stone-500',
    'decoration-stone-600',
    'decoration-stone-700',
    'decoration-stone-800',
    'decoration-stone-900',
    'decoration-red-50',
    'decoration-red-100',
    'decoration-red-200',
    'decoration-red-300',
    'decoration-red-400',
    'decoration-red-500',
    'decoration-red-600',
    'decoration-red-700',
    'decoration-red-800',
    'decoration-red-900',
    'decoration-orange-50',
    'decoration-orange-100',
    'decoration-orange-200',
    'decoration-orange-300',
    'decoration-orange-400',
    'decoration-orange-500',
    'decoration-orange-600',
    'decoration-orange-700',
    'decoration-orange-800',
    'decoration-orange-900',
    'decoration-amber-50',
    'decoration-amber-100',
    'decoration-amber-200',
    'decoration-amber-300',
    'decoration-amber-400',
    'decoration-amber-500',
    'decoration-amber-600',
    'decoration-amber-700',
    'decoration-amber-800',
    'decoration-amber-900',
    'decoration-yellow-50',
    'decoration-yellow-100',
    'decoration-yellow-200',
    'decoration-yellow-300',
    'decoration-yellow-400',
    'decoration-yellow-500',
    'decoration-yellow-600',
    'decoration-yellow-700',
    'decoration-yellow-800',
    'decoration-yellow-900',
    'decoration-lime-50',
    'decoration-lime-100',
    'decoration-lime-200',
    'decoration-lime-300',
    'decoration-lime-400',
    'decoration-lime-500',
    'decoration-lime-600',
    'decoration-lime-700',
    'decoration-lime-800',
    'decoration-lime-900',
    'decoration-green-50',
    'decoration-green-100',
    'decoration-green-200',
    'decoration-green-300',
    'decoration-green-400',
    'decoration-green-500',
    'decoration-green-600',
    'decoration-green-700',
    'decoration-green-800',
    'decoration-green-900',
    'decoration-emerald-50',
    'decoration-emerald-100',
    'decoration-emerald-200',
    'decoration-emerald-300',
    'decoration-emerald-400',
    'decoration-emerald-500',
    'decoration-emerald-600',
    'decoration-emerald-700',
    'decoration-emerald-800',
    'decoration-emerald-900',
    'decoration-teal-50',
    'decoration-teal-100',
    'decoration-teal-200',
    'decoration-teal-300',
    'decoration-teal-400',
    'decoration-teal-500',
    'decoration-teal-600',
    'decoration-teal-700',
    'decoration-teal-800',
    'decoration-teal-900',
    'decoration-cyan-50',
    'decoration-cyan-100',
    'decoration-cyan-200',
    'decoration-cyan-300',
    'decoration-cyan-400',
    'decoration-cyan-500',
    'decoration-cyan-600',
    'decoration-cyan-700',
    'decoration-cyan-800',
    'decoration-cyan-900',
    'decoration-sky-50',
    'decoration-sky-100',
    'decoration-sky-200',
    'decoration-sky-300',
    'decoration-sky-400',
    'decoration-sky-500',
    'decoration-sky-600',
    'decoration-sky-700',
    'decoration-sky-800',
    'decoration-sky-900',
    'decoration-blue-50',
    'decoration-blue-100',
    'decoration-blue-200',
    'decoration-blue-300',
    'decoration-blue-400',
    'decoration-blue-500',
    'decoration-blue-600',
    'decoration-blue-700',
    'decoration-blue-800',
    'decoration-blue-900',
    'decoration-indigo-50',
    'decoration-indigo-100',
    'decoration-indigo-200',
    'decoration-indigo-300',
    'decoration-indigo-400',
    'decoration-indigo-500',
    'decoration-indigo-600',
    'decoration-indigo-700',
    'decoration-indigo-800',
    'decoration-indigo-900',
    'decoration-violet-50',
    'decoration-violet-100',
    'decoration-violet-200',
    'decoration-violet-300',
    'decoration-violet-400',
    'decoration-violet-500',
    'decoration-violet-600',
    'decoration-violet-700',
    'decoration-violet-800',
    'decoration-violet-900',
    'decoration-purple-50',
    'decoration-purple-100',
    'decoration-purple-200',
    'decoration-purple-300',
    'decoration-purple-400',
    'decoration-purple-500',
    'decoration-purple-600',
    'decoration-purple-700',
    'decoration-purple-800',
    'decoration-purple-900',
    'decoration-fuchsia-50',
    'decoration-fuchsia-100',
    'decoration-fuchsia-200',
    'decoration-fuchsia-300',
    'decoration-fuchsia-400',
    'decoration-fuchsia-500',
    'decoration-fuchsia-600',
    'decoration-fuchsia-700',
    'decoration-fuchsia-800',
    'decoration-fuchsia-900',
    'decoration-pink-50',
    'decoration-pink-100',
    'decoration-pink-200',
    'decoration-pink-300',
    'decoration-pink-400',
    'decoration-pink-500',
    'decoration-pink-600',
    'decoration-pink-700',
    'decoration-pink-800',
    'decoration-pink-900',
    'decoration-rose-50',
    'decoration-rose-100',
    'decoration-rose-200',
    'decoration-rose-300',
    'decoration-rose-400',
    'decoration-rose-500',
    'decoration-rose-600',
    'decoration-rose-700',
    'decoration-rose-800',
    'decoration-rose-900'
]

TextDecorationStyle = Literal[
    'decoration-solid',
    'decoration-double',
    'decoration-dotted',
    'decoration-dashed',
    'decoration-wavy'
]

TextDecorationThickness = Literal[
    'decoration-auto',
    'decoration-from-font',
    'decoration-0',
    'decoration-1',
    'decoration-2',
    'decoration-4',
    'decoration-8'
]

TextUnderlineOffset = Literal[
    'underline-offset-auto',
    'underline-offset-0',
    'underline-offset-1',
    'underline-offset-2',
    'underline-offset-4',
    'underline-offset-8'
]

TextTransform = Literal[
    'uppercase',
    'lowercase',
    'capitalize',
    'normal-case'
]

TextOverflow = Literal[
    'truncate',
    'text-ellipsis',
    'text-clip'
]

TextIndent = Literal[
    'indent-0',
    'indent-px',
    'indent-0.5',
    'indent-1',
    'indent-1.5',
    'indent-2',
    'indent-2.5',
    'indent-3',
    'indent-3.5',
    'indent-4',
    'indent-5',
    'indent-6',
    'indent-7',
    'indent-8',
    'indent-9',
    'indent-10',
    'indent-11',
    'indent-12',
    'indent-14',
    'indent-16',
    'indent-20',
    'indent-24',
    'indent-28',
    'indent-32',
    'indent-36',
    'indent-40',
    'indent-44',
    'indent-48',
    'indent-52',
    'indent-56',
    'indent-60',
    'indent-64',
    'indent-72',
    'indent-80',
    'indent-96'
]

VerticalAlign = Literal[
    'align-baseline',
    'align-top',
    'align-middle',
    'align-bottom',
    'align-text-top',
    'align-text-bottom',
    'align-sub',
    'align-super'
]

Whitespace = Literal[
    'whitespace-normal',
    'whitespace-nowrap',
    'whitespace-pre',
    'whitespace-pre-line',
    'whitespace-pre-wrap'
]

WordBreak = Literal[
    'break-normal',
    'break-words',
    'break-all',
    'break-keep'
]

Content = Literal[
    'content-none'
]


class Typography:

    def __init__(self, element: Element = Element('')) -> None:
        self.element = element

    def __add(self, _class: str) -> None:
        self.element.classes(add=_class)

    def apply(self, ex_element: Element) -> Element:
        """Apply the Style to an outer element.

        :param ex_element: External Element
        :return: External Element
        """
        return ex_element.classes(add=' '.join(self.element._classes))

    def font_family(self, _font_family: FontFamily):
        """Utilities for controlling the font family of an element."""
        self.__add(_font_family)
        return self

    def font_size(self, _font_size: FontSize):
        """Utilities for controlling the font size of an element."""
        self.__add(_font_size)
        return self

    def font_smoothing(self, _font_smoothing: FontSmoothing):
        """Utilities for controlling the font smoothing of an element."""
        self.__add(_font_smoothing)
        return self

    def font_style(self, _font_style: FontStyle):
        """Utilities for controlling the style of text."""
        self.__add(_font_style)
        return self

    def font_weight(self, _font_weight: FontWeight):
        """Utilities for controlling the font weight of an element."""
        self.__add(_font_weight)
        return self

    def font_variant_numeric(self, _font_variant_numeric: FontVariantNumeric):
        """Utilities for controlling the variant of numbers."""
        self.__add(_font_variant_numeric)
        return self

    def letter_spacing(self, _letter_spacing: LetterSpacing):
        """Utilities for controlling the tracking (letter spacing) of an element."""
        self.__add(_letter_spacing)
        return self

    def line_height(self, _line_height: LineHeight):
        """Utilities for controlling the leading (line height) of an element."""
        self.__add(_line_height)
        return self

    def list_style_type(self, _list_style_type: ListStyleType):
        """Utilities for controlling the bullet/number style of a list."""
        self.__add(_list_style_type)
        return self

    def list_style_position(self, _list_style_position: ListStylePosition):
        """Utilities for controlling the position of bullets/numbers in lists."""
        self.__add(_list_style_position)
        return self

    def text_align(self, _text_align: TextAlign):
        """Utilities for controlling the alignment of text."""
        self.__add(_text_align)
        return self

    def text_color(self, _text_color: TextColor):
        """Utilities for controlling the text color of an element."""
        self.__add(_text_color)
        return self

    def text_decoration(self, _text_decoration: TextDecoration):
        """Utilities for controlling the decoration of text."""
        self.__add(_text_decoration)
        return self

    def text_decoration_color(self, _text_decoration_color: TextDecorationColor):
        """Utilities for controlling the color of text decorations."""
        self.__add(_text_decoration_color)
        return self

    def text_decoration_style(self, _text_decoration_style: TextDecorationStyle):
        """Utilities for controlling the style of text decorations."""
        self.__add(_text_decoration_style)
        return self

    def text_decoration_thickness(self, _text_decoration_thickness: TextDecorationThickness):
        """Utilities for controlling the thickness of text decorations."""
        self.__add(_text_decoration_thickness)
        return self

    def text_underline_offset(self, _text_underline_offset: TextUnderlineOffset):
        """Utilities for controlling the offset of a text underline."""
        self.__add(_text_underline_offset)
        return self

    def text_transform(self, _text_transform: TextTransform):
        """Utilities for controlling the transformation of text."""
        self.__add(_text_transform)
        return self

    def text_overflow(self, _text_overflow: TextOverflow):
        """Utilities for controlling text overflow in an element."""
        self.__add(_text_overflow)
        return self

    def text_indent(self, _text_indent: TextIndent):
        """Utilities for controlling the amount of empty space shown before text in a block."""
        self.__add(_text_indent)
        return self

    def vertical_align(self, _vertical_align: VerticalAlign):
        """Utilities for controlling the vertical alignment of an inline or table-cell box."""
        self.__add(_vertical_align)
        return self

    def whitespace(self, _whitespace: Whitespace):
        """Utilities for controlling an element's white-space property."""
        self.__add(_whitespace)
        return self

    def word_break(self, _word_break: WordBreak):
        """Utilities for controlling word breaks in an element."""
        self.__add(_word_break)
        return self

    def content(self, _content: Content):
        """Utilities for controlling the content of the before and after pseudo-elements."""
        self.__add(_content)
        return self
