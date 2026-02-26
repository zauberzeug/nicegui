from __future__ import annotations

import ctypes
import sys
from ctypes import wintypes
from pathlib import Path

user32 = ctypes.windll.user32 if sys.platform == 'win32' else None  # type: ignore[assignment]
shell32 = ctypes.windll.shell32 if sys.platform == 'win32' else None  # type: ignore[assignment]
WM_SETICON, ICON_BIG, ICON_SMALL = 0x0080, 1, 0
IMAGE_ICON, LR_LOADFROMFILE = 1, 0x00000010

# COM GUIDs for IPropertyStore
if sys.platform == 'win32':
    class GUID(ctypes.Structure):
        _fields_ = [('Data1', ctypes.c_ulong), ('Data2', ctypes.c_ushort),  # noqa: RUF012
                    ('Data3', ctypes.c_ushort), ('Data4', ctypes.c_ubyte * 8)]

    class PROPERTYKEY(ctypes.Structure):
        _fields_ = [('fmtid', GUID), ('pid', ctypes.c_ulong)]  # noqa: RUF012

    # PKEY_AppUserModel_ID = {9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}, 5
    PKEY_AppUserModel_ID = PROPERTYKEY(
        GUID(0x9F4C2855, 0x9F79, 0x4B39, (0xA8, 0xD0, 0xE1, 0xD4, 0x2D, 0xE1, 0xD5, 0xF3)), 5)

    # PKEY_AppUserModel_RelaunchIconResource = {9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}, 2
    PKEY_AppUserModel_RelaunchIconResource = PROPERTYKEY(
        GUID(0x9F4C2855, 0x9F79, 0x4B39, (0xA8, 0xD0, 0xE1, 0xD4, 0x2D, 0xE1, 0xD5, 0xF3)), 2)


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
    """Set window icon via LoadImageW/WM_SETICON for title bar and Alt+Tab."""
    if sys.platform != 'win32' or not Path(icon_path).is_file():
        return False
    path = str(Path(icon_path).resolve())
    hicon = user32.LoadImageW(None, path, IMAGE_ICON, 0, 0, LR_LOADFROMFILE)
    if not hicon:
        return False
    user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon)
    user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon)
    return True


def set_window_property_store(hwnd: int, app_id: str, icon_path: str) -> bool:
    """Set window properties via IPropertyStore for proper taskbar icon on Windows 7+."""
    if sys.platform != 'win32':
        return False

    try:
        # Define PROPVARIANT structure
        class PROPVARIANT(ctypes.Structure):
            _fields_ = [  # noqa: RUF012
                ('vt', ctypes.c_ushort),
                ('wReserved1', ctypes.c_ushort),
                ('wReserved2', ctypes.c_ushort),
                ('wReserved3', ctypes.c_ushort),
                ('pwszVal', ctypes.c_wchar_p),
                ('padding', ctypes.c_ulonglong),
            ]

        VT_LPWSTR = 31

        # Get IPropertyStore interface
        IID_IPropertyStore = GUID(0x886D8EEB, 0x8CF2, 0x4446,
                                  (0x8D, 0x02, 0xCD, 0xBA, 0x1D, 0xBD, 0xCF, 0x99))

        # SHGetPropertyStoreForWindow
        SHGetPropertyStoreForWindow = shell32.SHGetPropertyStoreForWindow
        SHGetPropertyStoreForWindow.argtypes = [wintypes.HWND, ctypes.POINTER(GUID), ctypes.POINTER(ctypes.c_void_p)]
        SHGetPropertyStoreForWindow.restype = ctypes.HRESULT

        pps = ctypes.c_void_p()
        hr = SHGetPropertyStoreForWindow(hwnd, ctypes.byref(IID_IPropertyStore), ctypes.byref(pps))
        if hr != 0 or not pps:
            return False

        # Get vtable
        vtable = ctypes.cast(ctypes.cast(pps, ctypes.POINTER(ctypes.c_void_p))[0],
                             ctypes.POINTER(ctypes.c_void_p * 10))[0]

        # SetValue is at index 6 in IPropertyStore vtable
        SetValue = ctypes.WINFUNCTYPE(ctypes.HRESULT, ctypes.c_void_p,
                                      ctypes.POINTER(PROPERTYKEY), ctypes.POINTER(PROPVARIANT))(vtable[6])

        # Commit is at index 7
        Commit = ctypes.WINFUNCTYPE(ctypes.HRESULT, ctypes.c_void_p)(vtable[7])

        # Release is at index 2
        Release = ctypes.WINFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p)(vtable[2])

        # Set AppUserModelID
        pv_id = PROPVARIANT()
        pv_id.vt = VT_LPWSTR
        pv_id.pwszVal = app_id
        SetValue(pps, ctypes.byref(PKEY_AppUserModel_ID), ctypes.byref(pv_id))

        # Set RelaunchIconResource (format: "path,index")
        icon_resource = f'{icon_path},0'
        pv_icon = PROPVARIANT()
        pv_icon.vt = VT_LPWSTR
        pv_icon.pwszVal = icon_resource
        SetValue(pps, ctypes.byref(PKEY_AppUserModel_RelaunchIconResource), ctypes.byref(pv_icon))

        # Commit changes
        Commit(pps)

        # Release
        Release(pps)

        return True
    except Exception:
        return False
