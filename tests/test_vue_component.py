from pathlib import Path

from nicegui import ui
from nicegui.testing.screen import Screen


def test_vue_element(screen: Screen, tmp_path: Path):
    vue_component_path = tmp_path / 'component.vue'
    vue_component_path.write_text('''
        <template>
            <div>
                <div>Template shows up</div>
                <div>{{ js_content }}</div>
            </div>
        </template>

        <script>
            export default {
                data() {
                    return {
                        js_content: "JavaScript runs",
                    };
                },
            };
        </script>

        <style scoped>
            :scope > div {
                color: red;
            }
        </style>
    ''')

    class MyVueElement(ui.element, component=vue_component_path):
        pass

    @ui.page('/')
    def page():
        MyVueElement()
        ui.label('This is not red')

    screen.open('/')
    assert screen.find('Template shows up').value_of_css_property('color') == 'rgba(255, 0, 0, 1)'
    assert screen.find('JavaScript runs').value_of_css_property('color') == 'rgba(255, 0, 0, 1)'
    assert screen.find('This is not red').value_of_css_property('color') == 'rgba(0, 0, 0, 1)'
