import streamlit as st

PRIMARY   = "#1A56DB"
ORANGE    = "#D97706"
GREEN     = "#059669"
PURPLE    = "#7C3AED"
DARK      = "#1E3A5F"
MUTED     = "#64748B"
BORDER    = "#DBEAFE"
LIGHT_BG  = "#F0F4F8"

CATEGORIES = [
    {
        "name": "Xử Lý Dữ Liệu",
        "color": PRIMARY,
        "algos": [
            {
                "icon": "⚙",
                "lesson": "Bài 1-2",
                "name": "Tiền Xử Lý Dữ Liệu",
                "desc": "Xử lý giá trị thiếu (Mean/Median/Mode), chuẩn hóa Min-Max & Z-score, rời rạc hóa Equal-Width / Equal-Frequency.",
                "tags": ["Missing Values", "Normalization", "Binning"],
            },
        ],
    },
    {
        "name": "Khai Thác Luật Kết Hợp",
        "color": ORANGE,
        "algos": [
            {
                "icon": "◈",
                "lesson": "Bài 2",
                "name": "Luật Kết Hợp — Apriori",
                "desc": "Tìm tập phổ biến bằng thuật toán Apriori, sinh luật kết hợp theo ngưỡng Support và Confidence.",
                "tags": ["Support", "Confidence", "Association Rules"],
            },
        ],
    },
    {
        "name": "Phân Lớp",
        "color": GREEN,
        "algos": [
            {
                "icon": "⊟",
                "lesson": "Bài 3",
                "name": "Tập Thô — Rough Sets",
                "desc": "Xấp xỉ trên/dưới, vùng biên, độ chính xác α và tìm Reduct từ ma trận phân biệt.",
                "tags": ["Approximation", "Boundary Region", "Reduct"],
            },
            {
                "icon": "∑",
                "lesson": "Bài 4 & 7",
                "name": "Naive Bayes",
                "desc": "Phân lớp theo định lý Bayes, hỗ trợ làm trơn Laplace. Ví dụ: đi chơi, Golf, dự đoán Laptop.",
                "tags": ["Bayesian", "Laplace Smoothing", "Classification"],
            },
            {
                "icon": "⊳",
                "lesson": "Bài 5",
                "name": "Cây Quyết Định — ID3",
                "desc": "Xây dựng cây quyết định theo ID3 dùng Entropy & Information Gain. Ví dụ: Golf, Trốn thuế.",
                "tags": ["Entropy", "Information Gain", "ID3"],
            },
        ],
    },
    {
        "name": "Gom Cụm",
        "color": PURPLE,
        "algos": [
            {
                "icon": "◎",
                "lesson": "Bài 6",
                "name": "K-Means",
                "desc": "Gom cụm theo vector trọng tâm, hiển thị từng iteration đến hội tụ. Ví dụ: 4 điểm 2D, k=2.",
                "tags": ["Centroid", "Euclidean Distance", "Clustering"],
            },
            {
                "icon": "⊙",
                "lesson": "Bài 8",
                "name": "Mạng Kohonen — SOM",
                "desc": "Self-Organizing Map: học không giám sát, trọng số nơron tiến hóa qua từng epoch.",
                "tags": ["SOM", "Neural Network", "Unsupervised"],
            },
        ],
    },
]


def _tags_html(tags, color):
    parts = []
    for t in tags:
        parts.append(
            f'<span style="display:inline-block;background:{color}15;color:{color};'
            f'border:1px solid {color}30;border-radius:20px;padding:1px 9px;'
            f'font-size:0.72em;font-weight:600;margin:3px 3px 0 0">{t}</span>'
        )
    return "".join(parts)


def _algo_card(algo, color):
    tags = _tags_html(algo["tags"], color)
    return f"""
<div class="dm-algo-card" style="border-top:3px solid {color};height:100%">
    <div style="font-size:1.5em;margin-bottom:4px;color:{color}">{algo["icon"]}</div>
    <span style="display:inline-block;background:{color};color:white;padding:2px 10px;
                 border-radius:20px;font-size:0.72em;font-weight:700;margin-bottom:8px">
        {algo["lesson"]}
    </span>
    <h4 style="color:{DARK};font-weight:700;margin:0 0 6px 0;font-size:0.98em;
               line-height:1.3">{algo["name"]}</h4>
    <p style="color:{MUTED};font-size:0.85em;margin:0 0 10px 0;line-height:1.55">
        {algo["desc"]}
    </p>
    <div>{tags}</div>
</div>
"""


def _section_header(name, color, count):
    return f"""
<div class="dm-step-header" style="display:none"></div>
<div style="display:flex;align-items:center;gap:10px;
            margin:0 0 14px 0;padding-bottom:10px;
            border-bottom:2px solid {BORDER}">
    <span style="width:10px;height:10px;border-radius:50%;
                 background:{color};display:inline-block;flex-shrink:0"></span>
    <span style="font-size:0.78em;font-weight:700;color:{MUTED};
                 letter-spacing:0.7px;text-transform:uppercase">{name}</span>
    <span style="margin-left:auto;font-size:0.75em;color:{MUTED};
                 background:{LIGHT_BG};padding:1px 10px;border-radius:20px;
                 border:1px solid {BORDER}">{count} thuật toán</span>
</div>
"""


def show():
    # ── Hero ───────────────────────────────────────────────────
    st.markdown("""
<div class="dm-hero">
    <h1>LHQLab - Data Mining Studio</h1>
    <p>Minh họa tương tác các thuật toán trong môn <strong>Data Mining</strong>
       — tất cả ví dụ lấy trực tiếp từ bài giảng.</p>
    <span class="gv-badge">GV: Thầy Mai Xuân Hùng</span>
</div>
""", unsafe_allow_html=True)

    # ── Stat metrics ───────────────────────────────────────────
    with st.container(border=True):
        st.markdown('<div class="dm-step-header" style="display:none"></div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Thuật toán", "7")
        with c2:
            st.metric("Nhóm phương pháp", "4")
        with c3:
            st.metric("Tập dữ liệu", "16")
        with c4:
            st.metric("Từ bài giảng", "100%")

    # ── Categories ─────────────────────────────────────────────
    for cat in CATEGORIES:
        n = len(cat["algos"])
        ncols = min(n, 3)

        with st.container(border=True):
            st.markdown(
                _section_header(cat["name"], cat["color"], n),
                unsafe_allow_html=True,
            )
            cols = st.columns(ncols)
            for i, algo in enumerate(cat["algos"]):
                with cols[i % ncols]:
                    st.markdown(_algo_card(algo, cat["color"]), unsafe_allow_html=True)

    # ── Footer tip ─────────────────────────────────────────────
    st.markdown("<div style='margin-top:32px'></div>", unsafe_allow_html=True)
    st.markdown(
        '<div class="dm-info">💡 Chọn thuật toán ở thanh bên trái để xem minh họa từng bước với dữ liệu từ bài giảng.</div>',
        unsafe_allow_html=True,
    )
