import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Dashboard Multi-Propiedad", page_icon="🏢", layout="wide")

# --- GENERACIÓN DE DATOS SIMULADOS (MOCK DATA) ---
pisos = ["Ático Centro", "Loft Playa", "Estudio Universidad", "Villa Sur", "Dúplex Norte", "Bajo Jardín", "Penthouse Lujo"]
canales = ["Airbnb", "Booking.com"]

# Datos de rendimiento por piso
data_pisos = pd.DataFrame({
    "Piso": pisos,
    "Ocupación (%)": np.random.randint(65, 98, size=7),
    "ADR (€)": np.random.randint(80, 250, size=7),
    "Ingresos MTD (€)": np.random.randint(1500, 6000, size=7),
    "Canal Principal": np.random.choice(canales, size=7),
    "Nota Airbnb": np.round(np.random.uniform(4.5, 5.0), 1),
    "Nota Booking": np.round(np.random.uniform(8.5, 10.0), 1)
})

# Datos para el calendario de reservas (Gantt)
hoy = datetime.now()
reservas = []
for piso in pisos:
    fecha_actual = hoy - timedelta(days=5) # Empezamos hace 5 días
    for _ in range(4): # 4 reservas por piso aprox para la demo
        inicio = fecha_actual + timedelta(days=np.random.randint(1, 4)) # huecos libres
        estancia = np.random.randint(2, 7)
        fin = inicio + timedelta(days=estancia)
        canal = np.random.choice(canales)
        precio = estancia * np.random.randint(80, 200)
        
        reservas.append({
            "Piso": piso,
            "Inicio": inicio,
            "Fin": fin,
            "Huésped": f"Huésped {np.random.randint(100,999)}",
            "Canal": canal,
            "Precio Total (€)": precio
        })
        fecha_actual = fin

df_reservas = pd.DataFrame(reservas)

# --- CABECERA ---
st.title("🏢 Dashboard de Gestión - Alquileres Vacacionales")
st.markdown("Visión global de los 7 apartamentos (Booking & Airbnb)")
st.divider()

# --- PESTAÑAS (TABS) ---
tab1, tab2, tab3, tab4 = st.tabs(["📈 Vista General", "🗓️ Calendario (Gantt)", "📊 Operativa y Rendimiento", "⭐ Calidad y Reputación"])

# --- TAB 1: VISTA GENERAL ---
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    
    # KPIs Superiores
    ingresos_totales = data_pisos["Ingresos MTD (€)"].sum()
    ocupacion_media = data_pisos["Ocupación (%)"].mean()
    adr_medio = data_pisos["ADR (€)"].mean()
    
    col1.metric("Ingresos Mes (MTD)", f"{ingresos_totales:,.0f} €", "+12% vs mes anterior")
    col2.metric("Ocupación Global", f"{ocupacion_media:.1f} %", "Óptimo", delta_color="normal")
    col3.metric("ADR Medio", f"{adr_medio:.0f} €", "-2% vs mes anterior", delta_color="inverse")
    col4.metric("Beneficio Neto (Est.)", f"{ingresos_totales * 0.65:,.0f} €", "Margen 65%")
    
    st.write("---")
    
    # Gráfico de ingresos mensuales simulados
    st.subheader("Evolución de Ingresos por Canal (Últimos 6 meses)")
    meses = ["Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto"]
    datos_grafico = pd.DataFrame({
        "Mes": meses * 2,
        "Canal": ["Airbnb"]*6 + ["Booking.com"]*6,
        "Ingresos": np.random.randint(8000, 20000, size=12)
    })
    fig_barras = px.bar(datos_grafico, x="Mes", y="Ingresos", color="Canal", barmode="group",
                        color_discrete_map={"Airbnb": "#FF5A5F", "Booking.com": "#003580"})
    st.plotly_chart(fig_barras, use_container_width=True)


# --- TAB 2: CALENDARIO (GANTT) ---
with tab2:
    st.subheader("Calendario de Ocupación a 30 días")
    st.markdown("Visualiza las reservas y los **huecos libres** entre estancias.")
    
    # Gráfico Timeline (Gantt)
    fig_gantt = px.timeline(
        df_reservas, 
        x_start="Inicio", 
        x_end="Fin", 
        y="Piso",
        color="Canal",
        hover_name="Huésped",
        hover_data=["Precio Total (€)"],
        color_discrete_map={"Airbnb": "#FF5A5F", "Booking.com": "#003580"}
    )
    # Ordenar eje Y y quitar leyenda redundante si se quiere
    fig_gantt.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig_gantt, use_container_width=True)


# --- TAB 3: OPERATIVA Y RENDIMIENTO ---
with tab3:
    col_izq, col_der = st.columns([2, 1])
    
    with col_izq:
        st.subheader("Rendimiento por Propiedad")
        st.dataframe(
            data_pisos[["Piso", "Ocupación (%)", "ADR (€)", "Ingresos MTD (€)", "Canal Principal"]],
            use_container_width=True,
            hide_index=True
        )
        
    with col_der:
        st.subheader("Operativa de HOY")
        st.info(f"📅 Fecha actual: {hoy.strftime('%d/%m/%Y')}")
        
        st.markdown("**Check-ins previstos:**")
        st.success("🟢 Ático Centro - 15:00h (Airbnb)")
        st.success("🟢 Villa Sur - 16:30h (Booking)")
        
        st.markdown("**Check-outs y Limpiezas:**")
        st.warning("🟠 Loft Playa - Salida 11:00h (Limpieza Pendiente)")
        st.error("🔴 Bajo Jardín - Salida 12:00h (Retraso huésped)")


# --- TAB 4: CALIDAD ---
with tab4:
    st.subheader("Puntuaciones y Reseñas")
    st.markdown("Mantener las puntuaciones altas es vital para el algoritmo de las plataformas.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Airbnb (Sobre 5.0)")
        for idx, row in data_pisos.iterrows():
            st.metric(row['Piso'], f"⭐ {row['Nota Airbnb']}")
    with col2:
        st.markdown("### Booking.com (Sobre 10.0)")
        for idx, row in data_pisos.iterrows():
            st.metric(row['Piso'], f"💙 {row['Nota Booking']}")
