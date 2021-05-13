# Nice GUI

# Usage

Write your nice GUI in a file `main.py`:

    import nice_gui

    ui = nice_gui.Ui()
    ui.label('Hello Nice GUI!')
    ui.Button('BUTTON', on_click: lambda: print('button was pressed'))

Launch it with

    python3 main.py

Or use with autoreloading by calling

    nicegui main.py

# Full Example

See [main.py](https://github.com/zauberzeug/nice_gui/blob/main/main.py)
