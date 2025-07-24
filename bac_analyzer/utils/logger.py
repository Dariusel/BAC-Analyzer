import logging

silence_libs = ["urllib3", "requests", "http.client"]

def init_logger():
    # Only configure logging if it's not already configured
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(levelname)s - %(message)s",
            datefmt="%H:%M:%S"
        )

        # Silence third-party noisy modules
        for lib in silence_libs:
            logging.getLogger(lib).setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("http.client").setLevel(logging.WARNING)