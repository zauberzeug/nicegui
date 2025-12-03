#!/usr/bin/env python3
from __future__ import annotations

import copy
import difflib
import re
import shutil
import subprocess
from pathlib import Path

import cssbeautifier
import rcssmin
import tinycss2
from tinycss2 import ast

ROOT = Path(__file__).parent
STATIC = ROOT / 'nicegui' / 'static'
NODE_MODULES = ROOT / 'node_modules'


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


def _extract_headwind_css(quasar_css_path: Path) -> None:
    matches = re.finditer(r'\.rotate-(\d+)\s*\{[^}]*\}', quasar_css_path.read_text())
    css = f'{", ".join(f".rotate-{m.group(1)}" for m in matches)} {{\n  rotate: 0deg;\n}}\n'
    (STATIC / 'headwind.css').write_text(css)


def _minify_js(input_path: Path, output_path: Path) -> None:
    subprocess.run(['npx', '--yes', 'terser', str(input_path), '--compress', '--mangle', '--output', str(output_path)],
                   capture_output=True, text=True, check=True)


shutil.copy2(NODE_MODULES / 'vue' / 'dist' / 'vue.esm-browser.js', STATIC / 'vue.esm-browser.js')
shutil.copy2(NODE_MODULES / 'vue' / 'dist' / 'vue.esm-browser.prod.js', STATIC / 'vue.esm-browser.prod.js')

shutil.copy2(NODE_MODULES / 'quasar' / 'dist' / 'quasar.umd.js', STATIC / 'quasar.umd.js')
shutil.copy2(NODE_MODULES / 'quasar' / 'dist' / 'quasar.umd.prod.js', STATIC / 'quasar.umd.prod.js')
for entry in (NODE_MODULES / 'quasar' / 'dist' / 'lang').glob('*.umd.prod.js'):
    shutil.copy2(entry, STATIC / 'lang' / entry.name)
_extract_quasar_css(NODE_MODULES / 'quasar' / 'dist' / 'quasar.rtl.css')
_extract_headwind_css(NODE_MODULES / 'quasar' / 'dist' / 'quasar.rtl.css')

shutil.copy2(NODE_MODULES / '@tailwindcss' / 'browser' / 'dist' / 'index.global.js', STATIC / 'tailwindcss.min.js')

shutil.copy2(NODE_MODULES / 'socket.io' / 'client-dist' / 'socket.io.min.js', STATIC / 'socket.io.min.js')
shutil.copy2(NODE_MODULES / 'socket.io' / 'client-dist' / 'socket.io.min.js.map', STATIC / 'socket.io.min.js.map')

_minify_js(NODE_MODULES / 'sass' / 'sass.default.js', STATIC / 'sass.default.js')
_minify_js(NODE_MODULES / 'sass' / 'sass.dart.js', STATIC / 'sass.dart.js')
_minify_js(NODE_MODULES / 'immutable' / 'dist' / 'immutable.es.js', STATIC / 'immutable.es.js')
