from monaco import Monaco

from nicegui import ui

Monaco(language="python", value="print('hello')", theme="vs-dark", minimap=True).style("width: 100vw; height: 100vh;")


ui.run()