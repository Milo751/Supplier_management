import streamlit as st

from app import data
from services.effective_dates_service import EffectiveDates, DateInsights
from utils.standardize_data import DateType

# Data
effective_dates = EffectiveDates(data)

date_insights = DateInsights(effective_dates.data)
min_date, min_document = date_insights.get_min_date_index()
max_date, mean_document = date_insights.get_max_date_index()

# View
st.title('Analísis de fechas efectivas')

st.write('Fechas efectivas de cada contrato:')
st.scatter_chart(effective_dates.data['Effective Date'], x_label='Index', y_label='Fecha efectiva')

col1, col2 = st.columns(2)
col1.metric(label=f'Fecha efectiva más antigua\n' ,value=min_date, help=f'Contrato: {min_document}')
col2.metric(label='Fecha efectiva más reciente' ,value=max_date, help=f'Contrato: {mean_document}')

df_decorated = DateType.df_to_string(effective_dates.data, 'Effective Date')
st.subheader('Datos')
st.dataframe(df_decorated, width=1000, height=500)