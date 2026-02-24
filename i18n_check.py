#!/usr/bin/env python3
"""Check website/translations/ for missing translations.

Each language is stored in a separate CSV file linked by SHA-256 hash of the English text.

Usage:
    python i18n_check.py              # report missing, exit 0
    python i18n_check.py --strict     # exit 1 if any missing
    python i18n_check.py --language ja # check only Japanese
    python i18n_check.py --fix        # auto-correct issues in-place
"""
import argparse
import csv
import hashlib
import re
import sys
from pathlib import Path

TRANSLATIONS_DIR = Path(__file__).parent / 'website' / 'translations'

# Matches exactly two backticks (RST inline literal), not three (markdown code fence)
_RST_DOUBLE_BACKTICK_RE = re.compile(r'(?<!`)``(?!`)')

# RST link: `text <URL>`_
_RST_LINK_RE = re.compile(r'`[^`]+<[^>]+>`_')
# Markdown link: [text](URL)
_MD_LINK_RE = re.compile(r'\[[^\]]+\]\([^)]+\)')

# Matches API identifiers that must NOT be translated:
_API_ID_RE = re.compile(
    r'^ui\.'
    r'(?:'
    r'\*[a-z_]+\*'
    r'|'
    r'[a-z_]+(?:\.[a-z_]+)*'
    r')'
    r'(?:\s*\(.*\))?$'
)


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def is_untranslatable(english: str) -> bool:
    """Return True if the English key is an API identifier that must not be translated."""
    return bool(_API_ID_RE.match(english))


def is_rst_text(english: str) -> bool:
    """Heuristic: English text containing RST double-backtick literals (not triple) is RST."""
    return bool(_RST_DOUBLE_BACKTICK_RE.search(english))


def check_rst_syntax(text: str) -> list[str]:
    """Parse text as RST and return any warning/error messages."""
    from io import StringIO

    from docutils.core import publish_parts

    warning_stream = StringIO()
    try:
        publish_parts(text, writer_name='html4', settings_overrides={
            'warning_stream': warning_stream,
        })
    except Exception as e:
        return [str(e)]
    output = warning_stream.getvalue().strip()
    return output.splitlines() if output else []


def _indent_set(text: str) -> set[int]:
    """Return the set of leading-whitespace widths among non-empty lines."""
    result: set[int] = set()
    for line in text.split('\n'):
        stripped = line.lstrip()
        if stripped:
            result.add(len(line) - len(stripped))
    return result


def _has_leading_newline(text: str) -> bool:
    return text.startswith('\n')


def _trailing_line(text: str) -> str | None:
    """Return the trailing whitespace-only line if present, else None."""
    lines = text.split('\n')
    if len(lines) > 1 and not lines[-1].strip():
        return lines[-1]
    return None


def check_indent(en_text: str, translation: str) -> bool:
    """Return True if the translation has inconsistent indentation vs the English text."""
    if '\n' not in en_text and '\n' not in translation:
        return False
    en_indents = _indent_set(en_text)
    tr_indents = _indent_set(translation)
    if not en_indents or not tr_indents:
        return False
    if min(en_indents) != min(tr_indents):
        return True
    if tr_indents - en_indents:
        return True
    if _has_leading_newline(en_text) != _has_leading_newline(translation):
        return True
    en_trail = _trailing_line(en_text)
    tr_trail = _trailing_line(translation)
    if (en_trail is not None) != (tr_trail is not None):
        return True
    return False


def fix_indent(en_text: str, translation: str) -> str:
    """Adjust the translation's indentation to match the English text's indent levels."""
    en_indents = _indent_set(en_text)
    tr_indents = _indent_set(translation)
    if not en_indents or not tr_indents:
        return translation

    en_base = min(en_indents)
    tr_base = min(tr_indents)
    shift = en_base - tr_base

    fixed_lines = []
    for line in translation.split('\n'):
        stripped = line.lstrip()
        if not stripped:
            fixed_lines.append(line)
            continue
        current = len(line) - len(stripped)
        shifted = max(0, current + shift)
        if shifted not in en_indents:
            shifted = min(en_indents, key=lambda x: abs(x - shifted))
        fixed_lines.append(' ' * shifted + stripped)
    result = '\n'.join(fixed_lines)

    if _has_leading_newline(en_text) and not _has_leading_newline(result):
        result = '\n' + result
    elif not _has_leading_newline(en_text) and _has_leading_newline(result):
        result = result.lstrip('\n')

    en_trail = _trailing_line(en_text)
    tr_trail = _trailing_line(result)
    if en_trail is not None and tr_trail is None:
        result = result + '\n' + en_trail
    elif en_trail is None and tr_trail is not None:
        lines = result.split('\n')
        while lines and not lines[-1].strip():
            lines.pop()
        result = '\n'.join(lines)

    return result


def read_en_csv() -> list[tuple[str, str]]:
    """Read en.csv and return [(sha256, english_text), ...]."""
    en_file = TRANSLATIONS_DIR / 'en.csv'
    if not en_file.exists():
        return []
    with en_file.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        return [(row['sha256'], row['text']) for row in reader if row.get('sha256') and row.get('text')]


def read_lang_csv(lang: str) -> dict[str, str]:
    """Read a language CSV and return {sha256: translation}."""
    lang_file = TRANSLATIONS_DIR / f'{lang}.csv'
    if not lang_file.exists():
        return {}
    with lang_file.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        return {row['sha256']: row.get('text', '') for row in reader if row.get('sha256')}


def save_lang_csv(lang: str, translations: dict[str, str], en_entries: list[tuple[str, str]]) -> None:
    """Write a language CSV sorted by sha256."""
    lang_file = TRANSLATIONS_DIR / f'{lang}.csv'
    with lang_file.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['sha256', 'text'], quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for h, _ in sorted(en_entries, key=lambda r: r[0]):
            writer.writerow({'sha256': h, 'text': translations.get(h, '')})


def main() -> None:
    parser = argparse.ArgumentParser(description='Check translation CSVs for completeness.')
    parser.add_argument('--strict', action='store_true', help='Exit with code 1 if any translations are missing')
    parser.add_argument('--language', action='append', default=[], help='Check only specific language(s)')
    parser.add_argument('--fix', action='store_true', help='Auto-correct issues in-place')
    args = parser.parse_args()

    en_entries = read_en_csv()
    if not en_entries:
        print(f'Error: {TRANSLATIONS_DIR / "en.csv"} does not exist or is empty. Run i18n_bootstrap.py first.')
        sys.exit(1)

    # Discover available languages
    all_languages: list[str] = []
    for lang_file in sorted(TRANSLATIONS_DIR.glob('*.csv')):
        lang = lang_file.stem
        if lang != 'en':
            all_languages.append(lang)

    check_languages = args.language if args.language else all_languages

    for lang in check_languages:
        lang_file = TRANSLATIONS_DIR / f'{lang}.csv'
        if not lang_file.exists():
            print(f'Error: Language "{lang}" not found. Available: {", ".join(all_languages)}')
            sys.exit(1)

    # Load all language translations
    lang_translations: dict[str, dict[str, str]] = {}
    for lang in all_languages:
        lang_translations[lang] = read_lang_csv(lang)

    needs_write: dict[str, bool] = {lang: False for lang in all_languages}

    # --- Check 1: untranslatable API identifiers ---
    api_bad: list[tuple[str, str, str]] = []
    for h, english in en_entries:
        if not is_untranslatable(english):
            continue
        for lang in all_languages:
            translation = lang_translations[lang].get(h, '').strip()
            if translation and translation != english:
                api_bad.append((english, lang, translation))
                if args.fix:
                    lang_translations[lang][h] = english
                    needs_write[lang] = True

    if api_bad:
        print(f'\nAPI identifiers that should not be translated: {len(api_bad)} violation(s)')
        for english, lang, translation in api_bad[:20]:
            print(f'  {lang}: "{english}" was translated as "{translation}"')
        if len(api_bad) > 20:
            print(f'  ... and {len(api_bad) - 20} more')

    # --- Check 2: inconsistent indentation / envelope ---
    indent_bad: list[tuple[str, str, str, str]] = []
    for h, english in en_entries:
        for lang in all_languages:
            translation = lang_translations[lang].get(h, '')
            if not translation.strip():
                continue
            if check_indent(english, translation):
                issues = []
                en_indents = sorted(_indent_set(english))
                tr_indents = sorted(_indent_set(translation))
                if en_indents != tr_indents:
                    issues.append(f'indent EN={en_indents} TR={tr_indents}')
                if _has_leading_newline(english) != _has_leading_newline(translation):
                    issues.append(f'lead \\n: EN={_has_leading_newline(english)} TR={_has_leading_newline(translation)}')
                if (_trailing_line(english) is not None) != (_trailing_line(translation) is not None):
                    issues.append(f'trail \\n: EN={_trailing_line(english) is not None} TR={_trailing_line(translation) is not None}')
                preview = english[:50].replace('\n', ' ').strip()
                indent_bad.append((h[:12], lang, preview, '; '.join(issues)))
                if args.fix:
                    lang_translations[lang][h] = fix_indent(english, translation)
                    needs_write[lang] = True

    if indent_bad:
        print(f'\nInconsistent indentation/envelope: {len(indent_bad)} violation(s)')
        for h_short, lang, preview, detail in indent_bad[:20]:
            print(f'  {h_short}... {lang}: {detail}  "{preview}..."')
        if len(indent_bad) > 20:
            print(f'  ... and {len(indent_bad) - 20} more')

    # --- Check 3: backtick count mismatch ---
    backtick_bad: list[tuple[str, str, str, int, int]] = []
    for h, english in en_entries:
        en_count = english.count('`')
        if en_count == 0:
            continue
        for lang in check_languages:
            translation = lang_translations[lang].get(h, '')
            if not translation.strip():
                continue
            tr_count = translation.count('`')
            if en_count != tr_count:
                preview = english[:50].replace('\n', ' ').strip()
                backtick_bad.append((h[:12], lang, preview, en_count, tr_count))

    if backtick_bad:
        print(f'\nBacktick count mismatch: {len(backtick_bad)} violation(s)')
        for h_short, lang, preview, en_count, tr_count in backtick_bad[:20]:
            print(f'  {h_short}... {lang}: EN has {en_count}, translation has {tr_count}  "{preview}..."')
        if len(backtick_bad) > 20:
            print(f'  ... and {len(backtick_bad) - 20} more')

    # --- Check 4: link count mismatch (RST and Markdown) ---
    link_bad: list[tuple[str, str, str, str]] = []
    for h, english in en_entries:
        en_rst = len(_RST_LINK_RE.findall(english))
        en_md = len(_MD_LINK_RE.findall(english))
        if en_rst == 0 and en_md == 0:
            continue
        for lang in check_languages:
            translation = lang_translations[lang].get(h, '')
            if not translation.strip():
                continue
            tr_rst = len(_RST_LINK_RE.findall(translation))
            tr_md = len(_MD_LINK_RE.findall(translation))
            issues = []
            if en_rst != tr_rst:
                issues.append(f'RST links EN={en_rst} TR={tr_rst}')
            if en_md != tr_md:
                issues.append(f'MD links EN={en_md} TR={tr_md}')
            if issues:
                preview = english[:50].replace('\n', ' ').strip()
                link_bad.append((h[:12], lang, preview, '; '.join(issues)))

    if link_bad:
        print(f'\nLink count mismatch: {len(link_bad)} violation(s)')
        for h_short, lang, preview, detail in link_bad[:20]:
            print(f'  {h_short}... {lang}: {detail}  "{preview}..."')
        if len(link_bad) > 20:
            print(f'  ... and {len(link_bad) - 20} more')

    # --- Check 5: RST syntax in translations ---
    rst_bad: list[tuple[str, str, str, str]] = []
    for h, english in en_entries:
        if not is_rst_text(english):
            continue
        for lang in check_languages:
            translation = lang_translations[lang].get(h, '')
            if not translation.strip():
                continue
            warnings = check_rst_syntax(translation)
            if warnings:
                preview = english[:50].replace('\n', ' ').strip()
                rst_bad.append((h[:12], lang, preview, '; '.join(warnings)))

    if rst_bad:
        print(f'\nRST syntax warnings in translations: {len(rst_bad)} issue(s)')
        for h_short, lang, preview, detail in rst_bad[:20]:
            print(f'  {h_short}... {lang}: "{preview}..."')
            for line in detail.split('; '):
                print(f'    {line}')
        if len(rst_bad) > 20:
            print(f'  ... and {len(rst_bad) - 20} more')

    # --- Write fixes ---
    if args.fix:
        for lang in all_languages:
            if needs_write[lang]:
                save_lang_csv(lang, lang_translations[lang], en_entries)
        fixed_total = len(api_bad) + len(indent_bad)
        if fixed_total:
            print(f'\nFixed {fixed_total} issue(s)')

    # --- Check 6: missing translations ---
    total = len(en_entries)
    any_missing = False

    for lang in check_languages:
        translations = lang_translations[lang]
        missing = [en for h, en in en_entries if not translations.get(h, '').strip()]
        if missing:
            any_missing = True
            print(f'\n{lang}: {len(missing)}/{total} translations missing')
            for english in missing[:10]:
                preview = english[:60].replace('\n', ' ').strip()
                print(f'  - "{preview}{"..." if len(english) > 60 else ""}"')
            if len(missing) > 10:
                print(f'  ... and {len(missing) - 10} more')
        else:
            print(f'{lang}: all {total} translations present')

    if args.strict and (any_missing or api_bad or indent_bad or backtick_bad or link_bad or rst_bad):
        sys.exit(1)


if __name__ == '__main__':
    main()
