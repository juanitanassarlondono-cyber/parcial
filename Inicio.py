import pandas as pd
import streamlit as st
from datetime import datetime

# Configuración general
st.set_page_config(
    page_title="Panel de Análisis de Sensores Urbanos",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Panel de Análisis de Sensores Urbanos")
st.markdown("Suba un archivo CSV para comenzar el análisis.")

# Ubicación EAFIT
eafit_location = pd.DataFrame({
    'lat': [6.2006],
    'lon': [-75.5783],
    'location': ['Universidad EAFIT']
})

st.subheader("📍 Ubicación del Sensor")
st.map(eafit_location, zoom=15)

# Cargar archivo
uploaded_file = st.file_uploader("Seleccione un archivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Procesar columna de tiempo
        if "Time" in df.columns:
            df["Time"] = pd.to_datetime(df["Time"])
            df = df.set_index("Time")

        # Asegurarse de tener una columna numérica
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

        if len(numeric_cols) == 0:
            st.error("El archivo debe contener al menos una columna numérica.")
            st.stop()

        # Usar la primera columna numérica automáticamente
        variable = numeric_cols[0]

        st.subheader(f"📈 Gráfico de la variable: {variable}")
        st.line_chart(df[variable])

        if st.checkbox("Mostrar datos crudos"):
            st.dataframe(df)

    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}")

else:
    st.warning("Por favor cargue un archivo CSV para comenzar.")

# Footer
st.markdown("---")
st.markdown("Desarrollado para el análisis de sensores urbanos – Universidad EAFIT.")
