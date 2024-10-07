import streamlit as st

from app import data
from services.effective_dates_service import EffectiveDates

# Data
agreement_dates = EffectiveDates(data, ['Document Name', 'Agreement Date'])

# View
st.title('Analísis de fechas donde se firmaron los contratos')

st.write('Fechas de acuerdo de cada contrato:')
st.scatter_chart(agreement_dates.data['Agreement Date'], x_label='Index', y_label='Fecha de acuerdo')

agreement_dates.data['Agreement Date'] = agreement_dates.data['Agreement Date'].dt.strftime('%d-%m-%Y')
st.subheader('Datos')
st.dataframe(agreement_dates.data, width=1000, height=500)