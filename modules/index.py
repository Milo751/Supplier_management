import streamlit as st

from app import data

# View
st.title('Gestión de proveedores')

st.write('Esta es la base normalizada de contratos con sus respectivos datos y proveedores asociados:')
st.dataframe(data, width=1000, height=500)