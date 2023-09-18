from nicegui import ui

ui.markdown("""### Mermaid - A Nice Diagramming Tool
- [Home](https://mermaid.js.org/)
- [Docs](https://mermaid.js.org/intro/)
- [Github](https://github.com/mermaid-js/mermaid)
                        
""")

ui.markdown("""#### Basic""")
with ui.row():
    with ui.column():
        ui.label("LR: Left-to-Right")
        ui.mermaid('''
            graph LR;
                A --> B;
                A --> C;
        ''')

    with ui.column():
        ui.label("TD: Top-to-Down")
        ui.mermaid('''
            graph TD;
                女 --> 好;
                子 --> 好;
        ''')

    with ui.column():
        ui.mermaid('''
            graph TD;
                A --> B;
                A --> C;
        ''')

    with ui.column():
        ui.mermaid('''
            graph TD;
                A --> B & C --> D;
        ''')

ui.markdown("""#### Flowchart """)
ui.mermaid('''
    graph TD
        A[Enter Chart Definition] --> B(Preview)
        B --> C{decide}
        C --> D[Keep]
        C --> E[Edit Definition]
        E --> B
        D --> F[Save Image and Code]
        F --> B
''')

ui.mermaid('''
    flowchart TD
        A[Start] --> B{Is it?}
        B -->|Yes| C[OK]
        C --> D[Rethink]
        D --> B
        B ---->|No| E[End]
''')

ui.run()