import pandas as pd

from .logger import Logger

class PrepareData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.logger = Logger()

    def load_data(self):
        try:
            data = pd.read_csv(self.file_path)
            self.logger.log_info(f"Data loaded from {self.file_path}")
            return data
        except FileNotFoundError:
            self.logger.log_error(f"File not found: {self.file_path}")
            return None
