"""The main entry point for the Personal Work Ledger (PWL) application."""

# Standard library imports
import sys
import os

# Add the project root to the Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Local application/module imports
from pwl_core.engine import PWLEngine
from pwl_core.core_logger import logger


def main():
    """Initializes and runs the PWL Engine."""
    engine = PWLEngine()
    try:
        engine.start()
        # The engine runs in background threads, so we need to keep the main thread
        # alive to wait for the shutdown signal (e.g., Esc key).
        # We can join the keyboard listener thread for this purpose.
        if engine._keyboard_listener:
            engine._keyboard_listener.join()
    except Exception as e:
        logger.critical(f"A critical error occurred in the main loop: {e}", exc_info=True)
    finally:
        # Ensure stop is called even if there's an unexpected error
        engine.stop()


if __name__ == "__main__":
    main()