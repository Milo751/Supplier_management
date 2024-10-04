class DateType:
    @staticmethod
    def date_to_string(date):
        date_str = date.strftime('%d-%m-%Y')
        return date_str
    
    @staticmethod
    def df_to_string(df, date_column):
        df[date_column] = df[date_column].dt.strftime('%d-%m-%Y')
        return df