#!/usr/bin/env python3
from reaktiv import Computed, Effect, Signal

from nicegui import ui


def root() -> None:
    price = Signal(25.0)
    quantity = Signal(2)
    tax_rate = Signal(10.0)

    subtotal = Computed(lambda: price() * quantity())
    tax = Computed(lambda: subtotal() * tax_rate() / 100)
    total = Computed(lambda: subtotal() + tax())

    ui.markdown('### Order Calculator')
    ui.number('Price ($)', value=price(), min=0, format='%.2f',
              on_change=lambda e: price.set(e.value))
    ui.number('Quantity', value=quantity(), min=1, step=1,
              on_change=lambda e: quantity.set(e.value))
    ui.number('Tax (%)', value=tax_rate(), min=0, max=100,
              on_change=lambda e: tax_rate.set(e.value))

    ui.separator()

    subtotal_label = ui.label()
    tax_label = ui.label()
    total_label = ui.label().classes('text-bold')

    Effect(lambda: subtotal_label.set_text(f'Subtotal: ${subtotal():.2f}'))
    Effect(lambda: tax_label.set_text(f'Tax: ${tax():.2f}'))
    Effect(lambda: total_label.set_text(f'Total: ${total():.2f}'))


ui.run(root)
