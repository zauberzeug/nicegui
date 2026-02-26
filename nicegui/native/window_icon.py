from __future__ import annotations

import ctypes
import sys
from ctypes import wintypes
from pathlib import Path

user32 = ctypes.windll.user32 if sys.platform == 'win32' else None  # type: ignore[assignment]
WM_SETICON, ICON_BIG, ICON_SMALL = 0x0080, 1, 0
IMAGE_ICON, LR_LOADFROMFILE = 1, 0x00000010


def find_window_by_title(title: str) -> int | None:
    """Find HWND by exact title. None on non-Windows or not found."""
    if sys.platform != 'win32':
        return None
    result: list[int] = []

    def enum_cb(hwnd: int, _: int) -> bool:
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, len(buf))
            if buf.value == title:
                result.append(hwnd)
                return False
        return True

    user32.EnumWindows(ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)(enum_cb), 0)
    return result[0] if result else None


def set_window_icon_windows(hwnd: int, icon_path: str) -> bool:
    """Set window icon via LoadImageW/WM_SETICON. False on non-Windows or failure."""
    if sys.platform != 'win32' or not Path(icon_path).is_file():
        return False
    path = str(Path(icon_path).resolve())
    hicon = user32.LoadImageW(None, path, IMAGE_ICON, 0, 0, LR_LOADFROMFILE)
    if not hicon:
        return False
    user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon)
    user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon)
    return True
