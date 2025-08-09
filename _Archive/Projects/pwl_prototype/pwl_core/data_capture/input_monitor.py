"""Monitors global keyboard and mouse events using pynput.

This module provides functions to capture system-wide input events in a non-blocking
manner. It uses separate threads for keyboard and mouse listeners, logging the events
through the project's core logger.
"""

# Standard library imports
from typing import Optional, Tuple, Union

# Third-party library imports
from pynput import keyboard, mouse

# Local application/module imports
from pwl_core.core_logger import logger


def on_press(key: Union[keyboard.Key, keyboard.KeyCode, None]) -> Optional[bool]:
    """Handles key press events and logs them.

    This callback function is executed whenever a key is pressed. It logs the
    specific key and stops the keyboard listener if the 'Esc' key is pressed.

    Args:
        key (Union[keyboard.Key, keyboard.KeyCode, None]): The key that was pressed.

    Returns:
        Optional[bool]: False if the listener should be stopped, else None.
    """
    try:
        # Log alphanumeric keys
        logger.debug(f"Key pressed: {key.char}")
    except AttributeError:
        # Log special keys (e.g., Ctrl, Alt, Esc)
        logger.debug(f"Special key pressed: {key}")

    if key == keyboard.Key.esc:
        logger.info("Escape key pressed. Stopping keyboard listener.")
        # Returning False from the on_press callback stops the listener.
        return False
    return None


def on_click(x: int, y: int, button: mouse.Button, pressed: bool) -> None:
    """Handles mouse click events and logs them.

    This callback is executed on mouse clicks. It logs the event details only when
    a button is pressed down, not on release.

    Args:
        x (int): The x-coordinate of the click.
        y (int): The y-coordinate of the click.
        button (mouse.Button): The mouse button that was clicked.
        pressed (bool): True if the button was pressed, False if released.

    Returns:
        None
    """
    if pressed:
        logger.debug(f"Mouse clicked at ({x}, {y}) with {button}")


def start_listener() -> Tuple[keyboard.Listener, mouse.Listener]:
    """Initializes and starts non-blocking keyboard and mouse listeners.

    This function creates listener threads for both keyboard and mouse events and
    starts them. The listeners run in the background, allowing the main program
    to continue execution.

    Returns:
        Tuple[keyboard.Listener, mouse.Listener]: A tuple containing the
        keyboard and mouse listener instances.
    """
    logger.info("Initializing input listeners...")
    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_click=on_click)

    keyboard_listener.start()
    mouse_listener.start()
    logger.info("Input listeners started in background threads.")

    return keyboard_listener, mouse_listener