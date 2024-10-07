import streamlit as st

from app import data
from services.effective_dates_service import EffectiveDates

# Data
expiration_dates = EffectiveDates(data, ['Document Name', 'Expiration Date'])

# View
st.title('Analísis de fechas de expiración')

st.write('Fechas de expiración de cada contrato:')
st.scatter_chart(expiration_dates.data['Expiration Date'], x_label='Index', y_label='Fecha de expiración')

expiration_dates.data['Expiration Date'] = expiration_dates.data['Expiration Date'].dt.strftime('%d-%m-%Y')
st.subheader('Datos')
st.dataframe(expiration_dates.data, width=1000, height=500)