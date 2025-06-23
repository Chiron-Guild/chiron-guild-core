# chiron-guild-core/Projects/pwl_prototype/scripts/test_logger.py

import sys
import os

# Add the project root directory to the Python path to allow for absolute imports.
# This must be done before the 'pwl_core' module can be imported.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    # Using insert(0, ...) gives this path priority.
    sys.path.insert(0, PROJECT_ROOT)

def run_test():
    """Runs the logger test by emitting messages at all standard levels."""
    # Import the logger here, after the path has been configured.
    # This resolves the C0413:wrong-import-position Pylint error.
    from pwl_core.core_logger import logger

    logger.info("--- Starting Logger Test ---")

    logger.debug("This is a detailed debug message for developers.")
    logger.info("This is an informational message about the application's progress.")
    logger.warning("This is a warning message. The application can continue, but something is unexpected.")
    logger.error("This is an error message. A specific operation failed.")
    logger.critical("This is a critical message. The application cannot continue.")

    logger.info("--- Logger Test Finished ---")

    print("\n--- Verification Steps ---")
    print("1. Check the console output above. You should see INFO, WARNING, ERROR, and CRITICAL messages.")
    print(f"2. Check the contents of the 'pwl_app.log' file located in the project root.")
    print("   It should contain all five message levels (DEBUG through CRITICAL).")

if __name__ == "__main__":
    run_test()