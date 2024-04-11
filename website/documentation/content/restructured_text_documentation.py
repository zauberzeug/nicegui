from nicegui import ui

from . import doc


@doc.demo(ui.restructured_text)
def main_demo() -> None:
    ui.restructured_text('This is **reStructuredText**.')


@doc.demo('reStructuredText with indentation', '''
    You can indent reStructuredText elements to create a hierarchy.
    Common indentation is automatically stripped from the beginning of each line to preserve the relative indentation,
    so you can indent multiline strings.
''')
def rst_with_indentation():
    ui.restructured_text('''
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
    If you specify the language, the code will be syntax-highlighted.
    See [this link](https://docs.typo3.org/m/typo3/docs-how-to-document/main/en-us/WritingReST/Reference/Code/Codeblocks.html#writing-rest-codeblocks-available-lexers) for a list of supported languages.
''')
def rst_with_code_blocks():
    ui.restructured_text('''
        .. code-block:: python3
        
            from nicegui import ui

            ui.label('Hello World!')

            ui.run()
    ''')


@doc.demo('reStructuredText with tables', '''
    See the [sphinx documentation](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#tables)
    for more information about reStructuredText tables.
''')
def rst_tables():
    ui.restructured_text('''
        +-------+-------+---------+--------+
        | A     | B     | A and B | A or B |
        +=======+=======+=========+========+
        | False | False | False   | False  |
        +-------+-------+---------+--------+
        | True  | False | False   | True   |
        +-------+-------+---------+--------+
        | False | True  | False   | True   |
        +-------+-------+---------+--------+
        | True  | True  | True    | True   |
        +-------+-------+---------+--------+
    ''')


doc.reference(ui.restructured_text)
