# chiron-guild-core/Projects/pwl_prototype/pwl_core/core_logger.py

import logging
import os

# Define the project root dynamically to ensure the log file path is correct.
# This navigates two levels up from this file's location (__file__).
# pwl_core/core_logger.py -> pwl_core -> project_root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE_PATH = os.path.join(PROJECT_ROOT, 'pwl_app.log')

# 1. Get the logger instance.
logger = logging.getLogger('pwl_logger')

# Set the logger's level to DEBUG. This is the lowest threshold; handlers will filter from here.
logger.setLevel(logging.DEBUG)

# 2. Create a formatter.
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 3. Create and configure handlers, only if the logger has no handlers yet.
# This prevents duplicate log entries if the module is imported multiple times.
if not logger.handlers:
    # Console Handler - prints INFO and higher levels to the console.
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    c_handler.setFormatter(formatter)

    # File Handler - writes DEBUG and higher levels to a file.
    f_handler = logging.FileHandler(LOG_FILE_PATH)
    f_handler.setLevel(logging.DEBUG)
    f_handler.setFormatter(formatter)

    # 4. Add handlers to the logger.
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)