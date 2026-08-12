
"""
🏠 Dashboard de Gestion de Alquileres Vacacionales
==================================================
Demo multi-propiedad (7 pisos) para Booking.com y Airbnb.
Datos simulados. Preparado para conectar APIs en el futuro.

Autor: Desarrollador Senior Python
Stack: Streamlit + Plotly + Pandas
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
import random

# ============================================================
# CONFIGURACION GLOBAL
# ============================================================
st.set_page_config(
    page_title="VacationRent Pro - Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PALETA DE COLORES CORPORATIVA (PREMIUM)
# ============================================================
COLORS = {
    "airbnb": "#FF5A5F",
    "booking": "#003580",
    "primary": "#1E3A5F",
    "secondary": "#4A90A4",
    "accent": "#F4A261",
    "success": "#2A9D8F",
    "danger": "#E76F51",
    "warning": "#E9C46A",
    "bg_card": "#F8F9FA",
    "text": "#2D3436",
    "light": "#FFFFFF",
    "muted": "#636E72"
}

# ============================================================
# ESTILOS CSS PERSONALIZADOS (PREMIUM)
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }

    .subtitle {
        font-size: 0.95rem;
        color: #636E72;
        margin-bottom: 1.5rem;
    }

    .kpi-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
        border-radius: 16px;
        padding: 1.2rem;
        border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0 4px 20px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
    }

    .kpi-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #636E72;
        margin-bottom: 0.4rem;
    }

    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0.2rem;
    }

    .kpi-delta-positive {
        color: #2A9D8F;
        font-weight: 600;
        font-size: 0.85rem;
    }

    .kpi-delta-negative {
        color: #E76F51;
        font-weight: 600;
        font-size: 0.85rem;
    }

    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1E3A5F;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #F4A261;
        display: inline-block;
    }

    .badge-airbnb {
        background-color: #FF5A5F;
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .badge-booking {
        background-color: #003580;
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .status-pendiente {
        color: #E76F51;
        font-weight: 600;
    }

    .status-completada {
        color: #2A9D8F;
        font-weight: 600;
    }

    .rating-bar-bg {
        background-color: #ECEFF1;
        border-radius: 10px;
        height: 10px;
        width: 100%;
    }

    .rating-bar-fill {
        height: 10px;
        border-radius: 10px;
        background: linear-gradient(90deg, #F4A261, #E76F51);
    }

    .footer-text {
        text-align: center;
        color: #636E72;
        font-size: 0.8rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #ECEFF1;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# GENERADOR DE DATOS SIMULADOS (MOCK DATA)
# ============================================================
@st.cache_data(ttl=3600)
def generar_datos_simulados():
    """
    Genera un conjunto completo de datos simulados para la demo.
    Estructura preparada para futura conexion con APIs reales.
    """

    random.seed(42)

    # --- CONFIGURACION DE PROPIEDADES ---
    pisos = [
        {"id": "P01", "nombre": "Atico Centro", "capacidad": 4, "precio_base": 120},
        {"id": "P02", "nombre": "Loft Playa", "capacidad": 2, "precio_base": 95},
        {"id": "P03", "nombre": "Suite Gran Via", "capacidad": 3, "precio_base": 135},
        {"id": "P04", "nombre": "Penthouse Sky", "capacidad": 6, "precio_base": 210},
        {"id": "P05", "nombre": "Estudio Bohemio", "capacidad": 2, "precio_base": 75},
        {"id": "P06", "nombre": "Duplex Familiar", "capacidad": 5, "precio_base": 160},
        {"id": "P07", "nombre": "Loft Industrial", "capacidad": 3, "precio_base": 110},
    ]

    nombres_huespedes = [
        "Maria Garcia", "John Smith", "Sophie Dubois", "Hans Muller", "Laura Rossi",
        "Chen Wei", "Ana Lopez", "Robert Johnson", "Emma Wilson", "Carlos Ruiz",
        "Yuki Tanaka", "Isabella Ferreira", "David Cohen", "Fatima Al-Rashid",
        "Thomas Andersen", "Nina Petrova", "James OBrien", "Sofia Andersson",
        "Lucas Martins", "Elena Kowalski", "Ahmed Hassan", "Clara Schmidt"
    ]

    canales = ["Airbnb", "Booking"]

    # Fecha de referencia: hoy (como pd.Timestamp para compatibilidad)
    hoy = pd.Timestamp(date.today())

    # --- 1. GENERAR RESERVAS (DataFrame principal) ---
    reservas_list = []

    for piso in pisos:
        # Generar entre 4 y 8 reservas por piso
        num_reservas = random.randint(4, 8)

        for _ in range(num_reservas):
            # Fecha de inicio aleatoria en un rango de -90 a +60 dias
            offset_dias = random.randint(-90, 60)
            inicio = hoy + timedelta(days=offset_dias)

            # Duracion de 2 a 7 noches
            duracion = random.randint(2, 7)
            fin = inicio + timedelta(days=duracion)

            # Precio con variacion segun temporada y canal
            factor_temporada = 1.0 + (0.3 if inicio.month in [6, 7, 8] else 0.0)
            canal = random.choice(canales)
            factor_canal = 1.05 if canal == "Airbnb" else 1.0
            precio_noche = piso["precio_base"] * factor_temporada * factor_canal * random.uniform(0.9, 1.15)
            precio_total = round(precio_noche * duracion, 2)

            reservas_list.append({
                "Piso": piso["nombre"],
                "Piso_ID": piso["id"],
                "Inicio": inicio,
                "Fin": fin,
                "Huesped": random.choice(nombres_huespedes),
                "Canal": canal,
                "Precio": precio_total,
                "Noches": duracion,
                "Precio_Noche": round(precio_noche, 2),
                "Estado": "Confirmada" if inicio.date() >= hoy.date() else "Completada",
                "Capacidad": piso["capacidad"]
            })

    df_reservas = pd.DataFrame(reservas_list)
    # CRITICO: convertir a datetime64 para poder usar .dt accessor
    df_reservas["Inicio"] = pd.to_datetime(df_reservas["Inicio"])
    df_reservas["Fin"] = pd.to_datetime(df_reservas["Fin"])

    # --- 2. DATOS DE RENDIMIENTO POR PISO (MTD) ---
    rendimiento_list = []
    for piso in pisos:
        ocupacion = random.randint(55, 92)
        adr = round(piso["precio_base"] * random.uniform(0.95, 1.25), 2)
        ingresos = round(adr * ocupacion / 100 * 30, 2)

        rendimiento_list.append({
            "Piso": piso["nombre"],
            "Ocupacion_%": ocupacion,
            "ADR_EUR": adr,
            "Ingresos_Mes_EUR": ingresos,
            "Reservas_Mes": random.randint(8, 22),
            "Noches_Vendidas": random.randint(18, 26)
        })

    df_rendimiento = pd.DataFrame(rendimiento_list)

    # --- 3. INGRESOS HISTORICOS (ultimos 6 meses) ---
    meses_historicos = []
    for i in range(5, -1, -1):
        mes_ref = hoy.replace(day=1) - pd.DateOffset(months=i)
        mes_nombre = mes_ref.strftime("%b %Y")

        factor_mes = 1.0 + (0.4 if mes_ref.month in [6, 7, 8] else 0.0)

        ing_airbnb = round(random.uniform(2800, 4200) * factor_mes, 2)
        ing_booking = round(random.uniform(2200, 3800) * factor_mes, 2)

        meses_historicos.append({
            "Mes": mes_nombre,
            "Airbnb": ing_airbnb,
            "Booking": ing_booking,
            "Total": ing_airbnb + ing_booking
        })

    df_ingresos = pd.DataFrame(meses_historicos)

    # --- 4. CHECK-INS / CHECK-OUTS DE HOY ---
    checkins_hoy = []
    checkouts_hoy = []

    for piso in pisos:
        if random.random() < 0.3:
            checkins_hoy.append({
                "Piso": piso["nombre"],
                "Huesped": random.choice(nombres_huespedes),
                "Canal": random.choice(canales),
                "Limpieza": random.choice(["Pendiente", "Completada"]),
                "Hora_Estimada": "{:02d}:00".format(random.randint(14, 18))
            })

        if random.random() < 0.3:
            checkouts_hoy.append({
                "Piso": piso["nombre"],
                "Huesped": random.choice(nombres_huespedes),
                "Canal": random.choice(canales),
                "Limpieza": random.choice(["Pendiente", "Completada"]),
                "Hora_Estimada": "{:02d}:00".format(random.randint(10, 12))
            })

    df_checkins = pd.DataFrame(checkins_hoy)
    df_checkouts = pd.DataFrame(checkouts_hoy)

    # --- 5. RATINGS / REPUTACION ---
    ratings_list = []
    for piso in pisos:
        rating_airbnb = round(random.uniform(4.2, 5.0), 1)
        rating_booking = round(random.uniform(8.0, 9.8), 1)
        num_reviews_airbnb = random.randint(12, 85)
        num_reviews_booking = random.randint(8, 65)

        ratings_list.append({
            "Piso": piso["nombre"],
            "Airbnb_Rating": rating_airbnb,
            "Airbnb_Reviews": num_reviews_airbnb,
            "Booking_Rating": rating_booking,
            "Booking_Reviews": num_reviews_booking,
            "Media_Ponderada": round(
                (rating_airbnb * num_reviews_airbnb + (rating_booking/2) * num_reviews_booking) 
                / (num_reviews_airbnb + num_reviews_booking), 2
            )
        })

    df_ratings = pd.DataFrame(ratings_list)

    return {
        "reservas": df_reservas,
        "rendimiento": df_rendimiento,
        "ingresos": df_ingresos,
        "checkins": df_checkins,
        "checkouts": df_checkouts,
        "ratings": df_ratings,
        "pisos": pisos,
        "hoy": hoy
    }


# ============================================================
# CARGAR DATOS
# ============================================================
datos = generar_datos_simulados()
df_reservas = datos["reservas"]
df_rendimiento = datos["rendimiento"]
df_ingresos = datos["ingresos"]
df_checkins = datos["checkins"]
df_checkouts = datos["checkouts"]
df_ratings = datos["ratings"]
pisos = datos["pisos"]
hoy = datos["hoy"]

# ============================================================
# HEADER PRINCIPAL
# ============================================================
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    st.markdown('<p class="main-title">🏠 VacationRent Pro</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Dashboard de Gestion Multi-Propiedad • ' + hoy.strftime("%d de %B de %Y") + '</p>', unsafe_allow_html=True)

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("📍 **" + str(len(pisos)) + " propiedades** activas")

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.success("🟢 **" + str(len(df_reservas[df_reservas["Estado"] == "Confirmada"])) + "** reservas futuras")

st.divider()

# ============================================================
# PESTANAS PRINCIPALES
# ============================================================
tab_a, tab_b, tab_c, tab_d = st.tabs([
    "📊 Vista General (KPIs)",
    "📅 Calendario de Reservas",
    "⚙️ Rendimiento Operativo",
    "⭐ Calidad y Reputacion"
])

# ============================================================
# PESTANA A: VISTA GENERAL (KPIs FINANCIEROS)
# ============================================================
with tab_a:
    st.markdown('<p class="section-header">Indicadores Clave de Rendimiento (KPIs)</p>', unsafe_allow_html=True)

    # Calcular KPIs del mes actual
    mes_actual = hoy.month
    año_actual = hoy.year

    reservas_mes = df_reservas[
        (df_reservas["Inicio"].dt.month == mes_actual) & 
        (df_reservas["Inicio"].dt.year == año_actual)
    ]

    ingresos_mes = reservas_mes["Precio"].sum()

    # Simular mes anterior para deltas
    mes_ant_ingresos = ingresos_mes * random.uniform(0.82, 1.18)
    delta_ingresos = ((ingresos_mes - mes_ant_ingresos) / mes_ant_ingresos * 100)

    # Ocupacion global (simulada)
    ocupacion_global = round(df_rendimiento["Ocupacion_%"].mean(), 1)
    ocupacion_ant = ocupacion_global + random.uniform(-8, 8)
    delta_ocupacion = round(ocupacion_global - ocupacion_ant, 1)

    # ADR medio
    adr_medio = round(df_rendimiento["ADR_EUR"].mean(), 2)
    adr_ant = adr_medio * random.uniform(0.92, 1.08)
    delta_adr = ((adr_medio - adr_ant) / adr_ant * 100)

    # Beneficio neto (estimado 65% de margen)
    beneficio_neto = round(ingresos_mes * 0.65, 2)
    beneficio_ant = beneficio_neto * random.uniform(0.80, 1.20)
    delta_beneficio = ((beneficio_neto - beneficio_ant) / beneficio_ant * 100)

    # --- KPI CARDS ---
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    def kpi_card_html(label, value, delta, is_pp=False):
        delta_class = "kpi-delta-positive" if delta >= 0 else "kpi-delta-negative"
        arrow = "▲" if delta >= 0 else "▼"
        suffix = "pp" if is_pp else "%"
        return f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="{delta_class}">{arrow} {abs(delta):.1f}{suffix} vs mes anterior</div>
        </div>
        """

    with kpi1:
        st.markdown(kpi_card_html("💰 Ingresos del Mes", f"EUR {ingresos_mes:,.0f}", delta_ingresos), unsafe_allow_html=True)

    with kpi2:
        st.markdown(kpi_card_html("📈 Tasa de Ocupacion", f"{ocupacion_global}%", delta_ocupacion, is_pp=True), unsafe_allow_html=True)

    with kpi3:
        st.markdown(kpi_card_html("🏷️ ADR Medio", f"EUR {adr_medio:.0f}", delta_adr), unsafe_allow_html=True)

    with kpi4:
        st.markdown(kpi_card_html("💵 Beneficio Neto Est.", f"EUR {beneficio_neto:,.0f}", delta_beneficio), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- GRAFICO DE INGRESOS (Ultimos 6 meses) ---
    st.markdown('<p class="section-header">Evolucion de Ingresos por Canal (Ultimos 6 Meses)</p>', unsafe_allow_html=True)

    fig_ingresos = go.Figure()

    fig_ingresos.add_trace(go.Bar(
        name="Airbnb",
        x=df_ingresos["Mes"],
        y=df_ingresos["Airbnb"],
        marker_color=COLORS["airbnb"],
        text=[f"EUR {v:,.0f}" for v in df_ingresos["Airbnb"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Airbnb: EUR %{y:,.0f}<extra></extra>"
    ))

    fig_ingresos.add_trace(go.Bar(
        name="Booking.com",
        x=df_ingresos["Mes"],
        y=df_ingresos["Booking"],
        marker_color=COLORS["booking"],
        text=[f"EUR {v:,.0f}" for v in df_ingresos["Booking"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Booking: EUR %{y:,.0f}<extra></extra>"
    ))

    fig_ingresos.add_trace(go.Scatter(
        name="Total",
        x=df_ingresos["Mes"],
        y=df_ingresos["Total"],
        mode="lines+markers+text",
        line=dict(color=COLORS["accent"], width=3),
        marker=dict(size=10, color=COLORS["accent"]),
        text=[f"EUR {v:,.0f}" for v in df_ingresos["Total"]],
        textposition="top center",
        textfont=dict(size=11, color=COLORS["primary"]),
        hovertemplate="<b>%{x}</b><br>Total: EUR %{y:,.0f}<extra></extra>"
    ))

    fig_ingresos.update_layout(
        barmode="group",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color=COLORS["text"]),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,0.8)"
        ),
        margin=dict(l=20, r=20, t=80, b=40),
        xaxis=dict(showgrid=False, title=""),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.05)", title="Ingresos (EUR)", tickformat=",.0f"),
        height=450,
        hovermode="x unified"
    )

    st.plotly_chart(fig_ingresos, use_container_width=True)

    # --- DISTRIBUCION POR CANAL (Pie Chart) ---
    col_pie1, col_pie2 = st.columns(2)

    with col_pie1:
        st.markdown('<p class="section-header">Distribucion de Reservas por Canal</p>', unsafe_allow_html=True)

        canal_counts = df_reservas["Canal"].value_counts().reset_index()
        canal_counts.columns = ["Canal", "Reservas"]

        fig_pie = px.pie(
            canal_counts,
            names="Canal",
            values="Reservas",
            color="Canal",
            color_discrete_map={"Airbnb": COLORS["airbnb"], "Booking": COLORS["booking"]},
            hole=0.55
        )

        fig_pie.update_traces(
            textinfo="percent+label",
            textfont_size=13,
            hovertemplate="<b>%{label}</b><br>Reservas: %{value}<br>Porcentaje: %{percent}<extra></extra>"
        )

        fig_pie.update_layout(
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=20, b=20),
            height=350,
            annotations=[dict(text="Canales", x=0.5, y=0.5, font_size=16, showarrow=False, font_color=COLORS["muted"])]
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    with col_pie2:
        st.markdown('<p class="section-header">Ocupacion por Propiedad</p>', unsafe_allow_html=True)

        fig_ocup = px.bar(
            df_rendimiento.sort_values("Ocupacion_%", ascending=True),
            x="Ocupacion_%",
            y="Piso",
            orientation="h",
            color="Ocupacion_%",
            color_continuous_scale=[COLORS["danger"], COLORS["warning"], COLORS["success"]],
            text="Ocupacion_%",
            range_x=[0, 100]
        )

        fig_ocup.update_traces(
            texttemplate="%{text}%",
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Ocupacion: %{x}%<extra></extra>"
        )

        fig_ocup.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", size=12),
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.05)", title="Ocupacion (%)"),
            yaxis=dict(title=""),
            coloraxis_showscale=False,
            height=350
        )

        st.plotly_chart(fig_ocup, use_container_width=True)


# ============================================================
# PESTANA B: CALENDARIO DE RESERVAS (GANTT / TIMELINE)
# ============================================================
with tab_b:
    st.markdown('<p class="section-header">Calendario de Reservas — Vista Gantt</p>', unsafe_allow_html=True)

    # Selector de mes para el calendario
    col_cal1, col_cal2, col_cal3 = st.columns([1, 1, 2])

    with col_cal1:
        meses_opciones = []
        for i in range(-1, 4):
            mes_ref = hoy.replace(day=1) + pd.DateOffset(months=i)
            meses_opciones.append(mes_ref.strftime("%B %Y"))

        mes_seleccionado = st.selectbox("📅 Seleccionar mes:", meses_opciones, index=1)

    with col_cal2:
        vista_opcion = st.selectbox("👁️ Vista:", ["Todas las reservas", "Solo Airbnb", "Solo Booking"], index=0)

    # Parsear mes seleccionado
    mes_sel_dt = pd.to_datetime(mes_seleccionado, format="%B %Y")
    mes_sel_num = mes_sel_dt.month
    año_sel_num = mes_sel_dt.year

    # Filtrar reservas del mes seleccionado
    df_cal = df_reservas[
        (df_reservas["Inicio"].dt.month == mes_sel_num) & 
        (df_reservas["Inicio"].dt.year == año_sel_num)
    ].copy()

    # Aplicar filtro de canal si es necesario
    if vista_opcion == "Solo Airbnb":
        df_cal = df_cal[df_cal["Canal"] == "Airbnb"]
    elif vista_opcion == "Solo Booking":
        df_cal = df_cal[df_cal["Canal"] == "Booking"]

    # Asegurar que cada piso aparezca en el eje Y
    nombres_pisos = [p["nombre"] for p in pisos]

    # Preparar datos para Plotly Timeline
    if len(df_cal) > 0:
        df_cal["Color_Canal"] = df_cal["Canal"].map({
            "Airbnb": COLORS["airbnb"],
            "Booking": COLORS["booking"]
        })

        fig_gantt = px.timeline(
            df_cal,
            x_start="Inicio",
            x_end="Fin",
            y="Piso",
            color="Canal",
            color_discrete_map={"Airbnb": COLORS["airbnb"], "Booking": COLORS["booking"]},
            hover_name="Huesped",
            hover_data={
                "Piso": False,
                "Inicio": True,
                "Fin": True,
                "Canal": True,
                "Precio": True,
                "Noches": True,
                "Huesped": False
            },
            category_orders={"Piso": list(reversed(nombres_pisos))},
            height=500
        )

        # Personalizar hover
        fig_gantt.update_traces(
            hovertemplate=(
                "<b>%{hovertext}</b><br>" +
                "📅 %{customdata[1]} → %{customdata[2]}<br>" +
                "🏠 %{y}<br>" +
                "📢 %{customdata[3]}<br>" +
                "💰 EUR %{customdata[4]:,.0f}<br>" +
                "🌙 %{customdata[5]} noches<extra></extra>"
            ),
            marker_line_color="white",
            marker_line_width=2,
            opacity=0.9
        )

        # Configurar ejes y layout
        fig_gantt.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", size=12, color=COLORS["text"]),
            xaxis=dict(
                title="",
                showgrid=True,
                gridcolor="rgba(0,0,0,0.05)",
                dtick="D1",
                tickformat="%d %b",
                tickangle=-45
            ),
            yaxis=dict(
                title="",
                showgrid=True,
                gridcolor="rgba(0,0,0,0.05)",
                categoryorder="array",
                categoryarray=list(reversed(nombres_pisos))
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor="rgba(255,255,255,0.8)"
            ),
            margin=dict(l=150, r=20, t=80, b=80),
            hovermode="closest"
        )

        # Anadir linea vertical para "hoy" si el mes seleccionado es el actual
        if mes_sel_num == hoy.month and año_sel_num == hoy.year:
            fig_gantt.add_vline(
                x=hoy,
                line_width=2,
                line_dash="dash",
                line_color=COLORS["accent"],
                annotation_text="Hoy",
                annotation_position="top",
                annotation_font_color=COLORS["accent"],
                annotation_font_size=12
            )

        st.plotly_chart(fig_gantt, use_container_width=True)

        # Tabla resumen de reservas del mes
        st.markdown('<p class="section-header">Reservas del Mes Seleccionado</p>', unsafe_allow_html=True)

        df_cal_display = df_cal[["Piso", "Inicio", "Fin", "Huesped", "Canal", "Noches", "Precio"]].copy()
        df_cal_display["Inicio"] = df_cal_display["Inicio"].dt.strftime("%d/%m/%Y")
        df_cal_display["Fin"] = df_cal_display["Fin"].dt.strftime("%d/%m/%Y")
        df_cal_display["Precio"] = df_cal_display["Precio"].apply(lambda x: f"EUR {x:,.0f}")

        st.dataframe(
            df_cal_display.sort_values("Inicio"),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Piso": st.column_config.TextColumn("🏠 Propiedad", width="medium"),
                "Inicio": st.column_config.TextColumn("📅 Entrada", width="small"),
                "Fin": st.column_config.TextColumn("📅 Salida", width="small"),
                "Huesped": st.column_config.TextColumn("👤 Huesped", width="medium"),
                "Canal": st.column_config.TextColumn("📢 Canal", width="small"),
                "Noches": st.column_config.NumberColumn("🌙 Noches", width="small"),
                "Precio": st.column_config.TextColumn("💰 Total", width="small")
            }
        )
    else:
        st.info("📭 No hay reservas registradas para **" + mes_seleccionado + "** con el filtro seleccionado.")

    # --- Leyenda de colores y guia ---
    st.markdown("""
    <div style="display: flex; gap: 20px; margin-top: 1rem; padding: 1rem; background: #F8F9FA; border-radius: 12px;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <div style="width: 20px; height: 20px; background: #FF5A5F; border-radius: 4px;"></div>
            <span style="font-size: 0.9rem; color: #2D3436;">Airbnb</span>
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
            <div style="width: 20px; height: 20px; background: #003580; border-radius: 4px;"></div>
            <span style="font-size: 0.9rem; color: #2D3436;">Booking.com</span>
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
            <div style="width: 20px; height: 2px; background: #F4A261; border: 1px dashed #F4A261;"></div>
            <span style="font-size: 0.9rem; color: #2D3436;">Fecha actual (hoy)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# PESTANA C: RENDIMIENTO Y CONTROL OPERATIVO
# ============================================================
with tab_c:
    st.markdown('<p class="section-header">Rendimiento por Propiedad (Mes Actual)</p>', unsafe_allow_html=True)

    # --- TABLA DE RENDIMIENTO ESTILIZADA ---
    df_rend_display = df_rendimiento.copy()
    df_rend_display["Ocupacion_%"] = df_rend_display["Ocupacion_%"].astype(str) + "%"
    df_rend_display["ADR_EUR"] = df_rend_display["ADR_EUR"].apply(lambda x: f"EUR {x:.0f}")
    df_rend_display["Ingresos_Mes_EUR"] = df_rend_display["Ingresos_Mes_EUR"].apply(lambda x: f"EUR {x:,.0f}")

    # Aplicar estilos condicionales con Pandas Styler (usando .map para pandas >= 2.1)
    def color_ocupacion_safe(val):
        try:
            num = float(str(val).replace("%", "").replace("EUR ", "").replace(",", ""))
            if num >= 80:
                return "background-color: #d4edda; color: #155724; font-weight: 600;"
            elif num >= 60:
                return "background-color: #fff3cd; color: #856404; font-weight: 600;"
            else:
                return "background-color: #f8d7da; color: #721c24; font-weight: 600;"
        except:
            return ""

    styled_rend = df_rend_display.style.map(
        color_ocupacion_safe, subset=["Ocupacion_%"]
    ).set_properties(**{
        "text-align": "center",
        "font-size": "0.95rem"
    }).set_table_styles([
        {"selector": "th", "props": [
            ("background-color", "#1E3A5F"),
            ("color", "white"),
            ("font-weight", "600"),
            ("padding", "12px"),
            ("text-align", "center")
        ]},
        {"selector": "td", "props": [
            ("padding", "10px 12px"),
            ("border-bottom", "1px solid #ECEFF1")
        ]},
        {"selector": "tr:hover", "props": [
            ("background-color", "#F8F9FA")
        ]}
    ])

    st.write(styled_rend.to_html(), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- CHECK-INS Y CHECK-OUTS DE HOY ---
    col_check1, col_check2 = st.columns(2)

    def render_check_card(row):
        estado_color = "status-completada" if row["Limpieza"] == "Completada" else "status-pendiente"
        estado_icon = "✅" if row["Limpieza"] == "Completada" else "⏳"
        canal_badge = "badge-airbnb" if row["Canal"] == "Airbnb" else "badge-booking"
        return f"""
        <div style="background: white; border-radius: 12px; padding: 1rem; margin-bottom: 0.8rem; 
                    border: 1px solid #ECEFF1; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-weight: 600; font-size: 1rem; color: #1E3A5F;">{row["Piso"]}</span>
                <span class="{canal_badge}">{row["Canal"]}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #636E72; font-size: 0.9rem;">👤 {row["Huesped"]}</span>
                <span style="color: #636E72; font-size: 0.85rem;">🕐 {row["Hora_Estimada"]}</span>
            </div>
            <div style="margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid #F0F0F0;">
                <span class="{estado_color}">{estado_icon} Limpieza: {row["Limpieza"]}</span>
            </div>
        </div>
        """

    with col_check1:
        st.markdown('<p class="section-header">🛬 Check-ins de Hoy</p>', unsafe_allow_html=True)

        if len(df_checkins) > 0:
            for idx, row in df_checkins.iterrows():
                st.markdown(render_check_card(row), unsafe_allow_html=True)
        else:
            st.info("No hay check-ins programados para hoy.")

    with col_check2:
        st.markdown('<p class="section-header">🛫 Check-outs de Hoy</p>', unsafe_allow_html=True)

        if len(df_checkouts) > 0:
            for idx, row in df_checkouts.iterrows():
                st.markdown(render_check_card(row), unsafe_allow_html=True)
        else:
            st.info("No hay check-outs programados para hoy.")

    # --- GRAFICO DE ADR vs OCUPACION (Scatter) ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-header">Analisis ADR vs Ocupacion por Propiedad</p>', unsafe_allow_html=True)

    fig_scatter = px.scatter(
        df_rendimiento,
        x="Ocupacion_%",
        y="ADR_EUR",
        size="Ingresos_Mes_EUR",
        color="Piso",
        text="Piso",
        size_max=50,
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    fig_scatter.update_traces(
        textposition="top center",
        textfont=dict(size=10),
        hovertemplate="<b>%{text}</b><br>Ocupacion: %{x}%<br>ADR: EUR %{y:.0f}<br>Ingresos: EUR %{marker.size:,.0f}<extra></extra>"
    )

    fig_scatter.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12),
        xaxis=dict(title="Ocupacion (%)", showgrid=True, gridcolor="rgba(0,0,0,0.05)", range=[40, 100]),
        yaxis=dict(title="ADR (EUR)", showgrid=True, gridcolor="rgba(0,0,0,0.05)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=80, b=40),
        height=450
    )

    # Anadir cuadrantes
    fig_scatter.add_hline(y=df_rendimiento["ADR_EUR"].mean(), line_dash="dot", line_color="gray", opacity=0.5)
    fig_scatter.add_vline(x=df_rendimiento["Ocupacion_%"].mean(), line_dash="dot", line_color="gray", opacity=0.5)

    st.plotly_chart(fig_scatter, use_container_width=True)


# ============================================================
# PESTANA D: CALIDAD Y REPUTACION
# ============================================================
with tab_d:
    st.markdown('<p class="section-header">Puntuaciones y Reputacion Online</p>', unsafe_allow_html=True)

    # --- RATINGS POR PROPIEDAD ---
    for idx, row in df_ratings.iterrows():
        col_r1, col_r2, col_r3, col_r4 = st.columns([2, 2, 2, 3])

        with col_r1:
            st.markdown("<h4 style='color: #1E3A5F; margin-bottom: 0.2rem;'>" + row["Piso"] + "</h4>", unsafe_allow_html=True)

        with col_r2:
            # Airbnb rating
            pct_airbnb = (row["Airbnb_Rating"] / 5.0) * 100
            st.markdown("""
            <div style="margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.2rem;">
                    <span style="font-size: 0.85rem; font-weight: 600; color: #FF5A5F;">🏠 Airbnb</span>
                    <span style="font-size: 0.9rem; font-weight: 700;">""" + str(row["Airbnb_Rating"]) + """/5.0</span>
                </div>
                <div class="rating-bar-bg">
                    <div class="rating-bar-fill" style="width: """ + str(pct_airbnb) + """%;"></div>
                </div>
                <span style="font-size: 0.75rem; color: #636E72;">""" + str(row["Airbnb_Reviews"]) + """ reseñas</span>
            </div>
            """, unsafe_allow_html=True)

        with col_r3:
            # Booking rating
            pct_booking = (row["Booking_Rating"] / 10.0) * 100
            st.markdown("""
            <div style="margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.2rem;">
                    <span style="font-size: 0.85rem; font-weight: 600; color: #003580;">📘 Booking</span>
                    <span style="font-size: 0.9rem; font-weight: 700;">""" + str(row["Booking_Rating"]) + """/10</span>
                </div>
                <div class="rating-bar-bg">
                    <div class="rating-bar-fill" style="width: """ + str(pct_booking) + """%;"></div>
                </div>
                <span style="font-size: 0.75rem; color: #636E72;">""" + str(row["Booking_Reviews"]) + """ reseñas</span>
            </div>
            """, unsafe_allow_html=True)

        with col_r4:
            # Media ponderada visual
            media = row["Media_Ponderada"]
            color_media = "#2A9D8F" if media >= 4.5 else "#E9C46A" if media >= 4.0 else "#E76F51"
            st.markdown("""
            <div style="text-align: center; padding: 0.5rem; background: #F8F9FA; border-radius: 12px;">
                <div style="font-size: 0.75rem; color: #636E72; text-transform: uppercase; letter-spacing: 1px;">Media Ponderada</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: """ + color_media + """;">""" + str(media) + """</div>
                <div style="font-size: 0.75rem; color: #636E72;">de 5.0</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

    # --- GRAFICO COMPARATIVO DE RATINGS ---
    st.markdown('<p class="section-header">Comparativa de Ratings por Propiedad</p>', unsafe_allow_html=True)

    fig_ratings = go.Figure()

    fig_ratings.add_trace(go.Bar(
        name="Airbnb (escala /5)",
        x=df_ratings["Piso"],
        y=df_ratings["Airbnb_Rating"],
        marker_color=COLORS["airbnb"],
        text=df_ratings["Airbnb_Rating"],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Airbnb: %{y}/5.0<extra></extra>"
    ))

    fig_ratings.add_trace(go.Bar(
        name="Booking (escala /10 → /5)",
        x=df_ratings["Piso"],
        y=df_ratings["Booking_Rating"] / 2,
        marker_color=COLORS["booking"],
        text=df_ratings["Booking_Rating"],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Booking: %{customdata}/10<extra></extra>",
        customdata=df_ratings["Booking_Rating"]
    ))

    fig_ratings.add_trace(go.Scatter(
        name="Media Ponderada",
        x=df_ratings["Piso"],
        y=df_ratings["Media_Ponderada"],
        mode="lines+markers+text",
        line=dict(color=COLORS["accent"], width=3, dash="dot"),
        marker=dict(size=12, symbol="diamond", color=COLORS["accent"]),
        text=df_ratings["Media_Ponderada"],
        textposition="top center",
        textfont=dict(size=11, color=COLORS["primary"]),
        hovertemplate="<b>%{x}</b><br>Media: %{y}<extra></extra>"
    ))

    fig_ratings.update_layout(
        barmode="group",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor="rgba(255,255,255,0.8)"),
        xaxis=dict(title="", showgrid=False, tickangle=-30),
        yaxis=dict(title="Puntuacion (escala /5)", showgrid=True, gridcolor="rgba(0,0,0,0.05)", range=[0, 5.5]),
        margin=dict(l=20, r=20, t=80, b=80),
        height=450,
        hovermode="x unified"
    )

    st.plotly_chart(fig_ratings, use_container_width=True)

    # --- RESUMEN DE REPUTACION GLOBAL ---
    col_rep1, col_rep2, col_rep3 = st.columns(3)

    with col_rep1:
        avg_airbnb = round(df_ratings["Airbnb_Rating"].mean(), 2)
        st.metric("⭐ Rating Medio Airbnb", f"{avg_airbnb}/5.0", "+" + str(round(random.uniform(0.05, 0.15), 2)))

    with col_rep2:
        avg_booking = round(df_ratings["Booking_Rating"].mean(), 2)
        st.metric("📘 Rating Medio Booking", f"{avg_booking}/10", "+" + str(round(random.uniform(0.1, 0.3), 2)))

    with col_rep3:
        total_reviews = df_ratings["Airbnb_Reviews"].sum() + df_ratings["Booking_Reviews"].sum()
        st.metric("📝 Total Reseñas", f"{total_reviews}", "+" + str(random.randint(5, 15)) + " este mes")


# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="footer-text">
    🏠 <b>VacationRent Pro</b> — Dashboard de Gestion Multi-Propiedad<br>
    Version Demo 1.0 • Datos simulados para fines de demostracion<br>
    <span style="color: #B2BEC3;">Preparado para integracion con APIs de Airbnb y Booking.com</span>
</div>
""", unsafe_allow_html=True)
