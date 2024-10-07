import streamlit as st

from app import data
from services.effective_dates_service import EffectiveDates

# Data
effective_dates = EffectiveDates(data, ['Document Name', 'Effective Date'])
min_date, min_name = effective_dates.get_min_date_index('Effective Date')
max_date, max_name = effective_dates.get_max_date_index('Effective Date')

# View
st.title('Analísis de fechas efectivas')

st.write('Fechas efectivas de cada contrato:')
st.scatter_chart(effective_dates.data['Effective Date'], x_label='Index', y_label='Fecha efectiva')

col1, col2 = st.columns(2)
col1.write('Fecha efectiva más antigua:')
col1.subheader(f'{min_name}: {min_date}')
col2.write('Fecha efectiva más reciente:')
col2.subheader(f'{max_name}: {max_date}')

effective_dates.data['Effective Date'] = effective_dates.data['Effective Date'].dt.strftime('%d-%m-%Y')
st.subheader('Datos')
st.dataframe(effective_dates.data, width=1000, height=500)