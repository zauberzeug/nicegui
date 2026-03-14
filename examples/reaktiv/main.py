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

        # NOTE: Effects must be assigned to variables to prevent garbage collection
        subtotal_effect = Effect(lambda: subtotal_label.set_text(f'Subtotal: ${subtotal():.2f}'))
        tax_effect = Effect(lambda: tax_label.set_text(f'Tax: ${tax():.2f}'))
        total_effect = Effect(lambda: total_label.set_text(f'Total: ${total():.2f}'))

    with ui.card().classes('w-72 items-stretch'):
        ui.markdown('### Bindable dataclass')

        @binding.bindable_dataclass
        class Order:
            price: float = 25.0
            quantity: int = 2
            tax_rate: float = 10.0
            subtotal: float = 0.0
            tax: float = 0.0
            total: float = 0.0

            def __post_init__(self) -> None:
                # multi-input binding for subtotal = price * quantity
                binding.bind_to(self, 'price', self, 'subtotal', lambda price: price * self.quantity)
                binding.bind_to(self, 'quantity', self, 'subtotal', lambda quantity: self.price * quantity)

                # multi-input binding for tax = tax_rate * subtotal / 100
                binding.bind_to(self, 'tax_rate', self, 'tax', lambda tax_rate: tax_rate * self.subtotal / 100)
                binding.bind_to(self, 'subtotal', self, 'tax', lambda subtotal: self.tax_rate * subtotal / 100)

                # multi-input binding for total = subtotal + tax
                binding.bind_to(self, 'tax', self, 'total', lambda tax: self.subtotal + tax)
                binding.bind_to(self, 'subtotal', self, 'total', lambda subtotal: self.tax + subtotal)

        order = Order()
        ui.number('Price ($)', value=order.price, min=0, format='%.2f').bind_value_to(order, 'price')
        ui.number('Quantity', value=order.quantity, min=1, step=1).bind_value_to(order, 'quantity')
        ui.number('Tax (%)', value=order.tax_rate, min=0, max=100).bind_value_to(order, 'tax_rate')

        ui.label().bind_text_from(order, 'subtotal', backward=lambda s: f'Subtotal: ${s:.2f}')
        ui.label().bind_text_from(order, 'tax', backward=lambda t: f'Tax: ${t:.2f}')
        ui.label().classes('text-bold').bind_text_from(order, 'total', backward=lambda t: f'Total: ${t:.2f}')


ui.run()
