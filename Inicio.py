import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime

# ------------------------------------------
# CONFIGURACIÓN DE ESTILO
# ------------------------------------------

st.set_page_config(
    page_title="Panel de Análisis de Sensores",
    page_icon="📡",
    layout="wide"
)

# Estilos visuales simples (NO afectan la lógica)
st.markdown("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
        }
        .main {
            padding-top: 1.5rem;
        }
        h1 {
            color: #003566;
            font-weight: 800;
        }
        h2, h3 {
            color: #001D3D;
        }
        .stTabs [data-baseweb="tab-list"] button {
            font-weight: bold;
            font-size: 1.1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------
# TÍTULO PRINCIPAL
# ------------------------------------------

st.title("📡 Panel de Análisis de Sensores Urbanos")
st.markdown("### Observa, analiza y comprende el comportamiento de los sensores instalados en la ciudad.")

st.write("---")

# ------------------------------------------
# SECCIÓN DE ARCHIVO
# ------------------------------------------

uploaded_file = st.file_uploader("📂 **Cargar archivo CSV de datos**", type=['csv'])

# ------------------------------------------
# MAPA — Lo movimos de arriba a la sección final (como pediste)
# ------------------------------------------

eafit_location = pd.DataFrame({
    'lat': [6.2006],
    'lon': [-75.5783],
})


# ------------------------------------------
# LÓGICA PRINCIPAL
# ------------------------------------------

if uploaded_file is not None:
    try:
        df1 = pd.read_csv(uploaded_file)

        # Ajuste del nombre de la variable SIN alterar tu lógica
        if 'Time' in df1.columns:
            other_columns = [col for col in df1.columns if col != 'Time']
            if len(other_columns) > 0:
                df1 = df1.rename(columns={other_columns[0]: 'variable'})
        else:
            df1 = df1.rename(columns={df1.columns[0]: 'variable'})

        if 'Time' in df1.columns:
            df1['Time'] = pd.to_datetime(df1['Time'])
            df1 = df1.set_index('Time')

        # ------------------------------------------
        # TABS — Mantengo las 4 secciones originales
        # ------------------------------------------

        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Visualización",
            "📊 Estadísticas",
            "🎚 Filtros",
            "🗺️ Ubicación del Sensor"
        ])

        # ------------------------------------------
        # TAB 1 — VISUALIZACIÓN
        # ------------------------------------------
        with tab1:
            st.subheader("📈 Visualización de la Variable Registrada")

            chart_type = st.selectbox(
                "Selecciona el tipo de gráfico",
                ["Línea", "Área", "Barra"]
            )

            if chart_type == "Línea":
                st.line_chart(df1["variable"])
            elif chart_type == "Área":
                st.area_chart(df1["variable"])
            else:
                st.bar_chart(df1["variable"])

            if st.checkbox("Mostrar tabla de datos"):
                st.dataframe(df1)

        # ------------------------------------------
        # TAB 2 — ESTADÍSTICAS
        # ------------------------------------------
        with tab2:
            st.subheader("📊 Resumen Estadístico de los Datos")

            stats_df = df1["variable"].describe()

            col1, col2 = st.columns(2)
            col1.dataframe(stats_df)

            col2.metric("Promedio", f"{stats_df['mean']:.2f}")
            col2.metric("Máximo", f"{stats_df['max']:.2f}")
            col2.metric("Mínimo", f"{stats_df['min']:.2f}")
            col2.metric("Desviación Estándar", f"{stats_df['std']:.2f}")

        # ------------------------------------------
        # TAB 3 — FILTROS
        # ------------------------------------------
        with tab3:
            st.subheader("🎚 Filtros por Valor")

            min_value = float(df1["variable"].min())
            max_value = float(df1["variable"].max())
            mean_value = float(df1["variable"].mean())

            if min_value == max_value:
                st.warning(f"⚠ Los valores son todos iguales: {min_value:.2f}")
                st.dataframe(df1)
            else:
                col1, col2 = st.columns(2)

                with col1:
                    min_val = st.slider(
                        "Selecciona un valor mínimo",
                        min_value, max_value, mean_value
                    )
                    filtrado_min = df1[df1["variable"] > min_val]
                    st.dataframe(filtrado_min)

                with col2:
                    max_val = st.slider(
                        "Selecciona un valor máximo",
                        min_value, max_value, mean_value
                    )
                    filtrado_max = df1[df1["variable"] < max_val]
                    st.dataframe(filtrado_max)

                if st.button("Descargar datos filtrados (> mínimo)"):
                    csv = filtrado_min.to_csv().encode("utf-8")
                    st.download_button(
                        label="Descargar CSV filtrado",
                        data=csv,
                        file_name="datos_filtrados.csv",
                        mime="text/csv"
                    )

        # ------------------------------------------
        # TAB 4 — UBICACIÓN DEL SENSOR (Mapa movido aquí)
        # ------------------------------------------
        with tab4:
            st.subheader("🗺️ Ubicación del Sensor en la Ciudad")
            st.map(eafit_location, zoom=15)

            st.write("### 📍 Info del sitio")
            st.write("**Universidad EAFIT**")
            st.write("- Latitud: 6.2006")
            st.write("- Longitud: -75.5783")
            st.write("- Altitud: ~1495 msnm")
            st.write("- Sensor: ESP32 (variable configurable)")

    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}")
else:
    st.info("📂 Carga un archivo CSV para comenzar.")


# ------------------------------------------
# FOOTER
# ------------------------------------------
st.write("---")
st.caption("Desarrollado para análisis de datos urbanos • Universidad EAFIT")

