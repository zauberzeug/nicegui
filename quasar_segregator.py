import copy
from pathlib import Path

import cssbeautifier  # pip install cssbeautifier
import rcssmin  # pip install rcssmin
import tinycss2  # pip install tinycss2
from tinycss2 import ast

ROOT = Path(__file__).parent
STATIC = ROOT / 'nicegui' / 'static'

rules = tinycss2.parse_stylesheet(
    (STATIC / 'quasar.css').read_text(), skip_whitespace=True)

rules_unimportant_only = []
rules_important_only = []
comments_stash = []


def process_qualified_rule(qualified_rule: ast.QualifiedRule):
    """Process a QualifiedRule and return two lists: (important_rules, unimportant_rules)."""
    declarations = tinycss2.parse_blocks_contents(qualified_rule.content or '')
    has_important = False
    has_unimportant = False
    for declaration in declarations:
        if isinstance(declaration, ast.Declaration) and declaration.important:
            has_important = True
        if isinstance(declaration, ast.Declaration) and not declaration.important:
            has_unimportant = True

    important_rules = []
    unimportant_rules = []

    if has_important and has_unimportant:
        rule_copy1_inner = copy.deepcopy(qualified_rule)
        rule_copy2_inner = copy.deepcopy(qualified_rule)
        rule_copy1_inner.content = [
            d for d in declarations
            if not isinstance(d, ast.Declaration) or d.important
        ]  # keep all non-Declaration nodes and only important Declarations
        rule_copy2_inner.content = [
            d for d in declarations
            if not isinstance(d, ast.Declaration) or not d.important
        ]  # keep all non-Declaration nodes and only unimportant Declarations
        important_rules.append(rule_copy1_inner)
        unimportant_rules.append(rule_copy2_inner)
        important_rules.extend(comments_stash)
        unimportant_rules.extend(comments_stash)
    elif has_important:
        important_rules.append(qualified_rule)
        important_rules.extend(comments_stash)
    else:
        unimportant_rules.append(qualified_rule)
        unimportant_rules.extend(comments_stash)

    comments_stash.clear()
    return important_rules, unimportant_rules


for rule in rules:
    if isinstance(rule, ast.Comment):
        comments_stash.append(rule)
    elif isinstance(rule, ast.QualifiedRule):
        i, u = process_qualified_rule(rule)
        rules_important_only.extend(i)
        rules_unimportant_only.extend(u)
    elif isinstance(rule, ast.AtRule):
        atrule_important_subrules = []
        atrule_unimportant_subrules = []
        subrules = tinycss2.parse_blocks_contents(rule.content or '')
        for subrule in subrules:
            if isinstance(subrule, ast.QualifiedRule):
                i, u = process_qualified_rule(subrule)
                atrule_important_subrules.extend(i)
                atrule_unimportant_subrules.extend(u)
            elif isinstance(subrule, ast.Comment):
                comments_stash.append(subrule)
            elif isinstance(subrule, ast.WhitespaceToken):
                continue  # ignore whitespace
            else:
                raise ValueError(f'Unexpected at-rule subrule: {type(subrule)}')
        if atrule_important_subrules:
            rule_copy1 = copy.deepcopy(rule)
            rule_copy1.content = atrule_important_subrules
            rules_important_only.append(rule_copy1)
        if atrule_unimportant_subrules:
            rule_copy2 = copy.deepcopy(rule)
            rule_copy2.content = atrule_unimportant_subrules
            rules_unimportant_only.append(rule_copy2)
    else:
        raise ValueError(f'Unexpected rule type: {type(rule)}')

print(f'Found {len(rules_unimportant_only)} unimportant-only rules, '
      f'{len(rules_important_only)} important-only rules, ')

# serialize them all
(STATIC / 'quasar_unimportant.css').write_text(
    cssbeautifier.beautify(tinycss2.serialize(rules_unimportant_only)) + '\n')
(STATIC / 'quasar_important.css').write_text(
    cssbeautifier.beautify(tinycss2.serialize(rules_important_only)) + '\n')

# minimize with rcssmin
(STATIC / 'quasar_unimportant.min.css').write_text(
    rcssmin.cssmin((STATIC / 'quasar_unimportant.css').read_text()) + '\n')
(STATIC / 'quasar_important.min.css').write_text(
    rcssmin.cssmin((STATIC / 'quasar_important.css').read_text()) + '\n')
