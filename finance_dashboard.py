"""
Rohan Bora — Personal Finance Dashboard  ·  Premium Dark Edition v2
Run: streamlit run finance_dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import re, os, hmac
from pathlib import Path

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RB Finance",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Dark Mode CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stHeader"] { display: none !important; }
.stDeployButton { display: none !important; }

/* ── Dark page ── */
.stApp { background: #060C18 !important; }
.block-container {
  background: transparent !important;
  padding: 0 2.2rem 4rem !important;
  max-width: 1480px !important;
}

/* ── Dark sidebar ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #030810 0%, #06101E 100%) !important;
  border-right: 1px solid rgba(59,130,246,0.12) !important;
}
[data-testid="stSidebar"] * { color: #94A3B8 !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #E2E8F0 !important; font-weight: 700 !important; }
[data-testid="stSidebar"] label { color: #94A3B8 !important; font-size: 13px !important; }
[data-testid="stSidebar"] input {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(59,130,246,0.2) !important;
  color: #E2E8F0 !important; border-radius: 8px !important;
  font-size: 14px !important; font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSidebar"] .stButton > button {
  background: linear-gradient(135deg, #1D4ED8 0%, #2563EB 100%) !important;
  color: white !important; border: none !important; border-radius: 10px !important;
  font-weight: 700 !important; font-size: 14px !important; width: 100% !important;
  padding: 12px !important; letter-spacing: 0.1px !important;
  box-shadow: 0 0 20px rgba(37,99,235,0.3), 0 4px 14px rgba(0,0,0,0.4) !important;
  transition: all 0.2s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  box-shadow: 0 0 28px rgba(37,99,235,0.5), 0 6px 20px rgba(0,0,0,0.5) !important;
  transform: translateY(-1px) !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploadDropzone"] {
  background: rgba(255,255,255,0.03) !important;
  border: 1px dashed rgba(59,130,246,0.25) !important;
  border-radius: 10px !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] {
  background: rgba(37,99,235,0.2) !important; color: #60A5FA !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(59,130,246,0.2) !important; border-radius: 8px !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: #0A1628 !important;
  border: 1px solid rgba(59,130,246,0.15) !important;
  border-radius: 14px !important; padding: 6px !important; gap: 4px !important;
  box-shadow: 0 4px 24px rgba(0,0,0,0.4) !important; margin-bottom: 6px !important;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 10px !important; padding: 11px 24px !important;
  font-weight: 600 !important; font-size: 14px !important;
  color: #64748B !important; background: transparent !important;
  border: none !important; transition: all 0.2s !important; letter-spacing: -0.1px !important;
}
.stTabs [data-baseweb="tab"]:hover { color: #94A3B8 !important; background: rgba(255,255,255,0.04) !important; }
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, #1E3A8A 0%, #1D4ED8 100%) !important;
  color: #E0EEFF !important;
  box-shadow: 0 0 16px rgba(37,99,235,0.3), 0 4px 12px rgba(0,0,0,0.3) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── Info/alert boxes ── */
[data-testid="stAlert"] {
  background: rgba(59,130,246,0.08) !important;
  border: 1px solid rgba(59,130,246,0.2) !important;
  border-radius: 10px !important; color: #93C5FD !important; font-size: 14px !important;
}
[data-testid="stAlert"] * { color: #93C5FD !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] { border-radius: 12px !important; overflow: hidden !important; }
[data-testid="stDataFrame"] th { background: #0A1628 !important; color: #94A3B8 !important; font-size: 12px !important; }
[data-testid="stDataFrame"] td { background: #0D1829 !important; color: #CBD5E1 !important; font-size: 14px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #060C18; }
::-webkit-scrollbar-thumb { background: #1E3A5F; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #2563EB; }

/* ── Divider ── */
hr { border-color: rgba(59,130,246,0.12) !important; margin: 1rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Dark Plotly template ──────────────────────────────────────────────────────
FONT = "'DM Sans','Inter',sans-serif"
pio.templates["rb_dark"] = go.layout.Template(
    layout=go.Layout(
        font=dict(family=FONT, size=13, color="#94A3B8"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.06)",
                   zeroline=False, tickfont=dict(size=12, color="#64748B", family=FONT), showgrid=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", showline=False, zeroline=False,
                   tickfont=dict(size=12, color="#64748B", family=FONT),
                   tickprefix="$", separatethousands=True, showgrid=True),
        hoverlabel=dict(bgcolor="#0F1E35", font=dict(family=FONT, color="#E2E8F0", size=14),
                        bordercolor="rgba(59,130,246,0.4)"),
        legend=dict(font=dict(size=13, family=FONT, color="#94A3B8"), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=4, r=4, t=16, b=4),
    )
)

# ── Constants ─────────────────────────────────────────────────────────────────
CATS = ['Food','Groceries','Shopping','Rent','Personal','Travel','Entertainment','Other']
CAT_COLORS = {
    'Food':          '#FB923C',
    'Groceries':     '#34D399',
    'Shopping':      '#A78BFA',
    'Rent':          '#F87171',
    'Personal':      '#60A5FA',
    'Travel':        '#FBBF24',
    'Entertainment': '#F472B6',
    'Other':         '#94A3B8',
}
MONTH_MAP   = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,
               'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
MONTH_NAMES = {v:k.capitalize() for k,v in MONTH_MAP.items()}

# ── Baseline data (verified · 2025 rent ≥ $3,250/mo) ─────────────────────────
BASELINE = [
    dict(yr=2024,mo=1,  Food=46.11,  Groceries=0,      Shopping=0,      Rent=0,       Personal=279.32,  Travel=753.00,  Entertainment=4.98,   Other=0,       Income=0),
    dict(yr=2024,mo=2,  Food=25.12,  Groceries=0,      Shopping=0,      Rent=0,       Personal=142.40,  Travel=134.89,  Entertainment=187.82, Other=1116.44, Income=0),
    dict(yr=2024,mo=3,  Food=208.85, Groceries=225.39, Shopping=0,      Rent=0,       Personal=539.75,  Travel=450.38,  Entertainment=0,      Other=85.99,   Income=0),
    dict(yr=2024,mo=4,  Food=90.04,  Groceries=20.36,  Shopping=0,      Rent=0,       Personal=475.60,  Travel=458.87,  Entertainment=15.98,  Other=0,       Income=0),
    dict(yr=2024,mo=5,  Food=61.93,  Groceries=0,      Shopping=0,      Rent=0,       Personal=1274.61, Travel=2.80,    Entertainment=31.43,  Other=0,       Income=0),
    dict(yr=2024,mo=6,  Food=198.78, Groceries=0,      Shopping=0,      Rent=0,       Personal=359.16,  Travel=901.95,  Entertainment=40.45,  Other=474.89,  Income=0),
    dict(yr=2024,mo=7,  Food=170.06, Groceries=213.20, Shopping=0,      Rent=0,       Personal=192.44,  Travel=704.43,  Entertainment=54.42,  Other=12.78,   Income=0),
    dict(yr=2024,mo=8,  Food=133.63, Groceries=0,      Shopping=0,      Rent=0,       Personal=194.05,  Travel=367.39,  Entertainment=24.50,  Other=0,       Income=0),
    dict(yr=2024,mo=9,  Food=11.80,  Groceries=186.69, Shopping=0,      Rent=0,       Personal=716.14,  Travel=8.84,    Entertainment=57.94,  Other=0,       Income=0),
    dict(yr=2024,mo=10, Food=49.51,  Groceries=71.24,  Shopping=283.82, Rent=1081.91, Personal=94.34,   Travel=417.33,  Entertainment=0,      Other=0,       Income=0),
    dict(yr=2024,mo=11, Food=92.77,  Groceries=104.17, Shopping=389.52, Rent=0,       Personal=105.97,  Travel=320.48,  Entertainment=22.97,  Other=0,       Income=0),
    dict(yr=2024,mo=12, Food=35.57,  Groceries=161.00, Shopping=899.20, Rent=0,       Personal=178.00,  Travel=312.13,  Entertainment=15.97,  Other=774.18,  Income=0),
    dict(yr=2025,mo=1,  Food=280.66, Groceries=154.64, Shopping=717.21, Rent=3250.00, Personal=93.73,   Travel=74.44,   Entertainment=2.99,   Other=14.48,   Income=6720.74),
    dict(yr=2025,mo=2,  Food=84.96,  Groceries=395.99, Shopping=924.88, Rent=3250.00, Personal=104.55,  Travel=211.15,  Entertainment=36.97,  Other=0,       Income=2227.41),
    dict(yr=2025,mo=3,  Food=292.36, Groceries=230.15, Shopping=29.43,  Rent=3250.00, Personal=251.95,  Travel=15.59,   Entertainment=19.46,  Other=71.98,   Income=4633.42),
    dict(yr=2025,mo=4,  Food=319.05, Groceries=108.58, Shopping=540.33, Rent=3250.00, Personal=63.52,   Travel=65.13,   Entertainment=2.99,   Other=0,       Income=5016.18),
    dict(yr=2025,mo=5,  Food=248.09, Groceries=249.46, Shopping=0,      Rent=3358.34, Personal=138.69,  Travel=485.32,  Entertainment=22.99,  Other=0,       Income=4704.83),
    dict(yr=2025,mo=6,  Food=200.29, Groceries=22.87,  Shopping=56.09,  Rent=3250.00, Personal=240.83,  Travel=0,       Entertainment=10.99,  Other=0,       Income=4748.67),
    dict(yr=2025,mo=7,  Food=244.77, Groceries=283.31, Shopping=651.73, Rent=3380.62, Personal=56.94,   Travel=0,       Entertainment=67.98,  Other=0,       Income=4571.74),
    dict(yr=2025,mo=8,  Food=0,      Groceries=0,      Shopping=0,      Rent=3250.00, Personal=0,       Travel=0,       Entertainment=0,      Other=0,       Income=0),
    dict(yr=2025,mo=9,  Food=201.45, Groceries=299.92, Shopping=189.11, Rent=3387.32, Personal=80.83,   Travel=46.90,   Entertainment=0,      Other=504.12,  Income=2658.32),
    dict(yr=2025,mo=10, Food=72.94,  Groceries=318.58, Shopping=0,      Rent=3250.00, Personal=343.00,  Travel=1939.50, Entertainment=0,      Other=0,       Income=8822.58),
    dict(yr=2025,mo=11, Food=131.16, Groceries=121.30, Shopping=285.24, Rent=3250.00, Personal=312.41,  Travel=1274.06, Entertainment=30.00,  Other=0,       Income=5097.38),
    dict(yr=2025,mo=12, Food=241.76, Groceries=79.23,  Shopping=222.99, Rent=3414.80, Personal=389.29,  Travel=201.39,  Entertainment=34.00,  Other=1915.84, Income=1244.56),
    dict(yr=2026,mo=1,  Food=246.84, Groceries=305.80, Shopping=291.85, Rent=50.00,   Personal=241.56,  Travel=0,       Entertainment=0,      Other=0,       Income=5579.14),
    dict(yr=2026,mo=2,  Food=254.25, Groceries=204.54, Shopping=1016.04,Rent=40.00,   Personal=738.72,  Travel=0,       Entertainment=0,      Other=0,       Income=5613.22),
]

INCOME_2024 = [
    ("Amazon Development Center US Inc — W-2", "Box 1 · EIN 20-8424306 · NY",   "$59,723"),
    ("Simplicity First Solutions LLC — W-2",   "Box 1 · EIN 82-3220641 · CA",   "$3,000"),
    ("Robinhood — Short-Term Capital Gains",    "SOFI Technologies + Upstart",   "$3,027"),
    ("Robinhood — Long-Term Capital Gains",     "Net realized loss",             "−$124"),
    ("Robinhood — Interest Income",             "1099-INT",                      "$68"),
    ("Robinhood — Dividends",                   "1099-DIV",                      "$2"),
]
INCOME_2025 = [
    ("Amazon Development Center US Inc — W-2", "Box 1 · EIN 20-8424306 · NY",    "$58,189"),
    ("Amazon Com Services LLC — W-2",           "Box 1 · EIN 82-0544687 · NY",   "$29,931"),
    ("Robinhood — Short-Term Capital Gains",    "Proceeds $75,891 · Cost $38,193","$37,906"),
    ("Robinhood — Long-Term Capital Gains",     "Proceeds $3,300 · Cost $4,300", "$30"),
    ("Robinhood — Dividends",                   "1099-DIV",                      "$2"),
    ("Robinhood — Interest Income",             "1099-INT",                      "$278"),
    ("Cash App — Bitcoin 1099-DA",              "Gross proceeds only",           "$22"),
]

# ── Excel parser ──────────────────────────────────────────────────────────────
CAT_MAP = {
    'food':'Food','restaurants':'Food','restaurant':'Food','dining':'Food','coffee':'Food',
    'groceries':'Groceries','grocery':'Groceries','supermarket':'Groceries',
    'shopping':'Shopping','general merchandise':'Shopping','electronics':'Shopping','vanmoof':'Shopping',
    'rent':'Rent','bilt':'Rent',
    'personal':'Personal','personal care':'Personal','online services':'Personal','subscription':'Personal',
    'travel':'Travel','transportation':'Travel','airline':'Travel','hotel':'Travel','lyft':'Travel','uber':'Travel',
    'entertainment':'Entertainment','movies':'Entertainment','spotify':'Entertainment',
}
def _norm(desc, bank):
    for kw, cat in CAT_MAP.items():
        if kw in str(desc).lower(): return cat
    for kw, cat in CAT_MAP.items():
        if kw in str(bank).lower(): return cat
    return 'Other'

def _parse_sheet(df):
    try:
        hr = next((i for i,r in df.iterrows()
                   if 'date' in [str(v).lower().strip() for v in r.values]
                   and any(x in [str(v).lower().strip() for v in r.values] for x in ['amount','amount2'])), None)
        if hr is None: return None
        df.columns = [str(v).strip() for v in df.iloc[hr].values]
        df = df.iloc[hr+1:].reset_index(drop=True).dropna(how='all')
        cols = {c.lower():c for c in df.columns}
        totals = {c:0.0 for c in CATS}; income = 0.0
        for _, row in df.iterrows():
            amt = 0.0
            if 'amount2' in cols:
                try: amt = float(str(row[cols['amount2']]).replace('$','').replace(',',''))
                except: pass
            if amt == 0 and 'amount' in cols:
                try:
                    v = float(str(row[cols['amount']]).replace('$','').replace(',',''))
                    amt = abs(v) if v < 0 else 0
                except: pass
            if amt <= 0: continue
            cat = 'Other'
            if 'category' in cols and str(row[cols['category']]).strip() in CATS:
                cat = str(row[cols['category']]).strip()
            else:
                cat = _norm(row.get(cols.get('description',''),''), row.get(cols.get('bankcategory',''),''))
            if amt >= 3000 and cat == 'Other': cat = 'Rent'
            totals[cat] += amt
            if 'income' in cols:
                try: income += float(str(row[cols['income']]).replace('$','').replace(',',''))
                except: pass
        totals['Income'] = income
        return totals
    except: return None

@st.cache_data(show_spinner="Reading Excel…")
def load_excel(src):
    from io import BytesIO
    try: xl = pd.ExcelFile(src if isinstance(src,(str,Path)) else BytesIO(src.read()))
    except Exception as e: st.sidebar.warning(f"Could not read: {e}"); return BASELINE.copy()
    known = {(r['yr'],r['mo']):dict(r) for r in BASELINE}; new = 0
    for sh in xl.sheet_names:
        m = re.match(r'([A-Za-z]{3})\s*(\d{2})\b', sh.strip())
        if not m: continue
        ms, ys = m.group(1).lower(), int(m.group(2))
        if ms not in MONTH_MAP: continue
        mo, yr = MONTH_MAP[ms], 2000+ys
        if (yr,mo) in known: continue
        r = _parse_sheet(xl.parse(sh, header=None))
        if r: known[(yr,mo)] = dict(yr=yr,mo=mo,**r); new += 1
    if new: st.sidebar.success(f"✓ {new} new month(s) loaded")
    return sorted(known.values(), key=lambda r:(r['yr'],r['mo']))

@st.cache_data
def get_baseline(): return BASELINE.copy()

# ── Helpers ───────────────────────────────────────────────────────────────────
def total_exp(r): return sum(r.get(c,0) for c in CATS)
def fmt(v): return f"${v:,.0f}"
def make_df(rows):
    df = pd.DataFrame(rows)
    # Fix: cast year to int before label formatting to avoid '24.0' bug
    df['label'] = df.apply(lambda r: f"{MONTH_NAMES[int(r['mo'])]} '{str(int(r['yr']))[2:]}", axis=1)
    df['total'] = df.apply(total_exp, axis=1)
    return df
def ann(df, yr):
    s = df[df['yr']==yr]
    t = {c:s[c].sum() for c in CATS}
    t['total'] = s['total'].sum(); t['income'] = s['Income'].sum()
    return t

# ── UI components (dark) ──────────────────────────────────────────────────────
def kpi(label, value, sub="", delta=None, good=True, accent="#3B82F6", icon=""):
    d = ""
    if delta:
        bg, tc = ("rgba(52,211,153,0.15)","#34D399") if good else ("rgba(248,113,113,0.15)","#F87171")
        d = f'<div style="margin-top:12px;display:inline-flex;align-items:center;gap:4px;font-size:13px;font-weight:700;color:{tc};background:{bg};padding:4px 11px;border-radius:20px;border:1px solid {tc}33;">{delta}</div>'
    return f"""
<div style="background:linear-gradient(145deg,#0D1829,#0F2040);
            border:1px solid rgba(59,130,246,0.15);border-top:3px solid {accent};
            border-radius:14px;padding:24px 26px 22px;height:100%;
            box-shadow:0 0 0 1px rgba(0,0,0,0.3),0 8px 32px rgba(0,0,0,0.4);">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
    <div style="font-size:12px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:0.12em;">{label}</div>
    <div style="font-size:20px;opacity:0.5;">{icon}</div>
  </div>
  <div style="font-size:38px;font-weight:800;color:#E2E8F0;letter-spacing:-2px;line-height:1;font-family:'DM Mono',monospace;">{value}</div>
  <div style="font-size:14px;color:#64748B;margin-top:8px;line-height:1.5;">{sub}</div>
  {d}
</div>"""

def section_head(title, sub=""):
    s = f'<span style="font-size:13px;color:#64748B;font-weight:400;margin-left:8px;">{sub}</span>' if sub else ""
    return f"""<div style="margin:32px 0 16px;display:flex;align-items:center;gap:10px;">
  <div style="width:3px;height:20px;background:linear-gradient(180deg,#3B82F6,#1D4ED8);border-radius:2px;flex-shrink:0;"></div>
  <span style="font-size:17px;font-weight:700;color:#E2E8F0;letter-spacing:-0.3px;">{title}</span>{s}
</div>"""

def income_table(rows, total_val):
    rhtml = "".join(f"""
<tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
  <td style="padding:14px 18px;font-size:14px;color:#CBD5E1;font-weight:500;">{r[0]}</td>
  <td style="padding:14px 18px;font-size:13px;color:#64748B;">{r[1]}</td>
  <td style="padding:14px 18px;font-size:15px;color:#E2E8F0;font-weight:600;text-align:right;font-family:'DM Mono',monospace;">{r[2]}</td>
</tr>""" for r in rows)
    return f"""
<div style="background:#0A1628;border:1px solid rgba(59,130,246,0.15);border-radius:14px;overflow:hidden;
            box-shadow:0 8px 32px rgba(0,0,0,0.4);">
  <table style="width:100%;border-collapse:collapse;">
    <thead><tr style="background:#060C18;border-bottom:1px solid rgba(59,130,246,0.12);">
      <th style="padding:13px 18px;text-align:left;font-size:11px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:0.12em;">Source</th>
      <th style="padding:13px 18px;text-align:left;font-size:11px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:0.12em;">Detail</th>
      <th style="padding:13px 18px;text-align:right;font-size:11px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:0.12em;">Amount</th>
    </tr></thead>
    <tbody>{rhtml}</tbody>
    <tfoot><tr style="background:rgba(52,211,153,0.07);border-top:1px solid rgba(52,211,153,0.2);">
      <td colspan="2" style="padding:16px 18px;font-size:12px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:0.12em;">Total Gross Income</td>
      <td style="padding:16px 18px;font-size:26px;font-weight:800;color:#34D399;text-align:right;font-family:'DM Mono',monospace;letter-spacing:-1px;">{total_val}</td>
    </tr></tfoot>
  </table>
</div>"""

def exp_table(df_rows, show_income=False):
    inc_th = '<th style="padding:12px 14px;text-align:right;font-size:11px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:0.1em;white-space:nowrap;">Net Income</th>' if show_income else ""
    cat_ths = "".join(f'<th style="padding:12px 14px;text-align:right;font-size:11px;font-weight:700;color:{CAT_COLORS[c]};opacity:0.85;text-transform:uppercase;letter-spacing:0.08em;white-space:nowrap;">{c}</th>' for c in CATS)
    head = f"""<thead><tr style="background:#060C18;border-bottom:1px solid rgba(59,130,246,0.1);">
      <th style="padding:12px 14px;text-align:left;font-size:11px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:0.1em;">Month</th>
      {cat_ths}
      <th style="padding:12px 14px;text-align:right;font-size:11px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:0.1em;white-space:nowrap;">Total</th>
      {inc_th}
    </tr></thead>"""
    rows_html = ""
    for i, r in enumerate(df_rows.itertuples()):
        bg = "rgba(255,255,255,0.01)" if i%2==0 else "rgba(255,255,255,0.028)"
        cat_tds = "".join(
            f'<td style="padding:11px 14px;text-align:right;font-size:14px;color:{CAT_COLORS[c]};font-family:\'DM Mono\',monospace;">'
            f'{fmt(getattr(r,c)) if getattr(r,c)>0 else "—"}</td>' for c in CATS)
        inc_td = (f'<td style="padding:11px 14px;text-align:right;font-size:14px;font-weight:600;color:#34D399;font-family:\'DM Mono\',monospace;">'
                  f'{fmt(r.Income) if r.Income>0 else "—"}</td>') if show_income else ""
        rows_html += (f'<tr style="background:{bg};border-bottom:1px solid rgba(255,255,255,0.04);">'
                      f'<td style="padding:11px 14px;font-size:14px;font-weight:600;color:#CBD5E1;white-space:nowrap;">{r.label}</td>'
                      f'{cat_tds}'
                      f'<td style="padding:11px 14px;text-align:right;font-size:15px;font-weight:700;color:#E2E8F0;font-family:\'DM Mono\',monospace;white-space:nowrap;">{fmt(r.total)}</td>'
                      f'{inc_td}</tr>')
    # Totals footer
    totals = {c: df_rows[c].sum() for c in CATS}
    grand  = df_rows['total'].sum()
    inc_total = df_rows['Income'].sum() if show_income and 'Income' in df_rows.columns else 0
    cat_tds_tot = "".join(
        f'<td style="padding:13px 14px;text-align:right;font-size:14px;font-weight:700;color:{CAT_COLORS[c]};font-family:\'DM Mono\',monospace;">'
        f'{fmt(totals[c]) if totals[c]>0 else "—"}</td>' for c in CATS)
    inc_td_tot = (f'<td style="padding:13px 14px;text-align:right;font-size:15px;font-weight:800;color:#34D399;font-family:\'DM Mono\',monospace;">'
                  f'{fmt(inc_total)}</td>') if show_income else ""
    footer = (f'<tr style="background:rgba(59,130,246,0.08);border-top:2px solid rgba(59,130,246,0.2);">'
              f'<td style="padding:13px 14px;font-size:13px;font-weight:800;color:#94A3B8;text-transform:uppercase;letter-spacing:0.1em;">TOTAL</td>'
              f'{cat_tds_tot}'
              f'<td style="padding:13px 14px;text-align:right;font-size:16px;font-weight:800;color:#E2E8F0;font-family:\'DM Mono\',monospace;">{fmt(grand)}</td>'
              f'{inc_td_tot}</tr>')
    return (f'<div style="background:#0A1628;border:1px solid rgba(59,130,246,0.12);border-radius:14px;'
            f'overflow:hidden;overflow-x:auto;box-shadow:0 8px 32px rgba(0,0,0,0.4);">'
            f'<table style="width:100%;border-collapse:collapse;">{head}<tbody>{rows_html}</tbody>'
            f'<tfoot>{footer}</tfoot></table></div>')

def ax(fig):
    fig.update_xaxes(showgrid=False, linecolor="rgba(255,255,255,0.06)",
                     tickfont=dict(size=12, color="#64748B", family=FONT))
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.04)", showline=False,
                     tickfont=dict(size=12, color="#64748B", family=FONT),
                     tickprefix="$", separatethousands=True)
    return fig

def sfig(h=300):
    f = go.Figure()
    f.update_layout(template="rb_dark", height=h,
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    return f

# ── Password gate ─────────────────────────────────────────────────────────────
def _check_password():
    try:    correct = st.secrets["password"]
    except: return True
    if st.session_state.get("_auth"): return True
    def _verify():
        if hmac.compare_digest(st.session_state.get("_pw",""), correct):
            st.session_state["_auth"] = True
        else: st.session_state["_bad"] = True
    st.markdown("""
    <div style="position:fixed;inset:0;background:#060C18;display:flex;align-items:center;justify-content:center;z-index:9999;">
      <div style="background:linear-gradient(145deg,#0A1628,#0F1E35);
                  border:1px solid rgba(59,130,246,0.2);border-radius:20px;
                  padding:52px 56px;width:440px;text-align:center;
                  box-shadow:0 0 60px rgba(37,99,235,0.15),0 24px 80px rgba(0,0,0,0.6);">
        <div style="width:60px;height:60px;background:linear-gradient(135deg,#1D4ED8,#7C3AED);
                    border-radius:16px;margin:0 auto 22px;display:flex;align-items:center;
                    justify-content:center;font-size:26px;
                    box-shadow:0 0 24px rgba(37,99,235,0.4);">💼</div>
        <div style="font-size:26px;font-weight:800;color:#E2E8F0;letter-spacing:-0.8px;">RB Finance</div>
        <div style="font-size:14px;color:#64748B;margin-top:7px;margin-bottom:36px;letter-spacing:0.2px;">PERSONAL DASHBOARD · ROHAN BORA</div>
      </div>
    </div>""", unsafe_allow_html=True)
    col = st.columns([1,2,1])[1]
    with col:
        st.text_input("", type="password", on_change=_verify, key="_pw",
                      placeholder="Enter password…", label_visibility="collapsed")
        if st.session_state.get("_bad"):
            st.error("Incorrect password.")
    return False

if not _check_password():
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:22px 4px 10px;">
      <div style="font-size:19px;font-weight:800;color:#E2E8F0;letter-spacing:-0.5px;">💼 RB Finance</div>
      <div style="font-size:12px;color:#64748B;margin-top:4px;letter-spacing:0.1px;">Rohan Bora · Personal Dashboard</div>
    </div>""", unsafe_allow_html=True)
    st.divider()
    st.markdown('<div style="font-size:12px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:8px;">Connect Excel</div>', unsafe_allow_html=True)
    excel_path    = st.text_input("", placeholder="/Users/rohanbo/…/expenses.xlsx", label_visibility="collapsed")
    uploaded_file = st.file_uploader("", type=['xlsx'], label_visibility="collapsed")
    load_btn      = st.button("⟳  Load / Refresh Data")
    st.divider()
    st.markdown('<div style="font-size:12px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:8px;">Filter Years</div>', unsafe_allow_html=True)
    year_filter = st.multiselect("", [2024,2025,2026], default=[2024,2025,2026], label_visibility="collapsed")
    st.divider()
    st.markdown("""<div style="font-size:13px;color:#94A3B8;line-height:2.2;">
      <div style="font-size:11px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:8px;">Verified Income</div>
      <span style="color:#94A3B8;">2024 AGI (Form 1040)</span><br>
      <span style="color:#60A5FA;font-family:'DM Mono',monospace;font-size:16px;font-weight:700;">$65,626</span><br><br>
      <span style="color:#94A3B8;">2025 W-2 Gross</span><br>
      <span style="color:#60A5FA;font-family:'DM Mono',monospace;font-size:16px;font-weight:700;">$88,120</span><br><br>
      <span style="color:#94A3B8;">2025 Investments</span><br>
      <span style="color:#34D399;font-family:'DM Mono',monospace;font-size:16px;font-weight:700;">$38,237</span><br><br>
      <span style="color:#94A3B8;">2025 Total Gross</span><br>
      <span style="color:#E2E8F0;font-family:'DM Mono',monospace;font-size:17px;font-weight:800;">$126,357</span>
    </div>""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
if load_btn: st.cache_data.clear()
if uploaded_file:                               rows = load_excel(uploaded_file)
elif excel_path and os.path.exists(excel_path): rows = load_excel(excel_path)
else:                                           rows = get_baseline()

df_all  = make_df(rows)
df_filt = df_all[df_all['yr'].isin(year_filter)] if year_filter else df_all
ann24   = ann(df_all,2024); ann25 = ann(df_all,2025); ann26 = ann(df_all,2026)
n26     = len(df_all[df_all['yr']==2026])

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,#030810 0%,#07122A 45%,#030C1E 100%);
            border-bottom:1px solid rgba(59,130,246,0.15);
            padding:36px 44px 32px;margin:0 -2.2rem 0;margin-bottom:32px;
            display:flex;align-items:center;justify-content:space-between;position:relative;overflow:hidden;">
  <div style="position:absolute;top:-80px;left:300px;width:500px;height:280px;
              background:radial-gradient(ellipse,rgba(37,99,235,0.08),transparent 70%);pointer-events:none;"></div>
  <div style="position:absolute;bottom:-60px;right:200px;width:300px;height:200px;
              background:radial-gradient(ellipse,rgba(124,58,237,0.06),transparent 70%);pointer-events:none;"></div>
  <div>
    <div style="font-size:28px;font-weight:800;color:#F1F5F9;letter-spacing:-1px;line-height:1;">Personal Finance Dashboard</div>
    <div style="font-size:14px;color:#64748B;margin-top:8px;letter-spacing:0.1px;">
      Rohan Bora &nbsp;·&nbsp; Jan 2024 – Feb 2026 &nbsp;·&nbsp; Income verified from W-2s, 1099s & Form 1040
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:12px;">
    <div style="background:rgba(59,130,246,0.1);border:1px solid rgba(59,130,246,0.2);
                padding:9px 20px;border-radius:20px;font-size:13px;font-weight:600;color:#60A5FA;letter-spacing:0.1px;">
      📅 Updated Feb 2026
    </div>
    <div style="width:44px;height:44px;background:linear-gradient(135deg,#1D4ED8,#7C3AED);
                border-radius:50%;display:flex;align-items:center;justify-content:center;
                font-size:15px;font-weight:800;color:white;
                box-shadow:0 0 16px rgba(37,99,235,0.4);">RB</div>
  </div>
</div>""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
t_master, t_2024, t_2025, t_2026 = st.tabs([
    "  🗂  Master Overview  ",
    "  📅  2024  ",
    "  📅  2025  ",
    "  📅  2026 YTD  ",
])

# ════════════════════════════════════════════════════════════════════
# MASTER
# ════════════════════════════════════════════════════════════════════
with t_master:
    st.markdown(section_head("At a Glance","All years · tax-verified income"), unsafe_allow_html=True)
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.markdown(kpi("2024 Gross Income","$65,626","Form 1040 AGI",icon="💼",accent="#0891B2"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("2024 Total Spent",fmt(ann24['total']),"Avg "+fmt(ann24['total']/12)+"/mo",icon="💳",accent="#A78BFA"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("2025 W-2 Income","$88,120","Amazon Dev + Services",delta="↑ 40.5% vs 2024",good=True,icon="💼",accent="#34D399"), unsafe_allow_html=True)
    with c4: st.markdown(kpi("2025 Total Spent",fmt(ann25['total']),"Rent-corrected · full year",delta=f"↑ {(ann25['total']/ann24['total']-1)*100:.0f}% vs 2024",good=False,icon="💳",accent="#F87171"), unsafe_allow_html=True)
    with c5: st.markdown(kpi("2026 YTD Spent",fmt(ann26['total']),f"{n26} months · "+fmt(ann26['total']/max(n26,1))+"/mo",icon="🗓",accent="#A78BFA"), unsafe_allow_html=True)

    # ── Monthly Trend ──
    st.markdown(section_head("Monthly Spending Trend","Jan 2024 – Feb 2026"), unsafe_allow_html=True)
    fig_tr = sfig(300)
    fig_tr.add_trace(go.Scatter(
        x=df_filt['label'], y=df_filt['total'].round(),
        mode='lines+markers',
        line=dict(color='#3B82F6',width=2.5,shape='spline',smoothing=0.4),
        fill='tozeroy', fillcolor='rgba(59,130,246,0.07)',
        marker=dict(size=5,color='#060C18',line=dict(color='#3B82F6',width=2)),
        hovertemplate='<b>%{x}</b><br>Total: $%{y:,.0f}<extra></extra>',
    ))
    fig_tr.update_layout(showlegend=False)
    ax(fig_tr)
    st.plotly_chart(fig_tr, use_container_width=True, config=dict(displayModeBar=False))

    # ── YoY + Income vs Expenses ──
    col_l, col_r = st.columns([3,2])
    with col_l:
        st.markdown(section_head("Year-over-Year by Category"), unsafe_allow_html=True)
        fig_yoy = sfig(320)
        for yr, color, name in [(2024,'rgba(96,165,250,0.85)','2024'),(2025,'rgba(248,113,113,0.85)','2025'),(2026,'rgba(167,139,250,0.85)','2026 YTD')]:
            a = ann(df_all,yr)
            fig_yoy.add_trace(go.Bar(name=name, x=CATS, y=[round(a[c]) for c in CATS],
                                     marker_color=color, marker_line_width=0,
                                     hovertemplate=f'<b>{name}</b><br>%{{x}}: $%{{y:,.0f}}<extra></extra>'))
        fig_yoy.update_layout(barmode='group', legend=dict(orientation='h',y=1.08,font_size=13))
        ax(fig_yoy)
        st.plotly_chart(fig_yoy, use_container_width=True, config=dict(displayModeBar=False))
    with col_r:
        st.markdown(section_head("Income vs. Expenses"), unsafe_allow_html=True)
        fig_ie = sfig(320)
        for label, income, expense in [('2024',65626,round(ann24['total'])),('2025',88120,round(ann25['total']))]:
            fig_ie.add_trace(go.Bar(name='Income' if label=='2024' else None,
                                    x=[label], y=[income], marker_color='rgba(52,211,153,0.82)',
                                    marker_line_width=0, legendgroup='inc', showlegend=(label=='2024'),
                                    hovertemplate=f'<b>{label} Income</b>: $%{{y:,.0f}}<extra></extra>'))
            fig_ie.add_trace(go.Bar(name='Expenses' if label=='2024' else None,
                                    x=[label], y=[expense], marker_color='rgba(248,113,113,0.82)',
                                    marker_line_width=0, legendgroup='exp', showlegend=(label=='2024'),
                                    hovertemplate=f'<b>{label} Expenses</b>: $%{{y:,.0f}}<extra></extra>'))
        fig_ie.update_layout(barmode='group', legend=dict(orientation='h',y=1.08,font_size=13))
        ax(fig_ie)
        st.plotly_chart(fig_ie, use_container_width=True, config=dict(displayModeBar=False))

    # ── NEW: Category Trends Over Time ──
    st.markdown(section_head("Category Spending Trends","Non-rent categories · monthly"), unsafe_allow_html=True)
    fig_cat = sfig(320)
    trend_cats = [c for c in CATS if c != 'Rent']
    for c in trend_cats:
        fig_cat.add_trace(go.Scatter(
            x=df_all['label'], y=df_all[c].round(),
            name=c, mode='lines',
            line=dict(color=CAT_COLORS[c], width=2, shape='spline', smoothing=0.5),
            hovertemplate=f'<b>%{{x}}</b><br>{c}: $%{{y:,.0f}}<extra></extra>',
        ))
    fig_cat.update_layout(legend=dict(orientation='h', y=1.1, font_size=12,
                                      itemclick='toggleothers'))
    ax(fig_cat)
    st.plotly_chart(fig_cat, use_container_width=True, config=dict(displayModeBar=False))

    # ── NEW: Savings Summary ──
    st.markdown(section_head("Annual Savings Summary"), unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    income_24 = 65626; spent_24 = ann24['total']; saved_24 = income_24 - spent_24
    income_25 = 88120; spent_25 = ann25['total']; saved_25 = income_25 - spent_25
    with c1: st.markdown(kpi("2024 Estimated Savings", fmt(saved_24),
                              f"{saved_24/income_24*100:.1f}% of gross income",
                              delta="✓ Strong",good=True,icon="🏦",accent="#34D399"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("2025 Estimated Savings", fmt(saved_25),
                              f"{saved_25/income_25*100:.1f}% of W-2 gross",
                              delta="✓ Healthy",good=True,icon="📈",accent="#34D399"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("2026 YTD Run Rate", fmt(ann26['total']/max(n26,1)*12),
                              "Annualized from " + str(n26) + " months",
                              icon="🗓",accent="#FBBF24"), unsafe_allow_html=True)

    st.markdown(section_head("Full Monthly Breakdown","All 26 months"), unsafe_allow_html=True)
    st.html(exp_table(df_all))

# ════════════════════════════════════════════════════════════════════
# 2024
# ════════════════════════════════════════════════════════════════════
with t_2024:
    st.markdown(section_head("2024 — Full Year","Form 1040 · AWS W-2 · Simplicity First W-2 · Robinhood 1099"), unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi("Gross Income","$65,626","AGI per Form 1040",icon="💼",accent="#34D399"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Total Spent",fmt(ann24['total']),"Avg "+fmt(ann24['total']/12)+"/mo",icon="💳",accent="#F87171"), unsafe_allow_html=True)
    savings_24 = 65626 - ann24['total']
    with c3: st.markdown(kpi("Est. Savings",fmt(savings_24),f"{savings_24/65626*100:.1f}% savings rate",delta="✓ Excellent",good=True,icon="📈",accent="#FBBF24"), unsafe_allow_html=True)
    top24=max(CATS,key=lambda c:ann24[c])
    with c4: st.markdown(kpi("Top Category",top24,fmt(ann24[top24])+f" · {ann24[top24]/ann24['total']*100:.0f}% of spend",icon="🏆",accent="#A78BFA"), unsafe_allow_html=True)

    st.markdown(section_head("Income Sources"), unsafe_allow_html=True)
    col_l, col_r = st.columns([3,2])
    with col_l: st.html(income_table(INCOME_2024,"$65,626"))
    with col_r:
        st.markdown(section_head("Spending Mix"), unsafe_allow_html=True)
        fig_d24 = sfig(300)
        fig_d24.add_trace(go.Pie(
            labels=CATS, values=[round(ann24[c]) for c in CATS],
            marker=dict(colors=[CAT_COLORS[c] for c in CATS],line=dict(color='#060C18',width=2)),
            hole=0.64, textinfo='percent', textfont=dict(size=12,color='#E2E8F0'),
            hovertemplate='<b>%{label}</b><br>$%{value:,.0f} (%{percent})<extra></extra>'))
        fig_d24.update_layout(legend=dict(orientation='h',y=-0.18,font_size=12,font_color='#94A3B8'))
        st.plotly_chart(fig_d24, use_container_width=True, config=dict(displayModeBar=False))

    st.markdown(section_head("Monthly Spending by Category"), unsafe_allow_html=True)
    df24 = df_all[df_all['yr']==2024]
    fig_b24 = sfig(320)
    for c in CATS:
        fig_b24.add_trace(go.Bar(name=c, x=df24['label'], y=df24[c].round(),
                                  marker_color=CAT_COLORS[c], marker_line_width=0,
                                  hovertemplate=f'<b>%{{x}}</b><br>{c}: $%{{y:,.0f}}<extra></extra>'))
    fig_b24.update_layout(barmode='stack',legend=dict(orientation='h',y=1.08,font_size=13))
    ax(fig_b24)
    st.plotly_chart(fig_b24, use_container_width=True, config=dict(displayModeBar=False))

    # NEW: Monthly trend line for 2024
    st.markdown(section_head("Monthly Total Trend"), unsafe_allow_html=True)
    fig_t24 = sfig(240)
    fig_t24.add_trace(go.Scatter(
        x=df24['label'], y=df24['total'].round(),
        mode='lines+markers+text', text=[fmt(v) for v in df24['total'].round()],
        textposition='top center', textfont=dict(size=12, color='#94A3B8', family=FONT),
        line=dict(color='#A78BFA',width=2.5,shape='spline'),
        fill='tozeroy', fillcolor='rgba(167,139,250,0.06)',
        marker=dict(size=6,color='#060C18',line=dict(color='#A78BFA',width=2)),
        hovertemplate='<b>%{x}</b><br>$%{y:,.0f}<extra></extra>',
    ))
    fig_t24.update_layout(showlegend=False)
    ax(fig_t24)
    st.plotly_chart(fig_t24, use_container_width=True, config=dict(displayModeBar=False))

    st.markdown(section_head("Monthly Detail"), unsafe_allow_html=True)
    st.html(exp_table(df24))

# ════════════════════════════════════════════════════════════════════
# 2025
# ════════════════════════════════════════════════════════════════════
with t_2025:
    st.markdown(section_head("2025 — Full Year","2× Amazon W-2s · Robinhood 1099-B/DIV/INT · Cash App 1099-DA"), unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi("W-2 Gross Income","$88,120","Amazon Dev + Amazon Services",delta="↑ 40.5% vs 2024",good=True,icon="💼",accent="#34D399"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Investment Income","$37,935","Robinhood cap gains + dividends",icon="📈",accent="#60A5FA"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Total Spent",fmt(ann25['total']),"Incl. $39,541 rent over 12 mo",delta=f"↑ {(ann25['total']/ann24['total']-1)*100:.0f}% vs 2024",good=False,icon="💳",accent="#F87171"), unsafe_allow_html=True)
    sr25 = (88120-ann25['total'])/88120*100
    with c4: st.markdown(kpi("Savings Rate (W-2)",f"{sr25:.1f}%",f"${88120-ann25['total']:,.0f} saved from salary",delta="✓ Healthy",good=True,icon="📊",accent="#FBBF24"), unsafe_allow_html=True)

    st.markdown(section_head("Income Sources"), unsafe_allow_html=True)
    col_l, col_r = st.columns([3,2])
    with col_l: st.html(income_table(INCOME_2025,"$126,357"))
    with col_r:
        st.markdown(section_head("Spending Mix"), unsafe_allow_html=True)
        fig_d25 = sfig(300)
        fig_d25.add_trace(go.Pie(
            labels=CATS, values=[round(ann25[c]) for c in CATS],
            marker=dict(colors=[CAT_COLORS[c] for c in CATS],line=dict(color='#060C18',width=2)),
            hole=0.64, textinfo='percent', textfont=dict(size=12,color='#E2E8F0'),
            hovertemplate='<b>%{label}</b><br>$%{value:,.0f} (%{percent})<extra></extra>'))
        fig_d25.update_layout(legend=dict(orientation='h',y=-0.18,font_size=12,font_color='#94A3B8'))
        st.plotly_chart(fig_d25, use_container_width=True, config=dict(displayModeBar=False))

    df25 = df_all[df_all['yr']==2025]

    # ── Monthly stacked spending ──
    st.markdown(section_head("Monthly Spending by Category"), unsafe_allow_html=True)
    fig_b25 = sfig(320)
    for c in CATS:
        fig_b25.add_trace(go.Bar(name=c, x=df25['label'], y=df25[c].round(),
                                  marker_color=CAT_COLORS[c], marker_line_width=0,
                                  hovertemplate=f'<b>%{{x}}</b><br>{c}: $%{{y:,.0f}}<extra></extra>'))
    fig_b25.update_layout(barmode='stack',legend=dict(orientation='h',y=1.08,font_size=13))
    ax(fig_b25)
    st.plotly_chart(fig_b25, use_container_width=True, config=dict(displayModeBar=False))

    # ── Monthly Take-Home vs. Expenses ──
    st.markdown(section_head("Monthly Take-Home vs. Expenses","Net income = paycheck deposits from expense sheets"), unsafe_allow_html=True)
    fig_ie25 = sfig(320)
    fig_ie25.add_trace(go.Bar(name='Net Take-Home', x=df25['label'], y=df25['Income'].round(),
                               marker_color='rgba(52,211,153,0.82)', marker_line_width=0,
                               hovertemplate='<b>%{x}</b><br>Take-Home: $%{y:,.0f}<extra></extra>'))
    fig_ie25.add_trace(go.Bar(name='Total Expenses', x=df25['label'], y=df25['total'].round(),
                               marker_color='rgba(248,113,113,0.82)', marker_line_width=0,
                               hovertemplate='<b>%{x}</b><br>Expenses: $%{y:,.0f}<extra></extra>'))
    fig_ie25.update_layout(barmode='group',legend=dict(orientation='h',y=1.08,font_size=13))
    ax(fig_ie25)
    st.plotly_chart(fig_ie25, use_container_width=True, config=dict(displayModeBar=False))

    # ── NEW: Monthly Net Cash Flow ──
    st.markdown(section_head("Monthly Net Cash Flow","Take-home minus expenses · green = positive"), unsafe_allow_html=True)
    df25_cf = df25[df25['Income']>0].copy()
    df25_cf['net'] = df25_cf['Income'] - df25_cf['total']
    fig_cf = sfig(260)
    colors_cf = ['rgba(52,211,153,0.85)' if v >= 0 else 'rgba(248,113,113,0.85)' for v in df25_cf['net']]
    fig_cf.add_trace(go.Bar(
        x=df25_cf['label'], y=df25_cf['net'].round(),
        marker_color=colors_cf, marker_line_width=0,
        text=[fmt(v) for v in df25_cf['net'].round()],
        textposition='outside', textfont=dict(size=12, color='#94A3B8', family=FONT),
        hovertemplate='<b>%{x}</b><br>Net: $%{y:,.0f}<extra></extra>',
    ))
    fig_cf.add_hline(y=0, line_color="rgba(255,255,255,0.12)", line_width=1)
    fig_cf.update_layout(showlegend=False)
    ax(fig_cf)
    st.plotly_chart(fig_cf, use_container_width=True, config=dict(displayModeBar=False))

    st.markdown(section_head("Monthly Detail"), unsafe_allow_html=True)
    st.html(exp_table(df25, show_income=True))

# ════════════════════════════════════════════════════════════════════
# 2026
# ════════════════════════════════════════════════════════════════════
with t_2026:
    st.markdown(section_head("2026 — Year to Date",f"{n26} months · Jan – Feb"), unsafe_allow_html=True)

    # Annualized projection
    monthly_avg_26 = ann26['total'] / max(n26, 1)
    projected_26   = monthly_avg_26 * 12

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi("YTD Spent",fmt(ann26['total']),f"{n26} months tracked",icon="🗓",accent="#A78BFA"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Monthly Average",fmt(monthly_avg_26),"per month so far",icon="📅",accent="#60A5FA"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Annualized Projection",fmt(projected_26),"If pace continues all year",icon="📊",accent="#FBBF24"), unsafe_allow_html=True)
    top26=max(CATS,key=lambda c:ann26[c])
    with c4: st.markdown(kpi("Top Category",top26,fmt(ann26[top26])+" YTD",icon="🏆",accent="#FB923C"), unsafe_allow_html=True)

    st.info("💡 Jan & Feb 2026 rent ($50 and $40) appears partial — Bilt payment may not yet be fully captured in those months.")

    df26 = df_all[df_all['yr']==2026]
    col_l, col_r = st.columns([1,1])
    with col_l:
        st.markdown(section_head("Monthly Spending"), unsafe_allow_html=True)
        fig_b26 = sfig(320)
        for c in CATS:
            if ann26[c]>0:
                fig_b26.add_trace(go.Bar(name=c, x=df26['label'], y=df26[c].round(),
                                          marker_color=CAT_COLORS[c], marker_line_width=0,
                                          hovertemplate=f'<b>%{{x}}</b><br>{c}: $%{{y:,.0f}}<extra></extra>'))
        fig_b26.update_layout(barmode='stack',legend=dict(orientation='h',y=1.1,font_size=13))
        ax(fig_b26)
        st.plotly_chart(fig_b26, use_container_width=True, config=dict(displayModeBar=False))
    with col_r:
        st.markdown(section_head("Spending Mix"), unsafe_allow_html=True)
        active=[c for c in CATS if ann26[c]>0]
        fig_d26 = sfig(320)
        fig_d26.add_trace(go.Pie(
            labels=active, values=[round(ann26[c]) for c in active],
            marker=dict(colors=[CAT_COLORS[c] for c in active],line=dict(color='#060C18',width=2)),
            hole=0.64, textinfo='percent', textfont=dict(size=12,color='#E2E8F0'),
            hovertemplate='<b>%{label}</b><br>$%{value:,.0f} (%{percent})<extra></extra>'))
        fig_d26.update_layout(legend=dict(orientation='h',y=-0.18,font_size=12,font_color='#94A3B8'))
        st.plotly_chart(fig_d26, use_container_width=True, config=dict(displayModeBar=False))

    if n26 > 0:
        st.markdown(section_head("Same-Period vs. 2025"), unsafe_allow_html=True)
        df25s = df_all[(df_all['yr']==2025)&(df_all['mo'].isin(df26['mo'].tolist()))]
        fig_comp = sfig(270)
        fig_comp.add_trace(go.Bar(name='2025 (same months)', x=df25s['label'],
                                   y=df25s['total'].round(), marker_color='rgba(248,113,113,0.75)', marker_line_width=0))
        fig_comp.add_trace(go.Bar(name='2026', x=df26['label'],
                                   y=df26['total'].round(), marker_color='rgba(167,139,250,0.85)', marker_line_width=0))
        fig_comp.update_layout(barmode='group',legend=dict(orientation='h',y=1.1,font_size=13))
        ax(fig_comp)
        st.plotly_chart(fig_comp, use_container_width=True, config=dict(displayModeBar=False))

    st.markdown(section_head("Monthly Detail"), unsafe_allow_html=True)
    st.html(exp_table(df26))
