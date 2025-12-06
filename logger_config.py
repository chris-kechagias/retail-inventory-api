import logging
import sys

LOG_FORMAT = "%(levelname)s: %(asctime)s - %(name)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging():
    """
    ds
    """

    # 1.
    root_logger = logging.getLogger()

    #
    if not root_logger.handlers:

        # 2.
        root_logger.setLevel(logging.INFO)

        # 3.
        handler = logging.StreamHandler(sys.stdout)

        # 4.
        formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

        # 5.
        handler.setFormatter(formatter)

        # 6.
        root_logger.addHandler(handler)


# Initialize logging configuration at module load
setup_logging()
