import pandas as pd

from utils.logger import Logger
from collections import Counter

class Providers:
    def __init__(self, data):
        self.logger = Logger()
        self.data = data[['Parties']]

    def count_parties(self):
        try:
            all_parties = [party for sublist in self.data['Parties'] for party in sublist]
            party_counts = Counter(all_parties)
            party_counts_df = pd.DataFrame.from_dict(party_counts, orient='index', columns=['Count']).reset_index()
            party_counts_df.rename(columns={'index': 'Party'}, inplace=True)
            self.logger.log_info('Parties counted successfully')
        except Exception as e:
            self.logger.log_error(f'Error counting parties: {str(e)}')
            party_counts_df = pd.DataFrame()
        return party_counts_df