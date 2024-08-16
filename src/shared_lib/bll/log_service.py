# log_service.py
import os
import logging
import datetime
from logging.handlers import TimedRotatingFileHandler

from shared_lib.tests import config

MAX_BYTES = config.log_max_bytes  # 10 MB


class CustomHandler(TimedRotatingFileHandler):
    def __init__(self, filename, maxBytes, backupCount, *args, **kwargs):
        super().__init__(filename, *args, **kwargs)
        self.maxBytes = maxBytes
        self.backupCount = backupCount

    def shouldRollover(self, record):
        # Call the parent class method
        if super().shouldRollover(record):
            return 1
        # Check if the current log file is larger than maxBytes
        if os.path.getsize(self.baseFilename) >= self.maxBytes:
            return 1
        return 0

    def doRollover(self):
        # Rollover the current log
        super().doRollover()
        # If there are more than backupCount logs, delete the oldest
        logs = sorted([log for log in os.listdir(self.directory) if log.startswith(self.prefix)])
        if len(logs) > self.backupCount:
            os.remove(os.path.join(self.directory, logs[0]))


# Configure logging
def configure_logging():
    # Create a log directory if it doesn't exist
    if not os.path.exists('log'):
        os.makedirs('log')

    # Get the current date in the format YYYY-MM-DD
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    # Set the log filename to the current date
    log_filename = os.path.join('log', f'{current_date}.log')
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

    # Create a handler that writes log messages to a file, with a new file created each day or when the file size exceeds 10MB
    handler = CustomHandler(log_filename, maxBytes=MAX_BYTES, backupCount=7, when='midnight', interval=1)
    logging.getLogger('').addHandler(handler)
