from nicegui import ui

from .screen import Screen


def test_markdown(screen: Screen):
    m = ui.markdown('This is **Markdown**')

    screen.open('/')
    element = screen.find('This is')
    assert element.text == 'This is Markdown'
    assert element.get_attribute('innerHTML') == 'This is <strong>Markdown</strong>'

    m.set_content('New **content**')
    element = screen.find('New')
    assert element.text == 'New content'
    assert element.get_attribute('innerHTML') == 'New <strong>content</strong>'


def test_markdown_with_mermaid(screen: Screen):
    m = ui.markdown('''
Mermaid:

```mermaid
graph TD;
    Node_A --> Node_B;
```
''', extras=['mermaid', 'fenced-code-blocks'])

    screen.open('/')
    screen.should_contain('Mermaid')
    assert screen.find_by_tag('svg').get_attribute('id') == f'mermaid_{m.id}_0'
    assert screen.find('Node_A').get_attribute('class') == 'nodeLabel'

    m.set_content('''
New:
    
```mermaid
graph TD;
    Node_C --> Node_D;
```
''')
    screen.should_contain('New')
    assert screen.find('Node_C').get_attribute('class') == 'nodeLabel'
    screen.should_not_contain('Node_A')


def test_strip_indentation(screen: Screen):
    ui.markdown('''
        **This is Markdown.**
    ''')

    screen.open('/')
    screen.should_contain('This is Markdown.')
    screen.should_not_contain('**This is Markdown.**')  # NOTE: '**' are translated to formatting and not visible
