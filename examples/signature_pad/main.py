#!/usr/bin/env python3
from signature_pad import SignaturePad

from nicegui import ui

pad = SignaturePad().classes('border')
ui.button('Clear', on_click=pad.clear)

ui.run()
