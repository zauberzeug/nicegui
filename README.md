# Nice GUI

We like streamlit but find it uses to much magic when it comes to state handling. In search for a nice library to write simple graphical user interfaces we discovered justpy. It's to "low-level-html" for our daily usage but provides a great basis for "Nice GUI".

![Example GUI Elements](/sceenshots/ui-elements.png?raw=true "GUI Elements")

## Usage

Write your nice GUI in a file `main.py`:

    from nice_gui import ui

    ui.label('Hello Nice GUI!')
    ui.button('BUTTON', on_click: lambda: print('button was pressed'))

Launch it with:

    python3 main.py

Note: the script will automatically reload the gui if you modify your code.

## API

See [main.py](https://github.com/zauberzeug/nice_gui/blob/main/main.py) for an example of all API calls you can make with Nice GUI.
