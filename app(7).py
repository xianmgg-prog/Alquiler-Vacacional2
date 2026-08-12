
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ============================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================
st.set_page_config(
    page_title="RentMaster Pro | Dashboard de Alquileres",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# TEMA PERSONALIZADO PREMIUM (CSS)
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        color: #e2e8f0;
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(145deg, rgba(30,41,59,0.9), rgba(15,23,42,0.95));
        border: 1px solid rgba(148,163,184,0.1);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
        border-color: rgba(148,163,184,0.2);
    }
    .kpi-title {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .kpi-value {
        color: #f8fafc;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .kpi-delta-positive {
        color: #34d399;
        font-size: 0.9rem;
        font-weight: 600;
    }
    .kpi-delta-negative {
        color: #f87171;
        font-size: 0.9rem;
        font-weight: 600;
    }

    /* Section Headers */
    .section-header {
        color: #f8fafc;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 32px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(56,189,248,0.3);
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Badges */
    .badge-pendiente {
        background: rgba(251,191,36,0.15);
        color: #fbbf24;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid rgba(251,191,36,0.3);
    }
    .badge-completada {
        background: rgba(52,211,153,0.15);
        color: #34d399;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid rgba(52,211,153,0.3);
    }
    .badge-checkin {
        background: rgba(56,189,248,0.15);
        color: #38bdf8;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid rgba(56,189,248,0.3);
    }
    .badge-checkout {
        background: rgba(248,113,113,0.15);
        color: #f87171;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid rgba(248,113,113,0.3);
    }

    /* Table styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }

    /* Progress bars */
    .progress-container {
        background: rgba(30,41,59,0.8);
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
        margin-top: 4px;
    }
    .progress-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }

    /* Calendar cells */
    .cal-cell {
        text-align: center;
        padding: 8px 4px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 500;
        min-width: 40px;
    }
    .cal-occupied {
        background: rgba(248,113,113,0.2);
        color: #f87171;
        border: 1px solid rgba(248,113,113,0.3);
    }
    .cal-free {
        background: rgba(52,211,153,0.2);
        color: #34d399;
        border: 1px solid rgba(52,211,153,0.3);
    }
    .cal-header {
        color: #94a3b8;
        font-size: 0.7rem;
        text-transform: uppercase;
        font-weight: 600;
    }

    /* Gauge container */
    .gauge-card {
        background: linear-gradient(145deg, rgba(30,41,59,0.9), rgba(15,23,42,0.95));
        border: 1px solid rgba(148,163,184,0.1);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0f172a;
    }
    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATOS MOCK (ROBUSTOS Y REALISTAS)
# ============================================================

PROPIEDADES = [
    {"id": 1, "nombre": "Ático Centro Histórico", "ubicacion": "Madrid Centro", "capacidad": 4, "tipo": "Ático"},
    {"id": 2, "nombre": "Loft Playa Malvarrosa", "ubicacion": "Valencia", "capacidad": 2, "tipo": "Loft"},
    {"id": 3, "nombre": "Penthouse Gran Vía", "ubicacion": "Madrid", "capacidad": 6, "tipo": "Penthouse"},
    {"id": 4, "nombre": "Casa Rural Sierra", "ubicacion": "Segovia", "capacidad": 8, "tipo": "Casa Rural"},
    {"id": 5, "nombre": "Estudio Bohemio", "ubicacion": "Barcelona", "capacidad": 2, "tipo": "Estudio"},
    {"id": 6, "nombre": "Dúplex Marina", "ubicacion": "Alicante", "capacidad": 5, "tipo": "Dúplex"},
    {"id": 7, "nombre": "Villa Jardín", "ubicacion": "Málaga", "capacidad": 10, "tipo": "Villa"},
]

# Datos mensuales de ingresos (últimos 12 meses)
MESES = ["Sep", "Oct", "Nov", "Dic", "Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago"]
INGRESOS_AIRBNB = [12400, 11800, 9500, 14200, 10800, 12100, 15600, 18900, 21300, 24800, 28500, 27200]
INGRESOS_BOOKING = [9800, 10200, 8100, 11500, 8900, 9500, 12800, 15200, 17800, 20100, 23400, 22100]
INGRESOS_TOTALES = [a + b for a, b in zip(INGRESOS_AIRBNB, INGRESOS_BOOKING)]

# Datos por propiedad (mes actual)
DATOS_PROPIEDADES = pd.DataFrame({
    "Propiedad": [p["nombre"] for p in PROPIEDADES],
    "Ubicación": [p["ubicacion"] for p in PROPIEDADES],
    "Ocupación (%)": [92, 78, 85, 65, 88, 72, 95],
    "ADR (€)": [145, 98, 210, 175, 115, 132, 280],
    "Ingresos Mes (€)": [12840, 6100, 17850, 9100, 8100, 7120, 26600],
    "Canal Principal": ["Airbnb", "Booking", "Airbnb", "Booking", "Airbnb", "Booking", "Airbnb"],
    "Reservas Mes": [18, 12, 14, 8, 15, 11, 22],
    "Noches Ocupadas": [28, 22, 25, 18, 26, 20, 30],
    "Noches Disponibles": [31, 31, 31, 31, 31, 31, 31],
})

# Operativa de hoy
HOY = datetime(2026, 8, 12)
OPERATIVA_HOY = pd.DataFrame({
    "Hora": ["11:00", "14:00", "15:30", "16:00", "17:00", "18:30", "20:00"],
    "Propiedad": [
        "Loft Playa Malvarrosa",
        "Ático Centro Histórico",
        "Penthouse Gran Vía",
        "Estudio Bohemio",
        "Dúplex Marina",
        "Casa Rural Sierra",
        "Villa Jardín"
    ],
    "Tipo": ["Check-out", "Check-in", "Check-in", "Check-out", "Check-in", "Check-out", "Check-in"],
    "Huéspedes": ["María G.", "John & Lisa", "Familia Ruiz", "Pierre D.", "Ana & Carlos", "Grupo 6px", "Familia López"],
    "Limpieza": ["Completada", "Pendiente", "Pendiente", "Completada", "Pendiente", "Completada", "Pendiente"],
})

# Calendario próximos 7 días
DIAS_CAL = [(HOY + timedelta(days=i)).strftime("%d/%m") for i in range(7)]
DIAS_SEM = [(HOY + timedelta(days=i)).strftime("%a") for i in range(7)]

# Mapa de calendario (1 = ocupado, 0 = libre)
CALENDARIO = {
    "Ático Centro Histórico": [1, 1, 0, 1, 1, 1, 0],
    "Loft Playa Malvarrosa": [0, 1, 1, 1, 0, 0, 1],
    "Penthouse Gran Vía": [1, 1, 1, 0, 1, 1, 1],
    "Casa Rural Sierra": [0, 0, 1, 1, 1, 0, 0],
    "Estudio Bohemio": [1, 0, 1, 1, 0, 1, 1],
    "Dúplex Marina": [1, 1, 0, 0, 1, 1, 0],
    "Villa Jardín": [1, 1, 1, 1, 1, 0, 1],
}

# Reputación
REPUTACION = {
    "Airbnb": {"score": 4.82, "total": 5, "reviews": 847, "trend": +0.04},
    "Booking": {"score": 9.1, "total": 10, "reviews": 623, "trend": +0.12},
}

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("<h1 style='color:#38bdf8; font-size:1.8rem; font-weight:800;'>🏢 RentMaster Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:0.85rem;'>Gestión Multi-Propiedad</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:rgba(148,163,184,0.2); margin:20px 0;'>", unsafe_allow_html=True)

    st.markdown("<p style='color:#64748b; font-size:0.75rem; text-transform:uppercase; font-weight:600; letter-spacing:0.1em;'>Navegación</p>", unsafe_allow_html=True)

    vista = st.radio("", ["📊 Vista General", "🏠 Propiedades", "📅 Operativa", "⭐ Reputación"], label_visibility="collapsed")

    st.markdown("<hr style='border-color:rgba(148,163,184,0.2); margin:20px 0;'>", unsafe_allow_html=True)

    st.markdown("<p style='color:#64748b; font-size:0.75rem; text-transform:uppercase; font-weight:600; letter-spacing:0.1em;'>Filtros</p>", unsafe_allow_html=True)

    filtro_canal = st.multiselect("Canal", ["Airbnb", "Booking"], default=["Airbnb", "Booking"])
    filtro_mes = st.selectbox("Período", ["Últimos 30 días", "Este mes", "Trimestre", "Año"])

    st.markdown("<hr style='border-color:rgba(148,163,184,0.2); margin:20px 0;'>", unsafe_allow_html=True)

    # Mini KPI sidebar
    st.markdown("<p style='color:#64748b; font-size:0.75rem; text-transform:uppercase; font-weight:600; letter-spacing:0.1em;'>Resumen Rápido</p>", unsafe_allow_html=True)

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("Ocupación", "82%", "+3%", label_visibility="collapsed")
    with col_s2:
        st.metric("ADR", "165€", "+8€", label_visibility="collapsed")

    st.markdown("<div style='margin-top:40px; text-align:center;'>" +
                "<p style='color:#475569; font-size:0.7rem;'>RentMaster Pro v2.1</p>" +
                "<p style='color:#334155; font-size:0.65rem;'>Modo DEMO</p></div>", unsafe_allow_html=True)

# ============================================================
# HEADER PRINCIPAL
# ============================================================
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("<h1 style='color:#f8fafc; font-size:2.2rem; font-weight:800; margin-bottom:4px;'>Dashboard de Gestión</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:1rem;'>7 propiedades activas · Agosto 2026</p>", unsafe_allow_html=True)
with col_h2:
    st.markdown(f"""
    <div style='text-align:right; padding-top:10px;'>
        <p style='color:#64748b; font-size:0.75rem; text-transform:uppercase; font-weight:600;'>Última actualización</p>
        <p style='color:#38bdf8; font-size:1rem; font-weight:600;'>{HOY.strftime("%d/%m/%Y %H:%M")}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border-color:rgba(148,163,184,0.15); margin:20px 0 30px 0;'>", unsafe_allow_html=True)

# ============================================================
# VISTA GENERAL
# ============================================================
if vista == "📊 Vista General":

    # --- KPIs ---
    st.markdown("<div class='section-header'>📈 Métricas Principales</div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-title'>💰 Ingresos MTD</div>
            <div class='kpi-value'>€49,300</div>
            <div class='kpi-delta-positive'>▲ +12.4% vs julio</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-title'>📊 Ocupación Global</div>
            <div class='kpi-value'>82.3%</div>
            <div class='kpi-delta-positive'>▲ +5.1% vs julio</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-title'>🏷️ ADR Medio</div>
            <div class='kpi-value'>€165</div>
            <div class='kpi-delta-positive'>▲ +€8 vs julio</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-title'>💵 Beneficio Neto</div>
            <div class='kpi-value'>€31,850</div>
            <div class='kpi-delta-positive'>▲ +15.2% vs julio</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Gráficos ---
    col_g1, col_g2 = st.columns([3, 2])

    with col_g1:
        st.markdown("<div class='section-header'>📉 Evolución de Ingresos</div>", unsafe_allow_html=True)

        df_ingresos = pd.DataFrame({
            "Mes": MESES,
            "Airbnb": INGRESOS_AIRBNB,
            "Booking": INGRESOS_BOOKING,
            "Total": INGRESOS_TOTALES
        })

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_ingresos["Mes"], y=df_ingresos["Airbnb"],
            mode='lines+markers',
            name='Airbnb',
            line=dict(color='#FF5A5F', width=3),
            marker=dict(size=8, symbol='circle'),
            fill='tozeroy',
            fillcolor='rgba(255,90,95,0.1)'
        ))

        fig.add_trace(go.Scatter(
            x=df_ingresos["Mes"], y=df_ingresos["Booking"],
            mode='lines+markers',
            name='Booking.com',
            line=dict(color='#003580', width=3),
            marker=dict(size=8, symbol='diamond'),
            fill='tozeroy',
            fillcolor='rgba(0,53,128,0.1)'
        ))

        fig.add_trace(go.Scatter(
            x=df_ingresos["Mes"], y=df_ingresos["Total"],
            mode='lines',
            name='Total',
            line=dict(color='#38bdf8', width=2, dash='dot'),
            marker=dict(size=6)
        ))

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', family='Inter'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                       bgcolor='rgba(15,23,42,0.8)', bordercolor='rgba(148,163,184,0.2)', borderwidth=1),
            margin=dict(l=40, r=40, t=60, b=40),
            xaxis=dict(showgrid=True, gridcolor='rgba(148,163,184,0.1)', gridwidth=0.5),
            yaxis=dict(showgrid=True, gridcolor='rgba(148,163,184,0.1)', gridwidth=0.5,
                      tickprefix='€', tickformat=','),
            hovermode='x unified',
            height=400
        )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col_g2:
        st.markdown("<div class='section-header'>🥧 Distribución por Canal</div>", unsafe_allow_html=True)

        total_airbnb = sum(INGRESOS_AIRBNB)
        total_booking = sum(INGRESOS_BOOKING)

        fig_pie = go.Figure(data=[go.Pie(
            labels=['Airbnb', 'Booking.com'],
            values=[total_airbnb, total_booking],
            hole=0.6,
            marker=dict(colors=['#FF5A5F', '#003580'], line=dict(color='rgba(15,23,42,0.8)', width=2)),
            textinfo='percent',
            textfont=dict(size=14, color='#f8fafc'),
            hovertemplate='<b>%{label}</b><br>€%{value:,.0f}<br>%{percent}<extra></extra>'
        )])

        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', family='Inter'),
            showlegend=True,
            legend=dict(orientation='h', yanchor='bottom', y=-0.1, xanchor='center', x=0.5,
                       font=dict(size=12)),
            margin=dict(l=20, r=20, t=40, b=40),
            height=400,
            annotations=[dict(text=f'€{total_airbnb+total_booking:,.0f}', x=0.5, y=0.5,
                            font=dict(size=18, color='#f8fafc', family='Inter'),
                            showarrow=False)]
        )

        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})

    # --- Gráfico de barras por propiedad ---
    st.markdown("<div class='section-header'>🏠 Ingresos por Propiedad (Mes Actual)</div>", unsafe_allow_html=True)

    fig_bar = go.Figure()

    colors_bar = ['#38bdf8', '#34d399', '#a78bfa', '#fbbf24', '#f87171', '#fb923c', '#22d3ee']

    fig_bar.add_trace(go.Bar(
        x=DATOS_PROPIEDADES["Propiedad"],
        y=DATOS_PROPIEDADES["Ingresos Mes (€)"],
        marker=dict(color=colors_bar, line=dict(color='rgba(15,23,42,0.8)', width=1)),
        text=DATOS_PROPIEDADES["Ingresos Mes (€)"].apply(lambda x: f'€{x:,}'),
        textposition='outside',
        textfont=dict(color='#e2e8f0', size=11),
        hovertemplate='<b>%{x}</b><br>Ingresos: €%{y:,.0f}<extra></extra>'
    ))

    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0', family='Inter'),
        margin=dict(l=40, r=40, t=20, b=80),
        xaxis=dict(showgrid=False, tickangle=-25, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor='rgba(148,163,184,0.1)', tickprefix='€', tickformat=','),
        showlegend=False,
        height=350
    )

    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

# ============================================================
# VISTA PROPIEDADES
# ============================================================
elif vista == "🏠 Propiedades":

    st.markdown("<div class='section-header'>🏠 Rendimiento por Propiedad</div>", unsafe_allow_html=True)

    # Tabla estilizada con barras de progreso
    df_display = DATOS_PROPIEDADES.copy()

    # Crear visualización personalizada
    for idx, row in df_display.iterrows():
        ocupacion = row["Ocupación (%)"]
        color_bar = "#34d399" if ocupacion >= 85 else "#fbbf24" if ocupacion >= 70 else "#f87171"

        col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns([2.5, 1, 1.2, 1.2, 1])

        with col_p1:
            st.markdown(f"""
            <div style='padding:12px 0;'>
                <p style='color:#f8fafc; font-weight:600; font-size:0.95rem; margin:0;'>{row["Propiedad"]}</p>
                <p style='color:#64748b; font-size:0.75rem; margin:0;'>{row["Ubicación"]} · {row["Canal Principal"]}</p>
            </div>
            """, unsafe_allow_html=True)

        with col_p2:
            st.markdown(f"""
            <div style='padding:12px 0; text-align:center;'>
                <p style='color:#f8fafc; font-weight:700; font-size:1.1rem; margin:0;'>{ocupacion}%</p>
                <div class='progress-container' style='width:80px; margin:0 auto;'>
                    <div class='progress-fill' style='width:{ocupacion}%; background:{color_bar};'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_p3:
            st.markdown(f"""
            <div style='padding:12px 0; text-align:center;'>
                <p style='color:#94a3b8; font-size:0.75rem; margin:0; text-transform:uppercase;'>ADR</p>
                <p style='color:#f8fafc; font-weight:600; font-size:1rem; margin:0;'>€{row["ADR (€)"]}</p>
            </div>
            """, unsafe_allow_html=True)

        with col_p4:
            st.markdown(f"""
            <div style='padding:12px 0; text-align:center;'>
                <p style='color:#94a3b8; font-size:0.75rem; margin:0; text-transform:uppercase;'>Ingresos</p>
                <p style='color:#34d399; font-weight:700; font-size:1rem; margin:0;'>€{row["Ingresos Mes (€)"]:,}</p>
            </div>
            """, unsafe_allow_html=True)

        with col_p5:
            st.markdown(f"""
            <div style='padding:12px 0; text-align:center;'>
                <p style='color:#94a3b8; font-size:0.75rem; margin:0; text-transform:uppercase;'>Reservas</p>
                <p style='color:#38bdf8; font-weight:700; font-size:1rem; margin:0;'>{row["Reservas Mes"]}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:rgba(148,163,184,0.08); margin:0;'>", unsafe_allow_html=True)

    # Detalle adicional
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>📋 Datos Detallados</div>", unsafe_allow_html=True)

    # DataFrame interactivo
    st.dataframe(
        DATOS_PROPIEDADES.style
        .background_gradient(subset=["Ocupación (%)"], cmap="RdYlGn", vmin=0, vmax=100)
        .format({"ADR (€)": "€{}", "Ingresos Mes (€)": "€{:,}"})
        .set_properties(**{'background-color': 'rgba(30,41,59,0.5)', 'color': '#e2e8f0', 'border-color': 'rgba(148,163,184,0.1)'}),
        use_container_width=True,
        height=350
    )

# ============================================================
# VISTA OPERATIVA
# ============================================================
elif vista == "📅 Operativa":

    # Check-ins y check-outs de hoy
    st.markdown("<div class='section-header'>📝 Operativa de Hoy — 12 de Agosto</div>", unsafe_allow_html=True)

    col_op1, col_op2 = st.columns([1, 1])

    with col_op1:
        st.markdown("<p style='color:#38bdf8; font-weight:600; font-size:1rem; margin-bottom:12px;'>⬇️ Check-ins</p>", unsafe_allow_html=True)
        checkins = OPERATIVA_HOY[OPERATIVA_HOY["Tipo"] == "Check-in"]
        for _, row in checkins.iterrows():
            limpieza_class = "badge-completada" if row["Limpieza"] == "Completada" else "badge-pendiente"
            st.markdown(f"""
            <div style='background:rgba(30,41,59,0.6); border:1px solid rgba(56,189,248,0.15); border-radius:12px; padding:14px; margin-bottom:10px;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <div>
                        <p style='color:#f8fafc; font-weight:600; margin:0; font-size:0.95rem;'>{row["Propiedad"]}</p>
                        <p style='color:#94a3b8; margin:0; font-size:0.8rem;'>{row["Huéspedes"]} · {row["Hora"]}</p>
                    </div>
                    <span class='{limpieza_class}'>{row["Limpieza"]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_op2:
        st.markdown("<p style='color:#f87171; font-weight:600; font-size:1rem; margin-bottom:12px;'>⬆️ Check-outs</p>", unsafe_allow_html=True)
        checkouts = OPERATIVA_HOY[OPERATIVA_HOY["Tipo"] == "Check-out"]
        for _, row in checkouts.iterrows():
            limpieza_class = "badge-completada" if row["Limpieza"] == "Completada" else "badge-pendiente"
            st.markdown(f"""
            <div style='background:rgba(30,41,59,0.6); border:1px solid rgba(248,113,113,0.15); border-radius:12px; padding:14px; margin-bottom:10px;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <div>
                        <p style='color:#f8fafc; font-weight:600; margin:0; font-size:0.95rem;'>{row["Propiedad"]}</p>
                        <p style='color:#94a3b8; margin:0; font-size:0.8rem;'>{row["Huéspedes"]} · {row["Hora"]}</p>
                    </div>
                    <span class='{limpieza_class}'>{row["Limpieza"]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Calendario de 7 días
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>📅 Disponibilidad Próximos 7 Días</div>", unsafe_allow_html=True)

    # Header de días
    cols_header = st.columns([1.5] + [1]*7)
    with cols_header[0]:
        st.markdown("<p style='color:#64748b; font-size:0.7rem; font-weight:600;'>PROPIEDAD</p>", unsafe_allow_html=True)
    for i in range(7):
        with cols_header[i+1]:
            st.markdown(f"""
            <div style='text-align:center;'>
                <p class='cal-header'>{DIAS_SEM[i]}</p>
                <p style='color:#f8fafc; font-weight:700; font-size:0.9rem; margin:0;'>{DIAS_CAL[i]}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(148,163,184,0.1); margin:8px 0;'>", unsafe_allow_html=True)

    # Filas de propiedades
    for propiedad, dias in CALENDARIO.items():
        cols_row = st.columns([1.5] + [1]*7)
        with cols_row[0]:
            st.markdown(f"<p style='color:#e2e8f0; font-weight:500; font-size:0.85rem; margin:8px 0;'>{propiedad}</p>", unsafe_allow_html=True)
        for i in range(7):
            with cols_row[i+1]:
                estado = "Ocupado" if dias[i] == 1 else "Libre"
                css_class = "cal-occupied" if dias[i] == 1 else "cal-free"
                st.markdown(f"""
                <div class='cal-cell {css_class}' style='margin:4px 0;'>
                    {"●" if dias[i] == 1 else "○"}
                </div>
                """, unsafe_allow_html=True)

    # Leyenda
    st.markdown("""
    <div style='display:flex; gap:20px; margin-top:16px; justify-content:center;'>
        <div style='display:flex; align-items:center; gap:6px;'>
            <div style='width:12px; height:12px; background:rgba(52,211,153,0.3); border:1px solid #34d399; border-radius:3px;'></div>
            <span style='color:#94a3b8; font-size:0.8rem;'>Disponible</span>
        </div>
        <div style='display:flex; align-items:center; gap:6px;'>
            <div style='width:12px; height:12px; background:rgba(248,113,113,0.3); border:1px solid #f87171; border-radius:3px;'></div>
            <span style='color:#94a3b8; font-size:0.8rem;'>Ocupado</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# VISTA REPUTACIÓN
# ============================================================
elif vista == "⭐ Reputación":

    st.markdown("<div class='section-header'>⭐ Calidad y Reputación</div>", unsafe_allow_html=True)

    col_r1, col_r2 = st.columns(2)

    with col_r1:
        st.markdown("<div class='gauge-card'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#FF5A5F; font-weight:700; font-size:1.2rem; margin-bottom:8px;'>🅰️ Airbnb</p>", unsafe_allow_html=True)

        score_airbnb = REPUTACION["Airbnb"]["score"]

        fig_gauge_air = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score_airbnb,
            delta={'reference': score_airbnb - REPUTACION["Airbnb"]["trend"], 'increasing': {'color': '#34d399'}},
            number={'font': {'size': 48, 'color': '#f8fafc', 'family': 'Inter'}},
            gauge={
                'axis': {'range': [0, 5], 'tickwidth': 1, 'tickcolor': '#334155'},
                'bar': {'color': '#FF5A5F', 'thickness': 0.75},
                'bgcolor': 'rgba(30,41,59,0.5)',
                'borderwidth': 2,
                'bordercolor': 'rgba(148,163,184,0.1)',
                'steps': [
                    {'range': [0, 3], 'color': 'rgba(248,113,113,0.1)'},
                    {'range': [3, 4], 'color': 'rgba(251,191,36,0.1)'},
                    {'range': [4, 5], 'color': 'rgba(52,211,153,0.1)'}
                ],
                'threshold': {
                    'line': {'color': '#f8fafc', 'width': 3},
                    'thickness': 0.8,
                    'value': 4.5
                }
            }
        ))

        fig_gauge_air.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            margin=dict(l=20, r=20, t=30, b=20),
            height=280
        )

        st.plotly_chart(fig_gauge_air, use_container_width=True, config={'displayModeBar': False})

        st.markdown(f"""
        <div style='text-align:center; margin-top:-10px;'>
            <p style='color:#94a3b8; font-size:0.85rem;'>Basado en <strong style='color:#f8fafc;'>{REPUTACION["Airbnb"]["reviews"]}</strong> reseñas</p>
            <p class='kpi-delta-positive'>▲ +{REPUTACION["Airbnb"]["trend"]:.2f} este mes</p>
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col_r2:
        st.markdown("<div class='gauge-card'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#003580; font-weight:700; font-size:1.2rem; margin-bottom:8px;'>🅱️ Booking.com</p>", unsafe_allow_html=True)

        score_booking = REPUTACION["Booking"]["score"]

        fig_gauge_book = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score_booking,
            delta={'reference': score_booking - REPUTACION["Booking"]["trend"], 'increasing': {'color': '#34d399'}},
            number={'font': {'size': 48, 'color': '#f8fafc', 'family': 'Inter'}},
            gauge={
                'axis': {'range': [0, 10], 'tickwidth': 1, 'tickcolor': '#334155'},
                'bar': {'color': '#003580', 'thickness': 0.75},
                'bgcolor': 'rgba(30,41,59,0.5)',
                'borderwidth': 2,
                'bordercolor': 'rgba(148,163,184,0.1)',
                'steps': [
                    {'range': [0, 6], 'color': 'rgba(248,113,113,0.1)'},
                    {'range': [6, 8], 'color': 'rgba(251,191,36,0.1)'},
                    {'range': [8, 10], 'color': 'rgba(52,211,153,0.1)'}
                ],
                'threshold': {
                    'line': {'color': '#f8fafc', 'width': 3},
                    'thickness': 0.8,
                    'value': 8.5
                }
            }
        ))

        fig_gauge_book.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            margin=dict(l=20, r=20, t=30, b=20),
            height=280
        )

        st.plotly_chart(fig_gauge_book, use_container_width=True, config={'displayModeBar': False})

        st.markdown(f"""
        <div style='text-align:center; margin-top:-10px;'>
            <p style='color:#94a3b8; font-size:0.85rem;'>Basado en <strong style='color:#f8fafc;'>{REPUTACION["Booking"]["reviews"]}</strong> reseñas</p>
            <p class='kpi-delta-positive'>▲ +{REPUTACION["Booking"]["trend"]:.2f} este mes</p>
        </div>
        </div>
        """, unsafe_allow_html=True)

    # Reviews recientes simuladas
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>💬 Reseñas Recientes</div>", unsafe_allow_html=True)

    reviews_mock = [
        {"platform": "Airbnb", "prop": "Ático Centro Histórico", "guest": "Sarah M.", "rating": 5, "date": "11/08/2026", "text": "Increíble ubicación, todo perfecto. Repetiremos seguro!"},
        {"platform": "Booking", "prop": "Villa Jardín", "guest": "Fam. Müller", "rating": 9.4, "date": "10/08/2026", "text": "Excelente villa, piscina fantástica. Muy recomendable para familias."},
        {"platform": "Airbnb", "prop": "Loft Playa Malvarrosa", "guest": "Carlos R.", "rating": 4, "date": "09/08/2026", "text": "Buen loft, aunque el wifi podría ser más rápido."},
        {"platform": "Booking", "prop": "Penthouse Gran Vía", "guest": "Emma L.", "rating": 10, "date": "08/08/2026", "text": "Vistas espectaculares, atención impecable. 10/10"},
        {"platform": "Airbnb", "prop": "Estudio Bohemio", "guest": "Tom & Jerry", "rating": 5, "date": "07/08/2026", "text": "Decoración única, muy acogedor. Perfecto para parejas."},
    ]

    for rev in reviews_mock:
        color_plat = "#FF5A5F" if rev["platform"] == "Airbnb" else "#003580"
        stars = "⭐" * int(rev["rating"]) if rev["platform"] == "Airbnb" else f"{rev['rating']}/10"

        st.markdown(f"""
        <div style='background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08); border-radius:12px; padding:16px; margin-bottom:10px;'>
            <div style='display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;'>
                <div>
                    <span style='background:{color_plat}20; color:{color_plat}; padding:2px 8px; border-radius:4px; font-size:0.7rem; font-weight:600; margin-right:8px;'>{rev["platform"]}</span>
                    <span style='color:#f8fafc; font-weight:600; font-size:0.9rem;'>{rev["prop"]}</span>
                </div>
                <span style='color:#fbbf24; font-weight:700; font-size:0.9rem;'>{stars}</span>
            </div>
            <p style='color:#cbd5e1; font-size:0.85rem; margin:0; line-height:1.5;'>"{rev["text"]}"</p>
            <p style='color:#64748b; font-size:0.75rem; margin:8px 0 0 0;'>— {rev["guest"]} · {rev["date"]}</p>
        </div>
        """, unsafe_allow_html=True)
