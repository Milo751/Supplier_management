import pandas as pd

class DateManage():
    def __init__(self, data):
        self.data = data

    def column_to_date(self, column):
        self.data[column] = pd.to_datetime(self.data[column], errors='coerce')
        self.data = self.data.dropna(subset=[column])
        return self.data
    
    @staticmethod
    def date_to_string(date):
        date_str = date.strftime('%d-%m-%Y')
        return date_str
    
    @staticmethod
    def df_to_string(df):
        df['Effective Date-Answer'] = df['Effective Date-Answer'].dt.strftime('%d-%m-%Y')
        df = df.rename(
            columns={
                'Document Name-Answer':'Contrato',
                'Effective Date-Answer':'Fecha efectiva'}
            )
        return df
    
class DateInsights():
    def __init__(self, data):
        self.data = data

    def get_min_date_index(self, column):
        min_date_row = self.data.loc[self.data[column].idxmin()]
        return DateManage.date_to_string(min_date_row['Effective Date-Answer']), min_date_row['Document Name-Answer']
    
    def get_max_date_index(self, column):
        max_date_row = self.data.loc[self.data[column].idxmax()]
        return DateManage.date_to_string(max_date_row['Effective Date-Answer']), max_date_row['Document Name-Answer']