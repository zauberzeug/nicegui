#!/usr/bin/env python3
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup
from secure import SecurePath


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


properties: List[Property] = []


def get_soup(url: str) -> BeautifulSoup:
    path = Path('/tmp') / url.split('/')[-1]
    if path.exists():
        html = path.read_text()
    else:
        req = requests.get(url)
        html = req.text
        path.write_text(html)
    return BeautifulSoup(html, 'html.parser')


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

for file in (Path(__file__).parent / 'nicegui' / 'tailwind_types').glob('*.py'):
    file.unlink()
for property in properties:
    if not property.members:
        continue
    with SecurePath(open(Path(__file__).parent / 'nicegui' / 'tailwind_types' / f'{property.snake_title}.py', 'w')) as f:
        f.write('from typing_extensions import Literal\n')
        f.write('\n')
        f.write(f'{property.pascal_title} = Literal[\n')
        for short_member in property.short_members:
            f.write(f"    '{short_member}',\n")
        f.write(']\n')

with open(Path(__file__).parent / 'nicegui' / 'tailwind.py', 'w') as f:
    f.write('from __future__ import annotations\n')
    f.write('\n')
    f.write('from typing import TYPE_CHECKING, List, Optional, Union, overload\n')
    f.write('\n')
    f.write('if TYPE_CHECKING:\n')
    f.write('    from .element import Element\n')
    for property in sorted(properties, key=lambda p: p.title):
        if not property.members:
            continue
        f.write(f'    from .tailwind_types.{property.snake_title} import {property.pascal_title}\n')
    f.write('\n')
    f.write('\n')
    f.write('class PseudoElement:\n')
    f.write('\n')
    f.write('    def __init__(self) -> None:\n')
    f.write('        self._classes: List[str] = []\n')
    f.write('\n')
    f.write('    def classes(self, add: str) -> None:\n')
    f.write('        self._classes.append(add)\n')
    f.write('\n')
    f.write('\n')
    f.write('class Tailwind:\n')
    f.write('\n')
    f.write("    def __init__(self, _element: Optional['Element'] = None) -> None:\n")
    f.write('        self.element: Union[PseudoElement, Element] = PseudoElement() if _element is None else _element\n')
    f.write('\n')
    f.write('    @overload\n')
    f.write('    def __call__(self, tailwind: Tailwind) -> Tailwind:\n')
    f.write('        ...\n')
    f.write('\n')
    f.write('    @overload\n')
    f.write('    def __call__(self, *classes: str) -> Tailwind:\n')
    f.write('        ...\n')
    f.write('\n')
    f.write('    def __call__(self, *args) -> Tailwind:\n')
    f.write('        if not args:\n')
    f.write('           return self\n')
    f.write('        if isinstance(args[0], Tailwind):\n')
    f.write('            args[0].apply(self.element)\n')
    f.write('        else:\n')
    f.write("            self.element.classes(' '.join(args))\n")
    f.write('        return self\n')
    f.write('\n')
    f.write("    def apply(self, element: 'Element') -> None:\n")
    f.write('        element._classes.extend(self.element._classes)\n')
    f.write('        element.update()\n')
    for property in properties:
        f.write('\n')
        if property.members:
            f.write(f"    def {property.snake_title}(self, value: {property.pascal_title}) -> 'Tailwind':\n")
            f.write(f'        """{property.description}"""\n')
            f.write(f"        self.element.classes('{property.common_prefix}' + value)\n")
            f.write(f'        return self\n')
        else:
            f.write(f"    def {property.snake_title}(self) -> 'Tailwind':\n")
            f.write(f'        """{property.description}"""\n')
            f.write(f"        self.element.classes('{property.common_prefix}')\n")
            f.write(f'        return self\n')
