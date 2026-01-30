# Input Chips with Blur Support

Demonstrates how `ui.input_chips` automatically adds typed values as chips when the input field loses focus (blur event), in addition to the Enter key behavior.

The example shows all three `new_value_mode` options:
- **toggle**: Adds value if absent, removes if present
- **add**: Always adds values (allows duplicates)
- **add-unique**: Only adds if not already present
