import os
import logging

class Logger:
    def __init__(self, log_folder='logs', log_file='app.log'):
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        log_path = os.path.join(log_folder, log_file)
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.FileHandler(log_path)]
        )
        self.logger = logging.getLogger()

    def log_debug(self, message):
        self.logger.debug(message)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_critical(self, message):
        self.logger.critical(message)