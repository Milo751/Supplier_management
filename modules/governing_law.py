import streamlit as st
import pandas as pd

from app import data
from services.governing_law_service import GoverningLaw

governing_law = GoverningLaw(data)
coordinates = governing_law.get_coordinates(governing_law.data['Governing Law'])

st.title('Analísis de leyes aplicables por zona geográfica')
st.map(coordinates)