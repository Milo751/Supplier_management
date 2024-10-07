import random
import pandas as pd

from utils.logger import Logger

class RenewalTerm:
    def __init__(self, data, columns):
        self.logger = Logger()
        self.data = data[columns]

    def count_group_by(self, column):
        try:
            count = self.data.groupby(column).size().reset_index(name='Count')
            self.logger.log_info('Data grouped successfully')
        except Exception as e:
            self.logger.log_error(f'Error grouping data: {str(e)}')
            count = pd.DataFrame()
        return count
    
    def generate_color(self, df):
        try:
            colors = ['#%06X' % random.randint(0, 0xFFFFFF) for _ in range(len(df))]
            df['Color'] = colors
            self.logger.log_info('Colors generated successfully')
        except Exception as e:
            self.logger.log_error(f'Error generating colors: {str(e)}')
        return df
