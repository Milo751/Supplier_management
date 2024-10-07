import streamlit as st

from services.model_service import Model
from app import data
from services.providers_service import Providers
from services.effective_dates_service import EffectiveDates
from services.renewal_term_service import RenewalTerm

# Data
providers = Providers(data)
count = providers.count_parties()
most_popular = count[count['Count'] == count['Count'].max()]

effective_dates = EffectiveDates(data, ['Document Name', 'Effective Date'])
min_date, min_name = effective_dates.get_min_date_index('Effective Date')
max_date, max_name = effective_dates.get_max_date_index('Effective Date')

renewal_term = RenewalTerm(data, ['Document Name', 'Renewal Term (days)'])
count = renewal_term.count_group_by('Renewal Term (days)')
count_filtered = count[(count['Renewal Term (days)'] != 0) & (count['Renewal Term (days)'] != 9999)]
shortest = int(count_filtered['Renewal Term (days)'].min())
longest = int(count_filtered['Renewal Term (days)'].max())

analitics = {
    'best_p': (most_popular["Party"].values[0], most_popular["Count"].values[0]),
    'old_eff_d': (min_date, min_name),
    'new_eff_d': (max_date, max_name),
    'short_rt': shortest,
    'long_rt': longest
}

model = Model(analitics)

# View
st.title('Consulta con modelo de lenguaje')
st.write('Este módulo permite consultar datos resaltados en el análisis del dataset.')

subheaders = [
    'Proveedor más popular:', 
    'Fecha efectiva más antigua:', 
    'Fecha efectiva más reciente:', 
    'Plazo de renovación más corto:', 
    'Plazo de renovación más extenso:'
    ]
questions = [
    '¿Quién es el proveedor más popular?', 
    '¿Cuál es la fecha efectiva más antigua?', 
    '¿Cuál es la fecha efectiva más reciente?', 
    '¿Cuál es el plazo de renovación más corto?', 
    '¿Cuál es el plazo de renovación más extenso?'
    ]

if st.button('Preguntar'):
    for subheader, question in zip(subheaders, questions):
        st.divider()
        with st.container():
            st.subheader(subheader)
            st.write(model.ask_question(question))
else:
    for subheader in subheaders:
        st.divider()
        with st.container():
            st.subheader(subheader)
