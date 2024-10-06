import streamlit as st
import pandas as pd

from app import data
from services.governing_law_service import GoverningLaw

governing_law = GoverningLaw(data)
unique_governing = governing_law.unique_governing_laws()
location = governing_law.get_location(unique_governing)

st.title('Analísis de leyes aplicables por zona geográfica')

st.write('Zonas geográficas encontradas:')
st.dataframe(location, width=1000, height=500)
st.map(location, latitude='Latitud', longitude='Longitud')