import streamlit as st

from app import data
from services.renewal_term_service import RenewalTerm

# Data
renewal_term = RenewalTerm(data, ['Document Name', 'Renewal Term (days)'])
count = renewal_term.count_group_by('Renewal Term (days)')
diagram_data = count[(count['Renewal Term (days)'] != 0) & (count['Renewal Term (days)'] != 9999)]
diagram_colors = renewal_term.generate_color(diagram_data)

# View
st.title('Analísis de plazos de renovación')

st.write('Cantidad de contratos por plazo de renovación:')
col1, col2 = st.columns(2)
col1.dataframe(count)
col2.subheader('Definiciones:')
col2.write('Cuando los días de renovación son 9999, significa que el contrato es perpetuo.')
col2.divider()
col2.write('Cuando los días de renovación son 0, significa que no estaba correctamente especificado o no se logro identificar en los documentos.')

st.write('Basado en los datos anteriores, se excluyeron los contratos perpetuos y los que no tenían un plazo de renovación especificado.')
st.bar_chart(diagram_colors, x='Count', y='Renewal Term (days)', color='Color', x_label='Cantidad de contratos', y_label='Plazo de renovación (días)')

col1, col2 = st.columns(2)
col1.metric(label='Plazo máximo de días para renovación', value=int(diagram_data['Renewal Term (days)'].max()))
col2.metric(label='Plazo mínimo de días para renovación', value=int(diagram_data['Renewal Term (days)'].min()))
