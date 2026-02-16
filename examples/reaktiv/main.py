#!/usr/bin/env python3
from reaktiv import Computed, Effect, Signal

from nicegui import binding, ui

with ui.row():
    with ui.card().classes('w-72 items-stretch'):
        ui.markdown('### Reaktiv signals')

        price = Signal(25.0)
        quantity = Signal(2)
        tax_rate = Signal(10.0)

        subtotal = Computed(lambda: price() * quantity())
        tax = Computed(lambda: subtotal() * tax_rate() / 100)
        total = Computed(lambda: subtotal() + tax())

        ui.number('Price ($)', value=price(), min=0, format='%.2f', on_change=lambda e: price.set(e.value))
        ui.number('Quantity', value=quantity(), min=1, step=1, on_change=lambda e: quantity.set(e.value))
        ui.number('Tax (%)', value=tax_rate(), min=0, max=100, on_change=lambda e: tax_rate.set(e.value))

        subtotal_label = ui.label()
        tax_label = ui.label()
        total_label = ui.label().classes('text-bold')

        Effect(lambda: subtotal_label.set_text(f'Subtotal: ${subtotal():.2f}'))
        Effect(lambda: tax_label.set_text(f'Tax: ${tax():.2f}'))
        Effect(lambda: total_label.set_text(f'Total: ${total():.2f}'))

    with ui.card().classes('w-72 items-stretch'):
        ui.markdown('### Bindable dataclass')

        @binding.bindable_dataclass
        class Order:
            price = 25.0
            quantity = 2
            tax_rate = 10.0
            subtotal = 0.0
            tax = 0.0
            total = 0.0

            def __init__(self):
                binding.bind_to(self, 'price', self, 'subtotal', lambda price: price * self.quantity)
                binding.bind_to(self, 'quantity', self, 'subtotal', lambda quantity: quantity * self.price)
                binding.bind_to(self, 'tax_rate', self, 'tax', lambda tax_rate: tax_rate * self.subtotal / 100)
                binding.bind_to(self, 'subtotal', self, 'total', lambda subtotal: subtotal + self.tax)

        order = Order()
        ui.number('Price ($)', value=order.price, min=0, format='%.2f').bind_value_to(order, 'price')
        ui.number('Quantity', value=order.quantity, min=1, step=1).bind_value_to(order, 'quantity')
        ui.number('Tax (%)', value=order.tax_rate, min=0, max=100).bind_value_to(order, 'tax_rate')

        ui.label().bind_text_from(order, 'subtotal', backward=lambda s: f'Subtotal: ${s:.2f}')
        ui.label().bind_text_from(order, 'tax', backward=lambda t: f'Tax: ${t:.2f}')
        ui.label().classes('text-bold').bind_text_from(order, 'total', backward=lambda t: f'Total: ${t:.2f}')


ui.run()
