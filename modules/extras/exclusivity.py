import streamlit as st

from app import data
from services.renewal_term_service import RenewalTerm

# Data
exclusivity = RenewalTerm(data, ['Document Name', 'Exclusivity'])
count = exclusivity.count_group_by('Exclusivity')

# View
st.title('Analísis de exclusividad')

st.write('Exclusividad de los contratos:')
st.dataframe(exclusivity.data, width=1000, height=500)

st.write('Cantidad de contratos por exclusividad:')
col1, col2 = st.columns(2)
col1.metric(label='Exclusividad', value=count.loc[count['Exclusivity'] == 'Yes', 'Count'].values[0],delta='+ Yes')
col2.metric(label='No Exclusividad', value=count.loc[count['Exclusivity'] == 'No', 'Count'].values[0], delta='- No')

st.bar_chart(count, x='Exclusivity', y='Count', x_label='Exclusividad', y_label='Cantidad de contratos')