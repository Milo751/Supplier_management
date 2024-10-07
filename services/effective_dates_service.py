from utils.logger import Logger

class EffectiveDates:
    def __init__(self, data, columns):
        self.logger = Logger()
        self.data = data[columns]

    def get_min_date_index(self, date_column):
        try:
            min_date_row = self.data.loc[self.data[date_column].idxmin()]
            min_name = min_date_row['Document Name']
            min_date = min_date_row[date_column].strftime('%d-%m-%Y')
            self.logger.log_info(f"Min date index: {min_date}")
        except Exception as e:
            self.logger.log_error(f"Error getting min date index: {e}")
            min_date = None
            min_name = None
        return min_date, min_name
    
    def get_max_date_index(self, date_column):
        try:
            max_date_row = self.data.loc[self.data[date_column].idxmax()]
            max_name = max_date_row['Document Name']
            max_date = max_date_row[date_column].strftime('%d-%m-%Y')
            self.logger.log_info(f"Max date index: {max_date}")
        except Exception as e:
            self.logger.log_error(f"Error getting max date index: {e}")
            max_date = None
            max_name = None
        return max_date, max_name
        
    
