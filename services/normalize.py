import re
import pandas as pd

from utils.logger import Logger
from utils.manage_csv import PrepareData
from utils.standardize_data import EditText

class PreprocessData:
    def __init__(self):
        self.data = PrepareData('data/master_clauses.csv').load_data()
        self.logger = Logger()
        
    def preprocess_data(self):
        try:
            answer_columns = [col for col in self.data.columns.tolist() if col.endswith('Answer')]
            data = self.data[answer_columns]
            non_answer_columns = [col for col in self.data.columns.tolist() if not col.endswith('Answer')]
            non_answer_columns.pop(0)
            data.columns = non_answer_columns
            preprocessed_data = NormalizeData().normalize_data(data)
            self.logger.log_info("Data preprocessed")
        except Exception as e:
            self.logger.log_error(f"Error preprocessing data: {e}")
            preprocessed_data = None
        return preprocessed_data
    
    
class NormalizeData:
    def __init__(self):
        self.logger = Logger()
    
    def _document_name(self, data, column='Document Name'):
        data[column] = data[column].apply(lambda x: ' '.join(re.split(r'\s+', x.strip().lower())).capitalize())
        data[column] = data[column].apply(lambda x: re.sub(r'agreement.*', '', x, flags=re.IGNORECASE))
        return data

    def _date(self, data, date_column):
        data[date_column] = pd.to_datetime(data[date_column], errors='coerce')
        return data

    # TODO: Son líneas demasiado largas, se pueden dividir
    def _providers(self, data, column='Parties'):
        data[column] = data[column].apply(lambda x: re.split(';', x) if isinstance(x, str) else [])
        data[column] = data[column].apply(lambda x: [entry if isinstance(entry, str) and not re.fullmatch(r'[\W_]+', entry) else None for entry in x])
        data[column] = data[column].apply(lambda x: [re.sub(r'\s*\(.*?\)', '', entry.strip().lower()).capitalize() for entry in x])
        data[column] = data[column].apply(lambda x: [EditText.clean_text_after(entry, r',.*') for entry in x])
        data[column] = data[column].apply(lambda x: [entry for entry in x if entry and not re.compile(r'(.)\1{4,}').search(entry)])
        return data
    
    def _governing_law(self, data, column='Governing Law'):
        data[column] = data[column].apply(lambda x: x if isinstance(x, str) and not re.fullmatch(r'[\W_]+', x) else None)
        data[column] = data[column].fillna('')
        data[column] = data[column].apply(lambda x: EditText.clean_text_after(x, r',.*'))
        data[column] = data[column].apply(lambda x: re.split(r';| and ', x) if isinstance(x, str) else [])
        return data
    
    def _count_days(value):
        if pd.isna(value) or value is None:
            return 0
        elif "perpetual" in value.lower():
            return 9999
        elif re.search(r'\d+', value):
            years = sum(int(num) for num in re.findall(r'(\d+)\s*years?', value, flags=re.IGNORECASE))
            months = sum(int(num) for num in re.findall(r'(\d+)\s*months?', value, flags=re.IGNORECASE))
            days = sum(int(num) for num in re.findall(r'(\d+)\s*days?', value, flags=re.IGNORECASE))
            total_days = (years * 365) + (months * 30) + days
            return total_days
        else:
            return None
    
    def normalize_data(self, data):
        try:
            data = NormalizeData._date(self, data, 'Effective Date')
            clean_data = data.dropna(subset=['Document Name','Effective Date'])
            trim_data = clean_data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            preprocessed_data = NormalizeData._document_name(self, trim_data)
            preprocessed_data = NormalizeData._date(self, preprocessed_data, 'Agreement Date')
            preprocessed_data = NormalizeData._date(self, preprocessed_data, 'Expiration Date')
            preprocessed_data = NormalizeData._providers(self, preprocessed_data)
            preprocessed_data = NormalizeData._governing_law(self, preprocessed_data)
            preprocessed_data['Renewal Term'] = preprocessed_data['Renewal Term'].apply(NormalizeData._count_days)
            preprocessed_data = preprocessed_data.rename(columns={'Renewal Term': 'Renewal Term (days)'})
            preprocessed_data.rename_axis(index='Index', inplace=True)
            self.logger.log_info("Data normalized")
        except Exception as e:
            self.logger.log_error(f"Error normalizing data: {e}")
            preprocessed_data = None
        return preprocessed_data

    