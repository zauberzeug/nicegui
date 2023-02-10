import re
import requests
from bs4 import BeautifulSoup


class GroupItem:
    title: str
    desc: str
    members: list

    def __init__(self, title: str, desc: str, members: list):
        self.title = title
        self.desc = desc
        self.members = members


selector_item_title = "#header h1"
selector_item_desc = "#header .mt-2"
selector_item_members = ".mt-10 td[class*=text-sky-400]"


class Group:
    title: str
    itens_raw: list
    itens: list[GroupItem]
    literals: list[str]
    functions: list[str]

    def __init__(self, title: str, itens_raw: list):
        self.title = title
        self.itens_raw = itens_raw
        self.itens = []
        self.literals = []
        self.functions = []


selector_groups = 'li[class="mt-12 lg:mt-8"]'
selector_group_title = "h5"
selector_group_itens_raw = "li a"


req = requests.get("https://tailwindcss.com/docs")
html = req.text
soup = BeautifulSoup(html, "html.parser")

groups: list[Group] = []

groups_html = soup.select(selector_groups)
for g in groups_html:
    group_title = g.select_one(selector_group_title)
    group_itens_raw = g.select(selector_group_itens_raw)

    groups.append(Group(group_title.text, group_itens_raw))

# Clear unwanted groups
unwanted_groups = [
    "Getting Started",
    "Core Concepts",
    "Customization",
    "Base Styles",
    "Official Plugins",
]
groups = [g for g in groups if g.title not in unwanted_groups]

# Get groups items info
for g in groups:
    print(f"{g.title}:")
    for i in g.itens_raw:
        print(f"\t{i.text}")
        _html = requests.get(f'https://tailwindcss.com{i["href"]}')
        _soup = BeautifulSoup(_html.text, "html.parser")

        item_title = _soup.select_one(selector_item_title)
        item_desc = _soup.select_one(selector_item_desc)
        item_members = _soup.select(selector_item_members)

        g.itens.append(
            GroupItem(
                item_title.text,
                item_desc.text,
                [f'"{i.text.split(" ")[0]}"' for i in item_members],
            )
        )
    print()

# Save groups info

for g in groups:
    print(f"{g.title}:")
    for i in g.itens:
        literal_title = i.title.replace(" ", "").replace("/", "").replace("-", "")
        function_title = re.sub(
            r"_{2,}",
            "_",
            i.title.replace(" ", "_").replace("/", "").replace("-", "_").lower(),
        )
        arg = "_" + i.title.split(" ").pop().replace("-", "_").lower()

        g.literals.append(f'{literal_title} = Literal[{",".join(i.members)}]')
        g.functions.append(
            f"""
    def {function_title}(self, {arg}: {literal_title}):
        \"""
        {i.desc}
        \"""
        self.__add({arg})
        return self
        """
        )
    print()

for g in groups:
    title = g.title.replace(" ", "").replace("&", "")
    print(f"{title}:")

    with open(f"{title}.py", "w", encoding="utf-8") as f:
        f.write(
            """
from typing import Literal
from nicegui.element import Element

"""
            + "\n\n".join(g.literals)
            + f"""


class {title}:
    def __init__(self, element: Element = Element("")) -> None:
        self.element = element

    def __add(self, _class: str) -> None:
        \"""
        Internal
        \"""
        self.element.classes(add=_class)

    def apply(self, ex_element: Element) -> Element:
        \"""
        Apply the Style to an outer element

        Args:
            ex_element (Element): External Element

        Returns:
            Element: External Element
        \"""
        return ex_element.classes(add=" ".join(self.element._classes))

"""
            + "\n".join(g.functions)
        )
