import importlib

import streamlit as st

from style import inject_css

st.set_page_config(
    page_title="LHQLab - Data Mining Studio",
    page_icon="\U0001f4ca",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

PAGES = {
    "Trang Ch\u1ee7": "page_home",
    "Ti\u1ec1n X\u1eed L\u00fd D\u1eef Li\u1ec7u": "page_preprocessing",
    "Lu\u1eadt K\u1ebft H\u1ee3p": "page_apriori",
    "T\u1eadp Th\u00f4": "page_rough_sets",
    "Naive Bayes": "page_naive_bayes",
    "C\u00e2y Quy\u1ebft \u0110\u1ecbnh": "page_decision_tree",
    "Thu\u1eadt To\u00e1n K-Means": "page_kmeans",
    "M\u1ea1ng Kohonen": "page_kohonen",
}

with st.sidebar:
    st.markdown(
        """
<div class="dm-brand">
    <div class="dm-brand-logo">
        <svg width="38" height="38" viewBox="0 0 38 38" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="38" height="38" rx="9" fill="#1A56DB"/>
            <circle cx="11" cy="27" r="3.5" fill="white"/>
            <circle cx="19" cy="15" r="3.5" fill="white"/>
            <circle cx="28" cy="21" r="3.5" fill="white"/>
            <circle cx="15" cy="9"  r="2.2" fill="rgba(255,255,255,0.55)"/>
            <line x1="11" y1="27" x2="19" y2="15" stroke="white" stroke-width="1.4" stroke-opacity="0.45"/>
            <line x1="19" y1="15" x2="28" y2="21" stroke="white" stroke-width="1.4" stroke-opacity="0.45"/>
            <line x1="15" y1="9"  x2="19" y2="15" stroke="white" stroke-width="1.4" stroke-opacity="0.3"/>
        </svg>
    </div>
    <div class="dm-brand-text">
        <div class="dm-brand-title">LHQLab - Data Mining Studio</div>
        <div class="dm-brand-sub">Nh&#243;m 10 - IS252.Q21</div>
    </div>
</div>
<div class="dm-sidebar-divider"></div>
""",
        unsafe_allow_html=True,
    )
    selected = st.radio("nav", list(PAGES.keys()), label_visibility="collapsed")

module_name = PAGES[selected]
module = importlib.import_module(module_name)
module.show()
