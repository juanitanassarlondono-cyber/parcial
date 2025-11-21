import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Panel de Análisis de Sensores Urbanos",
    page_icon="📡",
    layout="wide"
)

st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            font-size: 16px;
        }
        /* Título principal (streamlit renderiza h1 para st.title) */
        h1 {
            font-size: 34px !important;
            font-weight: 700 !important;
            color: #1A5276 !important;
            margin-bottom: 0.1rem;
        }
        /* Subtítulos comunes */
        h2, h3 {
            color: #154360 !important;
            font-weight: 600 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📡 Panel de Análisis de Sensores Urbanos")
st.markdown("""
    Esta herramienta le permite visualizar, analizar y filtrar datos generados por sensores
    instalados en diferentes puntos de la ciudad.  
    Suba un archivo CSV para comenzar el análisis.
""")

eafit_location = pd.DataFrame({
    'lat': [6.2006],
    'lon': [-75.5783],
    'location': ['Universidad EAFIT']
})

st.subheader("📍 Ubicación de los Sensores - Universidad EAFIT")
st.map(eafit_location, zoom=15)

uploaded_file = st.file_uploader('Seleccione archivo CSV', type=['csv'])

if uploaded_file is not None:
    try:
        df1 = pd.read_csv(uploaded_file)
        
        if 'Time' in df1.columns:
            other_columns = [col for col in df1.columns if col != 'Time']
            if len(other_columns) > 0:
                df1 = df1.rename(columns={other_columns[0]: 'variable'})
        else:
            df1 = df1.rename(columns={df1.columns[0]: 'variable'})
        
        if 'Time' in df1.columns:
            df1['Time'] = pd.to_datetime(df1['Time'])
            df1 = df1.set_index('Time')

        tab1, tab2, tab3, tab4 = st.tabs(["📈 Visualización", "📊 Estadísticas", "🔍 Filtros", "🗺️ Información del Sitio"])

        with tab1:
            st.subheader('Visualización de Datos')
            
            chart_type = st.selectbox(
                "Seleccione tipo de gráfico",
                ["Línea", "Área", "Barra"]
            )
            
            if chart_type == "Línea":
                st.line_chart(df1["variable"])
            elif chart_type == "Área":
                st.area_chart(df1["variable"])
            else:
                st.bar_chart(df1["variable"])

            if st.checkbox('Mostrar datos crudos'):
                st.write(df1)

        with tab2:
            st.subheader('Análisis Estadístico')
            
            stats_df = df1["variable"].describe()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.dataframe(stats_df)
            
            with col2:
                st.metric("Valor Promedio", f"{stats_df['mean']:.2f}")
                st.metric("Valor Máximo", f"{stats_df['max']:.2f}")
                st
::contentReference[oaicite:0]{index=0}
