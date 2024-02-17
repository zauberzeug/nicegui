from nicegui import ui

from . import doc


@doc.demo(ui.rst)
def main_demo() -> None:
    ui.rst('This is **reStructuredText**.')


@doc.demo('reStructuredText with indentation', '''
    Common indentation is automatically stripped from the beginning of each line.
    So you can indent reStructuredText elements, and they will still be rendered correctly.
''')
def rst_with_indentation():
    ui.rst('''
            This is an example of a reStructuredText paragraph with several indentation levels.

            You can use multiple levels of indentation to structure your content.
            Each level of indentation represents a different level of hierarchy.

            - Level 1
                - Level 2
                    - Level 3
                        - Level 4
                            - Level 5
    ''')


@doc.demo('reStructuredText with code blocks', '''
    You can use code blocks to show code examples.
    If you specify the language, the code will be syntax highlighted.
    See [this link](https://docs.typo3.org/m/typo3/docs-how-to-document/main/en-us/WritingReST/Reference/Code/Codeblocks.html#writing-rest-codeblocks-available-lexers) for a list of supported languages.
''')
def rst_with_code_blocks():
    ui.rst('''
        .. code-block:: python3
        
            from nicegui import ui

            ui.label('Hello World!')

            ui.run()
    ''')


@doc.demo('reStructuredText tables', '''
    reStructuredText tables.
    See the [sphinx documentation](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#tables).
''')
def rst_tables():
    ui.rst('''
    +------------------------+------------+----------+----------+
    | Header row, column 1   | Header 2   | Header 3 | Header 4 |
    | (header rows optional) |            |          |          |
    +========================+============+==========+==========+
    | body row 1, column 1   | column 2   | column 3 | column 4 |
    +------------------------+------------+----------+----------+
    | body row 2             | ...        | ...      |          |
    +------------------------+------------+----------+----------+
    ''')


doc.reference(ui.rst)
