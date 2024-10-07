import streamlit as st

from app import data
from services.effective_dates_service import EffectiveDates

# Data
expiration_dates = EffectiveDates(data, ['Document Name', 'Expiration Date'])
min_date, min_name = expiration_dates.get_min_date_index('Expiration Date')
max_date, max_name = expiration_dates.get_max_date_index('Expiration Date')

# View
st.title('Analísis de fechas de expiración')

st.write('Fechas de expiración de cada contrato:')
st.scatter_chart(expiration_dates.data['Expiration Date'], x_label='Index', y_label='Fecha de expiración')
col1, col2 = st.columns(2)
col1.write('Fecha efectiva más antigua:')
col1.subheader(f'{min_name}: {min_date}')
col2.write('Fecha efectiva más reciente:')
col2.subheader(f'{max_name}: {max_date}')

expiration_dates.data['Expiration Date'] = expiration_dates.data['Expiration Date'].dt.strftime('%d-%m-%Y')
st.subheader('Datos')
st.dataframe(expiration_dates.data, width=1000, height=500)