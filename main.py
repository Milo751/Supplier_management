import streamlit as st
import pandas as pd

data = pd.read_csv('data/master_clauses.csv')

pages = {
    "Inicio": [
        st.Page("modules/index.py", title="Gestión de proveedores", icon=":material/home:"),
    ],
    "Insights predefinidos": [
        st.Page("modules/providers.py", title="Proveedores", icon=":material/groups:"),
        st.Page("modules/renewal_term.py", title="Plazo de renovación", icon=":material/replay:"),
        st.Page("modules/effective_dates.py", title="Fechas efectivas", icon=":material/event_available:"),
        st.Page("modules/governing_law.py", title="Ley aplicable", icon=":material/gavel:"),       
    ]
}

pg = st.navigation(pages)
pg.run()