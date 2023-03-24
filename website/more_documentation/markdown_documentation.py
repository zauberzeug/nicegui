from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    ui.markdown('''This is **Markdown**.''')


def more() -> None:
    @text_demo('Markdown with indentation', '''
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

    @text_demo('Markdown with code blocks', '''
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
