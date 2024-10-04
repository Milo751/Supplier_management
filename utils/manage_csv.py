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
    
    
class NormalizeData:
    def __init__(self, data):
        self.data = data
        self.logger = Logger()

    def normalize(self, subset_columns=None):
        try:
            self.data = self.data.dropna(subset=subset_columns)
            self.data = self.data.drop_duplicates()
            self.logger.log_info("Data normalized")
        except Exception as e:
            self.logger.log_error(f"Error normalizing data: {e}")
        return self.data
    
    def rename_columns(self, columns):
        try:
            self.data.columns = columns
            self.logger.log_info("Columns renamed")
        except Exception as e:
            self.logger.log_error(f"Error renaming columns: {e}")
        return self.data
