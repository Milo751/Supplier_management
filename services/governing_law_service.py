import pandas as pd
import streamlit as st

from utils.logger import Logger

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
    
    @st.cache_resource
    def get_location(_self, unique_laws):
        countries = _self.get_countries(unique_laws)
        location = _self.get_continents(countries)
        return location
    
    def get_countries(self, unique_laws):
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

    def get_continents(self, countries):
        continents_df = CountriesContinents().load_continents()
        countries_continents = pd.merge(
        countries, 
        continents_df, 
        left_on='Pais', 
        right_on='ISO', 
        how='left'
        )
        # Eliminar columnas no necesarias
        countries_continents = countries_continents.drop(columns=['name', 'Continent_ISO', 'ISO'], errors='ignore')
        
        # Manejar los países que no tienen continente
        if countries_continents['Continent'].isnull().any():
            missing_countries = countries_continents[countries_continents['Continent'].isnull()]['Pais'].tolist()
            for country in missing_countries:
                self.logger.log_error(f"Continent for country {country} not found")
        
        # Devolver el DataFrame con las columnas relevantes
        return countries_continents[['Ciudad', 'Pais', 'Continent', 'Latitud', 'Longitud']]

    
class CountriesContinents:
    def __init__(self):
        self.logger = Logger()
    
    def load_countries(self):
        countries = pd.read_csv('data/worldcities.csv')
        countries = countries[['city','country', 'lat', 'lng', 'admin_name']]
        return countries
    
    def load_continents(self):
        continents = pd.read_csv('data/countries and continents.csv', na_values=["N/A", "null", "", " "], keep_default_na=False)
        continents = continents[['name', 'Continent', 'ISO4217-currency_country_name']]
        continents = continents.rename(columns={'ISO4217-currency_country_name': 'ISO'})
        continents['ISO'].fillna(continents['name'], inplace=True)
        continents['ISO'] = continents['ISO'].str.title()
        return continents
        