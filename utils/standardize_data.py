import re

class DateType:
    @staticmethod
    def df_to_string(df, date_column):
        df[date_column] = df[date_column].dt.strftime('%d-%m-%Y')
        return df
    
class EditText:
    def clean_text_after(text, pattern):
        return re.sub(pattern, '', text)