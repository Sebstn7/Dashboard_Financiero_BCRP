# Dashboard financiero - BCRP
# Sebastian Porras

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os

# --- Datos ---
RUTA_DATOS = os.path.join(os.path.dirname(__file__), "datos")

def cargar_csv(nombre):
    df = pd.read_csv(os.path.join(RUTA_DATOS, f"{nombre}.csv"))
    meses = {
        "Ene": 1, "Feb": 2, "Mar": 3, "Abr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Ago": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dic": 12,
    }
    partes = df["periodo"].str.split(".")
    df["mes"] = partes.str[0].map(meses)
    df["anio"] = partes.str[1].astype(int)
    df["fecha"] = pd.to_datetime(df["anio"].astype(str) + "-" + df["mes"].astype(str) + "-01")
    return df

credito_total = cargar_csv("credito_total_financiero")
credito_mn = cargar_csv("credito_mn_financiero")
credito_me = cargar_csv("credito_me_financiero")
credito_emp = cargar_csv("credito_empresas")
credito_cons = cargar_csv("credito_consumo")
credito_hipo = cargar_csv("credito_hipotecario")
tpm = cargar_csv("tasa_politica_monetaria")
tasa_corp = cargar_csv("tasa_activas_corporativos")
tasa_gdes = cargar_csv("tasa_activas_grandes")
tasa_pas = cargar_csv("tasa_pasivas")
ipc_df = cargar_csv("ipc")

# Colores del portafolio
C = {
    "primary": "#5F86AE",
    "secondary": "#F6D6BF",
    "accent1": "#8B5CF6",
    "accent2": "#34D399",
    "gray": "#94A3B8",
    "bg": "#0A0A0F",
    "card": "#1A1A2E",
    "text": "#E2E8F0",
    "danger": "#EF4444",
}

MIN_DATE = credito_total["fecha"].min()
MAX_DATE = credito_total["fecha"].max()

# --- App ---
app = dash.Dash(__name__, title="Dashboard Financiero - Perú")

def kpi_card_style(color):
    return {
        "backgroundColor": C["card"],
        "padding": "14px 20px",
        "borderRadius": "10px",
        "borderLeft": f"3px solid {color}",
    }

app.layout = html.Div(
    children=[
        # Header
        html.Div(
            style={
                "backgroundColor": C["card"],
                "padding": "20px 40px",
                "borderBottom": f"3px solid {C['primary']}",
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
            },
            children=[
                html.Div([
                    html.H1(
                        "Sistema Financiero Peruano",
                        style={"margin": "0", "fontSize": "26px", "color": C["primary"], "fontFamily": "'Space Grotesk', sans-serif", "fontWeight": 700},
                    ),
                    html.P(
                        "BCRP · 2015 - 2025",
                        style={"margin": "2px 0 0 0", "fontSize": "12px", "color": C["gray"]},
                    ),
                ]),
                html.Div(
                    "SP",
                    style={
                        "width": "40px", "height": "40px", "borderRadius": "50%",
                        "background": f"linear-gradient(135deg, {C['primary']}, {C['secondary']})",
                        "display": "flex", "alignItems": "center", "justifyContent": "center",
                        "color": C["bg"], "fontWeight": "bold", "fontSize": "16px",
                        "fontFamily": "'Space Grotesk', sans-serif",
                    },
                ),
            ],
        ),
        # KPIs
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(180px, 1fr))", "gap": "14px", "padding": "20px 40px"},
            children=[
                html.Div(id="kpi-credito", style=kpi_card_style(C["primary"])),
                html.Div(id="kpi-tpm", style=kpi_card_style(C["secondary"])),
                html.Div(id="kpi-ipc", style=kpi_card_style(C["accent1"])),
                html.Div(id="kpi-crecimiento", style=kpi_card_style(C["accent2"])),
            ],
        ),
        # Filtros
        html.Div(
            style={"padding": "0 40px 20px 40px", "display": "flex", "gap": "16px", "alignItems": "center", "flexWrap": "wrap"},
            children=[
                html.Span("Filtrar:", style={"fontSize": "13px", "color": C["gray"], "fontWeight": 600}),
                dcc.DatePickerRange(id="date-range", min_date_allowed=MIN_DATE, max_date_allowed=MAX_DATE, start_date=MIN_DATE, end_date=MAX_DATE, display_format="MMM YYYY"),
                html.Span("Tasa:", style={"fontSize": "13px", "color": C["gray"], "fontWeight": 600}),
                dcc.Dropdown(id="tasa-selector", options=[
                    {"label": "Política Monetaria", "value": "tpm"},
                    {"label": "Activa Corporativos", "value": "corp"},
                    {"label": "Activa Grandes Empresas", "value": "gdes"},
                    {"label": "Pasiva Ahorro", "value": "pas"},
                ], value="tpm", clearable=False, style={"width": "220px", "color": "#000"}),
            ],
        ),
        # Graficos
        html.Div(
            style={"padding": "0 40px 40px 40px"},
            children=[
                html.Div(
                    style={"backgroundColor": C["card"], "borderRadius": "12px", "marginBottom": "20px", "overflow": "hidden"},
                    children=[
                        html.Div("Crédito al Sector Privado", style={"padding": "14px 20px", "fontFamily": "'Space Grotesk', sans-serif", "fontSize": "15px", "fontWeight": 600, "color": C["text"], "background": f"linear-gradient(90deg, {C['primary']}22, transparent)", "borderBottom": "1px solid #2A2A3E"}),
                        dcc.Graph(id="graph-credito", style={"height": "320px", "margin": "0"}),
                    ],
                ),
                html.Div(
                    style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px", "marginBottom": "20px"},
                    children=[
                        html.Div(
                            style={"backgroundColor": C["card"], "borderRadius": "12px", "overflow": "hidden"},
                            children=[
                                html.Div("Crédito por Tipo", style={"padding": "14px 20px", "fontFamily": "'Space Grotesk', sans-serif", "fontSize": "15px", "fontWeight": 600, "color": C["text"], "background": f"linear-gradient(90deg, {C['secondary']}22, transparent)", "borderBottom": "1px solid #2A2A3E"}),
                                dcc.Graph(id="graph-tipo-credito", style={"height": "320px"}),
                            ],
                        ),
                        html.Div(
                            style={"backgroundColor": C["card"], "borderRadius": "12px", "overflow": "hidden"},
                            children=[
                                html.Div("MN vs ME", style={"padding": "14px 20px", "fontFamily": "'Space Grotesk', sans-serif", "fontSize": "15px", "fontWeight": 600, "color": C["text"], "background": f"linear-gradient(90deg, {C['accent1']}22, transparent)", "borderBottom": "1px solid #2A2A3E"}),
                                dcc.Graph(id="graph-mn-me", style={"height": "320px"}),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    style={"backgroundColor": C["card"], "borderRadius": "12px", "overflow": "hidden"},
                    children=[
                        html.Div("Tasas e IPC", style={"padding": "14px 20px", "fontFamily": "'Space Grotesk', sans-serif", "fontSize": "15px", "fontWeight": 600, "color": C["text"], "background": f"linear-gradient(90deg, {C['accent2']}22, transparent)", "borderBottom": "1px solid #2A2A3E"}),
                        dcc.Graph(id="graph-tasas", style={"height": "360px"}),
                    ],
                ),
            ],
        ),
        # Footer
        html.Div(
            style={"textAlign": "center", "padding": "20px", "borderTop": "1px solid #2A2A3E", "color": C["gray"], "fontSize": "12px"},
            children=[
                "Sebastian Porras · ",
                html.A("LinkedIn", href="https://www.linkedin.com/in/sebastian-porras-b98430376/", style={"color": C["primary"], "textDecoration": "none"}),
                " · BCRP",
            ],
        ),
    ],
    style={"backgroundColor": C["bg"], "color": C["text"], "fontFamily": "'Outfit', sans-serif", "minHeight": "100vh", "fontSize": "14px"},
)

# --- Callbacks ---

@app.callback(
    [Output("kpi-credito", "children"), Output("kpi-tpm", "children"), Output("kpi-ipc", "children"), Output("kpi-crecimiento", "children")],
    [Input("date-range", "start_date"), Input("date-range", "end_date")],
)
def update_kpis(start, end):
    mask = (credito_total["fecha"] >= start) & (credito_total["fecha"] <= end)
    df_f = credito_total[mask]
    if df_f.empty:
        return [html.Div([html.Div("Sin datos")])] * 4
    ultimo = df_f["valor"].iloc[-1]
    primero = df_f["valor"].iloc[0]
    crec = ((ultimo / primero) - 1) * 100 if primero > 0 else 0
    tpm_act = tpm[(tpm["fecha"] >= start) & (tpm["fecha"] <= end)]
    tpm_val = tpm_act["valor"].iloc[-1] if not tpm_act.empty else 0
    ipc_f = ipc_df[(ipc_df["fecha"] >= start) & (ipc_df["fecha"] <= end)]
    ipc_val = ipc_f["valor"].iloc[-1] if not ipc_f.empty else 0
    def kpi(label, value, color, suffix=""):
        return html.Div([
            html.Div(label, style={"fontSize": "11px", "color": C["gray"], "textTransform": "uppercase", "letterSpacing": "0.5px"}),
            html.Div(f"{value}{suffix}", style={"fontSize": "22px", "fontWeight": "700", "color": color, "fontFamily": "'Space Grotesk', sans-serif"}),
        ])
    return [
        kpi("Crédito Total", f"S/ {ultimo:,.0f}", C["primary"], "M"),
        kpi("TPM", f"{tpm_val:.2f}", C["secondary"], "%"),
        kpi("IPC", f"{ipc_val:.2f}", C["accent1"], ""),
        kpi("Crecimiento", f"{crec:+.1f}", C["accent2"] if crec > 0 else C["danger"], "%"),
    ]

@app.callback(Output("graph-credito", "figure"), [Input("date-range", "start_date"), Input("date-range", "end_date")])
def plot_credito(start, end):
    mask = (credito_total["fecha"] >= start) & (credito_total["fecha"] <= end)
    df = credito_total[mask]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["fecha"], y=df["valor"], mode="lines+markers", name="Crédito Total", line=dict(color=C["primary"], width=2.5), marker=dict(size=4, color=C["primary"]), fill="tozeroy", fillcolor=f"rgba(95, 134, 174, 0.12)"))
    fig.update_layout(plot_bgcolor=C["card"], paper_bgcolor=C["card"], font=dict(color=C["text"]), margin=dict(l=40, r=20, t=10, b=30), xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#2A2A3E", title="Millones S/"), hovermode="x unified")
    return fig

@app.callback(Output("graph-tipo-credito", "figure"), [Input("date-range", "start_date"), Input("date-range", "end_date")])
def plot_tipo_credito(start, end):
    def f(df): return df[(df["fecha"] >= start) & (df["fecha"] <= end)]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=f(credito_emp)["fecha"], y=f(credito_emp)["valor"], mode="lines", name="Empresas", line=dict(color=C["primary"], width=2.5)))
    fig.add_trace(go.Scatter(x=f(credito_cons)["fecha"], y=f(credito_cons)["valor"], mode="lines", name="Consumo", line=dict(color=C["secondary"], width=2.5)))
    fig.add_trace(go.Scatter(x=f(credito_hipo)["fecha"], y=f(credito_hipo)["valor"], mode="lines", name="Hipotecario", line=dict(color=C["accent1"], width=2.5)))
    fig.update_layout(plot_bgcolor=C["card"], paper_bgcolor=C["card"], font=dict(color=C["text"]), margin=dict(l=40, r=20, t=10, b=30), xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#2A2A3E", title="Millones S/"), legend=dict(orientation="h", y=1.08, x=0, font=dict(size=11)), hovermode="x unified")
    return fig

@app.callback([Output("graph-mn-me", "figure"), Output("graph-tasas", "figure")], [Input("date-range", "start_date"), Input("date-range", "end_date"), Input("tasa-selector", "value")])
def plot_resto(start, end, tasa_sel):
    mn_f = credito_mn[(credito_mn["fecha"] >= start) & (credito_mn["fecha"] <= end)]
    me_f = credito_me[(credito_me["fecha"] >= start) & (credito_me["fecha"] <= end)]
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(go.Scatter(x=mn_f["fecha"], y=mn_f["valor"], mode="lines", name="MN (S/)", line=dict(color=C["primary"], width=2.5)), secondary_y=False)
    fig1.add_trace(go.Scatter(x=me_f["fecha"], y=me_f["valor"], mode="lines", name="ME (US$)", line=dict(color=C["secondary"], width=2, dash="dash")), secondary_y=True)
    fig1.update_layout(plot_bgcolor=C["card"], paper_bgcolor=C["card"], font=dict(color=C["text"]), margin=dict(l=40, r=20, t=10, b=30), legend=dict(orientation="h", y=1.08, x=0), hovermode="x unified")
    fig1.update_xaxes(showgrid=False)
    fig1.update_yaxes(showgrid=True, gridcolor="#2A2A3E")
    fig1.update_yaxes(title_text="Millones S/", secondary_y=False)
    fig1.update_yaxes(title_text="Millones US$", secondary_y=True)
    tpm_f = tpm[(tpm["fecha"] >= start) & (tpm["fecha"] <= end)]
    ipc_f = ipc_df[(ipc_df["fecha"] >= start) & (ipc_df["fecha"] <= end)]
    mapa = {"tpm": ("TPM", tpm_f, C["primary"]), "corp": ("Activa Corporativos", tasa_corp[(tasa_corp["fecha"] >= start) & (tasa_corp["fecha"] <= end)], C["secondary"]), "gdes": ("Grandes Empresas", tasa_gdes[(tasa_gdes["fecha"] >= start) & (tasa_gdes["fecha"] <= end)], C["accent1"]), "pas": ("Pasiva Ahorro", tasa_pas[(tasa_pas["fecha"] >= start) & (tasa_pas["fecha"] <= end)], C["gray"])}
    fig2 = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)
    nombre_sel, df_sel, color_sel = mapa[tasa_sel]
    fig2.add_trace(go.Scatter(x=df_sel["fecha"], y=df_sel["valor"], mode="lines", name=nombre_sel, line=dict(color=color_sel, width=2.5)), row=1, col=1)
    fig2.add_trace(go.Scatter(x=tpm_f["fecha"], y=tpm_f["valor"], mode="lines", name="TPM (ref)", line=dict(color=C["gray"], width=1.2, dash="dot")), row=1, col=1)
    fig2.add_trace(go.Scatter(x=ipc_f["fecha"], y=ipc_f["valor"], mode="lines", name="IPC", line=dict(color=C["primary"], width=2), fill="tozeroy", fillcolor=f"rgba(95, 134, 174, 0.08)"), row=2, col=1)
    fig2.update_layout(plot_bgcolor=C["card"], paper_bgcolor=C["card"], font=dict(color=C["text"]), margin=dict(l=40, r=20, t=10, b=30), hovermode="x unified")
    fig2.update_xaxes(showgrid=False)
    fig2.update_yaxes(showgrid=True, gridcolor="#2A2A3E")
    fig2.update_yaxes(title_text="%", row=1, col=1)
    fig2.update_yaxes(title_text="Índice", row=2, col=1)
    for fig in [fig1, fig2]:
        fig.update_layout(legend=dict(orientation="h", y=1.08, x=0, font=dict(size=11)))
    return fig1, fig2

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
