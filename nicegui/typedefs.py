"""
Define types used throughout to assist with auto-complete.
"""
from typing import List, Dict, Any

from typing_extensions import TypedDict

# note: This element of typed dict is necessary due to the use of the "class" keyword.
# note: Ideally the dict types get better refined moving forward to give more clarity to the caller.
ElementAsDict = TypedDict('ElementAsDict', {
    'id': int,
    'tag': str,
    'class': List[str],
    'style': Dict[str, str],
    'props': Dict[str, Any],
    'events': Dict[str, Dict],
    'text': str,
    'slots': Dict
})

