# Reaktiv Order Calculator

An order calculator using reactive signals from the [reaktiv](https://github.com/buiapp/reaktiv) library.

![Screenshot](screenshot.webp)

This example demonstrates two approaches to building a reactive order calculator:

1. Using `Signal` and `Computed` from the reaktiv library to create reactive values and effects.
2. Using NiceGUI's `binding.bindable_dataclass` to create a bindable dataclass
   that automatically updates the total when price, quantity, or tax rate changes.
