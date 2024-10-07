import streamlit as st
from services.normalize import PreprocessData

# Data
preprocess = PreprocessData()
data = preprocess.preprocess_data()

pages = {
    "Inicio": [
        st.Page("modules/index.py", title="Gestión de proveedores", icon=":material/home:"),
    ],
    "Análisis de datos solicitados": [
        st.Page("modules/providers.py", title="Proveedores", icon=":material/groups:"),
        st.Page("modules/renewal_term.py", title="Plazo de renovación", icon=":material/replay:"),
        st.Page("modules/effective_dates.py", title="Fechas efectivas", icon=":material/event_available:"),
        st.Page("modules/governing_law.py", title="Ley aplicable", icon=":material/gavel:"),       
    ],
    "Análisis de datos extras": [
        st.Page("modules/extras/agreement_date.py", title="Fecha de acuerdo", icon=":material/event_note:"),
        st.Page("modules/extras/expiration_date.py", title="Fecha de terminación", icon=":material/event_busy:"),
        st.Page("modules/extras/notification_period.py", title="Periodo de notificación", icon=":material/notifications:"),
        st.Page("modules/extras/exclusivity.py", title="Exclusividad", icon=":material/lock:"),
    ],
}

pg = st.navigation(pages)
pg.run()