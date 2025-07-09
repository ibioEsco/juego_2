import logging
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, log_file: str, max_bytes: int = 1000000, backup_count: int = 3):
        self.logger = logging.getLogger("fastapi_logger")
        self.logger.setLevel(logging.INFO)

        handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger