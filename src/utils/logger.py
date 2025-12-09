import logging


def setup_logger():
    logger = logging.getLogger("plmtool")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = "%(asctime)s - %(levelname)s - %(message)s"
        handler.setFormatter(logging.Formatter(fmt))
        logger.addHandler(handler)

    return logger
