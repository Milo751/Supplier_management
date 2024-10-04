from utils.logger import Logger
from utils.manage_csv import PrepareData, NormalizeData
from googletrans import Translator

class SetData:
    def __init__(self):
        self.data = PrepareData('data/master_clauses.csv').load_data()
        self.logger = Logger()
        
    def column_names(self):
        try:
            non_answer_columns = [col for col in self.data.columns.tolist() if not col.endswith('Answer')]
            non_answer_columns.pop(0)
            self.logger.log_info("Columns names getted")
        except Exception as e:
            self.logger.log_error(f"Error getting column names: {e}")
        return non_answer_columns
        
    def preprocessed_data(self, column_names):
        try:
            answer_columns = [col for col in self.data.columns.tolist() if col.endswith('Answer')]
            data = self.data[answer_columns]
            renamed_data = NormalizeData(data).rename_columns(column_names)
            self.logger.log_info("Data preprocessed getted")
        except Exception as e:
            self.logger.log_error(f"Error getting preprocessed data: {e}")
            renamed_data = None
        return renamed_data