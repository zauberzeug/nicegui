#!/usr/bin/env python3
import re
from dataclasses import dataclass, field
from pathlib import Path

import requests
from bs4 import BeautifulSoup, ResultSet, Tag


@dataclass
class Property:
    title: str
    description: str
    members: list


@dataclass
class Section:
    title: str
    links: ResultSet[Tag]
    properties: list[Property] = field(default_factory=list)
    literals: list[str] = field(default_factory=list)
    functions: list[str] = field(default_factory=list)


def get_soup(url: str) -> BeautifulSoup:
    path = Path('/tmp') / url.split('/')[-1]
    if path.exists():
        html = path.read_text()
    else:
        req = requests.get(url)
        html = req.text
        path.write_text(html)
    return BeautifulSoup(html, 'html.parser')


def make_pascal_case(string: str) -> str:
    return ''.join(word.capitalize() for word in re.sub(r'[-/ &]', ' ', string).split())


def make_snake_case(string: str) -> str:
    return '_'.join(word.lower() for word in re.sub(r'[-/ &]', ' ', string).split())


sections: list[Section] = []
soup = get_soup('https://tailwindcss.com/docs')
for li in soup.select('li[class="mt-12 lg:mt-8"]'):
    title = li.select_one('h5').text
    links = li.select('li a')
    if title not in {'Getting Started', 'Core Concepts', 'Customization', 'Base Styles', 'Official Plugins'}:
        sections.append(Section(title, links))

for section in sections:
    print(f'{section.title}:')
    for a in section.links:
        print(f'\t{a.text}')
        soup = get_soup(f'https://tailwindcss.com{a["href"]}')
        title = soup.select_one('#header h1').text
        description = soup.select_one('#header .mt-2').text
        properties = soup.select('.mt-10 td[class*=text-sky-400]')
        section.properties.append(Property(title, description, [p.text.split(' ')[0] for p in properties]))

for section in sections:
    for property in section.properties:
        literal_title = make_pascal_case(property.title)
        function_title = make_snake_case(property.title)
        arg = '_' + function_title
        literals = ',\n    '.join(f"'{member}'" for member in property.members)
        section.literals.append(f'{literal_title} = Literal[\n    {literals}\n]')
        section.functions.append(f'''
    def {function_title}(self, {arg}: {literal_title}):
        """{property.description}"""
        self.__add({arg})
        return self''')

    filename = make_snake_case(section.title)
    title = make_pascal_case(section.title)
    Path(f'{filename}.py').write_text('''
from typing import Literal

from nicegui.element import Element

''' + '\n\n'.join(section.literals) + f'''


class {title}:

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
''' + '\n'.join(section.functions) + '\n')
