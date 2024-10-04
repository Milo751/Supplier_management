import streamlit as st
import pandas as pd

from app import data
from utils.dates_manage import DateManage, DateInsights

st.set_page_config(
    page_title='Analísis de fechas efectivas de contratos',
    page_icon=":memo:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('Analísis de fechas efectivas de contratos')

df = data[['Document Name-Answer', 'Effective Date-Answer']]
contract_column = 'Document Name-Answer'
date_column = 'Effective Date-Answer'

date_manage = DateManage(df)
df_normalized = date_manage.column_to_date(date_column)

st.write('Fechas efectivas de cada contrato:')
st.scatter_chart(df_normalized[date_column], x_label='Index', y_label='Fecha efectiva', )

date_insights = DateInsights(df_normalized)
min_date, min_document = date_insights.get_min_date_index(date_column)
max_date, mean_document = date_insights.get_max_date_index(date_column)

col1, col2 = st.columns(2)
col1.metric(label=f'Fecha efectiva más antigua\n' ,value=min_date, help=f'Contrato: {min_document}')
col2.metric(label='Fecha efectiva más reciente' ,value=max_date, help=f'Contrato: {mean_document}')

df_decorated = date_manage.df_to_string(df_normalized, date_column)
st.subheader('Datos')
st.dataframe(df_decorated)