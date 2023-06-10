#!/usr/bin/env python3
import ast
import json
import os
from pathlib import Path

from icecream import ic

dir_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir_path)


class DemoVisitor(ast.NodeVisitor):

    def __init__(self, topic: str) -> None:
        super().__init__()
        self.topic = topic

    def visit_FunctionDef(self, node):
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                function = decorator.func
                if isinstance(function, ast.Name) and function.id == 'text_demo':
                    title = decorator.args[0].s
                    content = ' '.join([l.strip() for l in decorator.args[1].s.splitlines()]).strip()
                    anchor = title.lower().replace(' ', '_')
                    url = f'/documentation/{self.topic}#{anchor}'
                    documents.append({
                        'title': f'{self.topic.replace("_", " ").title()}: {title}',
                        'content': content,
                        'url': url
                    })
        self.generic_visit(node)


documents = []
for file in Path('./more_documentation').glob('*.py'):
    with open(file, 'r') as source:
        tree = ast.parse(source.read())
        DemoVisitor(file.stem.removesuffix('_documentation')).visit(tree)

with open('static/search_index.json', 'w') as f:
    json.dump(documents, f, indent=2)
