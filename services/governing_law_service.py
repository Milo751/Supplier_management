import pandas as pd
import streamlit as st

from utils.logger import Logger
from utils.manage_csv import PrepareData

class GoverningLaw:
    def __init__(self, data):
        self.logger = Logger()
        self.data = data[['Document Name', 'Governing Law']]

    def unique_governing_laws(self):
        all_laws = [law for sublist in self.data['Governing Law'] for law in sublist]
        unique_laws = set(all_laws)
        if '' in unique_laws:
            unique_laws.remove('')
        return unique_laws
    
    def get_location(self, unique_laws):
        countries = self._get_countries(unique_laws)
        location = self._get_continents(countries)
        return location
    
    def _get_countries(self, unique_laws):
        countries_continents = CountriesContinents()
        countries = countries_continents.load_countries()
        location = pd.DataFrame(columns=['Ciudad', 'Pais', 'Latitud', 'Longitud'])
        
        for law in unique_laws:
            country_row = countries[(countries['country'] == law) | (countries['city'] == law) | (countries['admin_name'] == law)]
            if not country_row.empty:
                country = country_row.iloc[0]['country']
                lat = country_row.iloc[0]['lat']
                lng = country_row.iloc[0]['lng']
                
                new_row = pd.DataFrame({
                    'Ciudad': [law],
                    'Pais': [country],
                    'Latitud': [lat],
                    'Longitud': [lng]
                })
                location = pd.concat([location, new_row], ignore_index=True)
            else:
                self.logger.log_error(f"City or country {law} not found")
        return location

    def _get_continents(self, countries):
        continents_df = CountriesContinents().load_continents()
        countries_continents = pd.merge(
        countries, 
        continents_df, 
        left_on='Pais', 
        right_on='ISO', 
        how='left'
        )
        countries_continents = countries_continents.drop(columns=['name', 'Continent_ISO', 'ISO'], errors='ignore')
        if countries_continents['Continent'].isnull().any():
            missing_countries = countries_continents[countries_continents['Continent'].isnull()]['Pais'].tolist()
            for country in missing_countries:
                self.logger.log_error(f"Continent for country {country} not found")
        return countries_continents[['Ciudad', 'Pais', 'Continent', 'Latitud', 'Longitud']]

    
class CountriesContinents:
    @staticmethod   
    def load_countries():
        csv_loader = PrepareData('data/worldcities.csv') 
        countries = csv_loader.load_data()
        countries = countries[['city','country', 'lat', 'lng', 'admin_name']]
        return countries
    
    @staticmethod
    def load_continents():
        csv_loader = PrepareData('data/countries and continents.csv')
        continents = csv_loader.load_data(na_values=["N/A", "null", "", " "], keep_default_na=False)
        continents = continents[['name', 'Continent', 'ISO4217-currency_country_name']]
        continents = continents.rename(columns={'ISO4217-currency_country_name': 'ISO'})
        continents['ISO'] = continents['ISO'].fillna(continents['name'])
        continents['ISO'] = continents['ISO'].str.title()
        return continents
        