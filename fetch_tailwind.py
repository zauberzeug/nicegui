#!/usr/bin/env python3
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import httpx
from bs4 import BeautifulSoup


@dataclass
class Property:
    title: str
    description: str
    members: List[str]
    short_members: List[str] = field(init=False)
    common_prefix: str = field(init=False)

    def __post_init__(self) -> None:
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
        return ''.join(word.capitalize() for word in re.sub(r'[-/ &]', ' ', self.title).split())

    @property
    def snake_title(self) -> str:
        return '_'.join(word.lower() for word in re.sub(r'[-/ &]', ' ', self.title).split())


def get_soup(url: str) -> BeautifulSoup:
    """Get the BeautifulSoup object for the given URL."""
    path = Path('/tmp/nicegui_tailwind') / url.split('/')[-1]
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        html = path.read_text(encoding='utf-8')
    else:
        req = httpx.get(url, timeout=5)
        html = req.text
        path.write_text(html, encoding='utf-8')
    return BeautifulSoup(html, 'html.parser')


def collect_properties() -> List[Property]:
    """Collect all Tailwind properties from the documentation."""
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
    """Generate the type files for the Tailwind properties."""
    for file in (Path(__file__).parent / 'nicegui' / 'tailwind_types').glob('*.py'):
        file.unlink()
    (Path(__file__).parent / 'nicegui' / 'tailwind_types' / '__init__.py').touch()
    for property_ in properties:
        if not property_.members:
            continue
        with (Path(__file__).parent / 'nicegui' / 'tailwind_types' / f'{property_.snake_title}.py') \
                .open('w', encoding='utf-8') as f:
            f.write('from typing import Literal\n')
            f.write('\n')
            f.write(f'{property_.pascal_title} = Literal[\n')
            for short_member in property_.short_members:
                f.write(f"    '{short_member}',\n")
            f.write(']\n')


def generate_tailwind_file(properties: List[Property]) -> None:
    """Generate the tailwind.py file."""
    with (Path(__file__).parent / 'nicegui' / 'tailwind.py').open('w', encoding='utf-8') as f:
        f.write('# pylint: disable=too-many-lines\n')
        f.write('from __future__ import annotations\n')
        f.write('\n')
        f.write('import weakref\n')
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
        f.write('    def __init__(self, _element: Optional[Element] = None) -> None:\n')
        f.write(
            '        self._element: Union[PseudoElement, weakref.ref[Element]] = \\\n')
        f.write('            PseudoElement() if _element is None else weakref.ref(_element)\n')
        f.write('\n')
        f.write('    @property\n')
        f.write('    def element(self) -> Union[PseudoElement, Element]:\n')
        f.write('        """The element or pseudo element this Tailwind object belongs to."""\n')
        f.write('        element = self._element if isinstance(self._element, PseudoElement) else self._element()\n')
        f.write('        if element is None:\n')
        f.write("            raise RuntimeError('The element this Tailwind object belongs to has been deleted.')\n")
        f.write('        return element\n')
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
        f.write('    def apply(self, element: Element) -> None:\n')
        f.write('        """Apply the tailwind classes to the given element."""\n')
        f.write('        element._classes.extend(self.element._classes)  # pylint: disable=protected-access\n')
        f.write('        element.update()\n')
        for property_ in properties:
            f.write('\n')
            prefix = property_.common_prefix
            if property_.members:
                f.write(f'    def {property_.snake_title}(self, value: {property_.pascal_title}) -> Tailwind:\n')
                f.write(f'        """{property_.description}"""\n')
                if '' in property_.short_members:
                    f.write(
                        f"        self.element.classes('{prefix}' + value if value else '{prefix.rstrip('''-''')}')\n")
                else:
                    f.write(f"        self.element.classes('{prefix}' + value)\n")
                f.write('        return self\n')
            else:
                f.write(f'    def {property_.snake_title}(self) -> Tailwind:\n')
                f.write(f'        """{property_.description}"""\n')
                f.write(f"        self.element.classes('{prefix}')\n")
                f.write('        return self\n')


def main() -> None:
    """Collect all Tailwind properties from the documentation and generate the Python files."""
    properties = collect_properties()
    generate_type_files(properties)
    generate_tailwind_file(properties)


if __name__ == '__main__':
    main()
