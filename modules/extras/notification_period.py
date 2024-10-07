import streamlit as st

from app import data
from services.renewal_term_service import RenewalTerm

# Data
notification_period = RenewalTerm(data, ['Document Name', 'Notification Renewal (days)'])
count = notification_period.count_group_by('Notification Renewal (days)')
diagram_data = count[(count['Notification Renewal (days)'] != 0) & (count['Notification Renewal (days)'] != 9999)]
diagram_colors = notification_period.generate_color(diagram_data)

# View
st.title('Analísis de plazos de renovación')

st.write('Cantidad de contratos por plazo de renovación:')
col1, col2 = st.columns(2)
col1.dataframe(count)
col2.subheader('Definiciones:')
col2.write('Cuando los días de renovación son 0, significa que no estaba correctamente especificado o no se logro identificar en los documentos.')

st.write('Basado en los datos anteriores, se excluyeron los contratos perpetuos y los que no tenían un plazo de renovación especificado.')
st.bar_chart(diagram_colors, x='Count', y='Notification Renewal (days)', color='Color', x_label='Cantidad de contratos', y_label='Plazo de renovación (días)')