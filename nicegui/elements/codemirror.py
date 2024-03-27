from pathlib import Path

from nicegui.element import Element


class CodeMirror(Element, component='codemirror.js'):
    def __init__(self):
        '''CodeMirror
        
        CodeMirror is a versatile text editor implemented in JavaScript for the browser.
        '''
        super().__init__()
