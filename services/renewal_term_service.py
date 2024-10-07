from utils.logger import Logger
import random

class RenewalTerm:
    def __init__(self, data, columns):
        self.logger = Logger()
        self.data = data[columns]

    def count_group_by(self, column):
        return self.data.groupby(column).size().reset_index(name='Count')
    
    def generate_color(self, df):
        colors = ['#%06X' % random.randint(0, 0xFFFFFF) for _ in range(len(df))]
        df['Color'] = colors
        return df
