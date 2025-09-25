#!/usr/bin/env python3
import copy

import cssbeautifier  # pip install cssbeautifier
import rcssmin  # pip install rcssmin
import tinycss2  # pip install tinycss2
from tinycss2 import ast

from library_path_constants import STATIC

parsed_rules = tinycss2.parse_stylesheet((STATIC / 'quasar.css').read_text(), skip_whitespace=True)

unimportant_rules = []
important_rules = []
pending_comments = []


def split_qualified_rule_by_importance(qualified_rule: ast.QualifiedRule):
    """Process a QualifiedRule and return two lists: (important_rules, unimportant_rules)."""
    parsed_declarations = tinycss2.parse_blocks_contents(qualified_rule.content or '', skip_whitespace=True)
    contains_important_declarations = False
    contains_unimportant_declarations = False
    for declaration in parsed_declarations:
        if isinstance(declaration, ast.Declaration) and declaration.important:
            contains_important_declarations = True
        if isinstance(declaration, ast.Declaration) and not declaration.important:
            contains_unimportant_declarations = True

    important_split_rules = []
    unimportant_split_rules = []

    if contains_important_declarations and contains_unimportant_declarations:
        important_rule_copy = copy.deepcopy(qualified_rule)
        unimportant_rule_copy = copy.deepcopy(qualified_rule)
        important_rule_copy.content = [
            d for d in parsed_declarations
            if not isinstance(d, ast.Declaration) or d.important
        ]  # keep all non-Declaration nodes and only important Declarations
        unimportant_rule_copy.content = [
            d for d in parsed_declarations
            if not isinstance(d, ast.Declaration) or not d.important
        ]  # keep all non-Declaration nodes and only unimportant Declarations
        important_split_rules.append(important_rule_copy)
        unimportant_split_rules.append(unimportant_rule_copy)
        important_split_rules.extend(pending_comments)
        unimportant_split_rules.extend(pending_comments)
    elif contains_important_declarations:
        important_split_rules.append(qualified_rule)
        important_split_rules.extend(pending_comments)
    else:
        unimportant_split_rules.append(qualified_rule)
        unimportant_split_rules.extend(pending_comments)

    pending_comments.clear()
    return important_split_rules, unimportant_split_rules


def process_at_rule(at_rule: ast.AtRule):
    """Process an AtRule and return two lists: (important_subrules, unimportant_subrules)."""
    important_subrules = []
    unimportant_subrules = []
    parsed_subrules = tinycss2.parse_blocks_contents(at_rule.content or '', skip_whitespace=True)
    for parsed_subrule in parsed_subrules:
        if isinstance(parsed_subrule, ast.QualifiedRule):
            imp_parts, unimp_parts = split_qualified_rule_by_importance(parsed_subrule)
            important_subrules.extend(imp_parts)
            unimportant_subrules.extend(unimp_parts)
        elif isinstance(parsed_subrule, ast.Comment):
            pending_comments.append(parsed_subrule)
        elif isinstance(parsed_subrule, ast.WhitespaceToken):
            continue  # ignore whitespace
        else:
            raise ValueError(f'Unexpected at-rule subrule: {type(parsed_subrule)}')
    return important_subrules, unimportant_subrules


for rule in parsed_rules:
    if isinstance(rule, ast.Comment):
        pending_comments.append(rule)
    elif isinstance(rule, ast.QualifiedRule):
        important_parts, unimportant_parts = split_qualified_rule_by_importance(rule)
        important_rules.extend(important_parts)
        unimportant_rules.extend(unimportant_parts)
    elif isinstance(rule, ast.AtRule):
        at_rule_important_subrules, at_rule_unimportant_subrules = process_at_rule(rule)
        if at_rule_important_subrules:
            important_at_rule_copy = copy.deepcopy(rule)
            important_at_rule_copy.content = at_rule_important_subrules
            important_rules.append(important_at_rule_copy)
        if at_rule_unimportant_subrules:
            unimportant_at_rule_copy = copy.deepcopy(rule)
            unimportant_at_rule_copy.content = at_rule_unimportant_subrules
            unimportant_rules.append(unimportant_at_rule_copy)
    else:
        raise ValueError(f'Unexpected rule type: {type(rule)}')

print(f'Found {len(unimportant_rules)} unimportant and {len(important_rules)} important rules.')

# serialize them all
options = {
    'indent_size': 2,
    'selector_separator_newline': False,
}
(STATIC / 'quasar.unimportant.css').write_text(cssbeautifier.beautify(tinycss2.serialize(unimportant_rules), options))
(STATIC / 'quasar.important.css').write_text(cssbeautifier.beautify(tinycss2.serialize(important_rules), options))

# minimize with rcssmin
(STATIC / 'quasar.unimportant.prod.css').write_text(rcssmin.cssmin((STATIC / 'quasar.unimportant.css').read_text()))
(STATIC / 'quasar.important.prod.css').write_text(rcssmin.cssmin((STATIC / 'quasar.important.css').read_text()))
