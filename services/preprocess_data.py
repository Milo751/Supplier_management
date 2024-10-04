import re
import pandas as pd

from utils.logger import Logger
from utils.manage_csv import PrepareData

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
    
    # TODO: Son líneas demasiado largas, se pueden dividir
    def _providers(self, data):
        data['Parties'] = data['Parties'].apply(lambda x: re.split(';', x) if isinstance(x, str) else [])
        data['Parties'] = data['Parties'].apply(lambda x: [re.sub(r'\s*\(.*?\)', '', entry.strip().lower()).capitalize() for entry in x])
        data['Parties'] = data['Parties'].apply(lambda x: [entry for entry in x if entry and not re.compile(r'(.)\1{4,}').search(entry)])
        return data
    
    def _governing_law(self, data):
        data['Governing Law'] = data['Governing Law'].apply(lambda x: x if isinstance(x, str) and not re.fullmatch(r'[\W_]+', x) else None)
        #data['Governing Law'] = data['Governing Law'].apply(lambda x: re.split(';', x) if isinstance(x, str) and not re.fullmatch(r'[\W_]+', x) else None)
        #data['Governing Law'] = data['Governing Law'].apply(lambda x: [item.split(',')[0].strip() for item in x])
        return data
    
    def normalize_data(self, data):
        try:
            data['Effective Date'] = pd.to_datetime(data['Effective Date'], errors='coerce')
            clean_data = data.dropna(subset=['Document Name','Effective Date'])
            trim_data = clean_data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            trim_data['Document Name'] = trim_data['Document Name'].apply(lambda x: ' '.join(re.split(r'\s+', x.strip().lower())).capitalize())
            preprocessed_data = NormalizeData._providers(self, trim_data)
            preprocessed_data = NormalizeData._governing_law(self, preprocessed_data)
            preprocessed_data.rename_axis(index='Index', inplace=True)
            self.logger.log_info("Data normalized")
        except Exception as e:
            self.logger.log_error(f"Error normalizing data: {e}")
            preprocessed_data = None
        return preprocessed_data

    