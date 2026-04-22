import tempfile
from pathlib import Path

import pytest

from nicegui.elements.markdown import remove_indentation
from nicegui.vbuild import VBuild


def check(text: str, *, html: str, css: str, js: str) -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        temp_file = Path(tmp_dir) / 'TEST.vue'
        temp_file.write_text(remove_indentation(text), encoding='utf-8')
        vbuild = VBuild(temp_file)
        assert remove_indentation(vbuild.html).strip() == remove_indentation(html).strip()
        assert remove_indentation(vbuild.style).strip() == remove_indentation(css).strip()
        assert remove_indentation(vbuild.script).strip() == remove_indentation(js).strip()


def test_template_only():
    check('''
        <template>
            <h1>Hello, World!</h1>
        </template>
    ''', html='''
        <script type="text/x-template" id="tpl-TEST">
            <h1 data-TEST>Hello, World!</h1>
        </script>
    ''', css='''
    ''', js='')


def test_template_with_style():
    check('''
        <template>
            <h1>Hello, World!</h1>
        </template>
        <style>
            h1 {
                color: red;
            }
        </style>
    ''', html='''
        <script type="text/x-template" id="tpl-TEST">
            <h1 data-TEST>Hello, World!</h1>
        </script>
    ''', css='''
        h1 {color: red; }
    ''', js='')


def test_template_with_scoped_style():
    check('''
        <template>
            <h1>Hello, World!</h1>
        </template>
        <style scoped>
            h1 {
                color: red;
            }
        </style>
    ''', html='''
        <script type="text/x-template" id="tpl-TEST">
            <h1 data-TEST>Hello, World!</h1>
        </script>
    ''', css='''
        h1[data-TEST], *[data-TEST] h1 {color: red; }
    ''', js='')


def test_scoped_style_applies_to_root_element():
    check('''
        <template>
            <div class="root">
                <div class="title">Title</div>
            </div>
        </template>
        <style scoped>
            .root {
                background-color: green;
            }
            .root .title {
                color: yellow;
            }
            .title {
                font-weight: bold;
            }
            .root, .title {
                padding: 4px;
            }
        </style>
    ''', html='''
        <script type="text/x-template" id="tpl-TEST">
            <div data-TEST class="root">
                <div class="title">Title</div>
            </div>
        </script>
    ''', css='''
        .root[data-TEST], *[data-TEST] .root {background-color: green; }
        .root[data-TEST] .title, *[data-TEST] .root .title {color: yellow; }
        .title[data-TEST], *[data-TEST] .title {font-weight: bold; }
        .root[data-TEST], *[data-TEST] .root, .title[data-TEST], *[data-TEST] .title {padding: 4px; }
    ''', js='')


def test_scoped_style_with_at_rules():
    check('''
        <template>
            <h1>Hello, World!</h1>
        </template>
        <style scoped>
            h1 {
                animation: fade 1s;
                font-family: 'MyFont';
            }
            @keyframes fade {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @-webkit-keyframes slide {
                0% { transform: translateX(0); }
                100% { transform: translateX(100px); }
            }
            @font-face {
                font-family: 'MyFont';
                src: url('/fonts/my.woff2') format('woff2');
            }
            @supports (display: grid) {
                h1 { display: grid; }
            }
            @layer reset, theme;
            @layer theme {
                h1:hover { color: red; }
            }
        </style>
    ''', html='''
        <script type="text/x-template" id="tpl-TEST">
            <h1 data-TEST>Hello, World!</h1>
        </script>
    ''', css='''
        h1[data-TEST], *[data-TEST] h1 {animation: fade 1s; font-family: "MyFont"; }
        @keyframes fade { from { opacity: 0; } to { opacity: 1; } }
        @-webkit-keyframes slide { 0% { transform: translateX(0); } 100% { transform: translateX(100px); } }
        @font-face { font-family: "MyFont"; src: url("/fonts/my.woff2") format("woff2"); }
        @supports (display: grid) { h1[data-TEST], *[data-TEST] h1 {display: grid; } }
        @layer reset, theme;
        @layer theme { h1[data-TEST]:hover, *[data-TEST] h1:hover {color: red; } }
    ''', js='')


def test_template_with_script():
    check('''
        <template>
            <h1>Hello, World!</h1>
        </template>
        <script>
            export default {
                methods: {
                    hello() {
                        alert('Hello, World!');
                    }
                }
            }
        </script>
    ''', html='''
        <script type="text/x-template" id="tpl-TEST">
            <h1 data-TEST>Hello, World!</h1>
        </script>
    ''', css='''
    ''', js='''
        export default {
            methods: {
                hello() {
                    alert('Hello, World!');
                }
            }
        }
    ''')


def test_multiple_templates():
    with pytest.raises(ValueError, match='File contains more than one template'):
        check('''
            <template>
                <h1>Hello, World!</h1>
            </template>
            <template>
                <h1>Hello, NiceGUI!</h1>
            </template>
        ''', html='', css='', js='')


def test_multiple_top_level_tags():
    with pytest.raises(ValueError, match='File has more than one top level tag'):
        check('''
            <template>
                <h1>Hello, World!</h1>
                <h1>Hello, NiceGUI!</h1>
            </template>
        ''', html='', css='', js='')
