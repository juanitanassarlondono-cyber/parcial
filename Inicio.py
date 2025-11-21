import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Panel de Análisis de Sensores Urbanos",
    page_icon="📡",
    layout="wide"
)

# Título principal
st.title("📡 Panel de Análisis de Sensores Urbanos")
st.markdown("Suba un archivo CSV para comenzar el análisis.")

# Ubicación del mapa (Universidad EAFIT)
eafit_location = pd.DataFrame({
    'lat': [6.2006],
    'lon': [-75.5783],
    'location': ['Universidad EAFIT']
})

st.subheader("📍 Ubicación de los Sensores - Universidad EAFIT")
st.map(eafit_location, zoom=15)

# Carga del archivo
uploaded_file = st.file_uploader('Seleccione un archivo CSV', type=['csv'])

if uploaded_file is not None:
    try:
        df1 = pd.read_csv(uploaded_file)

        # Alinear nombres de columnas
        if 'Time' in df1.columns:
            other_columns = [col for col in df1.columns if col != 'Time']
            if other_columns:
                df1 = df1.rename(columns={other_columns[0]: 'variable'})
        else:
            df1 = df1.rename(columns={df1.columns[0]: 'variable'})

        # Procesar columna Time si existe
        if 'Time' in df1.columns:
            df1['Time'] = pd.to_datetime(df1['Time'])
            df1 = df1.set_index('Time')

        # Tabs principales
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Visualización",
            "📊 Estadísticas",
            "🔍 Filtros",
            "🗺️ Información del Sitio"
        ])

        # -------- TAB 1: VISUALIZACIÓN ----------
        with tab1:
            st.subheader("Visualización de Datos")

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

            if st.checkbox("Mostrar datos crudos"):
                st.dataframe(df1)

        # -------- TAB 2: ESTADÍSTICAS ----------
        with tab2:
            st.subheader("Análisis Estadístico")

            stats_df = df1["variable"].describe()

            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(stats_df)

            with col2:
                st.metric("Promedio", f"{stats_df['mean']:.2f}")
                st.metric("Máximo", f"{stats_df['max']:.2f}")
                st.metric("Mínimo", f"{stats_df['min']:.2f}")
                st.metric("Desviación Estándar", f"{stats_df['std']:.2f}")

        # -------- TAB 3: FILTROS ----------
        with tab3:
            st.subheader("Filtros de Datos")

            min_value = float(df1["variable"].min())
            max_value = float(df1["variable"].max())
            mean_value = float(df1["variable"].mean())

            if min_value == max_value:
                st.warning(f"⚠️ Todos los valores del dataset son iguales: {min_value:.2f}")
                st.info("No es posible aplicar filtros sin variación en los datos.")
                st.dataframe(df1)
            else:
                col1, col2 = st.columns(2)

                with col1:
                    min_val = st.slider(
                        "Valor mínimo",
                        min_value, max_value, mean_value,
                        key="min_val"
                    )

                    filtrado_min = df1[df1["variable"] > min_val]
                    st.write(f"Registros con valores superiores a {min_val:.2f}:")
                    st.dataframe(filtrado_min)

                with col2:
                    max_val = st.slider(
                        "Valor máximo",
                        min_value, max_value, mean_value,
                        key="max_val"
                    )

                    filtrado_max = df1[df1["variable"] < max_val]
                    st.write(f"Registros con valores inferiores a {max_val:.2f}:")
                    st.dataframe(filtrado_max)

                if st.button("Descargar datos filtrados"):
                    csv = filtrado_min.to_csv().encode("utf-8")
                    st.download_button(
                        "Descargar CSV",
                        csv,
                        "datos_filtrados.csv",
                        "text/csv"
                    )

        # -------- TAB 4: INFORMACIÓN DEL SITIO ----------
        with tab4:
            st.subheader("Información del Sitio de Medición")

            col1, col2 = st.columns(2)

            with col1:
                st.write("*📍 Ubicación del Sensor*")
                st.write("Universidad EAFIT")
                st.write(f"Latitud: {eafit_location['lat'][0]}")
                st.write(f"Longitud: {eafit_location['lon'][0]}")
                st.write("Altitud aproximada: 1495 msnm")
                st.write("Tipo de sensor: ESP32")

            with col2:
                st.map(eafit_location, zoom=15)

    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}")
        st.info("Verifique que el archivo incluye al menos una columna válida.")

else:
    st.warning("Por favor cargue un archivo CSV para comenzar el análisis.")

# Footer
st.markdown("---")
st.markdown("Desarrollado para el análisis de sensores urbanos – Universidad EAFIT, Medellín.")
