import os
import tempfile

import pytest

from nicegui import ui
from nicegui.element import Element
from nicegui.testing.screen import Screen

SOURCE_CODE = '''
<template>
  <div>
  <div>Template content shows up</div>
  <div>{{ js_check }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      js_check: 'JS content shows up'
    };
  },
};
</script>

<style scoped>
:scope > div {
  color: red;
}
</style>
'''


@pytest.fixture
def vue_component_file():
    tmp_file = tempfile.NamedTemporaryFile(suffix='.vue', delete=False)
    temp_file_path = tmp_file.name
    tmp_file.write(SOURCE_CODE.encode('utf-8'))
    tmp_file.close()

    print(f'Temporary Vue file created at: {temp_file_path}')

    yield temp_file_path

    os.unlink(temp_file_path)


def test_vue_element(screen: Screen, vue_component_file):
    class MyVueElement(Element, component=str(vue_component_file)):
        def __init__(self) -> None:
            super().__init__()

    @ui.page('/')
    def page():
        MyVueElement()
        ui.label('This should not be red')
    screen.open('/')
    samples = [
        ('Template content shows up', 'rgba(255, 0, 0, 1)'),
        ('JS content shows up', 'rgba(255, 0, 0, 1)'),
        ('This should not be red', 'rgba(0, 0, 0, 1)'),
    ]
    for text, color in samples:
        assert screen.find(text).value_of_css_property('color') == color
