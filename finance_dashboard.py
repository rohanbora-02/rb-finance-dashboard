"""
Rohan Bora — Personal Finance Dashboard  ·  Premium Edition
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

# ── Premium CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stHeader"] { display: none !important; }
.stDeployButton { display: none !important; }

/* ── Page background ── */
.stApp { background: #EEF2F7; }
.block-container { padding: 0 2rem 3rem !important; max-width: 1440px !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0B1221 0%, #111E35 50%, #0D1829 100%) !important;
  border-right: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown div,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stTextInput label { color: #94A3B8 !important; font-size: 12px; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #F1F5F9 !important; font-weight: 700 !important; }
[data-testid="stSidebar"] input {
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  color: #F1F5F9 !important; border-radius: 8px !important; font-size: 12px !important;
}
[data-testid="stSidebar"] .stButton > button {
  background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
  color: white !important; border: none !important; border-radius: 10px !important;
  font-weight: 700 !important; font-size: 13px !important; width: 100% !important;
  padding: 11px !important; letter-spacing: -0.1px !important;
  box-shadow: 0 4px 14px rgba(37,99,235,0.45) !important;
  transition: all 0.2s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 20px rgba(37,99,235,0.55) !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] {
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploadDropzone"] {
  background: rgba(255,255,255,0.04) !important;
  border: 1px dashed rgba(255,255,255,0.2) !important; border-radius: 10px !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: white !important; gap: 4px !important; padding: 6px !important;
  border-radius: 14px !important;
  box-shadow: 0 1px 3px rgba(0,0,0,0.07), 0 4px 16px rgba(0,0,0,0.05) !important;
  border: 1px solid #E2E8F0 !important; margin-bottom: 4px !important;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 10px !important; padding: 10px 22px !important;
  font-weight: 600 !important; font-size: 13px !important; color: #64748B !important;
  background: transparent !important; border: none !important; transition: all 0.2s !important;
  letter-spacing: -0.1px !important;
}
.stTabs [data-baseweb="tab"]:hover { color: #1E40AF !important; background: #F0F7FF !important; }
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
  color: white !important;
  box-shadow: 0 4px 14px rgba(37,99,235,0.35) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
[data-testid="stDataFrame"] table { font-family: 'DM Sans', sans-serif !important; font-size: 12px !important; }

/* ── Info/warning boxes ── */
[data-testid="stAlert"] { border-radius: 10px !important; font-size: 13px !important; }

/* ── Divider ── */
hr { border-color: #E2E8F0 !important; opacity: 0.7 !important; margin: 1rem 0 !important; }

/* ── Multiselect tags ── */
[data-baseweb="tag"] { background: rgba(37,99,235,0.12) !important; color: #1D4ED8 !important; }
</style>
""", unsafe_allow_html=True)

# ── Plotly premium template ───────────────────────────────────────────────────
FONT = "'DM Sans', 'Inter', sans-serif"
pio.templates["rb_premium"] = go.layout.Template(
    layout=go.Layout(
        font=dict(family=FONT, size=11, color="#374151"),
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        xaxis=dict(gridcolor="#F3F4F6", linecolor="#E5E7EB", zeroline=False,
                   tickfont=dict(size=10, color="#9CA3AF"), showgrid=False),
        yaxis=dict(gridcolor="#F3F4F6", linecolor="rgba(0,0,0,0)", zeroline=False,
                   tickfont=dict(size=10, color="#9CA3AF"), showgrid=True),
        hoverlabel=dict(bgcolor="#111827", font=dict(family=FONT, color="#F9FAFB", size=12),
                        bordercolor="rgba(0,0,0,0)"),
        legend=dict(font=dict(size=10, family=FONT), bgcolor="rgba(0,0,0,0)",
                    bordercolor="rgba(0,0,0,0)"),
        margin=dict(l=4, r=4, t=12, b=4),
        colorway=["#2563EB","#10B981","#F59E0B","#EF4444","#8B5CF6","#EC4899","#06B6D4","#94A3B8"],
    )
)

# ── Constants ─────────────────────────────────────────────────────────────────
CATS = ['Food','Groceries','Shopping','Rent','Personal','Travel','Entertainment','Other']
CAT_COLORS = {
    'Food':'#F97316', 'Groceries':'#22C55E', 'Shopping':'#8B5CF6',
    'Rent':'#EF4444',  'Personal':'#3B82F6',  'Travel':'#F59E0B',
    'Entertainment':'#EC4899', 'Other':'#94A3B8',
}
MONTH_MAP = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,
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

# ── Income data (from tax documents) ─────────────────────────────────────────
INCOME_2024 = [
    ("Amazon Development Center US Inc — W-2", "Box 1 wages · EIN 20-8424306 · NY state", "$59,723"),
    ("Simplicity First Solutions LLC — W-2",   "Box 1 wages · EIN 82-3220641 · CA state", "$3,000"),
    ("Robinhood — Short-Term Capital Gains",    "SOFI Technologies + Upstart Holdings",    "$3,027"),
    ("Robinhood — Long-Term Capital Gains",     "Net realized loss",                       "−$124"),
    ("Robinhood — Interest Income",             "1099-INT",                                "$68"),
    ("Robinhood — Dividends",                   "1099-DIV",                                "$2"),
]
INCOME_2025 = [
    ("Amazon Development Center US Inc — W-2", "Box 1 wages · EIN 20-8424306 · NY state",   "$58,189"),
    ("Amazon Com Services LLC — W-2",           "Box 1 wages · EIN 82-0544687 · NY state",   "$29,931"),
    ("Robinhood — Short-Term Capital Gains",    "Proceeds $75,891 · Cost $38,193",            "$37,906"),
    ("Robinhood — Long-Term Capital Gains",     "Proceeds $3,300 · Cost $4,300",              "$30"),
    ("Robinhood — Dividends",                   "1099-DIV",                                   "$2"),
    ("Robinhood — Interest Income",             "1099-INT",                                   "$278"),
    ("Cash App — Bitcoin Proceeds (1099-DA)",   "Gross proceeds only · gain/loss not reported","$22"),
]

# ── Excel Parser ──────────────────────────────────────────────────────────────
CAT_MAP = {
    'food':'Food','restaurants':'Food','restaurant':'Food','dining':'Food','coffee':'Food',
    'groceries':'Groceries','grocery':'Groceries','supermarket':'Groceries',
    'shopping':'Shopping','general merchandise':'Shopping','electronics':'Shopping','vanmoof':'Shopping',
    'rent':'Rent','bilt':'Rent',
    'personal':'Personal','personal care':'Personal','online services':'Personal','subscription':'Personal',
    'travel':'Travel','transportation':'Travel','airline':'Travel','hotel':'Travel','lyft':'Travel','uber':'Travel',
    'entertainment':'Entertainment','movies':'Entertainment','spotify':'Entertainment',
}

def normalize_cat(desc, bank):
    for kw, cat in CAT_MAP.items():
        if kw in str(desc).lower(): return cat
    for kw, cat in CAT_MAP.items():
        if kw in str(bank).lower(): return cat
    return 'Other'

def parse_excel_sheet(df):
    try:
        header_row = next((i for i,r in df.iterrows()
                           if 'date' in [str(v).lower().strip() for v in r.values]
                           and any(x in [str(v).lower().strip() for v in r.values] for x in ['amount','amount2'])), None)
        if header_row is None: return None
        df.columns = [str(v).strip() for v in df.iloc[header_row].values]
        df = df.iloc[header_row+1:].reset_index(drop=True).dropna(how='all')
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
                cat = normalize_cat(row.get(cols.get('description',''),''), row.get(cols.get('bankcategory',''),''))
            if amt >= 3000 and cat == 'Other': cat = 'Rent'
            totals[cat] += amt
            if 'income' in cols:
                try: income += float(str(row[cols['income']]).replace('$','').replace(',',''))
                except: pass
        totals['Income'] = income
        return totals
    except: return None

@st.cache_data(show_spinner="Reading Excel…")
def load_excel(path_or_bytes):
    from io import BytesIO
    try:
        xl = pd.ExcelFile(path_or_bytes if isinstance(path_or_bytes,(str,Path)) else BytesIO(path_or_bytes.read()))
    except Exception as e:
        st.sidebar.warning(f"Could not read Excel: {e}"); return BASELINE.copy()
    known = {(r['yr'],r['mo']):dict(r) for r in BASELINE}
    new_found = 0
    for sheet in xl.sheet_names:
        m = re.match(r'([A-Za-z]{3})\s*(\d{2})\b', sheet.strip())
        if not m: continue
        mon_str, yr_short = m.group(1).lower(), int(m.group(2))
        if mon_str not in MONTH_MAP: continue
        mo, yr = MONTH_MAP[mon_str], 2000+yr_short
        if (yr,mo) in known: continue
        result = parse_excel_sheet(xl.parse(sheet, header=None))
        if result:
            known[(yr,mo)] = dict(yr=yr, mo=mo, **result); new_found += 1
    if new_found: st.sidebar.success(f"✓ {new_found} new month(s) loaded from Excel")
    return sorted(known.values(), key=lambda r:(r['yr'],r['mo']))

@st.cache_data
def get_baseline(): return BASELINE.copy()

# ── Data helpers ──────────────────────────────────────────────────────────────
def total_exp(r): return sum(r.get(c,0) for c in CATS)
def fmt(v): return f"${v:,.0f}"
def make_df(rows):
    df = pd.DataFrame(rows)
    df['label'] = df.apply(lambda r: f"{MONTH_NAMES[r['mo']]} '{str(r['yr'])[2:]}", axis=1)
    df['total'] = df.apply(lambda r: total_exp(r), axis=1)
    return df
def ann(df, yr):
    s = df[df['yr']==yr]
    t = {c:s[c].sum() for c in CATS}
    t['total'] = s['total'].sum(); t['income'] = s['Income'].sum()
    return t

# ── UI component helpers ──────────────────────────────────────────────────────
def kpi(label, value, sub="", delta=None, good=True, color="#2563EB", icon=""):
    top = f"border-top:3px solid {color}"
    d_html = ""
    if delta:
        bg, tc = ("#D1FAE5","#065F46") if good else ("#FEE2E2","#991B1B")
        d_html = f'<span style="display:inline-flex;align-items:center;gap:3px;font-size:11px;font-weight:700;color:{tc};background:{bg};padding:3px 10px;border-radius:20px;margin-top:10px;">{delta}</span>'
    return f"""
<div style="background:#fff;border-radius:14px;padding:22px 24px 20px;{top};
            box-shadow:0 1px 3px rgba(0,0,0,0.05),0 4px 20px rgba(0,0,0,0.06);
            border:1px solid #F1F5F9;height:100%;display:flex;flex-direction:column;">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
    <div style="font-size:10px;font-weight:700;color:#9CA3AF;text-transform:uppercase;letter-spacing:0.1em;">{label}</div>
    <div style="font-size:18px;opacity:0.55;">{icon}</div>
  </div>
  <div style="font-size:30px;font-weight:800;color:#0F172A;letter-spacing:-1.5px;line-height:1;font-family:'DM Mono','DM Sans',monospace;">{value}</div>
  <div style="font-size:11px;color:#6B7280;margin-top:6px;line-height:1.4;">{sub}</div>
  {d_html}
</div>"""

def section_head(title, sub=""):
    s = f'<span style="font-size:12px;color:#9CA3AF;font-weight:400;margin-left:10px;">{sub}</span>' if sub else ""
    return f'<div style="margin:28px 0 14px 0;display:flex;align-items:baseline;gap:4px;"><span style="font-size:13px;font-weight:700;color:#374151;letter-spacing:-0.2px;">{title}</span>{s}</div>'

def income_table(rows, total_val):
    rhtml = "".join(f"""
    <tr style="border-bottom:1px solid #F8FAFC;">
      <td style="padding:11px 16px;font-size:13px;color:#1E293B;font-weight:500;">{r[0]}</td>
      <td style="padding:11px 16px;font-size:12px;color:#94A3B8;">{r[1]}</td>
      <td style="padding:11px 16px;font-size:13px;color:#0F172A;font-weight:600;text-align:right;font-family:'DM Mono',monospace;">{r[2]}</td>
    </tr>""" for r in rows)
    return f"""
<div style="background:#fff;border-radius:14px;overflow:hidden;
            box-shadow:0 1px 3px rgba(0,0,0,0.05),0 4px 20px rgba(0,0,0,0.06);border:1px solid #F1F5F9;">
  <table style="width:100%;border-collapse:collapse;">
    <thead><tr style="background:#F8FAFC;border-bottom:2px solid #E2E8F0;">
      <th style="padding:10px 16px;text-align:left;font-size:10px;font-weight:700;color:#9CA3AF;text-transform:uppercase;letter-spacing:0.1em;">Source</th>
      <th style="padding:10px 16px;text-align:left;font-size:10px;font-weight:700;color:#9CA3AF;text-transform:uppercase;letter-spacing:0.1em;">Detail</th>
      <th style="padding:10px 16px;text-align:right;font-size:10px;font-weight:700;color:#9CA3AF;text-transform:uppercase;letter-spacing:0.1em;">Amount</th>
    </tr></thead>
    <tbody>{rhtml}</tbody>
    <tfoot><tr style="background:linear-gradient(90deg,#F0F7FF,#EFF6FF);border-top:2px solid #DBEAFE;">
      <td colspan="2" style="padding:14px 16px;font-size:11px;font-weight:700;color:#6B7280;text-transform:uppercase;letter-spacing:0.1em;">Total Gross Income</td>
      <td style="padding:14px 16px;font-size:22px;font-weight:800;color:#059669;text-align:right;font-family:'DM Mono',monospace;letter-spacing:-1px;">{total_val}</td>
    </tr></tfoot>
  </table>
</div>"""

def exp_table(df_rows, show_income=False):
    extra_th = '<th style="padding:10px 14px;text-align:right;font-size:10px;font-weight:700;color:#9CA3AF;text-transform:uppercase;letter-spacing:0.1em;">Net Income</th>' if show_income else ""
    head = f"""<thead><tr style="background:#F8FAFC;border-bottom:2px solid #E2E8F0;">
      <th style="padding:10px 14px;text-align:left;font-size:10px;font-weight:700;color:#9CA3AF;text-transform:uppercase;letter-spacing:0.1em;">Month</th>
      {"".join(f'<th style="padding:10px 14px;text-align:right;font-size:10px;font-weight:700;color:{CAT_COLORS[c]};text-transform:uppercase;letter-spacing:0.08em;">{c}</th>' for c in CATS)}
      <th style="padding:10px 14px;text-align:right;font-size:10px;font-weight:700;color:#374151;text-transform:uppercase;letter-spacing:0.1em;">Total</th>
      {extra_th}
    </tr></thead>"""
    rows_html = ""
    for i, r in enumerate(df_rows.itertuples()):
        bg = "#FFFFFF" if i%2==0 else "#FAFAFA"
        extra_td = f'<td style="padding:9px 14px;text-align:right;font-size:12px;color:#059669;font-weight:600;font-family:\'DM Mono\',monospace;">{fmt(r.Income) if r.Income > 0 else "—"}</td>' if show_income else ""
        cat_tds = "".join(f'<td style="padding:9px 14px;text-align:right;font-size:12px;color:#374151;font-family:\'DM Mono\',monospace;">{fmt(getattr(r,c)) if getattr(r,c)>0 else "—"}</td>' for c in CATS)
        rows_html += f'<tr style="background:{bg};border-bottom:1px solid #F1F5F9;"><td style="padding:9px 14px;font-size:12px;font-weight:600;color:#0F172A;">{r.label}</td>{cat_tds}<td style="padding:9px 14px;text-align:right;font-size:13px;font-weight:700;color:#0F172A;font-family:\'DM Mono\',monospace;">{fmt(r.total)}</td>{extra_td}</tr>'
    return f'<div style="background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.05),0 4px 20px rgba(0,0,0,0.06);border:1px solid #F1F5F9;overflow-x:auto;"><table style="width:100%;border-collapse:collapse;">{head}<tbody>{rows_html}</tbody></table></div>'

def card(content_html, pad="24px 26px"):
    return f'<div style="background:#fff;border-radius:14px;padding:{pad};box-shadow:0 1px 3px rgba(0,0,0,0.05),0 4px 20px rgba(0,0,0,0.06);border:1px solid #F1F5F9;">{content_html}</div>'

def chart_title(title, sub=""):
    s = f'<div style="font-size:11px;color:#9CA3AF;margin-top:2px;">{sub}</div>' if sub else ""
    return f'<div style="margin-bottom:16px;"><div style="font-size:14px;font-weight:700;color:#0F172A;letter-spacing:-0.3px;">{title}</div>{s}</div>'

# ── Apply Plotly template helpers ─────────────────────────────────────────────
def styled_fig(height=300):
    f = go.Figure()
    f.update_layout(template="rb_premium", height=height)
    return f

def ax(fig):
    fig.update_xaxes(showgrid=False, linecolor="#E5E7EB",
                     tickfont=dict(size=10, color="#9CA3AF", family=FONT))
    fig.update_yaxes(gridcolor="#F3F4F6", showline=False,
                     tickfont=dict(size=10, color="#9CA3AF", family=FONT),
                     tickprefix="$", separatethousands=True)
    return fig

# ── Password gate ────────────────────────────────────────────────────────────
def _check_password() -> bool:
    """Returns True if the user entered the correct password (or if no secret is set — local dev)."""
    # Local dev: if no secrets configured, skip the gate
    try:
        correct = st.secrets["password"]
    except Exception:
        return True  # No secret set → running locally, allow through

    if st.session_state.get("_auth", False):
        return True

    def _verify():
        if hmac.compare_digest(st.session_state.get("_pw", ""), correct):
            st.session_state["_auth"] = True
        else:
            st.session_state["_auth_failed"] = True

    st.markdown("""
    <div style="min-height:100vh;display:flex;align-items:center;justify-content:center;background:#EEF2F7;">
      <div style="background:white;border-radius:20px;padding:48px 52px;width:420px;
                  box-shadow:0 4px 6px rgba(0,0,0,0.05),0 20px 60px rgba(0,0,0,0.12);
                  border:1px solid #E2E8F0;text-align:center;">
        <div style="width:56px;height:56px;background:linear-gradient(135deg,#2563EB,#7C3AED);
                    border-radius:16px;margin:0 auto 20px;display:flex;align-items:center;
                    justify-content:center;font-size:24px;">💼</div>
        <div style="font-size:22px;font-weight:800;color:#0F172A;letter-spacing:-0.8px;">RB Finance</div>
        <div style="font-size:13px;color:#94A3B8;margin-top:6px;margin-bottom:32px;">Personal Dashboard · Rohan Bora</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    with col:
        st.text_input("Password", type="password", on_change=_verify,
                      key="_pw", label_visibility="collapsed",
                      placeholder="Enter password…")
        if st.session_state.get("_auth_failed"):
            st.error("Incorrect password — try again.")
    return False

if not _check_password():
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:20px 4px 8px;">
      <div style="font-size:20px;font-weight:800;color:#F1F5F9;letter-spacing:-0.8px;">💼 RB Finance</div>
      <div style="font-size:11px;color:#475569;margin-top:3px;">Rohan Bora · Personal Dashboard</div>
    </div>""", unsafe_allow_html=True)
    st.divider()

    st.markdown('<div style="font-size:11px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">Connect Excel</div>', unsafe_allow_html=True)
    excel_path   = st.text_input("", placeholder="/Users/rohanbo/…/2026 Income-Expense.xlsx",
                                 label_visibility="collapsed")
    uploaded_file = st.file_uploader("", type=['xlsx'], label_visibility="collapsed")
    load_btn = st.button("⟳  Load / Refresh Data")

    st.divider()
    st.markdown('<div style="font-size:11px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">Filter</div>', unsafe_allow_html=True)
    year_filter = st.multiselect("", options=[2024,2025,2026], default=[2024,2025,2026],
                                 label_visibility="collapsed")
    st.divider()
    st.markdown("""
    <div style="font-size:11px;color:#475569;line-height:1.8;">
      <div style="font-weight:700;color:#64748B;margin-bottom:4px;">VERIFIED INCOME</div>
      <b style="color:#94A3B8;">2024</b><br>
      &nbsp;Amazon Dev W-2: $59,723<br>
      &nbsp;Simplicity First W-2: $3,000<br>
      &nbsp;Robinhood (net): $2,903<br>
      &nbsp;<b>AGI: $65,626</b><br><br>
      <b style="color:#94A3B8;">2025</b><br>
      &nbsp;Amazon Dev W-2: $58,189<br>
      &nbsp;Amazon Services W-2: $29,931<br>
      &nbsp;Total W-2: $88,120<br>
      &nbsp;Robinhood gains: $37,935<br>
      &nbsp;<b>Gross Total: ~$126,335</b>
    </div>""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
if load_btn: st.cache_data.clear()
if uploaded_file:              rows = load_excel(uploaded_file)
elif excel_path and os.path.exists(excel_path): rows = load_excel(excel_path)
else:                          rows = get_baseline()

df_all = make_df(rows)
df_filt = df_all[df_all['yr'].isin(year_filter)] if year_filter else df_all

ann24 = ann(df_all, 2024)
ann25 = ann(df_all, 2025)
ann26 = ann(df_all, 2026)
n26   = len(df_all[df_all['yr']==2026])

# ── Dashboard header ──────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#0B1221 0%,#142040 55%,#0E1E3A 100%);
            border-radius:0 0 20px 20px;padding:28px 36px 26px;margin:0 -2rem 0;
            display:flex;align-items:center;justify-content:space-between;margin-bottom:28px;">
  <div>
    <div style="font-size:24px;font-weight:800;color:#F1F5F9;letter-spacing:-0.8px;">Personal Finance Dashboard</div>
    <div style="font-size:13px;color:#64748B;margin-top:5px;">Rohan Bora &nbsp;·&nbsp; Jan 2024 – Feb 2026 &nbsp;·&nbsp; Income verified from W-2s, 1099s & Form 1040</div>
  </div>
  <div style="display:flex;align-items:center;gap:10px;">
    <div style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.1);
                padding:7px 16px;border-radius:20px;font-size:11px;font-weight:600;color:#94A3B8;">
      📅 Updated Feb 2026
    </div>
    <div style="width:38px;height:38px;background:linear-gradient(135deg,#2563EB,#7C3AED);
                border-radius:50%;display:flex;align-items:center;justify-content:center;
                font-size:13px;font-weight:800;color:white;">RB</div>
  </div>
</div>""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
t_master, t_2024, t_2025, t_2026 = st.tabs([
    "  🗂  Master Overview  ",
    "  📅  2024  ",
    "  📅  2025  ",
    "  📅  2026 YTD  ",
])

# ════════════════════════════════════════════════════════════════════════════
#  MASTER TAB
# ════════════════════════════════════════════════════════════════════════════
with t_master:
    st.markdown(section_head("At a Glance", "All years · verified income"), unsafe_allow_html=True)
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.markdown(kpi("2024 Gross Income","$65,626","Form 1040 AGI",icon="💼",color="#0891B2"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("2024 Total Spent",fmt(ann24['total']),"Avg "+fmt(ann24['total']/12)+"/mo",icon="💳",color="#6366F1"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("2025 W2 Income","$88,120","Amazon Dev + Services",delta="↑ 40.5% vs 2024",good=True,icon="💼",color="#059669"), unsafe_allow_html=True)
    with c4: st.markdown(kpi("2025 Total Spent",fmt(ann25['total']),"Rent-corrected full year",delta=f"↑ {(ann25['total']/ann24['total']-1)*100:.0f}% vs 2024",good=False,icon="💳",color="#EF4444"), unsafe_allow_html=True)
    with c5: st.markdown(kpi("2026 YTD Spent",fmt(ann26['total']),f"{n26} months · "+fmt(ann26['total']/max(n26,1))+"/mo avg",icon="🗓",color="#7C3AED"), unsafe_allow_html=True)

    st.markdown(section_head("Spending Trend", "Jan 2024 – Feb 2026"), unsafe_allow_html=True)
    fig_trend = styled_fig(290)
    fig_trend.add_trace(go.Scatter(
        x=df_filt['label'], y=df_filt['total'].round(),
        mode='lines+markers',
        line=dict(color='#2563EB', width=2.5, shape='spline', smoothing=0.4),
        fill='tozeroy', fillcolor='rgba(37,99,235,0.06)',
        marker=dict(size=5, color='white', line=dict(color='#2563EB',width=2)),
        hovertemplate='<b>%{x}</b><br>Total Spending: $%{y:,.0f}<extra></extra>',
    ))
    fig_trend.update_layout(showlegend=False, margin=dict(l=4,r=4,t=8,b=4))
    ax(fig_trend)
    st.markdown(card(chart_title("Monthly Spending Trend","Aug 2025 data unavailable · shown as zero")+
                     "<div id='trend_chart'></div>"), unsafe_allow_html=True)
    st.plotly_chart(fig_trend, use_container_width=True, config=dict(displayModeBar=False))

    col_l, col_r = st.columns([3,2])
    with col_l:
        st.markdown(section_head("Year-over-Year by Category"), unsafe_allow_html=True)
        fig_yoy = styled_fig(310)
        for yr, col, name in [(2024,'rgba(37,99,235,0.82)','2024'),(2025,'rgba(239,68,68,0.82)','2025'),(2026,'rgba(124,58,237,0.82)','2026 YTD')]:
            a = ann(df_all, yr)
            fig_yoy.add_trace(go.Bar(name=name, x=CATS, y=[round(a[c]) for c in CATS],
                                     marker_color=col, marker_line_width=0,
                                     hovertemplate=f'<b>{name}</b><br>%{{x}}: $%{{y:,.0f}}<extra></extra>'))
        fig_yoy.update_layout(barmode='group', legend=dict(orientation='h',y=1.1,x=0))
        ax(fig_yoy)
        st.plotly_chart(fig_yoy, use_container_width=True, config=dict(displayModeBar=False))

    with col_r:
        st.markdown(section_head("Income vs. Expenses"), unsafe_allow_html=True)
        fig_ie = styled_fig(310)
        for label, income, expense, yr in [
            ('2024', 65626, round(ann24['total']), 2024),
            ('2025', 88120, round(ann25['total']), 2025),
        ]:
            fig_ie.add_trace(go.Bar(name='Income', x=[label], y=[income],
                                    marker_color='rgba(5,150,105,0.82)', marker_line_width=0,
                                    hovertemplate=f'<b>{label} Income</b>: $%{{y:,.0f}}<extra></extra>',
                                    legendgroup='income', showlegend=(yr==2024)))
            fig_ie.add_trace(go.Bar(name='Expenses', x=[label], y=[expense],
                                    marker_color='rgba(239,68,68,0.82)', marker_line_width=0,
                                    hovertemplate=f'<b>{label} Expenses</b>: $%{{y:,.0f}}<extra></extra>',
                                    legendgroup='expense', showlegend=(yr==2024)))
        fig_ie.update_layout(barmode='group', legend=dict(orientation='h',y=1.1,x=0))
        ax(fig_ie)
        st.plotly_chart(fig_ie, use_container_width=True, config=dict(displayModeBar=False))

    st.markdown(section_head("Full Monthly Breakdown"), unsafe_allow_html=True)
    all_rows = df_all.copy()
    st.markdown(exp_table(all_rows), unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
#  2024 TAB
# ════════════════════════════════════════════════════════════════════════════
with t_2024:
    st.markdown(section_head("2024 — Full Year", "Sources: IRS Form 1040 · AWS W-2 · Simplicity First W-2 · Robinhood 1099"), unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi("Gross Income","$65,626","AGI per Form 1040",icon="💼",color="#059669"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Total Spent",fmt(ann24['total']),"Avg "+fmt(ann24['total']/12)+"/mo",icon="💳",color="#EF4444"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Savings Rate","74.0%","$48,560 retained",delta="✓ Excellent",good=True,icon="📈",color="#F59E0B"), unsafe_allow_html=True)
    top24 = max(CATS, key=lambda c: ann24[c])
    with c4: st.markdown(kpi("Top Category",top24,fmt(ann24[top24])+" · "+f"{ann24[top24]/ann24['total']*100:.0f}% of spend",icon="🏆",color="#8B5CF6"), unsafe_allow_html=True)

    st.markdown(section_head("Income Sources"), unsafe_allow_html=True)
    col_l, col_r = st.columns([3,2])
    with col_l:
        st.markdown(income_table(INCOME_2024, "$65,626"), unsafe_allow_html=True)
    with col_r:
        st.markdown(section_head("Spending Mix"), unsafe_allow_html=True)
        fig_d24 = styled_fig(280)
        vals24 = [round(ann24[c]) for c in CATS]
        fig_d24.add_trace(go.Pie(labels=CATS, values=vals24,
                                  marker=dict(colors=[CAT_COLORS[c] for c in CATS], line=dict(color='#fff',width=2)),
                                  hole=0.62, textinfo='percent', textfont_size=10,
                                  hovertemplate='<b>%{label}</b><br>$%{value:,.0f} (%{percent})<extra></extra>'))
        fig_d24.update_layout(legend=dict(orientation='h',y=-0.2,font_size=10), showlegend=True)
        st.plotly_chart(fig_d24, use_container_width=True, config=dict(displayModeBar=False))

    st.markdown(section_head("Monthly Spending by Category"), unsafe_allow_html=True)
    df24 = df_all[df_all['yr']==2024]
    fig_b24 = styled_fig(300)
    for c in CATS:
        fig_b24.add_trace(go.Bar(name=c, x=df24['label'], y=df24[c].round(),
                                  marker_color=CAT_COLORS[c], marker_line_width=0,
                                  hovertemplate=f'<b>%{{x}}</b><br>{c}: $%{{y:,.0f}}<extra></extra>'))
    fig_b24.update_layout(barmode='stack', legend=dict(orientation='h',y=1.08,font_size=10))
    ax(fig_b24)
    st.plotly_chart(fig_b24, use_container_width=True, config=dict(displayModeBar=False))

    st.markdown(section_head("Monthly Detail"), unsafe_allow_html=True)
    st.markdown(exp_table(df24), unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
#  2025 TAB
# ════════════════════════════════════════════════════════════════════════════
with t_2025:
    st.markdown(section_head("2025 — Full Year", "Sources: 2× Amazon W-2s · Robinhood 1099-B/DIV/INT · Cash App 1099-DA"), unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi("W-2 Gross Income","$88,120","Amazon Dev + Amazon Services",delta="↑ 40.5% vs 2024",good=True,icon="💼",color="#059669"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Investment Income","$37,935","Robinhood cap gains + dividends",icon="📈",color="#0891B2"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Total Spent",fmt(ann25['total']),"Incl. $39,541 rent (12 mo)",delta=f"↑ {(ann25['total']/ann24['total']-1)*100:.0f}% vs 2024",good=False,icon="💳",color="#EF4444"), unsafe_allow_html=True)
    sr25 = (88120 - ann25['total']) / 88120 * 100
    with c4: st.markdown(kpi("Savings Rate (W-2)",f"{sr25:.1f}%",f"${88120-ann25['total']:,.0f} saved vs gross W-2",delta="✓ Healthy",good=True,icon="📊",color="#F59E0B"), unsafe_allow_html=True)

    st.markdown(section_head("Income Sources"), unsafe_allow_html=True)
    col_l, col_r = st.columns([3,2])
    with col_l:
        st.markdown(income_table(INCOME_2025, "$126,335"), unsafe_allow_html=True)
    with col_r:
        st.markdown(section_head("Spending Mix"), unsafe_allow_html=True)
        fig_d25 = styled_fig(280)
        vals25 = [round(ann25[c]) for c in CATS]
        fig_d25.add_trace(go.Pie(labels=CATS, values=vals25,
                                  marker=dict(colors=[CAT_COLORS[c] for c in CATS], line=dict(color='#fff',width=2)),
                                  hole=0.62, textinfo='percent', textfont_size=10,
                                  hovertemplate='<b>%{label}</b><br>$%{value:,.0f} (%{percent})<extra></extra>'))
        fig_d25.update_layout(legend=dict(orientation='h',y=-0.2,font_size=10), showlegend=True)
        st.plotly_chart(fig_d25, use_container_width=True, config=dict(displayModeBar=False))

    st.markdown(section_head("Monthly Spending by Category"), unsafe_allow_html=True)
    df25 = df_all[df_all['yr']==2025]
    fig_b25 = styled_fig(310)
    for c in CATS:
        fig_b25.add_trace(go.Bar(name=c, x=df25['label'], y=df25[c].round(),
                                  marker_color=CAT_COLORS[c], marker_line_width=0,
                                  hovertemplate=f'<b>%{{x}}</b><br>{c}: $%{{y:,.0f}}<extra></extra>'))
    fig_b25.update_layout(barmode='stack', legend=dict(orientation='h',y=1.08,font_size=10))
    ax(fig_b25)
    st.plotly_chart(fig_b25, use_container_width=True, config=dict(displayModeBar=False))

    st.markdown(section_head("Monthly Take-Home vs. Expenses", "Net income = paycheck deposits captured in expense sheets"), unsafe_allow_html=True)
    fig_ie25 = styled_fig(300)
    fig_ie25.add_trace(go.Bar(name='Net Take-Home', x=df25['label'], y=df25['Income'].round(),
                               marker_color='rgba(5,150,105,0.82)', marker_line_width=0,
                               hovertemplate='<b>%{x}</b><br>Take-Home: $%{y:,.0f}<extra></extra>'))
    fig_ie25.add_trace(go.Bar(name='Total Expenses', x=df25['label'], y=df25['total'].round(),
                               marker_color='rgba(239,68,68,0.82)', marker_line_width=0,
                               hovertemplate='<b>%{x}</b><br>Expenses: $%{y:,.0f}<extra></extra>'))
    fig_ie25.update_layout(barmode='group', legend=dict(orientation='h',y=1.08,font_size=10))
    ax(fig_ie25)
    st.plotly_chart(fig_ie25, use_container_width=True, config=dict(displayModeBar=False))

    st.markdown(section_head("Monthly Detail"), unsafe_allow_html=True)
    st.markdown(exp_table(df25, show_income=True), unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
#  2026 TAB
# ════════════════════════════════════════════════════════════════════════════
with t_2026:
    st.markdown(section_head("2026 — Year to Date", f"{n26} months tracked · Jan – Feb"), unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1: st.markdown(kpi("YTD Spent",fmt(ann26['total']),f"{n26} months",icon="🗓",color="#7C3AED"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Monthly Average",fmt(ann26['total']/max(n26,1)),"per month tracked",icon="📅",color="#2563EB"), unsafe_allow_html=True)
    top26 = max(CATS, key=lambda c: ann26[c])
    with c3: st.markdown(kpi("Top Category",top26,fmt(ann26[top26])+" YTD",icon="🏆",color="#F59E0B"), unsafe_allow_html=True)

    st.info("💡 Jan & Feb 2026 rent ($50 and $40) appears partial — Bilt payment may not yet be captured in those months.")

    df26 = df_all[df_all['yr']==2026]
    col_l, col_r = st.columns([1,1])
    with col_l:
        st.markdown(section_head("Monthly Spending"), unsafe_allow_html=True)
        fig_b26 = styled_fig(300)
        for c in CATS:
            if ann26[c] > 0:
                fig_b26.add_trace(go.Bar(name=c, x=df26['label'], y=df26[c].round(),
                                          marker_color=CAT_COLORS[c], marker_line_width=0,
                                          hovertemplate=f'<b>%{{x}}</b><br>{c}: $%{{y:,.0f}}<extra></extra>'))
        fig_b26.update_layout(barmode='stack', legend=dict(orientation='h',y=1.1,font_size=10))
        ax(fig_b26)
        st.plotly_chart(fig_b26, use_container_width=True, config=dict(displayModeBar=False))

    with col_r:
        st.markdown(section_head("Spending Mix"), unsafe_allow_html=True)
        active26 = [c for c in CATS if ann26[c]>0]
        fig_d26 = styled_fig(300)
        fig_d26.add_trace(go.Pie(labels=active26, values=[round(ann26[c]) for c in active26],
                                  marker=dict(colors=[CAT_COLORS[c] for c in active26], line=dict(color='#fff',width=2)),
                                  hole=0.62, textinfo='percent', textfont_size=10,
                                  hovertemplate='<b>%{label}</b><br>$%{value:,.0f} (%{percent})<extra></extra>'))
        fig_d26.update_layout(legend=dict(orientation='h',y=-0.2,font_size=10), showlegend=True)
        st.plotly_chart(fig_d26, use_container_width=True, config=dict(displayModeBar=False))

    if n26 > 0:
        st.markdown(section_head("Same-Period Comparison", "2026 YTD vs same months in 2025"), unsafe_allow_html=True)
        df25_same = df_all[(df_all['yr']==2025)&(df_all['mo'].isin(df26['mo'].tolist()))]
        fig_comp = styled_fig(260)
        fig_comp.add_trace(go.Bar(name='2025 (same months)', x=df25_same['label'],
                                   y=df25_same['total'].round(), marker_color='rgba(239,68,68,0.7)', marker_line_width=0))
        fig_comp.add_trace(go.Bar(name='2026', x=df26['label'],
                                   y=df26['total'].round(), marker_color='rgba(124,58,237,0.82)', marker_line_width=0))
        fig_comp.update_layout(barmode='group', legend=dict(orientation='h',y=1.1,font_size=11))
        ax(fig_comp)
        st.plotly_chart(fig_comp, use_container_width=True, config=dict(displayModeBar=False))

    st.markdown(section_head("Monthly Detail"), unsafe_allow_html=True)
    st.markdown(exp_table(df26), unsafe_allow_html=True)
