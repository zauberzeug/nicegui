# Screenshots

This folder contains NiceGUI examples.

## Screenshots

Instruction how to take screenshots of all _(or rather most)_ examples.
Beware that each example will open a new browser tab.

<!--
As an improvement all examples could be updated to read an environment variable that could
possibly tell them call: `ui.run(show=False)`
-->

```shell
# Make sure dependencies are installed
poetry install

# Take screenshots of _most_ examples
poetry run python screenshot.py

# Example output
Processing: signature_pad
Screenshot saved to signature_pad/screenshot.png
Finished processing: signature_pad

Processing: custom_vue_component
Screenshot saved to custom_vue_component/screenshot.png
Finished processing: custom_vue_component
...
```
