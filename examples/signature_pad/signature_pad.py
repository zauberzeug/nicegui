from typing import Dict, Optional

from nicegui import ui


class SignaturePad(ui.element,
                   component='signature_pad.js',
                   dependencies=['node_modules/signature_pad/dist/signature_pad.min.js']):

    def __init__(self, options: Optional[Dict] = None) -> None:
        """SignaturePad

        An element that integrates the `Signature Pad library <https://szimek.github.io/signature_pad/>`_.
        """
        super().__init__()
        self._props['options'] = options or {}

    def clear(self):
        """Clear the signature."""
        self.run_method('clear')
