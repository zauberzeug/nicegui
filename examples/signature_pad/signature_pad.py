from typing import Dict

from nicegui import ui


class SignaturePad(ui.element,
                   component='signature_pad.js',
                   exposed_libraries=['node_modules/signature_pad/dist/signature_pad.min.js']):

    def __init__(self, options: Dict = {}) -> None:
        """SignaturePad

        An element that integrates the `Signature Pad library <https://szimek.github.io/signature_pad/>`_.
        """
        super().__init__()
        self._props['options'] = options

    def clear(self):
        """Clear the signature."""
        self.run_method('clear')
