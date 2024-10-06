import streamlit as st
import pandas as pd

from app import data
from services.providers_service import Providers

# Data
providers = Providers(data)
count = providers.count_parties()
best_ones = count.nlargest(10, 'Count')
most_popular = count[count['Count'] == count['Count'].max()]

# View
st.title('Analísis de proveedores')

st.write('Cantidad de veces que aparece cada proveedor en los contratos:')
st.dataframe(count, width=1000, height=500)

st.write('Top 10 proveedores más populares:')
st.bar_chart(best_ones, x='Party', y='Count', x_label='Proveedor', y_label='Cantidad de contratos')

