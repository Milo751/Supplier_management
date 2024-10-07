import streamlit as st

from app import data
from services.effective_dates_service import EffectiveDates

# Data
effective_dates = EffectiveDates(data, ['Document Name', 'Effective Date'])

# View
st.title('Analísis de fechas efectivas')

st.write('Fechas efectivas de cada contrato:')
st.scatter_chart(effective_dates.data['Effective Date'], x_label='Index', y_label='Fecha efectiva')

effective_dates.data['Effective Date'] = effective_dates.data['Effective Date'].dt.strftime('%d-%m-%Y')
st.subheader('Datos')
st.dataframe(effective_dates.data, width=1000, height=500)