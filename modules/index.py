import streamlit as st
import pandas as pd

from app import data

st.title('Gestión de proveedores')

st.write('Esta es la base actual de contratos con sus respectivos datos y proveedores asociados:')
st.dataframe(data.head())

st.write('Columnas disponibles:')
column_names_df = pd.DataFrame(data.columns, columns=['Columnas'])
st.table(column_names_df)