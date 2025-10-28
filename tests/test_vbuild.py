from pathlib import Path

import pytest

from nicegui.vbuild import VBuild, VueParser, add_css_prefix


@pytest.mark.parametrize('css,prefix,checks', [
    ('p { color: red; } .a, .b { margin: 0; }', '.prefix', ['.prefix p', '.prefix .a', '.prefix .b']),
    ('@media (max-width:600px) {.x { display:block } }', '#root', ['@media (max-width:600px)', '#root .x']),
    ('''
    @media (max-width:600px) {
        :scope, h2 { color: blue; }
    }
    .a, :scope .b { color: green }
    ''', '.pref', ['@media (max-width:600px)', '.pref h2', '.pref .a', '.pref .b']),
])
def test_add_css_prefix_cases(css, prefix, checks):
    out = add_css_prefix(css, prefix)
    for c in checks:
        assert c in out


def test_vueparser_and_vbuild(tmp_path: Path):
    content = (
        '<template><div><h1>Hello</h1></div></template>'
        '<script>console.log("x")</script>'
        '<style>.a { color: red; }</style>'
        '<style scoped>.b { color: blue; }</style>'
    )
    p = tmp_path / 'comp.vue'
    p.write_text(content, encoding='utf-8')

    parser = VueParser(p)
    assert parser.html is not None and '<div>' in parser.html
    assert parser.script is not None and 'console.log("x")' in parser.script
    assert any('.a' in s for s in parser.styles)
    assert any('.b' in s for s in parser.scopedStyles)

    vb = VBuild(p)
    name = p.stem
    assert vb.html.startswith('<script type="text/x-template"')
    assert f'data-{name}' in vb.html
    assert 'console.log("x")' in vb.script
    assert '.a' in vb.style and '.b' in vb.style
    assert f'*[data-{name}]' in vb.style
