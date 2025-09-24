import copy
from pathlib import Path

import cssbeautifier  # pip install cssbeautifier
import rcssmin  # pip install rcssmin
import tinycss2  # pip install tinycss2
from tinycss2 import ast

ROOT = Path(__file__).parent
STATIC = ROOT / 'nicegui' / 'static'

rules = tinycss2.parse_stylesheet(
    (STATIC / 'quasar.css').read_text(), skip_whitespace=True, skip_comments=True)

rules_unimportant_only = []
rules_important_only = []

for rule in rules:
    if not isinstance(rule, (ast.QualifiedRule, ast.AtRule)):
        raise TypeError(f'Unexpected {rule}. Script needs update.')
    declarations = tinycss2.parse_blocks_contents(rule.content or '')
    has_important = False
    has_unimportant = False
    for declaration in declarations:
        if isinstance(declaration, ast.Declaration) and declaration.important:
            has_important = True
        if isinstance(declaration, ast.Declaration) and not declaration.important:
            has_unimportant = True
    if has_important and has_unimportant:
        rule_copy1 = copy.deepcopy(rule)
        rule_copy2 = copy.deepcopy(rule)
        rule_copy1.content = [
            d for d in declarations
            if not isinstance(d, ast.Declaration) or d.important
        ]  # keep all non-Declaration nodes and only important Declarations
        rule_copy2.content = [
            d for d in declarations
            if not isinstance(d, ast.Declaration) or not d.important
        ]  # keep all non-Declaration nodes and only unimportant Declarations
        rules_important_only.append(rule_copy1)
        rules_unimportant_only.append(rule_copy2)
    elif has_important:
        rules_important_only.append(rule)
    else:
        rules_unimportant_only.append(rule)

print(f'Found {len(rules_unimportant_only)} unimportant-only rules, '
      f'{len(rules_important_only)} important-only rules, ')

# serialize them all
(STATIC / 'quasar_unimportant.css').write_text(
    cssbeautifier.beautify(tinycss2.serialize(rules_unimportant_only)))
(STATIC / 'quasar_important.css').write_text(
    cssbeautifier.beautify(tinycss2.serialize(rules_important_only)))

# minimize with rcssmin
(STATIC / 'quasar_unimportant.min.css').write_text(
    rcssmin.cssmin((STATIC / 'quasar_unimportant.css').read_text()))
(STATIC / 'quasar_important.min.css').write_text(
    rcssmin.cssmin((STATIC / 'quasar_important.css').read_text()))
