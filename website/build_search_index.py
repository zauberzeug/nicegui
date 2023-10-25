#!/usr/bin/env python3
import ast
import inspect
import json
import os
import re
from _ast import AsyncFunctionDef
from pathlib import Path
from typing import List, Optional, Union

from nicegui import app, ui

dir_path = Path(__file__).parent
os.chdir(dir_path)


def ast_string_node_to_string(node):
    if isinstance(node, ast.Str):
        return node.s
    elif isinstance(node, ast.JoinedStr):
        return ''.join(ast_string_node_to_string(part) for part in node.values)
    else:
        return str(ast.unparse(node))


def cleanup(markdown_string: str) -> str:
    # Remove link URLs but keep the description
    markdown_string = re.sub(r'\[([^\[]+)\]\([^\)]+\)', r'\1', markdown_string)
    # Remove inline code ticks
    markdown_string = re.sub(r'`([^`]+)`', r'\1', markdown_string)
    # Remove code blocks
    markdown_string = re.sub(r'```([^`]+)```', r'\1', markdown_string)
    markdown_string = re.sub(r'``([^`]+)``', r'\1', markdown_string)
    # Remove braces
    markdown_string = re.sub(r'\{([^\}]+)\}', r'\1', markdown_string)
    return markdown_string


class DocVisitor(ast.NodeVisitor):

    def __init__(self, topic: Optional[str] = None) -> None:
        super().__init__()
        self.topic = topic
        self.current_title = None
        self.current_content: List[str] = []

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            function_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            function_name = node.func.attr
        else:
            raise NotImplementedError(f'Unknown function type: {node.func}')
        if function_name in ['heading', 'subheading']:
            self._handle_new_heading()
            self.current_title = node.args[0].s
        elif function_name == 'markdown':
            if node.args:
                raw = ast_string_node_to_string(node.args[0]).splitlines()
                raw = ' '.join(l.strip() for l in raw).strip()
                self.current_content.append(cleanup(raw))
        self.generic_visit(node)

    def _handle_new_heading(self) -> None:
        if self.current_title:
            self.add_to_search_index(self.current_title, self.current_content if self.current_content else 'Overview')
            self.current_content = []

    def visit_AsyncFunctionDef(self, node: AsyncFunctionDef) -> None:
        self.visit_FunctionDef(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if node.name == 'main_demo':
            docstring = ast.get_docstring(node)
            if docstring is None:
                api = getattr(ui, self.topic) if hasattr(ui, self.topic) else getattr(app, self.topic)
                docstring = api.__doc__ or api.__init__.__doc__
                for name, method in api.__dict__.items():
                    if not name.startswith('_') and inspect.isfunction(method):
                        # add method name to docstring
                        docstring += name + ' '
                        docstring += method.__doc__ or ''
            lines = cleanup(docstring).splitlines()
            self.add_to_search_index(lines[0], lines[1:], main=True)

        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                function = decorator.func
                if isinstance(function, ast.Name) and function.id == 'text_demo':
                    title = decorator.args[0].s
                    content = cleanup(decorator.args[1].s).splitlines()
                    self.add_to_search_index(title, content)
                if isinstance(function, ast.Name) and function.id == 'element_demo':
                    attr_name = decorator.args[0].attr
                    obj_name = decorator.args[0].value.id
                    if obj_name == 'app':
                        docstring: str = getattr(app, attr_name).__doc__
                        docstring = ' '.join(l.strip() for l in docstring.splitlines()).strip()
                        self.current_content.append(cleanup(docstring))
                    else:
                        print(f'Unknown object: {obj_name} for element_demo', flush=True)
        self.generic_visit(node)

    def add_to_search_index(self, title: str, content: Union[str, list], main: bool = False) -> None:
        if isinstance(content, list):
            content_str = ' '.join(l.strip() for l in content).strip()
        else:
            content_str = content

        anchor = title.lower().replace(' ', '_')
        url = f'/documentation/{self.topic or ""}'
        if not main:
            url += f'#{anchor}'
            if self.topic:
                title = f'{self.topic.replace("_", " ").title()}: {title}'
        documents.append({
            'title': title,
            'content': content_str,
            'url': url,
        })


class MainVisitor(ast.NodeVisitor):

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            function_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            function_name = node.func.attr
        else:
            return
        if function_name == 'example_link':
            title = ast_string_node_to_string(node.args[0])
            name = name = title.lower().replace(' ', '_')
            # TODO: generalize hack to use folder if main.py is not available
            file = 'main.py' if not any(x in name for x in ['ros', 'docker']) else ''
            documents.append({
                'title': 'Example: ' + title,
                'content': ast_string_node_to_string(node.args[1]),
                'url': f'https://github.com/zauberzeug/nicegui/tree/main/examples/{name}/{file}',
            })


def generate_for(file: Path, topic: Optional[str] = None) -> None:
    tree = ast.parse(file.read_text())
    doc_visitor = DocVisitor(topic)
    doc_visitor.visit(tree)
    if doc_visitor.current_title:
        doc_visitor._handle_new_heading()  # to finalize the last heading


documents = []
tree = ast.parse(Path('../main.py').read_text())
MainVisitor().visit(tree)

generate_for(Path('./documentation.py'))
for file in Path('./more_documentation').glob('*.py'):
    generate_for(file, file.stem.removesuffix('_documentation'))

with open('static/search_index.json', 'w') as f:
    json.dump(documents, f, indent=2)
