import logging
import sys
import os

# Define the log format string
LOG_FORMAT = "%(levelname)s: %(asctime)s - %(name)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging():
    """
    Configures the root logger with console output.

    Sets up INFO-level logging with timestamps and module names.
    Prevents duplicate handler registration.
    """

    # 1. Get the root logger
    root_logger = logging.getLogger()

    # Prevent duplicate handlers
    if not root_logger.handlers:
        root_logger.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

        # 1. Console Handler (for Render/Docker)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        # 2. File Handler (for local debugging)
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        file_handler = logging.FileHandler("logs/app.log")
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


# Initialize logging at module import
setup_logging()
