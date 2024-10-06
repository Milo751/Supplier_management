from utils.logger import Logger
from collections import Counter
import pandas as pd

class Providers:
    def __init__(self, data):
        self.logger = Logger()
        self.data = data[['Parties']]

    def count_parties(self):
        all_parties = [party for sublist in self.data['Parties'] for party in sublist]
        party_counts = Counter(all_parties)
        party_counts_df = pd.DataFrame.from_dict(party_counts, orient='index', columns=['Count']).reset_index()
        party_counts_df.rename(columns={'index': 'Party'}, inplace=True)
        return party_counts_df