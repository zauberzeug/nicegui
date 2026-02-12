from . import _doc as doc
from ._doc import redirects, registry
from ._doc.page import DocumentationPage

__all__ = [
    'DocumentationPage',
    'doc',
    'registry',
    'redirects',
]
