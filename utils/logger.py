import logging

from logging.handlers import RotatingFileHandler

class Logger:
    def setup_logging(log_level):
        handler = RotatingFileHandler('logs/app.log', maxBytes=5000000, backupCount=2)
        logging.basicConfig(handlers=[handler], 
                            level=log_level,
                            format='%(asctime)s - %(levelname)s - %(message)s'
                            )