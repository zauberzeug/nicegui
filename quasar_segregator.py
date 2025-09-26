#!/usr/bin/env python3
import copy
import difflib

import cssbeautifier
import rcssmin
import tinycss2
from tinycss2 import ast

from library_path_constants import STATIC

FORMAT_OPTIONS = {'indent_size': 2, 'selector_separator_newline': False}


def segregate() -> None:
    """Segregate quasar.css into important and unimportant CSS files."""
    rules = tinycss2.parse_stylesheet((STATIC / 'quasar.css').read_text(), skip_whitespace=True)
    reference_css = cssbeautifier.beautify(tinycss2.serialize(rules), FORMAT_OPTIONS)
    important_css = cssbeautifier.beautify(tinycss2.serialize(_extract_all(rules, important=True)), FORMAT_OPTIONS)
    unimportant_css = cssbeautifier.beautify(tinycss2.serialize(_extract_all(rules, important=False)), FORMAT_OPTIONS)

    important_matcher = difflib.SequenceMatcher(None, reference_css.splitlines(), important_css.splitlines())
    unimportant_matcher = difflib.SequenceMatcher(None, reference_css.splitlines(), unimportant_css.splitlines())
    assert '!important' not in unimportant_css, 'Unimportant CSS contains !important declarations.'
    assert all(tag in {'equal', 'delete'} for tag, *_ in important_matcher.get_opcodes()), \
        'Important CSS contains extra lines that are not in reference CSS.'
    assert all(tag in {'equal', 'delete'} for tag, *_ in unimportant_matcher.get_opcodes()), \
        'Unimportant CSS contains extra lines that are not in reference CSS.'
    assert reference_css.count(';') == important_css.count(';') + unimportant_css.count(';'), \
        'Reference CSS does not have the same number of declarations as the sum of important and unimportant CSS.'

    (STATIC / 'quasar.important.css').write_text(important_css)
    (STATIC / 'quasar.unimportant.css').write_text(unimportant_css)
    (STATIC / 'quasar.important.prod.css').write_text(rcssmin.cssmin(important_css))
    (STATIC / 'quasar.unimportant.prod.css').write_text(rcssmin.cssmin(unimportant_css))


def _extract_all(rules: list[ast.Node], *, important: bool) -> list[ast.QualifiedRule | ast.AtRule]:
    """Extract all qualified and at-rules with the given importance."""
    new_rules = [_extract(r, important=important) for r in rules if isinstance(r, (ast.QualifiedRule, ast.AtRule))]
    return [rule for rule in new_rules if rule.content]


def _extract(rule: ast.QualifiedRule | ast.AtRule, *, important: bool) -> ast.QualifiedRule | ast.AtRule:
    """Extract a qualified or at-rule containing only declarations with the given importance."""
    new_rule = copy.deepcopy(rule)
    nodes = tinycss2.parse_blocks_contents(rule.content, skip_whitespace=True)
    if isinstance(rule, ast.AtRule):
        new_rule.content = _extract_all(nodes, important=important)
    else:
        new_rule.content = [node for node in nodes if isinstance(node, ast.Declaration) and node.important == important]
    return new_rule


if __name__ == '__main__':
    segregate()
