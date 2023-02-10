"""
Define types used throughout to assist with auto-complete.
"""
from typing import List, Dict, Any, Union

from typing_extensions import TypedDict, Literal

# note: This format of typed dict is necessary due to the use of the "class" keyword.
# note: Ideally the dict types get better refined moving forward to give more clarity to the caller.
ElementAsDict = TypedDict(
    "ElementAsDict",
    {
        "id": int,
        "tag": str,
        "class": List[str],
        "style": Dict[str, str],
        "props": Dict[str, Any],
        "events": Dict[str, Dict],
        "text": str,
        "slots": Dict,
    },
)

WindowsEvents = Literal[
    "afterprint",
    "beforeprint",
    "beforeunload",
    "error",
    "hashchange",
    "load",
    "message",
    "offline",
    "online",
    "pagehide",
    "pageshow",
    "popstate",
    "resize",
    "storage",
    "unload",
]
FormEvents = Literal[
    "blur",
    "change",
    "contextmenu",
    "focus",
    "input",
    "invalid",
    "reset",
    "search",
    "select",
    "submit",
]
KeyboardEvents = Literal["keydown", "keypress", "keyup"]
MouseEvents = Literal[
    "click",
    "dblclick",
    "mousedown",
    "mousemove",
    "mouseout",
    "mouseover",
    "mouseup",
    "mousewheel",
    "wheel",
]
DragEvents = Literal[
    "drag",
    "dragend",
    "dragenter",
    "dragleave",
    "dragover",
    "dragstart",
    "drop",
    "scroll",
]
ClipboardEvents = Literal["copy", "cut", "paste"]
MediaEvents = Literal[
    "abort",
    "canplay",
    "canplaythrough",
    "cuechange",
    "durationchange",
    "emptied",
    "ended",
    "error",
    "loadeddata",
    "loadedmetadata",
    "loadstart",
    "pause",
    "play",
    "playing",
    "progress",
    "ratechange",
    "seeked",
    "seeking",
    "stalled",
    "suspend",
    "timeupdate",
    "volumechange",
    "waiting",
]
MiscEvents = Literal["toggle"]

AnyHTMLEvent = Union[
    WindowsEvents,
    FormEvents,
    KeyboardEvents,
    MouseEvents,
    DragEvents,
    ClipboardEvents,
    MediaEvents,
    MiscEvents,
]
