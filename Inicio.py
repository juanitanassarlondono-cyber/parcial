import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime
import plotly.express as px

# Configuración general
st.set_page_config(
    page_title="Panel de Análisis de Sensores Urbanos",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Panel de Análisis de Sensores Urbanos")
st.markdown("Suba un archivo CSV para comenzar el análisis.")

# Ubicación del mapa
eafit_location = pd.DataFrame({
    'lat': [6.2006],
    'lon': [-75.5783],
    'location': ['Universidad EAFIT']
})

st.subheader("📍 Ubicación de los Sensores - Universidad EAFIT")
st.map(eafit_location, zoom=15)

# Cargar archivo
uploaded_file = st.file_uploader("Seleccione un archivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df1 = pd.read_csv(uploaded_file)

        # Detectar columna de tiempo
        if "Time" in df1.columns:
            df1["Time"] = pd.to_datetime(df1["Time"])
            df1 = df1.set_index("Time")

        # Selección dinámica de columna
        columnas_numericas = df1.select_dtypes(include=["number"]).columns.tolist()

        if not columnas_numericas:
            st.error("No se encontraron columnas numéricas para graficar.")
            st.stop()

        variable = st.selectbox("Seleccione la variable a analizar", columnas_numericas)

        # Tabs principales
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Visualización",
            "📊 Estadísticas",
            "🔍 Filtros",
            "🛠️ Interactivo (Plotly)",
            "💡 Insights automáticos"
        ])

        # -------- TAB 1: VISUALIZACIÓN -------
        with tab1:
            st.subheader("Visualización básica")

            tipo = st.selectbox(
                "Tipo de gráfico",
                ["Línea", "Área", "Barras"]
            )

            if tipo == "Línea":
                st.line_chart(df1[variable])
            elif tipo == "Área":
                st.area_chart(df1[variable])
            else:
                st.bar_chart(df1[variable])

            if st.checkbox("Mostrar datos crudos"):
                st.dataframe(df1)

        # -------- TAB 2: ESTADÍSTICAS -------
        with tab2:
            st.subheader("Análisis Estadístico")

            stats_df = df1[variable].describe()
            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(stats_df)

            with col2:
                st.metric("Promedio", f"{stats_df['mean']:.2f}")
                st.metric("Máximo", f"{stats_df['max']:.2f}")
                st.metric("Mínimo", f"{stats_df['min']:.2f}")
                st.metric("Desviación Estándar", f"{stats_df['std']:.2f}")

        # -------- TAB 3: FILTROS -------
        with tab3:
            st.subheader("Filtros de Datos")

            if "Time" in df1.index.names:
                # Rango de fechas dinámico
                fecha_min = df1.index.min()
                fecha_max = df1.index.max()

                rango_fechas = st.slider(
                    "Rango de fechas",
                    min_value=fecha_min,
                    max_value=fecha_max,
                    value=(fecha_min, fecha_max)
                )

                df_filtro_fecha = df1.loc[rango_fechas[0]:rango_fechas[1]]
            else:
                df_filtro_fecha = df1

            # Filtros por valor
            min_val = float(df_filtro_fecha[variable].min())
            max_val = float(df_filtro_fecha[variable].max())

            val_min, val_max = st.slider(
                "Rango de valores",
                min_val, 
                max_val, 
                (min_val, max_val)
            )

            df_filtrado = df_filtro_fecha[
                (df_filtro_fecha[variable] >= val_min) &
                (df_filtro_fecha[variable] <= val_max)
            ]

            st.write("Datos filtrados:")
            st.dataframe(df_filtrado)

            # Descargar datos filtrados
            csv = df_filtrado.to_csv().encode("utf-8")
            st.download_button(
                "Descargar CSV filtrado",
                csv,
                "datos_filtrados.csv",
                "text/csv"
            )

        # -------- TAB 4: PLOTLY INTERACTIVO -------
        with tab4:
            st.subheader("Gráfico interactivo (zoom, hover, pan)")

            fig = px.line(
                df1.reset_index(),
                x=df1.reset_index().columns[0] if "Time" in df1.index.names else df1.index,
                y=variable,
                title=f"Serie temporal de {variable}"
            )
            st.plotly_chart(fig, use_container_width=True)

        # -------- TAB 5: INSIGHTS AUTOMÁTICOS -------
        with tab5:
            st.subheader("Insights automáticos del dataset")

            avg = df1[variable].mean()
            maxi = df1[variable].max()
            mini = df1[variable].min()
            std = df1[variable].std()

            st.write(f"- El valor promedio es *{avg:.2f}*.")
            st.write(f"- El valor máximo observado es *{maxi:.2f}*.")
            st.write(f"- El valor mínimo registrado es *{mini:.2f}*.")
            st.write(f"- La variabilidad (desviación estándar) es *{std:.2f}*.")

            if std < 0.1 * avg:
                st.info("La señal es bastante estable y con poca variabilidad.")
            else:
                st.info("La señal presenta variaciones considerables a lo largo del tiempo.")

    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}")
else:
    st.warning("Por favor cargue un archivo CSV para comenzar el análisis.")

# Footer
st.markdown("---")
st.markdown("Desarrollado para el análisis de sensores urbanos – Universidad EAFIT.")
