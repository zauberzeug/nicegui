from __future__ import annotations

import ctypes
import re
import sys
from ctypes import wintypes
from typing import ClassVar

from ..logging import log

_WINDOWS_APP_ID_PREFIX = 'nicegui.'
_WINDOWS_APP_ID_MAX_LENGTH = 128


def apply_icon(title: str, icon_path: str) -> None:
    """Find the native window by title and set its icon (title bar, Alt+Tab, taskbar)."""
    hwnd = _find_window_by_title(title)
    if not hwnd:
        log.warning('Could not find native window by title to set icon')
        return
    if not _set_window_icon_windows(hwnd, icon_path):
        log.warning('Could not set native window icon (unsupported format?)')
    app_id = _create_windows_app_id(title)
    _set_window_property_store(hwnd, app_id, icon_path)


def _create_windows_app_id(title: str) -> str:
    """Create a sanitized Windows AppUserModelID from the window title."""
    normalized_title = re.sub(r'[^0-9A-Za-z]+', '_', title).strip('_')
    suffix = normalized_title or 'app'
    max_suffix_length = _WINDOWS_APP_ID_MAX_LENGTH - len(_WINDOWS_APP_ID_PREFIX)
    return f'{_WINDOWS_APP_ID_PREFIX}{suffix[:max_suffix_length]}'


user32 = ctypes.windll.user32 if sys.platform == 'win32' else None  # type: ignore[attr-defined]
shell32 = ctypes.windll.shell32 if sys.platform == 'win32' else None  # type: ignore[attr-defined]
WM_SETICON, ICON_BIG, ICON_SMALL = 0x0080, 1, 0
IMAGE_ICON, LR_LOADFROMFILE = 1, 0x00000010


class GUID(ctypes.Structure):
    """COM GUIDs for IPropertyStore (defined unconditionally for mypy on non-Windows)"""
    _fields_: ClassVar = [
        ('Data1', ctypes.c_ulong),
        ('Data2', ctypes.c_ushort),
        ('Data3', ctypes.c_ushort),
        ('Data4', ctypes.c_ubyte * 8),
    ]


class PROPERTYKEY(ctypes.Structure):
    _fields_: ClassVar = [
        ('fmtid', GUID),
        ('pid', ctypes.c_ulong),
    ]


# PKEY_AppUserModel_ID = {9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}, 5
PKEY_AppUserModel_ID = \
    PROPERTYKEY(GUID(0x9F4C2855, 0x9F79, 0x4B39, (0xA8, 0xD0, 0xE1, 0xD4, 0x2D, 0xE1, 0xD5, 0xF3)), 5)

# PKEY_AppUserModel_RelaunchIconResource = {9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}, 2
PKEY_AppUserModel_RelaunchIconResource = \
    PROPERTYKEY(GUID(0x9F4C2855, 0x9F79, 0x4B39, (0xA8, 0xD0, 0xE1, 0xD4, 0x2D, 0xE1, 0xD5, 0xF3)), 2)


class PROPVARIANT(ctypes.Structure):
    _fields_: ClassVar = [
        ('vt', ctypes.c_ushort),
        ('wReserved1', ctypes.c_ushort),
        ('wReserved2', ctypes.c_ushort),
        ('wReserved3', ctypes.c_ushort),
        ('pwszVal', ctypes.c_wchar_p),
        ('padding', ctypes.c_ulonglong),
    ]


VT_LPWSTR = 31


def _find_window_by_title(title: str) -> int | None:
    """Find HWND by exact title. None on non-Windows or not found."""
    if user32 is None:
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


def _set_window_icon_windows(hwnd: int, icon_path: str) -> bool:
    """Set window icon via LoadImageW/WM_SETICON for title bar and Alt+Tab."""
    if user32 is None:
        return False
    hicon = user32.LoadImageW(None, icon_path, IMAGE_ICON, 0, 0, LR_LOADFROMFILE)
    if not hicon:
        return False
    old_small = user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon)
    old_big = user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon)
    # Keep the new icon handle alive while the window exists.
    # Destroying it too early can cause Alt+Tab/taskbar to fall back to defaults.
    for old_icon in (old_small, old_big):
        if old_icon and old_icon != hicon:
            user32.DestroyIcon(old_icon)
    return True


def _set_window_property_store(hwnd: int, app_id: str, icon_path: str) -> bool:
    """Set window properties via IPropertyStore for proper taskbar icon on Windows 7+."""
    if shell32 is None:
        return False

    pps = ctypes.c_void_p()
    release_fn = None

    try:
        # Get IPropertyStore interface
        IID_IPropertyStore = GUID(0x886D8EEB, 0x8CF2, 0x4446, (0x8D, 0x02, 0xCD, 0xBA, 0x1D, 0xBD, 0xCF, 0x99))

        SHGetPropertyStoreForWindow = shell32.SHGetPropertyStoreForWindow
        SHGetPropertyStoreForWindow.argtypes = [wintypes.HWND, ctypes.POINTER(GUID), ctypes.POINTER(ctypes.c_void_p)]
        SHGetPropertyStoreForWindow.restype = ctypes.HRESULT

        hr = SHGetPropertyStoreForWindow(hwnd, ctypes.byref(IID_IPropertyStore), ctypes.byref(pps))
        if hr != 0 or not pps:
            log.warning('Could not get IPropertyStore for window (HRESULT=%s)', hr)
            return False

        vtable = ctypes.cast(
            ctypes.cast(pps, ctypes.POINTER(ctypes.c_void_p))[0],
            ctypes.POINTER(ctypes.c_void_p * 10),
        )[0]
        set_value = ctypes.WINFUNCTYPE(ctypes.HRESULT, ctypes.c_void_p,
                                       ctypes.POINTER(PROPERTYKEY), ctypes.POINTER(PROPVARIANT))(vtable[6])
        commit = ctypes.WINFUNCTYPE(ctypes.HRESULT, ctypes.c_void_p)(vtable[7])
        release_fn = ctypes.WINFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p)(vtable[2])

        pv_id = PROPVARIANT(VT_LPWSTR, 0, 0, 0, app_id, 0)
        hr = set_value(pps, ctypes.byref(PKEY_AppUserModel_ID), ctypes.byref(pv_id))
        if hr != 0:
            log.warning('Could not set AppUserModelID property (HRESULT=%s)', hr)
            return False

        icon_resource = f'{icon_path},0'
        pv_icon = PROPVARIANT(VT_LPWSTR, 0, 0, 0, icon_resource, 0)
        hr = set_value(pps, ctypes.byref(PKEY_AppUserModel_RelaunchIconResource), ctypes.byref(pv_icon))
        if hr != 0:
            log.warning('Could not set RelaunchIconResource property (HRESULT=%s)', hr)
            return False

        hr = commit(pps)
        if hr != 0:
            log.warning('Could not commit property store changes (HRESULT=%s)', hr)
            return False

        return True
    except (ctypes.ArgumentError, OSError, TypeError, ValueError):
        log.exception('Error while setting native window property store values')
        return False
    finally:
        if pps and release_fn is not None:
            release_fn(pps)
