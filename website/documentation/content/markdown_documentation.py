from nicegui import ui

from . import doc


@doc.demo(ui.markdown)
def main_demo() -> None:
    ui.markdown('This is **Markdown**.')


@doc.demo('Markdown with indentation', '''
    Common indentation is automatically stripped from the beginning of each line.
    So you can indent markdown elements, and they will still be rendered correctly.
''')
def markdown_with_indentation():
    ui.markdown('''
        ### Example

        This line is not indented.

            This block is indented.
            Thus it is rendered as source code.

        This is normal text again.
    ''')


@doc.demo('Markdown with code blocks', '''
    You can use code blocks to show code examples.
    If you specify the language after the opening triple backticks, the code will be syntax highlighted.
    See [the Pygments website](https://pygments.org/languages/) for a list of supported languages.
''')
def markdown_with_code_blocks():
    ui.markdown('''
        ```python
        from nicegui import ui

        ui.label('Hello World!')

        ui.run(dark=True)
        ```
    ''')


@doc.demo('Markdown tables', '''
    By activating the "tables" extra, you can use Markdown tables.
    See the [markdown2 documentation](https://github.com/trentm/python-markdown2/wiki/Extras#implemented-extras) for a list of available extras.
''')
def markdown_tables():
    ui.markdown('''
        | First name | Last name |
        | ---------- | --------- |
        | Max        | Planck    |
        | Marie      | Curie     |
    ''', extras=['tables'])


@doc.demo('Mermaid diagrams', '''
    You can use Mermaid diagrams with the "mermaid" extra.
    See the [markdown2 documentation](https://github.com/trentm/python-markdown2/wiki/Extras#implemented-extras) for a list of available extras.
''')
def mermaid():
    md = ui.markdown('''
        ```mermaid
        graph TD;
            A-->B;
            A-->C;
            B-->D;
            C-->D;
        ```
    ''', extras=['mermaid'])


@doc.demo('LaTeX formulas', '''
    By activating the "latex" extra, you can use LaTeX formulas.
    This requires markdown2 version >=2.5 as well as latex2mathml to be installed.
''')
def markdown_latex():
    ui.markdown(r'''
        Euler's identity:

        $$e^{i\pi} = -1$$
    ''', extras=['latex'])


@doc.demo('Change Markdown content', '''
    You can change the content of a Markdown element by setting its `content` property or calling `set_content`.
''')
def markdown_new_content():
    markdown = ui.markdown('Sample content')
    ui.button('Change Content', on_click=lambda: markdown.set_content('This is new content'))


@doc.demo('Styling elements inside Markdown', '''
    To style HTML elements inside a `ui.markdown` element, you can add custom CSS rules for the "nicegui-markdown" class.
''')
def markdown_styling():
    ui.add_css('''
        .nicegui-markdown a {
            color: orange;
            text-decoration: none;
        }
        .nicegui-markdown a:hover {
            color: orange;
            text-decoration: underline;
        }
    ''')
    ui.markdown('This is a [link](https://example.com).')


doc.reference(ui.markdown)
