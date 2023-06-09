#!/usr/bin/env python3
import ast
import glob
import json
import os
import textwrap

dir_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir_path)


class DemoVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                function = decorator.func
                if isinstance(function, ast.Name) and function.id == 'text_demo':
                    title = decorator.args[0].s
                    content = ' '.join([l.strip() for l in decorator.args[1].s.splitlines()]).strip()
                    url = "/docs/" + node.name
                    documents.append({
                        'title': title,
                        'content': content,
                        'url': url
                    })
                elif isinstance(function, ast.Attribute) and function.attr == 'text_demo':
                    title = decorator.args[0].s
                    content = textwrap.dedent(decorator.args[1].s)
                    url = "/docs/" + node.name
                    documents.append({
                        'title': title,
                        'content': content,
                        'url': url
                    })
        self.generic_visit(node)


documents = []
for file in glob.glob("more_documentation/*.py"):
    with open(file, "r") as source:
        tree = ast.parse(source.read())
        DemoVisitor().visit(tree)

with open('static/search_data.json', 'w') as f:
    json.dump(documents, f)
