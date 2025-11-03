import tempfile
from pathlib import Path

import pytest

from nicegui.elements.markdown import remove_indentation
from nicegui.vbuild import VBuild


def check(text: str, html: str, style: str, script: str) -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        temp_file = Path(tmp_dir) / 'TEST.vue'
        temp_file.write_text(remove_indentation(text), encoding='utf-8')
        vbuild = VBuild(temp_file)
        assert remove_indentation(vbuild.html).strip() == remove_indentation(html).strip()
        assert remove_indentation(vbuild.style).strip() == remove_indentation(style).strip()
        assert remove_indentation(vbuild.script).strip() == remove_indentation(script).strip()


def test_template_only():
    check('''
        <template>
            <h1>Hello, World!</h1>
        </template>
    ''', '''
        <script type="text/x-template" id="tpl-TEST">
            <h1 data-"TEST">Hello, World!</h1>
        </script>
    ''', '''
    ''', '''
        var TEST = Vue.component(\'TEST\', {template:"#tpl-TEST",});
    ''')


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
    ''', '''
        <script type="text/x-template" id="tpl-TEST">
            <h1 data-"TEST">Hello, World!</h1>
        </script>
    ''', '''
        h1 {color: red; }
    ''', '''
        var TEST = Vue.component(\'TEST\', {template:"#tpl-TEST",});
    ''')


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
    ''', '''
        <script type="text/x-template" id="tpl-TEST">
            <h1 data-"TEST">Hello, World!</h1>
        </script>
    ''', '''
        *[data-TEST] h1 {color: red; }
    ''', '''
        var TEST = Vue.component(\'TEST\', {template:"#tpl-TEST",});
    ''')


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
    ''', '''
        <script type="text/x-template" id="tpl-TEST">
            <h1 data-"TEST">Hello, World!</h1>
        </script>
    ''', '''
    ''', '''
        var TEST = Vue.component(\'TEST\', {template:"#tpl-TEST",
                methods: {
                    hello() {
                        alert('Hello, World!');
                    }
                }
            });
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
        ''', '', '', '')


def test_multiple_top_level_tags():
    with pytest.raises(ValueError, match='File has more than one top level tag'):
        check('''
            <template>
                <h1>Hello, World!</h1>
                <h1>Hello, NiceGUI!</h1>
            </template>
        ''', '', '', '')
