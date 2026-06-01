import streamlit as st

# ── Color tokens ──────────────────────────────────────────────
PRIMARY       = "#1A56DB"
PRIMARY_DARK  = "#1E3A5F"
PRIMARY_LIGHT = "#EBF3FF"
BORDER        = "#DBEAFE"
BG            = "#F0F4F8"
SURFACE       = "#FFFFFF"
TEXT          = "#1E293B"
TEXT_MUTED    = "#64748B"
SUCCESS       = "#059669"
SUCCESS_BG    = "#ECFDF5"
WARNING       = "#D97706"
WARNING_BG    = "#FFFBEB"
ERROR         = "#DC2626"
ERROR_BG      = "#FEF2F2"


def inject_css():
    st.markdown(f"""
<style>
/* ── GLOBAL ─────────────────────────────────────────── */
html, body, [class*="css"] {{
    font-family: 'Inter', 'Segoe UI', sans-serif;
}}

/* ── SIDEBAR ────────────────────────────────────────── */
[data-testid="stSidebar"] {{
    background-color: {SURFACE} !important;
    border-right: 1px solid {BORDER} !important;
    box-shadow: 2px 0 12px rgba(26,86,219,0.06) !important;
    overflow-x: hidden !important;
}}

/* Zero padding trên toàn bộ sidebar wrapper — kể cả .block-container */
[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] > div > div,
[data-testid="stSidebar"] > div > div > div,
[data-testid="stSidebar"] .block-container,
[data-testid="stSidebarContent"],
[data-testid="stSidebarUserContent"] {{
    padding-left: 0 !important;
    padding-right: 0 !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}}

/* Brand block */
.dm-brand {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 20px 12px 20px;
}}

.dm-brand-logo {{
    flex-shrink: 0;
    line-height: 0;
}}

.dm-brand-title {{
    font-size: 15px;
    font-weight: 700;
    color: {PRIMARY_DARK};
    line-height: 1.3;
}}

.dm-brand-sub {{
    font-size: 13px;
    color: {TEXT_MUTED};
    line-height: 1.35;
    margin-top: 3px;
}}

.dm-sidebar-divider {{
    height: 1px;
    background: {BORDER};
    margin: 0 0 6px 0;
}}

/* Ẩn chữ "nav" — widget label của radio */
[data-testid="stSidebar"] .stRadio > label,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] .stRadio > div:first-of-type:not(:last-of-type) {{
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    visibility: hidden !important;
    position: absolute !important;
}}

/* Sidebar radio — nav menu container */
[data-testid="stSidebar"] .stRadio,
[data-testid="stSidebar"] .stRadio > div,
[data-testid="stSidebar"] .stRadio > div > div {{
    padding: 0 !important;
    margin: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
}}

[data-testid="stSidebar"] .stRadio > div {{
    gap: 2px !important;
    flex-direction: column !important;
}}

/* Nav item label
   width: 200% + overflow-x:hidden trên sidebar = tự bleed đến mép phải */
[data-testid="stSidebar"] .stRadio label {{
    background: transparent !important;
    padding: 11px 20px !important;
    cursor: pointer !important;
    transition: background 0.15s, color 0.15s !important;
    color: {TEXT} !important;
    font-size: 1em !important;
    font-weight: 500 !important;
    border: none !important;
    border-left: 3px solid transparent !important;
    width: 200% !important;
    box-sizing: border-box !important;
    display: flex !important;
    align-items: center !important;
    margin: 0 !important;
    border-radius: 0 !important;
}}

[data-testid="stSidebar"] .stRadio label:hover {{
    background: {PRIMARY_LIGHT} !important;
    color: {PRIMARY} !important;
}}

/* Active state */
[data-testid="stSidebar"] .stRadio label:has(input[type="radio"]:checked) {{
    background: {PRIMARY_LIGHT} !important;
    color: {PRIMARY} !important;
    font-weight: 600 !important;
    border-left: 3px solid {PRIMARY} !important;
}}

/* Ẩn radio circle input */
[data-testid="stSidebar"] .stRadio input[type="radio"] {{
    display: none !important;
}}

/* Ẩn div visual của radio circle (con đầu tiên của label) */
[data-testid="stSidebar"] .stRadio label > div:first-child {{
    display: none !important;
}}

[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {{
    font-size: 1em !important;
    margin: 0 !important;
    line-height: 1.4 !important;
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    letter-spacing: normal !important;
    word-spacing: normal !important;
    white-space: nowrap !important;
    text-align: left !important;
}}

[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p::before {{
    width: 20px !important;
    min-width: 20px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    line-height: 1 !important;
    color: inherit !important;
}}

[data-testid="stSidebar"] .stRadio label:nth-of-type(1) [data-testid="stMarkdownContainer"] p::before {{
    content: "\\2302";
}}

[data-testid="stSidebar"] .stRadio label:nth-of-type(2) [data-testid="stMarkdownContainer"] p::before {{
    content: "\\2699";
}}

[data-testid="stSidebar"] .stRadio label:nth-of-type(3) [data-testid="stMarkdownContainer"] p::before {{
    content: "\\25C8";
}}

[data-testid="stSidebar"] .stRadio label:nth-of-type(4) [data-testid="stMarkdownContainer"] p::before {{
    content: "\\229F";
}}

[data-testid="stSidebar"] .stRadio label:nth-of-type(5) [data-testid="stMarkdownContainer"] p::before {{
    content: "\\2211";
}}

[data-testid="stSidebar"] .stRadio label:nth-of-type(6) [data-testid="stMarkdownContainer"] p::before {{
    content: "\\22B3";
}}

[data-testid="stSidebar"] .stRadio label:nth-of-type(7) [data-testid="stMarkdownContainer"] p::before {{
    content: "\\25CE";
}}

[data-testid="stSidebar"] .stRadio label:nth-of-type(8) [data-testid="stMarkdownContainer"] p::before {{
    content: "\\2299";
}}

/* ── TOPBAR ─────────────────────────────────────────── */
header[data-testid="stHeader"] {{
    background-color: {SURFACE} !important;
    border-bottom: 1px solid {BORDER} !important;
}}

/* ── HEADINGS ───────────────────────────────────────── */
.stApp h1 {{
    color: {PRIMARY_DARK} !important;
    font-weight: 700 !important;
    padding-bottom: 10px !important;
    border-bottom: 3px solid {PRIMARY} !important;
    margin-bottom: 4px !important;
}}

.stApp h2 {{
    color: {PRIMARY_DARK} !important;
    font-weight: 600 !important;
}}

.stApp h3 {{
    color: {TEXT} !important;
    font-weight: 600 !important;
}}

/* ── BUTTONS ────────────────────────────────────────── */
.stButton > button {{
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
    border: none !important;
}}

.stButton > button[kind="primary"],
.stButton > button:not([kind]) {{
    background-color: {PRIMARY} !important;
    color: white !important;
    box-shadow: 0 2px 8px rgba(26,86,219,0.25) !important;
    padding: 10px 0 !important;
}}

.stButton > button[kind="primary"]:hover,
.stButton > button:not([kind]):hover {{
    background-color: #1547C0 !important;
    box-shadow: 0 4px 16px rgba(26,86,219,0.35) !important;
    transform: translateY(-1px) !important;
}}

.stButton > button[kind="secondary"] {{
    background: transparent !important;
    border: 2px solid {PRIMARY} !important;
    color: {PRIMARY} !important;
}}

.stButton > button[kind="secondary"]:hover {{
    background: {PRIMARY_LIGHT} !important;
}}

/* ── EXPANDERS ──────────────────────────────────────── */
[data-testid="stExpander"] {{
    background: {SURFACE} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
    margin-bottom: 8px !important;
    overflow: hidden !important;
}}

[data-testid="stExpander"] summary {{
    font-weight: 600 !important;
    color: {PRIMARY_DARK} !important;
    padding: 12px 16px !important;
}}

[data-testid="stExpander"] summary:hover {{
    background: {PRIMARY_LIGHT} !important;
}}

[data-testid="stExpander"][open] {{
    border-left: 3px solid {PRIMARY} !important;
}}

/* ── METRICS ────────────────────────────────────────── */
[data-testid="metric-container"] {{
    background: {SURFACE} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    padding: 16px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    border-left: 4px solid {PRIMARY} !important;
}}

[data-testid="stMetricLabel"] {{
    color: {TEXT_MUTED} !important;
    font-size: 0.85em !important;
    font-weight: 500 !important;
}}

[data-testid="stMetricValue"] {{
    color: {PRIMARY_DARK} !important;
    font-weight: 700 !important;
}}

/* ── DATAFRAMES ─────────────────────────────────────── */
[data-testid="stDataFrame"] {{
    border-radius: 10px !important;
    overflow: hidden !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
    border: 1px solid {BORDER} !important;
}}

/* ── PLOTLY CHARTS ──────────────────────────────────── */
[data-testid="stPlotlyChart"] {{
    background: {SURFACE} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 10px rgba(26,86,219,0.07) !important;
    overflow: hidden !important;
    padding: 4px !important;
}}

/* ── ALERTS ─────────────────────────────────────────── */
[data-testid="stAlert"] {{
    border-radius: 10px !important;
    border-left-width: 4px !important;
}}

/* ── INPUTS ─────────────────────────────────────────── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {{
    border-radius: 8px !important;
    border-color: {BORDER} !important;
}}

[data-testid="stSlider"] [data-testid="stMarkdownContainer"] p {{
    font-weight: 600 !important;
    color: {TEXT} !important;
}}

/* ── RADIO (main content) ───────────────────────────── */
.stRadio label {{
    font-size: 0.9em !important;
}}

/* ── TABS ───────────────────────────────────────────── */
[data-testid="stTabs"] {{
    border-bottom: 2px solid {BORDER} !important;
}}

[data-testid="stTab"] {{
    border-radius: 8px 8px 0 0 !important;
}}

/* ── DIVIDER ────────────────────────────────────────── */
hr {{
    border-color: {BORDER} !important;
    margin: 16px 0 !important;
}}

/* ── MAIN BLOCK CONTAINER ───────────────────────────── */
.main .block-container {{
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
    max-width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
}}

/* Override Streamlit's own stMainBlockContainer padding */
[data-testid="stMainBlockContainer"] {{
    padding-left: 3rem !important;
    padding-right: 3rem !important;
    max-width: 100% !important;
}}

/* ── SECTION CARDS (st.container border=True) ───────── */
/* Target bordered stVerticalBlock that directly contains a step header */
[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .dm-step-header) {{
    --background-color: #FFFFFF;
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    border: 1px solid {BORDER} !important;
    border-radius: 14px !important;
    box-shadow: 0 3px 16px rgba(26,86,219,0.08) !important;
    margin-bottom: 20px !important;
    padding: 20px 24px !important;
}}

[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .dm-step-header)
[data-testid="stElementContainer"] {{
    background: transparent !important;
    background-color: transparent !important;
}}

[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .dm-step-header)
.dm-step-header {{
    margin-top: 0 !important;
}}

/* ── CUSTOM HTML COMPONENTS ─────────────────────────── */

/* Card container */
.dm-card {{
    background: {SURFACE};
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 2px 8px rgba(26,86,219,0.07);
    border: 1px solid {BORDER};
    margin-bottom: 16px;
}}

/* Step header */
.dm-step-header {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 20px 0 12px 0;
}}

.dm-step-badge {{
    background: {PRIMARY};
    color: white;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.78em;
    font-weight: 700;
    white-space: nowrap;
    letter-spacing: 0.3px;
}}

.dm-step-title {{
    color: {PRIMARY_DARK};
    font-weight: 600;
    font-size: 1.05em;
    margin: 0;
}}

/* Sub-step header (dùng bên trong card kết quả) */
.dm-substep-header {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 20px 0 10px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid {BORDER};
}}

.dm-substep-header:first-child {{
    margin-top: 4px;
}}

.dm-substep-badge {{
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: {PRIMARY_LIGHT};
    color: {PRIMARY};
    font-size: 0.78em;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    border: 1px solid {BORDER};
}}

.dm-substep-title {{
    color: {PRIMARY_DARK};
    font-weight: 600;
    font-size: 0.95em;
    margin: 0;
}}

/* Result highlight box */
.dm-result {{
    background: {PRIMARY_LIGHT};
    border-left: 4px solid {PRIMARY};
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    color: {PRIMARY_DARK};
    font-weight: 600;
    margin: 8px 0;
}}

/* Info box */
.dm-info {{
    background: {PRIMARY_LIGHT};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 12px 16px;
    color: {PRIMARY_DARK};
    font-size: 0.9em;
    margin-bottom: 16px;
}}

/* Success box */
.dm-success {{
    background: {SUCCESS_BG};
    border-left: 4px solid {SUCCESS};
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    color: #065F46;
    font-weight: 600;
}}

/* Warning box */
.dm-warning {{
    background: {WARNING_BG};
    border-left: 4px solid {WARNING};
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    color: #92400E;
}}

/* Lesson badge (dùng trong home) */
.dm-lesson-badge {{
    display: inline-block;
    background: {PRIMARY};
    color: white;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75em;
    font-weight: 700;
    letter-spacing: 0.3px;
    margin-bottom: 6px;
}}

/* Home algorithm card */
.dm-algo-card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 14px;
    box-shadow: 0 2px 12px rgba(26,86,219,0.07);
    transition: box-shadow 0.2s, transform 0.2s;
    cursor: default;
    height: 100%;
}}

.dm-algo-card:hover {{
    box-shadow: 0 6px 20px rgba(26,86,219,0.14);
    transform: translateY(-2px);
}}

.dm-algo-card h4 {{
    color: {PRIMARY_DARK} !important;
    font-weight: 700 !important;
    margin: 8px 0 6px 0 !important;
    font-size: 1.05em !important;
    border: none !important;
}}

.dm-algo-card p {{
    color: {TEXT_MUTED} !important;
    font-size: 0.88em !important;
    margin: 0 !important;
    line-height: 1.5 !important;
}}

.dm-icon {{
    font-size: 1.8em;
    margin-bottom: 4px;
}}

/* Hero section on home */
.dm-hero {{
    background: linear-gradient(135deg, {PRIMARY_DARK} 0%, #2563EB 100%);
    border-radius: 16px;
    padding: 32px 36px;
    color: white;
    margin-bottom: 28px;
}}

.dm-hero h1 {{
    color: white !important;
    border-bottom: none !important;
    font-size: 2em !important;
    margin-bottom: 8px !important;
}}

.dm-hero p {{
    color: rgba(255,255,255,0.85) !important;
    font-size: 1em !important;
    margin: 0 !important;
}}

.dm-hero .gv-badge {{
    display: inline-block;
    background: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.4);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.85em;
    margin-top: 12px;
    color: white;
}}
</style>
""", unsafe_allow_html=True)


# ── Helper functions cho các page ─────────────────────────────

def step(number: int, title: str):
    """Hiển thị header bước với badge số."""
    st.markdown(f"""
<div class="dm-step-header">
    <span class="dm-step-badge">Bước {number}</span>
    <span class="dm-step-title">{title}</span>
</div>
""", unsafe_allow_html=True)


def substep(number: int, title: str):
    """Header bước con, dùng bên trong card kết quả."""
    st.markdown(f"""
<div class="dm-substep-header">
    <span class="dm-substep-badge">{number}</span>
    <span class="dm-substep-title">{title}</span>
</div>
""", unsafe_allow_html=True)


def result_header(title: str):
    """Header card kết quả (màu xanh lá, không số bước) — dùng cho output động."""
    st.markdown(f"""
<div class="dm-step-header">
    <span class="dm-step-badge" style="background:#059669">Kết quả</span>
    <span class="dm-step-title">{title}</span>
</div>
""", unsafe_allow_html=True)


def input_header(title: str):
    """Header card nhập liệu/dữ liệu (màu xám, không số bước)."""
    st.markdown(f"""
<div class="dm-step-header">
    <span class="dm-step-badge" style="background:{TEXT_MUTED}">Dữ liệu</span>
    <span class="dm-step-title">{title}</span>
</div>
""", unsafe_allow_html=True)


def result_box(text: str):
    st.markdown(f'<div class="dm-result">{text}</div>', unsafe_allow_html=True)


def info_box(text: str):
    st.markdown(f'<div class="dm-info">ℹ️ &nbsp;{text}</div>', unsafe_allow_html=True)


def success_box(text: str):
    st.markdown(f'<div class="dm-success">✅ &nbsp;{text}</div>', unsafe_allow_html=True)


def warning_box(text: str):
    st.markdown(f'<div class="dm-warning">⚠️ &nbsp;{text}</div>', unsafe_allow_html=True)
