#!/usr/bin/env python3
from __future__ import annotations

import copy
import difflib
import shutil
from pathlib import Path

import cssbeautifier
import rcssmin
import tinycss2
from tinycss2 import ast

from library_path_constants import NODE_MODULES, STATIC


def _extract_quasar_css(css_path: Path) -> None:
    def _extract_all(rules: list[ast.Node], *, important: bool) -> list[ast.QualifiedRule | ast.AtRule]:
        new_rules = [_extract(r, important=important) for r in rules if isinstance(r, (ast.QualifiedRule, ast.AtRule))]
        return [rule for rule in new_rules if rule.content]

    def _extract(rule: ast.QualifiedRule | ast.AtRule, *, important: bool) -> ast.QualifiedRule | ast.AtRule:
        new_rule = copy.deepcopy(rule)
        nodes = tinycss2.parse_blocks_contents(rule.content, skip_whitespace=True)
        new_rule.content = _extract_all(nodes, important=important) if isinstance(rule, ast.AtRule) \
            else [n for n in nodes if isinstance(n, ast.Declaration) and n.important == important]
        return new_rule

    FORMAT_OPTIONS = {'indent_size': 2, 'selector_separator_newline': False}
    rules = tinycss2.parse_stylesheet(css_path.read_text(), skip_whitespace=True)
    reference_css = cssbeautifier.beautify(tinycss2.serialize(rules), FORMAT_OPTIONS)
    important_css = cssbeautifier.beautify(tinycss2.serialize(_extract_all(rules, important=True)), FORMAT_OPTIONS)
    unimportant_css = cssbeautifier.beautify(tinycss2.serialize(_extract_all(rules, important=False)), FORMAT_OPTIONS)

    important_matcher = difflib.SequenceMatcher(None, reference_css.splitlines(), important_css.splitlines())
    unimportant_matcher = difflib.SequenceMatcher(None, reference_css.splitlines(), unimportant_css.splitlines())
    assert '!important' not in unimportant_css, 'Unimportant CSS contains !important declarations.'
    assert all(tag in {'equal', 'delete'} for tag, *_ in important_matcher.get_opcodes()), 'Extra important lines.'
    assert all(tag in {'equal', 'delete'} for tag, *_ in unimportant_matcher.get_opcodes()), 'Extra unimportant lines.'
    assert reference_css.count(';') == important_css.count(';') + unimportant_css.count(';'), 'Extra declarations.'

    (STATIC / 'quasar.important.css').write_text(important_css)
    (STATIC / 'quasar.unimportant.css').write_text(unimportant_css)
    (STATIC / 'quasar.important.prod.css').write_text(rcssmin.cssmin(important_css))
    (STATIC / 'quasar.unimportant.prod.css').write_text(rcssmin.cssmin(unimportant_css))


shutil.copy2(NODE_MODULES / 'vue' / 'dist' / 'vue.global.js', STATIC / 'vue.global.js')
shutil.copy2(NODE_MODULES / 'vue' / 'dist' / 'vue.global.prod.js', STATIC / 'vue.global.prod.js')

shutil.copy2(NODE_MODULES / 'quasar' / 'dist' / 'quasar.umd.js', STATIC / 'quasar.umd.js')
shutil.copy2(NODE_MODULES / 'quasar' / 'dist' / 'quasar.umd.prod.js', STATIC / 'quasar.umd.prod.js')
for entry in (NODE_MODULES / 'quasar' / 'dist' / 'lang').glob('*.umd.prod.js'):
    shutil.copy2(entry, STATIC / 'lang' / entry.name)
_extract_quasar_css(NODE_MODULES / 'quasar' / 'dist' / 'quasar.rtl.css')

shutil.copy2(NODE_MODULES / '@tailwindcss' / 'browser' / 'dist' / 'index.global.js', STATIC / 'tailwindcss.min.js')

shutil.copy2(NODE_MODULES / 'socket.io' / 'client-dist' / 'socket.io.min.js', STATIC / 'socket.io.min.js')
shutil.copy2(NODE_MODULES / 'socket.io' / 'client-dist' / 'socket.io.min.js.map', STATIC / 'socket.io.min.js.map')

shutil.copy2(NODE_MODULES / 'es-module-shims' / 'dist' / 'es-module-shims.js', STATIC / 'es-module-shims.js')
