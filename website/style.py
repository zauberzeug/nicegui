import re
from typing import List, Optional

from nicegui import context, ui

from .examples import Example

SPECIAL_CHARACTERS = re.compile('[^(a-z)(A-Z)(0-9)-]')


def link_target(name: str, offset: str = '0') -> ui.link_target:
    """
    Create a link target that can be linked to with a hash.

    Args:
        name (str): The name of the link target.
        offset (str, optional): The offset position of the link target. Defaults to '0'.

    Returns:
        ui.link_target: The created link target.

    Raises:
        AssertionError: If the parent slot of the link target is None.

    Example:
        target = link_target('my_target', '10px')
        target.style('color: red')
        target.parent_slot.parent.classes('relative')
    """
    target = ui.link_target(name).style(f'position: absolute; top: {offset}; left: 0')
    assert target.parent_slot is not None
    target.parent_slot.parent.classes('relative')
    return target


def section_heading(subtitle_: str, title_: str) -> None:
    """Render a section heading with a subtitle.

    This function is used to render a section heading with a subtitle in a graphical user interface.
    It takes two parameters: `subtitle_` and `title_`, both of which are strings.

    Parameters:
        subtitle_ (str): The subtitle to be displayed below the section heading.
        title_ (str): The main title of the section heading.

    Returns:
        None

    Example:
        section_heading("Welcome to NiceGUI", "Getting Started")
    """
    ui.label(subtitle_).classes('md:text-lg font-bold')
    ui.markdown(title_).classes('text-3xl md:text-5xl font-medium mt-[-12px] fancy-em')


def heading(title_: str) -> ui.markdown:
    """
    Render a heading.

    Args:
        title_ (str): The title of the heading.

    Returns:
        ui.markdown: The rendered heading.

    Example:
        >>> heading("Hello, World!")
        <ui.markdown object at 0x7f9a1c8e8a90>
    """
    return ui.markdown(title_).classes('text-2xl md:text-3xl xl:text-4xl font-medium text-white')


def title(content: str) -> ui.markdown:
    """
    Render a title.

    Args:
        content (str): The content of the title.

    Returns:
        ui.markdown: A Markdown component representing the title.

    Example:
        >>> title("Hello, World!")
        <ui.markdown class="text-4xl sm:text-5xl md:text-6xl font-medium fancy-em">Hello, World!</ui.markdown>
    """
    return ui.markdown(content).classes('text-4xl sm:text-5xl md:text-6xl font-medium fancy-em')


def subtitle(content: str) -> ui.markdown:
    """
    Render a subtitle.

    This function takes a string `content` as input and returns a `ui.markdown` object
    with the specified content rendered as a subtitle. The rendered subtitle will have
    the following CSS classes applied: 'text-xl', 'sm:text-2xl', 'md:text-3xl', and 'leading-7'.

    Parameters:
        content (str): The content to be rendered as a subtitle.

    Returns:
        ui.markdown: The rendered subtitle as a `ui.markdown` object.
    """
    return ui.markdown(content).classes('text-xl sm:text-2xl md:text-3xl leading-7')


def example_link(example: Example) -> None:
    """
    Render a link to an example.

    Args:
        example (Example): The example object containing the information for the link.

    Returns:
        None

    This function renders a link to an example. It creates a link element using the `ui.link` function
    and applies various styles and classes to customize its appearance. The link is rendered with a
    background color, padding, rounded corners, and a box shadow. The link's target is set to the URL
    specified in the `example` object.

    The link is composed of two elements: a label and a description. The label is rendered using the
    `ui.label` function and the description is rendered using the `ui.markdown` function. Additional
    classes are applied to the label and description to modify their appearance.

    Example usage:
        example = Example(title='Example Title', description='Example Description', url='https://example.com')
        example_link(example)
    """
    with ui.link(target=example.url) \
            .classes('bg-[#5898d420] p-4 self-stretch rounded flex flex-col gap-2') \
            .style('box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1)'):
        ui.label(example.title).classes(replace='font-bold')
        ui.markdown(example.description).classes(replace='bold-links arrow-links')


def features(icon: str, title_: str, items: List[str]) -> None:
    """
    Render a list of features.

    Args:
        icon (str): The icon to be displayed.
        title_ (str): The title of the feature list.
        items (List[str]): The list of items to be displayed.

    Returns:
        None

    Example:
        features('fa fa-star', 'Features', ['Item 1', 'Item 2', 'Item 3'])
    """
    with ui.column().classes('gap-1'):
        ui.icon(icon).classes('max-sm:hidden text-3xl md:text-5xl mb-3 text-primary opacity-80')
        ui.label(title_).classes('font-bold mb-3')
        ui.markdown('\n'.join(f'- {item}' for item in items)).classes('bold-links arrow-links -ml-4')


def side_menu() -> ui.left_drawer:
    """
    Render the side menu.

    This function creates and returns a `ui.left_drawer` object that represents a side menu.
    The side menu is styled with a specific background color and positioned at a specific location.

    Returns:
        ui.left_drawer: The rendered side menu.

    Example:
        menu = side_menu()
        # Use the `menu` object to further customize or interact with the side menu.
    """
    return ui.left_drawer() \
        .classes('column no-wrap gap-1 bg-[#eee] dark:bg-[#1b1b1b] mt-[-20px] px-8 py-20') \
        .style('height: calc(100% + 20px) !important')


def subheading(text: str, *, link: Optional[str] = None, major: bool = False, anchor_name: Optional[str] = None) -> None:
    """
    Render a subheading with an anchor that can be linked to with a hash.

    Args:
        text (str): The text to be displayed as the subheading.
        link (Optional[str]): The URL to link the subheading to. Defaults to None.
        major (bool): Whether the subheading is a major heading. Defaults to False.
        anchor_name (Optional[str]): The name of the anchor. If not provided, a name will be generated based on the text. Defaults to None.

    Returns:
        None

    Raises:
        None

    Examples:
        # Render a subheading without a link
        subheading("Subheading")

        # Render a subheading with a link
        subheading("Subheading", link="https://example.com")

        # Render a major subheading with a link and a custom anchor name
        subheading("Subheading", link="https://example.com", major=True, anchor_name="custom-anchor")
    """
    name = anchor_name or create_anchor_name(text)
    ui.html(f'<div id="{name}"></div>').style('position: relative; top: -90px')
    with ui.row().classes('gap-2 items-center relative'):
        classes = 'text-3xl' if major else 'text-2xl'
        if link:
            ui.link(text, link).classes(classes)
        else:
            ui.label(text).classes(classes)
        with ui.link(target=f'#{name}').classes('absolute').style('transform: translateX(-150%)'):
            ui.icon('link', size='sm').classes('opacity-10 hover:opacity-80')
    drawers = [element for element in context.get_client().elements.values() if isinstance(element, ui.left_drawer)]
    if drawers:
        menu = drawers[0]
        with menu:
            async def click():
                if await ui.run_javascript('!!document.querySelector("div.q-drawer__backdrop")', timeout=5.0):
                    menu.hide()
                    ui.open(f'#{name}')
            ui.link(text, target=f'#{name}').props('data-close-overlay').on('click', click, []) \
                .classes('font-bold mt-4' if major else '')


def create_anchor_name(text: str) -> str:
    """
    Create an anchor name that can be linked to with a hash.

    This function takes a string as input and replaces any special characters
    (excluding alphanumeric characters, underscores, and hyphens) with an
    underscore. It then converts the resulting string to lowercase.

    Parameters:
        text (str): The input text for creating the anchor name.

    Returns:
        str: The anchor name that can be used for linking.

    Example:
        >>> create_anchor_name("Hello, World!")
        'hello_world'
    """
    return SPECIAL_CHARACTERS.sub('_', text).lower()
