from utils.logger import Logger

class EffectiveDates:
    def __init__(self, data):
        self.logger = Logger()
        self.data = data[['Document Name', 'Effective Date']]
        
  
class DateInsights():
    def __init__(self, data):
        self.data = data

    def get_min_date_index(self):
        min_date_row = self.data.loc[self.data['Effective Date'].idxmin()]
        return min_date_row['Effective Date'].strftime('%d-%m-%Y'), min_date_row['Document Name']
    
    def get_max_date_index(self):
        max_date_row = self.data.loc[self.data['Effective Date'].idxmax()]
        return max_date_row['Effective Date'].strftime('%d-%m-%Y'), max_date_row['Document Name']
        
    
