import pandas as pd
import streamlit as st
import time

# Ruta del archivo CSV
CSV_PATH = "D:/OneDrive - CELSIA S.A E.S.P/BICC/IncidentesActual.csv"

# Función para cargar datos con manejo de errores
def cargar_datos():
    try:
        df = pd.read_csv(CSV_PATH, encoding="utf-16", sep=",")
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return pd.DataFrame()

# Cargar los datos
df = cargar_datos()

# Función para actualizar cada 30 minutos
def refrescar_dashboard():
    while True:
        time.sleep(1800)  # 30 minutos en segundos
        st.experimental_rerun()

# Llamar la función de actualización en segundo plano
refrescar_dashboard()

# Mostrar título
st.title("📊 Dashboard de Incidentes Eléctricos")
st.markdown("Actualizado automáticamente cada 30 minutos.")

# Verificar si hay datos
if df.empty:
    st.warning("No hay datos disponibles para mostrar.")
else:
    # Agrupación por zona
    st.header("🔹 Total de incidentes por zona")
    incidentes_zona = df.groupby("SubregionName").size().reset_index(name="Cantidad de Incidentes")
    incidentes_zona = incidentes_zona.sort_values(by="Cantidad de Incidentes", ascending=False)
    st.dataframe(incidentes_zona)
    st.bar_chart(incidentes_zona.set_index("SubregionName"))

    # Separar por origen
    df_llamadas = df[df["Origen"] == "PhoneCallCreated"]
    df_eventos = df[df["Origen"] != "PhoneCallCreated"]

    # Mostrar cantidad de incidentes por zona
    st.header("🔹 Incidentes por zona (según origen)")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📞 Por llamadas (PhoneCallCreated)")
        incidentes_llamadas = df_llamadas.groupby("SubregionName").size().reset_index(name="Cantidad de Incidentes")
        incidentes_llamadas = incidentes_llamadas.sort_values(by="Cantidad de Incidentes", ascending=False)
        st.dataframe(incidentes_llamadas)
        st.bar_chart(incidentes_llamadas.set_index("SubregionName"))

    with col2:
        st.subheader("⚙️ Por eventos de campo / operador")
        incidentes_eventos = df_eventos.groupby("SubregionName").size().reset_index(name="Cantidad de Incidentes")
        incidentes_eventos = incidentes_eventos.sort_values(by="Cantidad de Incidentes", ascending=False)
        st.dataframe(incidentes_eventos)
        st.bar_chart(incidentes_eventos.set_index("SubregionName"))

    # Sumar clientes sin servicio por zona
    st.header("🔹 Clientes sin servicio por zona")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📞 Por llamadas (PhoneCallCreated)")
        llamadas = df_llamadas.groupby("SubregionName")["NumUnrestCustomers"].sum().reset_index()
        llamadas = llamadas.rename(columns={"NumUnrestCustomers": "Clientes sin servicio"})
        llamadas = llamadas.sort_values(by="Clientes sin servicio", ascending=False)
        st.dataframe(llamadas)

    with col2:
        st.subheader("⚙️ Por eventos de campo / operador")
        eventos = df_eventos.groupby("SubregionName")["NumUnrestCustomers"].sum().reset_index()
        eventos = eventos.rename(columns={"NumUnrestCustomers": "Clientes sin servicio"})
        eventos = eventos.sort_values(by="Clientes sin servicio", ascending=False)
        st.dataframe(eventos)
