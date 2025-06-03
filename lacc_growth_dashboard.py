# lacc_growth_dashboard.py  —  Versión BI Pro + Forecast
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import altair as alt
from prophet import Prophet    #  ← FIXED: use the standard Prophet package
from datetime import date, timedelta

# ──────────────────────────────
# CONFIGURACIÓN GENERAL
# ──────────────────────────────
st.set_page_config(
    page_title="LACC · Crecimiento BI 🚀",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------- Estilos globales (CSS) ----------
st.markdown(
    """
    <style>
        body, .stApp {
            background: linear-gradient(135deg,#0f1123 0%,#1e2030 40%, #0f1123 100%);
            color: #e8e8e8; font-family: 'Inter', sans-serif;
        }
        #MainMenu, footer {visibility: hidden;}
        div[data-testid="metric-container"] {
            background: rgba(255,255,255,0.06); padding:1rem; border-radius:0.8rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.35);
        }
        div[data-testid="metric-container"] > label {color:#00E5FF;}
    </style>
    """,
    unsafe_allow_html=True
)

# ──────────────────────────────
# LOGO & HERO
# ──────────────────────────────
logo_col, title_col = st.columns([1, 5])
with logo_col:
    st.image("logo_lacc.png", width=140)      # ⇽ coloca aquí tu logo
with title_col:
    st.title("📈 Latin America Cybersecurity Challenge · Dashboard BI 2024-2025")

st.markdown(
    """
    <div style="font-size:1.35rem;line-height:1.6em;text-align:justify;">
      <strong>En menos de dos años, el <span style="color:#00E5FF;">LACC</span> pasó de idea a epicentro de la ciberseguridad latinoamericana.</strong><br><br>
      Cada seguidor es un nuevo defensor de nuestros datos. Veamos la historia… y el futuro que nos espera.
    </div>
    """,
    unsafe_allow_html=True
)

# ──────────────────────────────
# 1 · DATOS SIMULADOS
# ──────────────────────────────
seguidores_actuales = {
    "LinkedIn ICC": 3386, "LinkedIn Latin": 307, "X Contacto": 3,
    "X LatamCaribe": 272, "Instagram": 126, "TikTok": 12, "YouTube": 103
}

periodos = pd.date_range("2024-01-01", "2025-06-30", freq="M")
data = {}
np.random.seed(42)

for red, fin in seguidores_actuales.items():
    base = int(fin * 0.05)
    tendencia = np.linspace(base, fin, len(periodos))
    ruido = np.random.normal(0, fin * 0.02, len(periodos))
    data[red] = np.maximum(0, tendencia + ruido).astype(int)

df = pd.DataFrame(data, index=periodos)

# Serie total por mes (no cumsum)
totales = df.sum(axis=1)

# ──────────────────────────────
# 2 · MÉTRICAS PRINCIPALES
# ──────────────────────────────
total_actual = int(totales.iloc[-1])
total_inicio = int(totales.iloc[0])
meses = len(totales) - 1
cagr = ((total_actual / total_inicio) ** (12 / meses) - 1) * 100

m1, m2, m3, m4 = st.columns(4)
m1.metric("👥 Seguidores totales", f"{total_actual:,}")
m2.metric("📈 CAGR", f"{cagr:,.1f}%")
m3.metric("🚀 Incremento absoluto", f"{total_actual - total_inicio:,}")
m4.metric("🌟 Red líder", df.iloc[-1].idxmax())

# Gauge objetivo
objetivo = st.sidebar.number_input("Objetivo 2025:", value=int(total_actual * 1.5), step=500)
gauge_fig = px.pie(
    names=["Avance", "Pendiente"],
    values=[total_actual, max(objetivo - total_actual, 0)],
    hole=0.6
).update_traces(textinfo='none').update_layout(
    title="Progreso hacia objetivo", showlegend=False,
    margin=dict(t=0, b=0, l=0, r=0)
)
st.plotly_chart(gauge_fig, use_container_width=True)

# ──────────────────────────────
# 3 · HISTÓRICO Y VISUALES
# ──────────────────────────────
st.header("🕸️ Evolución mensual por red social")
st.plotly_chart(
    px.line(df, x=df.index, y=df.columns,
            labels={"value": "Seguidores", "variable": "Red", "index": "Fecha"}),
    use_container_width=True
)

st.markdown("---")
st.header("🔮 Crecimiento total acumulado")
st.plotly_chart(
    px.area(x=totales.index, y=totales.values,
            labels={"x": "Fecha", "y": "Seguidores totales"}),
    use_container_width=True
)

# Heatmap
st.header("🔥 Heatmap de nuevos seguidores por mes")
heat = df.diff().fillna(0).astype(int).reset_index().melt(
    id_vars="index", var_name="Red", value_name="Nuevos")
heat["Mes"] = heat["index"].dt.strftime("%Y-%m")

heatmap = alt.Chart(heat).mark_rect().encode(
    x=alt.X('Mes:O', sort=periodos.strftime("%Y-%m").tolist(),
            axis=alt.Axis(labelAngle=-75)),
    y='Red:O',
    color=alt.Color('Nuevos:Q', scale=alt.Scale(scheme='greens')),
    tooltip=['Red', 'Mes', 'Nuevos']
).properties(height=300)
st.altair_chart(heatmap, use_container_width=True)

# ──────────────────────────────
# 4 · FORECAST PROPHET
# ──────────────────────────────
st.markdown("---")
st.header("📈 Predicción automática de seguidores totales")

horizon = st.slider("Meses a proyectar:", 3, 24, 12, 3)

# Preparar datos para Prophet
df_prophet = pd.DataFrame({"ds": totales.index, "y": totales.values})
model = Prophet(yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False)
model.fit(df_prophet)

future = model.make_future_dataframe(periods=horizon, freq="M")
forecast = model.predict(future)

# Graficar
fig_forecast = px.line(
    forecast, x="ds", y="yhat",
    labels={"ds": "Fecha", "yhat": "Seguidores proyectados"},
    title="Proyección de seguidores totales"
)
fig_forecast.add_scatter(
    x=totales.index, y=totales.values,
    mode="markers+lines", name="Histórico", line=dict(color="#00E5FF")
)
st.plotly_chart(fig_forecast, use_container_width=True)

pred_value = int(forecast.iloc[-1]["yhat"])
st.metric(f"Proyección a {forecast.iloc[-1]['ds'].strftime('%b %Y')}",
          f"{pred_value:,}")

# ──────────────────────────────
# 5 · EMBUDO Y PIE
# ──────────────────────────────
st.markdown("---")
st.header("🧩 Embudo de conversión (awareness → leads)")
seg = total_actual
newsletter = int(seg * 0.30)
participantes = int(newsletter * 0.40)
leads = int(participantes * 0.10)
funnel_df = pd.DataFrame({
    "Stage": ["Seguidores", "Newsletter", "Participantes CTF", "Leads"],
    "Count": [seg, newsletter, participantes, leads]
})
st.plotly_chart(px.funnel(funnel_df, x='Count', y='Stage', orientation='h'),
                use_container_width=True)

st.header("📊 Distribución % de seguidores por red")
st.plotly_chart(px.pie(values=df.iloc[-1], names=df.columns, hole=0.4),
                use_container_width=True)

# ──────────────────────────────
# 6 · CIERRE
# ──────────────────────────────
st.markdown(
    """
    ---
    ## 🌎 Próximos hitos  
    * **Jul 2025:** Evento presencia LACC (500+ hackers éticos)  
    * **Ago 2025:** Programa de becas en ciberseguridad  
    * **Dic 2025:** CSIRT regional operativo  
    
    <div style="text-align:center;font-size:1.25rem;margin-top:1rem;">
      <strong>Únete, difunde, hackea el futuro con nosotros — #SomosLACC</strong>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption("🔒 LACC – Unidos por la Ciberseguridad en Latinoamérica.")
