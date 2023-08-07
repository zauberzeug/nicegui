#!/usr/bin/env python3
from nicegui import ui

ui.chart(
    {
        'plotOptions': {
            'series': {
                'dragDrop': {'draggableX': 'true', 'draggableY': 'true', 'dragPrecisionX': 1, 'dragPrecisionY': 1},
            }
        },
        'series': [
            {'name': 'A', 'data': [{'x': 20, 'y': 10}, {'x': 30, 'y': 20}, {'x': 40, 'y': 30}]},
            {'name': 'B', 'data': [{'x': 50, 'y': 40}, {'x': 60, 'y': 50}, {'x': 70, 'y': 60}]},
        ],
    },
    extras=['draggable-points'],
    on_change=lambda e: ui.notify(f'The value changed to {e}.'),
)

ui.run()
