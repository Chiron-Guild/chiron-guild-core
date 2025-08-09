"""Monitors the active window to retrieve title and process information.

This version uses the built-in ctypes library to avoid the pywin32 dependency,
making it suitable for environments where pywin32 cannot be installed.
"""

# Standard library imports
import ctypes
from typing import Dict, Optional

# Third-party library imports
import psutil
import pygetwindow as gw

# Local application/module imports
from pwl_core.core_logger import logger

# Define necessary Windows API functions and types using ctypes
user32 = ctypes.windll.user32
pid = ctypes.c_ulong()


def get_active_window_info() -> Optional[Dict[str, str]]:
    """Gets information about the currently active foreground window.

    Retrieves the window title, the process name, and the process ID (PID)
    of the application that owns the active window.

    Returns:
        Optional[Dict[str, str]]: A dictionary containing 'title',
        'process_name', and 'pid', or None if no active window is found
        or an error occurs.
    """
    try:
        active_window = gw.getActiveWindow()
        if not active_window:
            logger.debug("No active window found.")
            return None

        # The _hWnd attribute is protected, but necessary for API calls.
        # We accept the Pylint W0212 warning here as a pragmatic choice.
        # pyright: reportPrivateUsage=false
        user32.GetWindowThreadProcessId(active_window._hWnd, ctypes.byref(pid))
        process_id = pid.value

        process = psutil.Process(process_id)
        process_name = process.name()
        window_title = active_window.title

        return {
            "title": window_title,
            "process_name": process_name,
            "pid": str(process_id),
        }
    except (gw.PyGetWindowException, psutil.NoSuchProcess, psutil.AccessDenied) as e:
        logger.error(f"Error getting active window info: {e}")
        return None