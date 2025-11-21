import pandas as pd
import streamlit as st
import numpy as np
import altair as alt
from datetime import datetime

# ---------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------
st.set_page_config(
    page_title="Panel de Análisis de Sensores",
    page_icon="🔎",
    layout="wide"
)

# ---------------------------------------
# ESTILOS PERSONALIZADOS
# ---------------------------------------
st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

h1 {
    font-weight: 800;
}

h2 {
    font-weight: 700;
    margin-top: 20px;
    color: #2e2e2e;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

.section-title {
    font-size: 28px;
    font-weight: 900;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# TÍTULO PRINCIPAL
# ---------------------------------------
st.markdown("<h1>🔎 Panel de Análisis de Sensores Urbanos</h1>", unsafe_allow_html=True)
st.write("Explora, filtra y analiza datos provenientes de sensores instalados en la ciudad.")


# ---------------------------------------
# CARD: CARGA DE ARCHIVO
# ---------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2>📂 Cargar archivo CSV</h2>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Seleccione un archivo CSV", type=["csv"])
st.markdown("</div>", unsafe_allow_html=True)


# Si no hay archivo → detener
if uploaded_file is None:
    st.stop()


# ---------------------------------------
# PROCESAMIENTO DE ARCHIVO
# ---------------------------------------
try:
    df = pd.read_csv(uploaded_file)

    # Renombrar la variable automáticamente
    if "Time" in df.columns:
        others = [c for c in df.columns if c != "Time"]
        df = df.rename(columns={others[0]: "variable"})
        df["Time"] = pd.to_datetime(df["Time"])
        df = df.set_index("Time")
    else:
        df = df.rename(columns={df.columns[0]: "variable"})

except Exception as e:
    st.error(f"Error al leer el archivo: {str(e)}")
    st.stop()


# ---------------------------------------
# CARD: VISUALIZACIÓN
# ---------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2>📈 Visualización general</h2>", unsafe_allow_html=True)

chart_type = st.selectbox("Tipo de gráfico", ["Línea", "Área", "Barras"])

if chart_type == "Línea":
    st.line_chart(df["variable"])
elif chart_type == "Área":
    st.area_chart(df["variable"])
else:
    st.bar_chart(df["variable"])

if st.checkbox("Mostrar datos originales"):
    st.dataframe(df)

st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------
# CARD: ANÁLISIS ESTADÍSTICO
# ---------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2>📊 Estadísticas del Sensor</h2>", unsafe_allow_html=True)

stats = df["variable"].describe()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Promedio", f"{stats['mean']:.2f}")
c2.metric("Máximo", f"{stats['max']:.2f}")
c3.metric("Mínimo", f"{stats['min']:.2f}")
c4.metric("Desviación Std", f"{stats['std']:.2f}")

# Histograma
hist = alt.Chart(df.reset_index()).mark_bar().encode(
    x=alt.X("variable", bin=True, title="Valores"),
    y=alt.Y("count()", title="Frecuencia")
).properties(height=300)

st.altair_chart(hist, use_container_width=True)

# Boxplot
box = alt.Chart(df.reset_index()).mark_boxplot().encode(
    y="variable"
).properties(height=150)

st.altair_chart(box, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------
# CARD: FILTROS
# ---------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2>🔍 Filtros de datos</h2>", unsafe_allow_html=True)

min_val = float(df["variable"].min())
max_val = float(df["variable"].max())

colA, colB = st.columns(2)

with colA:
    min_filter = st.slider("Filtrar valores mayores a:", min_val, max_val, min_val)
    df_filtrado_min = df[df["variable"] > min_filter]
    st.write(df_filtrado_min)

with colB:
    max_filter = st.slider("Filtrar valores menores a:", min_val, max_val, max_val)
    df_filtrado_max = df[df["variable"] < max_filter]
    st.write(df_filtrado_max)

st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------
# CARD: INFORMACIÓN DEL SITIO (CON MAPA)
# ---------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2>🗺️ Información del sitio de medición</h2>", unsafe_allow_html=True)

loc_df = pd.DataFrame({
    "lat": [6.2006],
    "lon": [-75.5783],
    "site": ["Universidad EAFIT"]
})

col1, col2 = st.columns(2)

with col1:
    st.write("### 📍 Ubicación del sensor")
    st.write("**Universidad EAFIT**")
    st.write("- Latitud: 6.2006")
    st.write("- Longitud: -75.5783")
    st.write("- Altitud: ~1495 msnm")
    st.write("- Sensor: ESP32")

with col2:
    st.map(loc_df, zoom=15)

st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------
# FOOTER
# ---------------------------------------
st.write("---")
st.write("Desarrollado para análisis de sensores urbanos – Universidad EAFIT")

