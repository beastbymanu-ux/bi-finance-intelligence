import streamlit as st
import json, time
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date

st.set_page_config(
    page_title="Financial Intelligence Pipeline",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load():
    with open("/app/data/demo_data.json") as f:
        return json.load(f)

d        = load()
kpis     = d["kpis"]
monthly  = d["monthly_summary"]
balances = d["daily_balances"]
forecast = d["forecast"]
txns     = d["transactions"]
sources  = d["sources"]

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Financial Intelligence")
    st.caption("Automated Reporting & Cash Flow Pipeline")
    st.divider()
    st.markdown("### Pipeline Status")
    for src, meta in sources.items():
        dot = f'<span style="color:{meta["color"]}">&#9679;</span>'
        st.markdown(f"{dot} **{meta['label']}** &mdash; Synced", unsafe_allow_html=True)
    st.divider()
    st.markdown("### Last Reconciliation")
    st.success("2026-04-01 06:00 UTC\n✅ 0 errors detected")
    st.metric("Transactions processed", f"{kpis['transactions_total']:,}")
    st.metric("Data sources active", kpis["data_sources"])
    st.divider()
    st.markdown("### Infrastructure")
    st.code("SQLite (on-premise)\nSQLAlchemy ORM\nFastAPI REST layer\nDocker on Vultr VPS", language="text")
    st.caption("Zero financial data leaves the server")
    st.caption("Built by [Manu](https://openclawlabs-pipeline.duckdns.org)")

# ── Header ───────────────────────────────────────────────────
st.title("📊 Financial Intelligence Pipeline")
st.markdown("**Private automated reporting** — 5 data sources · 423 transactions reconciled · 90-day forecast · zero manual work")
st.divider()

# ── KPIs ─────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Current Balance",    f"€{kpis['current_balance']:,.0f}")
k2.metric("Avg Monthly Inflow", f"€{kpis['avg_monthly_inflow']:,.0f}", "+vs last qtr")
k3.metric("Avg Monthly Net",    f"€{kpis['avg_monthly_net']:,.0f}")
k4.metric("Runway",             f"{kpis['runway_months']} mo" if kpis["runway_months"] < 99 else "Profitable", "healthy")
k5.metric("Recon. Errors",      kpis["reconciliation_errors"], "was 12/mo manual")
st.divider()

# ── Tabs ─────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["💰 Cash Flow", "🔮 Forecast", "🗂️ Transactions", "🏗️ Architecture"])

# ══════════════ TAB 1 — CASH FLOW ════════════════════════════
with tab1:
    st.subheader("Monthly Cash Flow — Oct 2025 → Mar 2026")

    df_m = pd.DataFrame(monthly)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_m["month"], y=df_m["inflow"],  name="Inflow",  marker_color="#00d4aa"))
    fig.add_trace(go.Bar(x=df_m["month"], y=df_m["outflow"], name="Outflow", marker_color="#FF4444"))
    fig.add_trace(go.Scatter(x=df_m["month"], y=df_m["net"], name="Net",
                             mode="lines+markers", line=dict(color="#4C9EFF", width=3),
                             marker=dict(size=8)))
    fig.update_layout(barmode="group", plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
                      font_color="white", legend=dict(bgcolor="#1a1a2e"),
                      yaxis_title="EUR", xaxis_title="Month")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Running Balance — Daily")
    df_b = pd.DataFrame(balances)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df_b["date"], y=df_b["balance"], fill="tozeroy",
                              fillcolor="rgba(0,212,170,0.15)", line=dict(color="#00d4aa", width=2),
                              name="Balance"))
    fig2.add_hline(y=df_b["balance"].mean(), line_dash="dash",
                   line_color="#FF9900", annotation_text="6-month avg")
    fig2.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
                       font_color="white", yaxis_title="EUR", xaxis_title="Date")
    st.plotly_chart(fig2, use_container_width=True)

# ══════════════ TAB 2 — FORECAST ══════════════════════════════
with tab2:
    st.subheader("90-Day Cash Flow Forecast")
    st.caption("Projection based on 3-month rolling average net cash flow")

    df_hist = pd.DataFrame(balances[-30:])
    df_fore = pd.DataFrame(forecast)

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df_hist["date"], y=df_hist["balance"],
                              name="Actual (last 30d)", line=dict(color="#00d4aa", width=2)))
    fig3.add_trace(go.Scatter(x=df_fore["date"], y=df_fore["projected_balance"],
                              name="Forecast (90d)", line=dict(color="#4C9EFF", width=2, dash="dot"),
                              fill="tozeroy", fillcolor="rgba(76,158,255,0.08)"))
    fig3.add_shape(type="line", x0="2026-04-01", x1="2026-04-01",
                   y0=0, y1=1, yref="paper",
                   line=dict(color="#FF9900", width=2, dash="dash"))
    fig3.add_annotation(x="2026-04-01", y=1, yref="paper",
                        text="Today", showarrow=False,
                        font=dict(color="#FF9900"), xanchor="left")
    fig3.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
                       font_color="white", yaxis_title="EUR (projected)")
    st.plotly_chart(fig3, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    end_balance = forecast[-1]["projected_balance"]
    col1.metric("Projected Balance (90d)", f"€{end_balance:,.0f}")
    col2.metric("Avg Monthly Net",         f"€{kpis['avg_monthly_net']:,.0f}")
    col3.metric("Confidence",              "Medium", "Based on 6-month history")

    st.info("**Methodology:** Prophet-style rolling average on 90-day window. "
            "In production: swap with Facebook Prophet or ARIMA for seasonality. "
            "All computation on-premise — no data sent to external forecast APIs.")

# ══════════════ TAB 3 — TRANSACTIONS ══════════════════════════
with tab3:
    st.subheader("Transaction Ledger — Last 60 Entries")

    source_filter = st.multiselect("Filter by source:",
                                    list(set(t["source"] for t in txns)),
                                    default=list(set(t["source"] for t in txns)))
    type_filter = st.radio("Type:", ["All", "Inflow only", "Outflow only"], horizontal=True)

    filtered = [t for t in txns if t["source"] in source_filter]
    if type_filter == "Inflow only":  filtered = [t for t in filtered if t["type"] == "inflow"]
    if type_filter == "Outflow only": filtered = [t for t in filtered if t["type"] == "outflow"]

    for t in reversed(filtered[-30:]):
        amt   = t["amount"]
        color = "#00d4aa" if t["type"] == "inflow" else "#FF4444"
        sign  = "+" if t["type"] == "inflow" else ""
        src_meta = sources.get(t["source"], {})
        src_color = src_meta.get("color", "#888")
        td, tdesc = t["date"], t["description"]
        st.markdown(
            f"""<div style="display:flex;justify-content:space-between;padding:6px 10px;
            margin:3px 0;background:#1a1a2e;border-radius:4px;border-left:3px solid {src_color}">
            <span style="color:#FFFFFF"><b>{td}</b> &nbsp; {tdesc}</span>
            <span style="color:{color};font-weight:bold">{sign}€{abs(amt):,.2f}</span>
            </div>""", unsafe_allow_html=True)

    if st.button("⚡ Simulate Reconciliation Cycle", type="primary"):
        bar  = st.progress(0)
        stat = st.empty()
        steps = [
            (12, "Connecting to ERP via SQLAlchemy ORM..."),
            (24, "Fetching invoice batch — 47 new records..."),
            (36, "Connecting to bank feed (OFX parser)..."),
            (50, "Fetching bank statement — 23 new transactions..."),
            (62, "Fetching Stripe settlements via API..."),
            (74, "Running reconciliation algorithm — matching 70 records..."),
            (84, "Detecting duplicates and anomalies..."),
            (92, "Writing reconciled data to SQLite..."),
            (100,"Updating forecast model — 0 errors detected."),
        ]
        for pct, msg in steps:
            bar.progress(pct); stat.markdown(f"`{msg}`"); time.sleep(0.35)
        st.success("Reconciliation complete — 70 transactions processed · 0 errors · ledger updated")

# ══════════════ TAB 4 — ARCHITECTURE ══════════════════════════
with tab4:
    st.subheader("🏗️ System Architecture")
    col_l, col_r = st.columns([3, 2])
    with col_l:
        st.code("""
[DATA SOURCES]
  ERP (SAP / Odoo / custom)   --> SQLAlchemy adapter
  Bank feeds (OFX/MT940)      --> OFX parser
  Stripe API                  --> REST webhook receiver
  Other APIs (Xero, QB)       --> FastAPI connectors
        |
        v
[INGESTION LAYER]             FastAPI background tasks
  - Scheduled pulls (cron)    every 6h
  - Webhook receivers         real-time
  - Duplicate detection       SHA-256 hash per transaction
        |
        v
[STORAGE]                     SQLite via SQLAlchemy ORM
  Tables: transactions        unified ledger
           accounts           chart of accounts
           reconciliations    audit trail
           forecasts          model outputs
        |
        v
[PROCESSING]
  Reconciliation engine       match ERP <-> bank <-> Stripe
  Anomaly detection           flag duplicates / gaps
  Forecast model              rolling average / Prophet
        |
        v
[OUTPUT LAYER]
  FastAPI REST                /metrics /transactions /forecast
  Streamlit dashboard         CFO-facing, always live
  Discord alerts              anomalies above threshold
  PDF export                  monthly board report (auto)

DATA BOUNDARY: all processing on client-owned Vultr VPS.
               No financial data sent to external servers.
        """, language="text")
    with col_r:
        st.markdown("### ROI Summary")
        roi = {
            "Manual reconciliation time":  "20h/mo → 0h",
            "Human error rate":            "~3% → 0%",
            "Report generation":           "2 days → real-time",
            "Data sources unified":        "5 silos → 1 ledger",
            "Monthly SaaS tools replaced": "€400/mo → €0",
            "Setup investment":            "€4,200 one-time",
            "Payback period":              "11 days",
        }
        for k, v in roi.items():
            st.markdown(f"**{k}**  \n`{v}`"); st.divider()

st.divider()
st.caption("Built by Manu · Private AI Infrastructure · Available for similar engagements · [openclawlabs-pipeline.duckdns.org](https://openclawlabs-pipeline.duckdns.org)")
