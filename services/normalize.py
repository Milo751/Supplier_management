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
            # Set column names
            answer_columns = [col for col in self.data.columns.tolist() if col.endswith('Answer')]
            data = self.data[answer_columns]
            non_answer_columns = [col for col in self.data.columns.tolist() if not col.endswith('Answer')]
            non_answer_columns.pop(0)
            data.columns = non_answer_columns
            data = data.rename(columns={'Notice Period To Terminate Renewal': 'Notification Renewal'})
            preprocessed_data = NormalizeData().normalize_data(data)
            self.logger.log_info("Data preprocessed")
        except Exception as e:
            self.logger.log_error(f"Error preprocessing data: {e}")
            preprocessed_data = None
        return preprocessed_data
    
    
class NormalizeData:
    def __init__(self):
        self.logger = Logger()
    
    def _document_name(self, entries):
        whitespace_pattern = re.compile(r'\s+')
        agreement_pattern = re.compile(r'\bagreement\b.*', flags=re.IGNORECASE)

        if not isinstance(entries, str):
            return entries
        entries = ' '.join(re.split(whitespace_pattern, entries.strip().lower())).capitalize()
        cleaned_entries = re.sub(agreement_pattern, '', entries).strip()
        return cleaned_entries


    def _dates(self, data, date_columns):
        for date_column in date_columns:
            data[date_column] = pd.to_datetime(data[date_column], errors='coerce')
        return data   
        
    def _providers(self, entries):
        remove_special_chars = re.compile(r'[\W_]+')
        remove_parentheses = re.compile(r'\s*\(.*?\)')
        remove_after_comma = re.compile(r',.*')
        remove_repeating_chars = re.compile(r'(.)\1{4,}')

        if not isinstance(entries, str):
            return []
        entries = re.split(';', entries)

        cleaned_entries = []
        for entry in entries:
            if re.fullmatch(remove_special_chars, entry):
                continue
            entry = re.sub(remove_parentheses, '', entry.strip().lower()).capitalize()
            entry = re.sub(remove_after_comma, '', entry)
            if re.search(remove_repeating_chars, entry):
                continue
            if entry:
                cleaned_entries.append(entry)
        return cleaned_entries
      
    def _governing_law(self, entries):
        remove_special_chars = re.compile(r'[\W_]+')
        remove_after_comma = re.compile(r',.*')
        split_pattern = re.compile(r';| and ')

        if not isinstance(entries, str):
            return []
        if re.fullmatch(remove_special_chars, entries):
            return []
        entries = re.sub(remove_after_comma, '', entries.strip())
        split_entries = re.split(split_pattern, entries)
        
        cleaned_entries = []
        for entry in split_entries:
            entry = entry.strip()
            if entry:
                cleaned_entries.append(entry)
        return cleaned_entries

    def _renewal_term(self, data, column='Renewal Term'):
        data[column] = data[column].apply(self._count_days)
        data = data.rename(columns={column: f'{column} (days)'})
        return data
    
    def _count_days(self, value):
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
            data = NormalizeData._dates(self, data, ['Effective Date', 'Agreement Date', 'Expiration Date'])
            clean_data = data.dropna(subset=['Document Name','Effective Date'])
            trim_data = clean_data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

            # Required data
            trim_data['Document Name'] = trim_data['Document Name'].apply(self._document_name)
            trim_data['Parties'] = trim_data['Parties'].apply(self._providers)
            trim_data['Governing Law'] = trim_data['Governing Law'].apply(self._governing_law)
            preprocessed_data = self._renewal_term(trim_data)

            # Extra data
            preprocessed_data = self._renewal_term(preprocessed_data, 'Notification Renewal')

            preprocessed_data.rename_axis(index='Index', inplace=True)
            self.logger.log_info("Data normalized")
        except Exception as e:
            self.logger.log_error(f"Error normalizing data: {e}")
            preprocessed_data = None
        return preprocessed_data

    