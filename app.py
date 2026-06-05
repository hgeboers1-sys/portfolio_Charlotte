import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

NAME       = "Charlotte"
ACCENT     = "#38bdf8"
ACCENT2    = "#0ea5e9"
BG         = "linear-gradient(135deg,#0c1a2e 0%,#1e3a5f 50%,#0f2340 100%)"
BADGE_COL  = "#93c5fd"
FILL_COL   = "rgba(56,189,248,0.15)"

st.set_page_config(page_title=f"{NAME} — Birthday Portfolio", page_icon="🎂",
                   layout="centered", initial_sidebar_state="collapsed")

st.markdown(f"""
<style>
  #MainMenu, footer, header {{ display:none!important }}
  .stDeployButton {{ display:none }}
  .stApp {{ background:{BG} }}
  .block-container {{ padding-top:2.5rem; padding-bottom:3rem; max-width:620px }}

  .badge {{
    display:inline-block; background:rgba(255,255,255,.08);
    border:1px solid rgba(255,255,255,.15); border-radius:40px;
    padding:5px 18px; font-size:12px; font-weight:500;
    letter-spacing:.06em; text-transform:uppercase; color:{BADGE_COL};
    margin-bottom:14px;
  }}
  h1.hero {{
    font-size:clamp(36px,8vw,58px); font-weight:800; margin:0 0 8px;
    background:linear-gradient(90deg,{ACCENT},{ACCENT2});
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text;
  }}
  .sub {{ font-size:15px; color:rgba(255,255,255,.5); margin-bottom:0 }}

  .pcard {{
    background:rgba(255,255,255,.07); border:1px solid rgba(255,255,255,.12);
    border-radius:22px; padding:26px 22px; margin-bottom:16px;
  }}
  .card-lbl {{
    font-size:11px; font-weight:600; letter-spacing:.1em;
    text-transform:uppercase; color:rgba(255,255,255,.35); margin-bottom:16px;
  }}
  .holding {{
    display:flex; align-items:center; justify-content:space-between;
    padding:11px 13px; border-radius:11px;
    background:rgba(255,255,255,.05); margin-bottom:8px;
  }}
  .h-left {{ display:flex; flex-direction:column; gap:2px }}
  .ticker {{ font-size:14px; font-weight:700; letter-spacing:.04em; color:#fff }}
  .hname  {{ font-size:11px; color:rgba(255,255,255,.4) }}
  .hprice {{ font-size:16px; font-weight:600; color:#fff }}
  .divider {{ height:1px; background:rgba(255,255,255,.07); margin:14px 0 }}
  .trow {{ display:flex; justify-content:space-between; align-items:baseline }}
  .tlbl {{ font-size:14px; color:rgba(255,255,255,.5) }}
  .tval {{ font-size:34px; font-weight:800; color:{ACCENT} }}
  .gbadge {{
    display:inline-block; margin-top:9px; font-size:12px; font-weight:600;
    padding:3px 11px; border-radius:20px;
    background:rgba(110,231,183,.12); color:#6ee7b7;
  }}

  .stats-row {{
    display:grid; grid-template-columns:1fr 1fr; gap:13px; margin-bottom:16px;
  }}
  .scard {{
    background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.07);
    border-radius:16px; padding:17px; text-align:center;
  }}
  .sval {{
    font-size:22px; font-weight:800;
    background:linear-gradient(90deg,{ACCENT},{ACCENT2});
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text;
  }}
  .slbl {{
    font-size:11px; color:rgba(255,255,255,.35); font-weight:500;
    text-transform:uppercase; letter-spacing:.06em; margin-top:4px;
  }}

  .chart-wrap {{
    background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.07);
    border-radius:20px; padding:20px 16px 12px; margin-bottom:16px;
  }}
  .ctitle {{ font-size:15px; font-weight:700; color:#fff; margin-bottom:3px }}
  .csub   {{ font-size:12px; color:rgba(255,255,255,.35) }}

  .etf-grid {{
    display:grid; grid-template-columns:1fr 1fr; gap:13px; margin-bottom:16px;
  }}
  .ecard {{
    background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.07);
    border-radius:14px; padding:15px 17px;
  }}
  .eticker {{ font-size:17px; font-weight:800; color:#fff; margin-bottom:2px }}
  .ename  {{ font-size:11px; color:rgba(255,255,255,.35); line-height:1.4; margin-bottom:9px }}
  .estat  {{ display:flex; justify-content:space-between; font-size:12px; margin-bottom:5px }}
  .ek {{ color:rgba(255,255,255,.35) }}
  .ev {{ font-weight:600; color:#fff }}
  .green {{ color:#6ee7b7!important }}

  .foot {{ text-align:center; font-size:11px; color:rgba(255,255,255,.2); line-height:1.7; margin-top:24px }}

  .tx-table {{
    width:100%; border-collapse:collapse; margin-bottom:16px;
    background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.07);
    border-radius:16px; overflow:hidden;
  }}
  .tx-table th {{
    font-size:10px; font-weight:600; letter-spacing:.08em; text-transform:uppercase;
    color:rgba(255,255,255,.35); padding:11px 14px; text-align:left;
    border-bottom:1px solid rgba(255,255,255,.07);
  }}
  .tx-table td {{
    font-size:13px; color:rgba(255,255,255,.75); padding:10px 14px;
    border-bottom:1px solid rgba(255,255,255,.05);
  }}
  .tx-table tr:last-child td {{ border-bottom:none }}
  .tx-buy  {{ display:inline-block; padding:2px 9px; border-radius:10px; font-size:11px;
              font-weight:600; background:rgba(110,231,183,.12); color:#6ee7b7; }}
  .tx-sell {{ display:inline-block; padding:2px 9px; border-radius:10px; font-size:11px;
              font-weight:600; background:rgba(248,113,113,.12); color:#f87171; }}
  .tx-section-lbl {{
    font-size:11px; font-weight:600; letter-spacing:.1em; text-transform:uppercase;
    color:rgba(255,255,255,.35); margin-bottom:10px; margin-top:4px;
  }}
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=3600, show_spinner=False)
def load_data():
    iwda = yf.Ticker("IWDA.AS").history(period="5y", interval="1wk")["Close"].dropna()
    sema = yf.Ticker("SEMA.MI").history(period="5y", interval="1wk")["Close"].dropna()
    df = pd.DataFrame({"IWDA": iwda, "SEMA": sema}).dropna()
    df.index = pd.to_datetime(df.index).tz_localize(None)
    df["Total"] = df["IWDA"] + df["SEMA"]
    return df


with st.spinner("Fetching live prices…"):
    df = load_data()

iwda_cur   = df["IWDA"].iloc[-1]
sema_cur   = df["SEMA"].iloc[-1]
total_cur  = df["Total"].iloc[-1]
iwda_start = df["IWDA"].iloc[0]
sema_start = df["SEMA"].iloc[0]
total_start = df["Total"].iloc[0]

# P&L since first purchase (21 May 2026)
IWDA_COST      = 121.52                              # 1 share
SEMA_COST      = 53.90                               # 1 share
COST_BASIS     = IWDA_COST + SEMA_COST

pnl_eur        = total_cur - COST_BASIS
pnl_pct        = pnl_eur / COST_BASIS * 100
pnl_sign       = "+" if pnl_eur >= 0 else ""
pnl_color      = "#6ee7b7" if pnl_eur >= 0 else "#f87171"

# Per-holding P&L
pnl_iwda       = iwda_cur - IWDA_COST
pnl_iwda_pct   = pnl_iwda / IWDA_COST * 100
pnl_iwda_col   = "#6ee7b7" if pnl_iwda >= 0 else "#f87171"
pnl_iwda_sign  = "+" if pnl_iwda >= 0 else ""

pnl_sema       = sema_cur - SEMA_COST
pnl_sema_pct   = pnl_sema / SEMA_COST * 100
pnl_sema_col   = "#6ee7b7" if pnl_sema >= 0 else "#f87171"
pnl_sema_sign  = "+" if pnl_sema >= 0 else ""

def pct(cur, start):
    g = (cur - start) / start * 100
    return f"{'+'if g>=0 else ''}{g:.1f}%"

# ── Header ──────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;margin-bottom:36px">
  <div class="badge">🎂 Happy 13th Birthday — May 22, 2026</div>
  <h1 class="hero">{NAME}</h1>
  <p class="sub">Your very first investment portfolio</p>
</div>
""", unsafe_allow_html=True)

# ── Portfolio card ───────────────────────────────────────────────
st.markdown(f"""
<div class="pcard">
  <div class="card-lbl">My Portfolio</div>
  <div class="holding">
    <div class="h-left">
      <span class="ticker">IWDA</span>
      <span class="hname">iShares MSCI World · 1 share · bought € {IWDA_COST:.2f}</span>
    </div>
    <div style="text-align:right">
      <div class="hprice">€ {iwda_cur:.2f}</div>
      <div style="font-size:11px;color:{pnl_iwda_col};margin-top:2px">{pnl_iwda_sign}€ {pnl_iwda:.2f} ({pnl_iwda_sign}{pnl_iwda_pct:.1f}%)</div>
    </div>
  </div>
  <div class="holding">
    <div class="h-left">
      <span class="ticker">SEMA</span>
      <span class="hname">iShares Emerging Markets · 1 share · bought € {SEMA_COST:.2f}</span>
    </div>
    <div style="text-align:right">
      <div class="hprice">€ {sema_cur:.2f}</div>
      <div style="font-size:11px;color:{pnl_sema_col};margin-top:2px">{pnl_sema_sign}€ {pnl_sema:.2f} ({pnl_sema_sign}{pnl_sema_pct:.1f}%)</div>
    </div>
  </div>
  <div class="divider"></div>
  <div class="trow">
    <span class="tlbl">Total value today</span>
    <span class="tval">€ {total_cur:.2f}</span>
  </div>
  <div class="trow" style="margin-top:10px">
    <span class="tlbl">Invested (cost basis)</span>
    <span style="font-size:18px;font-weight:600;color:rgba(255,255,255,.6)">€ {COST_BASIS:.2f}</span>
  </div>
  <div class="divider"></div>
  <div class="trow">
    <span class="tlbl">P&amp;L since 21 May 2026</span>
    <span style="font-size:28px;font-weight:800;color:{pnl_color}">{pnl_sign}€ {pnl_eur:.2f}</span>
  </div>
  <div class="gbadge" style="background:{'rgba(110,231,183,.12)' if pnl_eur>=0 else 'rgba(248,113,113,.12)'};color:{pnl_color}">{pnl_sign}{pnl_pct:.1f}% since 21 May 2026</div>
</div>
""", unsafe_allow_html=True)

# ── Stats ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stats-row">
  <div class="scard">
    <div class="sval" style="color:{pnl_color}">{pnl_sign}€ {pnl_eur:.2f}</div>
    <div class="slbl">P&amp;L since 21 May 2026</div>
  </div>
  <div class="scard">
    <div class="sval" style="color:{pnl_color}">{pnl_sign}{pnl_pct:.1f}%</div>
    <div class="slbl">Return on investment</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Chart ────────────────────────────────────────────────────────
baseline = df["Total"].min() * 0.96
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df.index, y=[baseline] * len(df),
    mode="lines", line=dict(color="rgba(0,0,0,0)"),
    showlegend=False, hoverinfo="skip"
))
fig.add_trace(go.Scatter(
    x=df.index, y=df["Total"],
    fill="tonexty", fillcolor=FILL_COL,
    line=dict(color=ACCENT, width=2.5),
    name="Total portfolio",
    hovertemplate="<b>Total</b>  € %{y:.2f}<extra></extra>"
))
fig.add_trace(go.Scatter(
    x=df.index, y=df["IWDA"],
    line=dict(color="#60a5fa", width=1.5),
    name="IWDA",
    hovertemplate="<b>IWDA</b>  € %{y:.2f}<extra></extra>"
))
fig.add_trace(go.Scatter(
    x=df.index, y=df["SEMA"],
    line=dict(color="#34d399", width=1.5),
    name="SEMA",
    hovertemplate="<b>SEMA</b>  € %{y:.2f}<extra></extra>"
))

# Buy marker
fig.add_vline(
    x=pd.Timestamp("2026-05-21"),
    line_width=1.5, line_dash="dot",
    line_color="rgba(255,255,255,0.25)",
    annotation_text="Bought IWDA + SEMA",
    annotation_position="top left",
    annotation_font_color="rgba(255,255,255,0.45)",
    annotation_font_size=10,
)

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="rgba(255,255,255,0.5)", size=11),
    hovermode="x unified",
    hoverlabel=dict(bgcolor="rgba(15,12,41,0.95)", font_color="#fff", bordercolor="rgba(255,255,255,0.15)"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                font=dict(color="rgba(255,255,255,0.6)", size=12)),
    xaxis=dict(
        showgrid=True, gridcolor="rgba(255,255,255,0.05)",
        tickfont=dict(color="rgba(255,255,255,0.4)"),
        rangeslider=dict(visible=False),
        rangeselector=dict(
            buttons=[
                dict(count=1,  label="1M", step="month",  stepmode="backward"),
                dict(count=6,  label="6M", step="month",  stepmode="backward"),
                dict(count=1,  label="1Y", step="year",   stepmode="backward"),
                dict(count=2,  label="2Y", step="year",   stepmode="backward"),
                dict(count=5,  label="5Y", step="year",   stepmode="backward"),
                dict(step="all", label="All"),
            ],
            bgcolor="rgba(255,255,255,0.06)",
            activecolor="rgba(56,189,248,0.35)",
            font=dict(color="rgba(255,255,255,0.7)", size=12),
            x=0, y=1.12,
        ),
    ),
    yaxis=dict(
        showgrid=True, gridcolor="rgba(255,255,255,0.05)",
        tickprefix="€", side="right",
        tickfont=dict(color="rgba(255,255,255,0.4)"),
    ),
    margin=dict(l=0, r=0, t=50, b=0),
    height=340,
)

st.markdown('<div class="chart-wrap"><div class="ctitle">Portfolio value over time</div><div class="csub">1 share IWDA + 1 share SEMA · weekly close · EUR</div>', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

# ── ETF info ─────────────────────────────────────────────────────
st.markdown(f"""
<div class="etf-grid">
  <div class="ecard">
    <div class="eticker">IWDA</div>
    <div class="ename">iShares Core MSCI World UCITS ETF<br>Euronext Amsterdam · EUR</div>
    <div class="estat"><span class="ek">Price today</span><span class="ev">€ {iwda_cur:.2f}</span></div>
    <div class="estat"><span class="ek">5Y return</span><span class="ev green">{pct(iwda_cur, iwda_start)}</span></div>
    <div class="estat"><span class="ek">Covers</span><span class="ev">~1,400 companies</span></div>
    <div class="estat"><span class="ek">Region</span><span class="ev">Developed world</span></div>
  </div>
  <div class="ecard">
    <div class="eticker">SEMA</div>
    <div class="ename">iShares MSCI EM UCITS ETF (Acc)<br>Euronext Milan · EUR</div>
    <div class="estat"><span class="ek">Price today</span><span class="ev">€ {sema_cur:.2f}</span></div>
    <div class="estat"><span class="ek">5Y return</span><span class="ev green">{pct(sema_cur, sema_start)}</span></div>
    <div class="estat"><span class="ek">Covers</span><span class="ev">~1,300 companies</span></div>
    <div class="estat"><span class="ek">Region</span><span class="ev">Emerging markets</span></div>
  </div>
</div>
<div class="foot">
  Prices update automatically · Data via Yahoo Finance<br>
  Past performance does not guarantee future results.
</div>
""", unsafe_allow_html=True)

# ── Transaction history ──────────────────────────────────────────
TRANSACTIONS = [
    {"date": "21 May 2026", "type": "Buy", "product": "IWDA", "name": "iShares MSCI World", "qty": 1, "price": 121.52},
    {"date": "21 May 2026", "type": "Buy", "product": "SEMA", "name": "iShares Emerging Markets", "qty": 1, "price": 53.90},
]

rows = ""
for tx in TRANSACTIONS:
    badge = f'<span class="tx-buy">Buy</span>' if tx["type"] == "Buy" else f'<span class="tx-sell">Sell</span>'
    rows += f"""
    <tr>
      <td>{tx["date"]}</td>
      <td>{badge}</td>
      <td><b>{tx["product"]}</b><br><span style="font-size:11px;color:rgba(255,255,255,.35)">{tx["name"]}</span></td>
      <td style="text-align:center">{tx["qty"]}</td>
      <td style="text-align:right">€ {tx["price"]:.2f}</td>
      <td style="text-align:right">€ {tx["qty"] * tx["price"]:.2f}</td>
    </tr>"""

st.markdown(f"""
<div class="tx-section-lbl">Transaction history</div>
<table class="tx-table">
  <thead>
    <tr>
      <th>Date</th><th>Type</th><th>Product</th><th style="text-align:center">Qty</th>
      <th style="text-align:right">Price</th><th style="text-align:right">Total</th>
    </tr>
  </thead>
  <tbody>{rows}</tbody>
</table>
""", unsafe_allow_html=True)
