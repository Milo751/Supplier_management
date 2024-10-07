import streamlit as st

from app import data
from services.effective_dates_service import EffectiveDates

# Data
agreement_dates = EffectiveDates(data, ['Document Name', 'Agreement Date'])
min_date, min_name = agreement_dates.get_min_date_index('Agreement Date')
max_date, max_name = agreement_dates.get_max_date_index('Agreement Date')

# View
st.title('Analísis de fechas donde se firmaron los contratos')

st.write('Fechas de acuerdo de cada contrato:')
st.scatter_chart(agreement_dates.data['Agreement Date'], x_label='Index', y_label='Fecha de acuerdo')

col1, col2 = st.columns(2)
col1.write('Fecha efectiva más antigua:')
col1.subheader(f'{min_name}: {min_date}')
col2.write('Fecha efectiva más reciente:')
col2.subheader(f'{max_name}: {max_date}')

agreement_dates.data['Agreement Date'] = agreement_dates.data['Agreement Date'].dt.strftime('%d-%m-%Y')
st.subheader('Datos')
st.dataframe(agreement_dates.data, width=1000, height=500)