#!/usr/bin/env python3
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup


@dataclass
class Property:
    """
    Represents a CSS property with its title, description, and members.

    Attributes:
        title (str): The title of the property.
        description (str): The description of the property.
        members (List[str]): The list of members for the property.
        short_members (List[str]): The list of members with common prefix removed.
        common_prefix (str): The common prefix shared by all members.

    Methods:
        __post_init__(): Initializes the short_members and common_prefix attributes.
        pascal_title(): Returns the title in PascalCase.
        snake_title(): Returns the title in snake_case.
    """

    title: str
    description: str
    members: List[str]
    short_members: List[str] = field(init=False)
    common_prefix: str = field(init=False)

    def __post_init__(self) -> None:
        """
        Initializes the short_members and common_prefix attributes.

        This method calculates the common prefix among the members and removes it from the short_members.
        If the property has a single value, it handles specific cases for 'Container', 'List Style Image',
        'Content', and 'Appearance' properties.
        """
        words = [s.split('-') for s in self.members]
        prefix = words[0]
        for w in words:
            i = 0
            while i < len(prefix) and i < len(w) and prefix[i] == w[i]:
                i += 1
            prefix = prefix[:i]
            if not prefix:
                break
        self.short_members = ['-'.join(word[len(prefix):]) for word in words]
        self.common_prefix = '-'.join(prefix) + '-' if prefix else ''
        if len(self.short_members) == 1:
            if self.title == 'Container':
                self.members.clear()
                self.short_members.clear()
                self.common_prefix = 'container'
            elif self.title in {'List Style Image', 'Content', 'Appearance'}:
                self.short_members = ['none']
                self.common_prefix = self.members[0].removesuffix('-none')
            else:
                raise ValueError(f'Unknown single-value property "{self.title}"')

    @property
    def pascal_title(self) -> str:
        """
        Returns the title in PascalCase.

        Returns:
            str: The title in PascalCase.
        """
        return ''.join(word.capitalize() for word in re.sub(r'[-/ &]', ' ', self.title).split())

    @property
    def snake_title(self) -> str:
        """
        Returns the title in snake_case.

        Returns:
            str: The title in snake_case.
        """
        return '_'.join(word.lower() for word in re.sub(r'[-/ &]', ' ', self.title).split())


def get_soup(url: str) -> BeautifulSoup:
    """
    Get the BeautifulSoup object for the given URL.

    Parameters:
        url (str): The URL of the webpage to fetch.

    Returns:
        BeautifulSoup: The BeautifulSoup object representing the parsed HTML.

    Raises:
        requests.exceptions.RequestException: If there was an error making the request.

    Notes:
        This function fetches the HTML content from the given URL and returns a BeautifulSoup object
        that can be used to parse and navigate the HTML structure.

        If the HTML content has been previously fetched and cached locally, it will be read from the cache
        instead of making a new request to the URL.

        The cache is stored in the '/tmp/nicegui_tailwind' directory, with each file named after the last
        segment of the URL.

        Example usage:
            url = 'https://example.com'
            soup = get_soup(url)
            # Use the soup object to navigate and extract data from the HTML structure.
    """
    path = Path('/tmp/nicegui_tailwind') / url.split('/')[-1]
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        html = path.read_text()
    else:
        req = requests.get(url, timeout=5)
        req.raise_for_status()
        html = req.text
        path.write_text(html)
    return BeautifulSoup(html, 'html.parser')

def collect_properties() -> List[Property]:
    """
    Collects all Tailwind properties from the documentation.

    This function scrapes the Tailwind CSS documentation website to collect
    information about Tailwind properties. It visits each page related to a
    specific property category and extracts the title, description, and
    members of each property. The collected information is then stored in a
    list of Property objects.

    Returns:
        A list of Property objects, each representing a Tailwind property.

    Raises:
        Any exceptions that occur during the web scraping process.

    Usage:
        properties = collect_properties()
        for prop in properties:
            print(prop.title)
            print(prop.description)
            print(prop.members)
    """
    properties: List[Property] = []
    soup = get_soup('https://tailwindcss.com/docs')
    for li in soup.select('li[class="mt-12 lg:mt-8"]'):
        title = li.select_one('h5').text
        links = li.select('li a')
        if title in {'Getting Started', 'Core Concepts', 'Customization', 'Base Styles', 'Official Plugins'}:
            continue
        print(f'{title}:')
        for a in links:
            soup = get_soup(f'https://tailwindcss.com{a["href"]}')
            title = soup.select_one('#header h1').text
            description = soup.select_one('#header .mt-2').text
            members = soup.select('.mt-10 td[class*=text-sky-400]')
            properties.append(Property(title, description, [p.text.split(' ')[0] for p in members]))
            print(f'\t{title} ({len(members)})')
    return properties

def generate_type_files(properties: List[Property]) -> None:
    """
    Generate the type files for the Tailwind properties.

    This function generates type files for the Tailwind properties based on the provided list of properties.
    It creates a file for each property in the 'nicegui/tailwind_types' directory, with the file name being the snake_case version of the property title.
    Each file contains a single type definition using the Literal type hint, representing the possible values for the property.

    Parameters:
    - properties (List[Property]): A list of Property objects representing the Tailwind properties.

    Returns:
    - None

    Example usage:
    ```
    properties = [...]  # List of Property objects
    generate_type_files(properties)
    ```

    Note:
    - This function assumes that the 'nicegui/tailwind_types' directory already exists.
    - If a file with the same name already exists in the 'nicegui/tailwind_types' directory, it will be overwritten.
    """
    for file in (Path(__file__).parent / 'nicegui' / 'tailwind_types').glob('*.py'):
        file.unlink()
    (Path(__file__).parent / 'nicegui' / 'tailwind_types' / '__init__.py').touch()
    for property_ in properties:
        if not property_.members:
            continue
        with (Path(__file__).parent / 'nicegui' / 'tailwind_types' / f'{property_.snake_title}.py').open('w') as f:
            f.write('from typing import Literal\n')
            f.write('\n')
            f.write(f'{property_.pascal_title} = Literal[\n')
            for short_member in property_.short_members:
                f.write(f"    '{short_member}',\n")
            f.write(']\n')


def generate_tailwind_file(properties: List[Property]) -> None:
    """
    Generate the tailwind.py file.

    This function generates the `tailwind.py` file, which is used to define the Tailwind class and its associated methods.
    The `tailwind.py` file is responsible for applying Tailwind CSS classes to HTML elements in the NiceGUI library.

    Parameters:
        properties (List[Property]): A list of Property objects representing the different Tailwind CSS properties.

    Returns:
        None

    Example usage:
        properties = [...]  # List of Property objects
        generate_tailwind_file(properties)
    """
    with (Path(__file__).parent / 'nicegui' / 'tailwind.py').open('w') as f:
        f.write('# pylint: disable=too-many-lines\n')
        f.write('from __future__ import annotations\n')
        f.write('\n')
        f.write('from typing import TYPE_CHECKING, List, Optional, Union, overload\n')
        f.write('\n')
        f.write('if TYPE_CHECKING:\n')
        f.write('    from .element import Element\n')
        for property_ in sorted(properties, key=lambda p: p.title):
            if not property_.members:
                continue
            f.write(f'    from .tailwind_types.{property_.snake_title} import {property_.pascal_title}\n')
        f.write('\n')
        f.write('\n')
        f.write('class PseudoElement:\n')
        f.write('\n')
        f.write('    def __init__(self) -> None:\n')
        f.write('        self._classes: List[str] = []\n')
        f.write('\n')
        f.write('    def classes(self, add: str) -> None:\n')
        f.write('        """Add the given classes to the element."""\n')
        f.write('        self._classes.append(add)\n')
        f.write('\n')
        f.write('\n')
        f.write('class Tailwind:\n')
        f.write('\n')
        f.write("    def __init__(self, _element: Optional[Element] = None) -> None:\n")
        f.write(
            '        self.element: Union[PseudoElement, Element] = PseudoElement() if _element is None else _element\n')
        f.write('\n')
        f.write('    @overload\n')
        f.write('    def __call__(self, tailwind: Tailwind) -> Tailwind:\n')
        f.write('        ...\n')
        f.write('\n')
        f.write('    @overload\n')
        f.write('    def __call__(self, *classes: str) -> Tailwind:\n')
        f.write('        ...\n')
        f.write('\n')
        f.write('    def __call__(self, *args) -> Tailwind:  # type: ignore\n')
        f.write('        if not args:\n')
        f.write('            return self\n')
        f.write('        if isinstance(args[0], Tailwind):\n')
        f.write('            args[0].apply(self.element)  # type: ignore\n')
        f.write('        else:\n')
        f.write("            self.element.classes(' '.join(args))\n")
        f.write('        return self\n')
        f.write('\n')
        f.write("    def apply(self, element: Element) -> None:\n")
        f.write('        """Apply the tailwind classes to the given element."""\n')
        f.write('        element._classes.extend(self.element._classes)  # pylint: disable=protected-access\n')
        f.write('        element.update()\n')
        for property_ in properties:
            f.write('\n')
            prefix = property_.common_prefix
            if property_.members:
                f.write(f"    def {property_.snake_title}(self, value: {property_.pascal_title}) -> Tailwind:\n")
                f.write(f'        """{property_.description}"""\n')
                if '' in property_.short_members:
                    f.write(
                        f"        self.element.classes('{prefix}' + value if value else '{prefix.rstrip('''-''')}')\n")
                else:
                    f.write(f"        self.element.classes('{prefix}' + value)\n")
                f.write(f'        return self\n')  # pylint: disable=f-string-without-interpolation
            else:
                f.write(f"    def {property_.snake_title}(self) -> Tailwind:\n")
                f.write(f'        """{property_.description}"""\n')
                f.write(f"        self.element.classes('{prefix}')\n")
                f.write(f'        return self\n')  # pylint: disable=f-string-without-interpolation


def main() -> None:
    """
    Collect all Tailwind properties from the documentation and generate the Python files.

    This function collects all the Tailwind properties from the documentation and generates the Python files
    required for using Tailwind CSS in a Python project. It performs the following steps:

    1. Collects the Tailwind properties using the `collect_properties()` function.
    2. Generates the type files using the `generate_type_files()` function.
    3. Generates the Tailwind file using the `generate_tailwind_file()` function.

    This function does not take any arguments and does not return any value.

    Example usage:
    ```
    main()
    ```

    Note: Make sure to run this script in the root directory of your project.
    """
    properties = collect_properties()
    generate_type_files(properties)
    generate_tailwind_file(properties)


if __name__ == '__main__':
    main()
