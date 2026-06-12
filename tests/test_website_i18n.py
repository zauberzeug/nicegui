import ast
import json
from pathlib import Path

from nicegui.helpers import remove_indentation

ROOT = Path(__file__).parent.parent
TRANSLATIONS_PATH = ROOT / 'website' / 'translations'


def test_translations_match_t_call_sites():
    """Every t() text has a translation and every translation has a t() call site."""
    texts = _collect_translatable_texts()
    assert texts, 'the website code should contain t() call sites'
    for path in sorted(TRANSLATIONS_PATH.glob('*.json')):
        translations: dict[str, str] = json.loads(path.read_text(encoding='utf-8'))
        missing = texts - translations.keys()
        orphaned = translations.keys() - texts
        assert not missing, f'{path.name} should contain translations for: {sorted(missing)}'
        assert not orphaned, f'{path.name} should not contain translations without a t() call site: {sorted(orphaned)}'
        language = path.stem
        prefixed = [text for text, translation in translations.items() if f'](/{language}/' in translation]
        assert not prefixed, \
            f'{path.name} should not prefix links with "/{language}" (t() adds the prefix): {prefixed}'


def _collect_translatable_texts() -> set[str]:
    """Collect the dedented string literals of all t() calls in the website code."""
    texts: set[str] = set()
    for path in [ROOT / 'main.py', *sorted((ROOT / 'website').rglob('*.py'))]:
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
            if not isinstance(node, ast.Call):
                continue
            function = node.func
            if not (
                (isinstance(function, ast.Name) and function.id == 't') or
                (isinstance(function, ast.Attribute) and function.attr == 't' and
                 isinstance(function.value, ast.Name) and function.value.id == 'i18n')
            ):
                continue
            assert len(node.args) == 1 and not node.keywords, \
                f'{path.relative_to(ROOT)}:{node.lineno}: t() should receive exactly one argument'
            argument = node.args[0]
            assert isinstance(argument, ast.Constant) and isinstance(argument.value, str), \
                f'{path.relative_to(ROOT)}:{node.lineno}: ' \
                't() should receive a string literal so translations can be validated'
            texts.add(remove_indentation(argument.value))
    return texts
