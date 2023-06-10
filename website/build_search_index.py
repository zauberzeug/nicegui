#!/usr/bin/env python3
import ast
import json
import os
from pathlib import Path
from typing import Union

from icecream import ic

from nicegui import app, ui

dir_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir_path)


class DemoVisitor(ast.NodeVisitor):

    def __init__(self, topic: str) -> None:
        super().__init__()
        self.topic = topic

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if node.name == 'main_demo':
            docstring = ast.get_docstring(node)
            if docstring is None:
                api = getattr(ui, self.topic) if hasattr(ui, self.topic) else getattr(app, self.topic)
                docstring = api.__doc__ or api.__init__.__doc__
            lines = docstring.splitlines()
            self.add_to_search_index(lines[0], lines[1:], main=True)

        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                function = decorator.func
                if isinstance(function, ast.Name) and function.id == 'text_demo':
                    title = decorator.args[0].s
                    content = decorator.args[1].s.splitlines()
                    self.add_to_search_index(title, content)
        self.generic_visit(node)

    def add_to_search_index(self, title: str, content: Union[str, list], main: bool = False) -> None:
        if isinstance(content, list):
            content_str = ' '.join([l.strip() for l in content]).strip()
        else:
            content_str = content

        anchor = title.lower().replace(' ', '_')
        url = f'/documentation/{self.topic}'
        if not main:
            url += f'#{anchor}'
            title = f'{self.topic.replace("_", " ").title()}: {title}'
        documents.append({
            'title': title,
            'content': content_str,
            'url': url
        })


documents = []
for file in Path('./more_documentation').glob('*.py'):
    with open(file, 'r') as source:
        tree = ast.parse(source.read())
        DemoVisitor(file.stem.removesuffix('_documentation')).visit(tree)

with open('static/search_index.json', 'w') as f:
    json.dump(documents, f, indent=2)
