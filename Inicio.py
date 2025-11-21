import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Panel de Análisis de Sensores Urbanos",
    page_icon="📡",
    layout="wide"
)

# Custom CSS (solo tipografía y títulos)
st.markdown("""
    <style>

    /* Tipografía general */
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        font-size: 17px;
    }

    /* Título principal */
    .main-title {
        font-size: 38px !important;
        font-weight: 700 !important;
        color: #1A5276;
        text-align: center;
        margin-bottom: 5px;
    }

    /* Subtítulos */
    h2, .stMarkdown h2, .stSubheader {
        color: #154360 !important;
        font-weight: 600 !important;
    }

    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<p class="main-title">📡 Panel de Análisis de Sensores Urbanos</p>', unsafe_allow_html=True)

st.markdown("""
    Esta herramienta le permite visualizar, analizar y filtrar datos generados por sensores
    instalados en diferentes puntos de la ciudad.  
    Suba un archivo CSV para comenzar el análisis.
""")

# Create map data for EAFIT
eafit_location = pd.DataFrame({
    'lat': [6.2006],
    'lon': [-75.5783],
    'location': ['Universidad EAFIT']
})

# Display map
st.subheader("📍 Ubicación del Sensor – Universidad EAFIT")
st.map(eafit_location, zoom=15)

# File uploader
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
                st.metric("Valor Mínimo", f"{stats_df['min']:.2f}")
                st.metric("Desviación Estándar", f"{stats_df['std']:.2f}")

        with tab3:
            st.subheader('Filtros de Datos')
            
            min_value = float(df1["variable"].min())
            max_value = float(df1["variable"].max())
            mean_value = float(df1["variable"].mean())
            
            if min_value == max_value:
                st.warning(f"⚠️ Todos los valores en el dataset son iguales: {min_value:.2f}")
                st.info("No es posible aplicar filtros cuando no hay variación en los datos.")
                st.dataframe(df1)
            else:
                col1, col2 = st.columns(2)
                
                with col1:
                    min_val = st.slider(
                        'Valor mínimo',
                        min_value,
                        max_value,
                        mean_value,
                        key="min_val"
                    )
                    filtrado_df_min = df1[df1["variable"] > min_val]
                    st.write(f"Registros con valor superior a {min_val:.2f}:")
                    st.dataframe(filtrado_df_min)
                    
                with col2:
                    max_val = st.slider(
                        'Valor máximo',
                        min_value,
                        max_value,
                        mean_value,
                        key="max_val"
                    )
                    filtrado_df_max = df1[df1["variable"] < max_val]
                    st.write(f"Registros con valor inferior a {max_val:.2f}:")
                    st.dataframe(filtrado_df_max)

                if st.button('Descargar datos filtrados'):
                    csv = filtrado_df_min.to_csv().encode('utf-8')
                    st.download_button(
                        label="Descargar CSV",
                        data=csv,
                        file_name='datos_filtrados.csv',
                        mime='text/csv',
                    )

        with tab4:
            st.subheader("Información del Sitio de Medición")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("### Ubicación del Sensor")
                st.write("**Universidad EAFIT**")
                st.write("- Latitud: 6.2006")
                st.write("- Longitud: -75.5783")
                st.write("- Altitud: ~1,495 metros sobre el nivel del mar")
            
            with col2:
                st.write("### Detalles del Sensor")
                st.write("- Tipo: ESP32")
                st.write("- Variable medida: Según configuración del sensor")
                st.write("- Frecuencia de medición: Según configuración")
                st.write("- Ubicación: Campus universitario")

    except Exception as e:
        st.error(f'Error al procesar el archivo: {str(e)}')
        st.info('Asegúrese de que el archivo CSV tenga al menos una columna con datos.')
else:
    st.warning('Por favor, cargue un archivo CSV para comenzar el análisis.')
    
# Footer
st.markdown("""
    ---
    Desarrollado para el análisis de datos de sensores urbanos.
    Ubicación: Universidad EAFIT, Medellín, Colombia
""")
