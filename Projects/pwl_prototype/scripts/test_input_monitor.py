"""Test script for the global input monitoring module.

This script starts the keyboard and mouse listeners from the input_monitor
module and waits for the 'Esc' key to be pressed to terminate them.
It serves as a simple demonstration and verification of the monitor's
functionality.
"""

# Local application/module imports
from pwl_core.core_logger import logger
from pwl_core.data_capture import input_monitor


def main() -> None:
    """Main function to run the input monitor test."""
    logger.info("Starting the input monitor test script.")

    # Start the listeners in non-blocking mode
    keyboard_listener, mouse_listener = input_monitor.start_listener()

    print("\n" + "="*60)
    print("Input listener test is running.")
    print("Press keys and click the mouse to see log output.")
    print("Press the 'Esc' key to stop the listeners and exit.")
    print("="*60 + "\n")

    # The main thread will block here until the keyboard listener is stopped.
    # The on_press function in the monitor module returns False on 'Esc'.
    keyboard_listener.join()

    # Once the keyboard listener has stopped, we explicitly stop the mouse listener.
    mouse_listener.stop()
    # Wait for the mouse listener thread to finish.
    mouse_listener.join()

    logger.info("All listeners have been stopped.")
    print("Input listeners stopped successfully.")


if __name__ == "__main__":
    main()