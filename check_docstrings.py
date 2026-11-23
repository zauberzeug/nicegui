#!/usr/bin/env python3
"""Run sphinx-lint's reST checks on Python docstrings, which sphinx-lint itself only applies to .rst files.

This catches e.g. single backticks (the reST default role, rendered in italics) where ``inline literals`` are meant.
"""
import ast
import sys
from pathlib import Path

from sphinxlint.checkers import all_checkers
from sphinxlint.sphinxlint import check_text

IGNORED_CHECKERS = {
    'line-too-long',  # handled by the Python linters
    'missing-final-newline',  # a docstring is not a file
    'trailing-whitespace',  # the indentation before the closing quotes is not part of the text
}
# includes checkers that sphinx-lint disables by default, most notably "default-role"
CHECKERS = {
    checker for name, checker in all_checkers.items()
    if '.rst' in checker.suffixes and name not in IGNORED_CHECKERS
}


def main() -> int:
    errors = 0
    for filename in sys.argv[1:]:
        for node in ast.walk(ast.parse(Path(filename).read_text(encoding='utf-8'))):
            if not isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            docstring = ast.get_docstring(node, clean=False)
            if docstring is None:
                continue
            for error in check_text(f'{filename}.rst', docstring, CHECKERS):
                print(f'{filename}:{node.body[0].lineno + error.line_no - 1}: {error.msg} ({error.checker_name})')
                errors += 1
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
