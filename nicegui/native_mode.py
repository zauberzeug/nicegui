import _thread
import multiprocessing
import socket
import tempfile
import time
import warnings
from threading import Thread
import sys

if sys.platform.startswith('win'):
    from ctypes import cdll, windll, CFUNCTYPE, byref, POINTER, c_int, c_ulong, c_bool
    import os

from . import globals

with warnings.catch_warnings():
    # webview depends on bottle which uses the deprecated CGI function (https://github.com/bottlepy/bottle/issues/1403)
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    import webview

def on_shown(icon_dir):
    if icon_dir is None:
        return
    # Set the window icon file dir
    icon = icon_dir
    # set up ctypes needed variables
    EnumWindows = cdll.user32.EnumWindows
    EnumWindowsProc = CFUNCTYPE(c_bool, POINTER(c_int), POINTER(c_int))
    IsWindowVisible = cdll.user32.IsWindowVisible
    IsWindowEnabled = cdll.user32.IsWindowEnabled
    GetWindowThreadProcessId = cdll.user32.GetWindowThreadProcessId
    # List of matching window handles
    hwnds = []
    # Get current process id / commented out within native_mode integration, get it from activate func
    pid = os.getpid()
    # Callback function that EnumWindows will be called while enumerating all windows, passing the hwnd and an empty arg
    def callback(hwnd, lParam_arg):
        if IsWindowVisible(hwnd) and IsWindowEnabled(hwnd):
            lpdw_process_id = c_ulong()
            result = GetWindowThreadProcessId(hwnd, byref(lpdw_process_id))
            found_pid = lpdw_process_id.value
            if found_pid == pid:
                hwnds.append(hwnd)

    EnumWindows(EnumWindowsProc(callback), None)
    # hwnds[0] should be the window we want, and the only hwnd in the list.
    hwnd = hwnds[0]
    # Constants for Win32 API calls
    ICON_SMALL = 0
    ICON_BIG = 1
    WM_SETICON = 0x0080
    # Load the icon file
    hIcon = windll.user32.LoadImageW(None, icon, 1, 0, 0, 0x00000010)
    # Set the window icon using WM_SETICON message
    windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hIcon)
    windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hIcon)


def open_window(url: str, title: str, width: int, height: int, fullscreen: bool, icon_dir = None) -> None:
    def icon_callback():
        on_shown(icon_dir)
    window = webview.create_window(title, url=url, width=width, height=height, fullscreen=fullscreen)
    if sys.platform.startswith('win'):
        window.events.shown += icon_callback
    webview.start(storage_path=tempfile.mkdtemp())
    

def activate(url: str, title: str, width: int, height: int, fullscreen: bool, icon_dir) -> None:
    def check_shutdown() -> None:
        while process.is_alive():
            time.sleep(0.1)
        globals.server.should_exit = True
        while globals.state != globals.State.STOPPED:
            time.sleep(0.1)
        _thread.interrupt_main()

    multiprocessing.freeze_support()
    process = multiprocessing.Process(target=open_window, args=(url, title, width, height, fullscreen, icon_dir), daemon=False)
    process.start()
    Thread(target=check_shutdown, daemon=True).start()


def find_open_port(start_port: int = 8000, end_port: int = 8999) -> int:
    '''Reliably find an open port in a given range.

    This function will actually try to open the port to ensure no firewall blocks it.
    This is better than, e.g., passing port=0 to uvicorn.
    '''
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            pass
    raise OSError('No open port found')
