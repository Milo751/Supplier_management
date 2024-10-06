from utils.logger import Logger
import random

class RenewalTerm:
    def __init__(self, data):
        self.logger = Logger()
        self.data = data[['Document Name', 'Renewal Term (days)']]

    def count_renewal_terms(self):
        return self.data.groupby('Renewal Term (days)').size().reset_index(name='Count')
    
    def generate_color(self, df):
        colors = ['#%06X' % random.randint(0, 0xFFFFFF) for _ in range(len(df))]
        df['Color'] = colors
        return df
