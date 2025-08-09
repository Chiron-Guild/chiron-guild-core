"""
Test script for window monitoring functionality.
Continuously monitors and displays active window information.
"""

import sys
import os
import time

# Add the project root to the Python path to allow for absolute imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# NOTE: Local imports are done inside the main() function after the path setup.
# This prevents Pylint's C0413:wrong-import-position error.


def main():
    """
    Main test function that continuously monitors active windows.
    """
    # Local application/module imports (after path setup)
    from pwl_core.data_capture.window_monitor import get_active_window_info
    from pwl_core.core_logger import logger

    logger.info("--- Starting Window Monitor Test ---")
    logger.info("Switch to different windows to see the output change.")
    logger.info("Press Ctrl+C to stop the test.")
    print("-" * 60)

    try:
        while True:
            window_info = get_active_window_info()

            if window_info:
                # Use logger for consistency, but print is also fine for a test script
                logger.info(f"Active Window: {window_info}")
            else:
                logger.info("No active window detected or info is inaccessible.")

            time.sleep(3)

    except KeyboardInterrupt:
        logger.info("\nWindow monitoring stopped by user.")
        print("-" * 60)
    except Exception as e:
        # A general catch-all for any other unexpected errors during the test
        logger.critical(f"An unexpected error occurred during test: {e}", exc_info=True)


if __name__ == "__main__":
    main()