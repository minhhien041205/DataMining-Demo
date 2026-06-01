import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datasets import BAYES_DATASETS
from style import step, input_header, info_box, success_box, warning_box, result_box


def train_bayes(df, target_col, laplace=False):
    classes = sorted(df[target_col].unique())
    n = len(df)
    m = len(classes)
    feature_cols = [c for c in df.columns if c != target_col]
    priors = {}
    likelihoods = {}

    for c in classes:
        df_c = df[df[target_col] == c]
        n_c = len(df_c)
        priors[c] = (n_c + 1) / (n + m) if laplace else n_c / n
        likelihoods[c] = {}
        for col in feature_cols:
            n_vals = df[col].nunique()
            likelihoods[c][col] = {}
            for val in df[col].unique():
                count = (df_c[col] == val).sum()
                if laplace:
                    likelihoods[c][col][val] = (count + 1) / (n_c + n_vals)
                else:
                    likelihoods[c][col][val] = count / n_c if n_c > 0 else 0

    return priors, likelihoods, classes, feature_cols


def predict_bayes(sample, priors, likelihoods, classes, feature_cols):
    scores = {}
    breakdowns = {}
    for c in classes:
        score = priors[c]
        detail = [("P(C)", round(priors[c], 6))]
        for col in feature_cols:
            val = sample.get(col)
            p = likelihoods[c].get(col, {}).get(val, 0)
            score *= p
            detail.append((f"P({col}={val}|{c})", round(p, 6)))
        scores[c] = round(score, 6)
        breakdowns[c] = detail
    return scores, breakdowns


def show():
    st.title("📊 Phân Lớp Naive Bayes")
    st.markdown("**Bài 4 & 7** — Phân lớp dựa trên định lý Bayes")
    st.markdown("---")

    ds_name = st.radio("Chọn tập dữ liệu:", list(BAYES_DATASETS.keys()))
    ds = BAYES_DATASETS[ds_name]
    info_box(ds["description"])

    df = ds["df"].copy()
    target_col = ds["target_col"]
    laplace = ds.get("laplace", False)
    feature_cols = [c for c in df.columns if c != target_col]

    with st.container(border=True):
        input_header("Tập dữ liệu huấn luyện")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with st.container(border=True):
        input_header("Mẫu cần phân lớp")
        if laplace:
            info_box("Tập dữ liệu này dùng <strong>làm trơn Laplace</strong> để tránh xác suất = 0.")
        default_sample = ds["test_sample"]
        sample_input = {}
        cols = st.columns(len(feature_cols))
        for i, col in enumerate(feature_cols):
            vals = sorted(df[col].unique().tolist())
            default_val = default_sample.get(col, vals[0])
            idx = vals.index(default_val) if default_val in vals else 0
            with cols[i]:
                sample_input[col] = st.selectbox(col, vals, index=idx, key=f"sel_{col}")
        st.markdown(f"**Mẫu X:** `{ds['test_label']}`")
        clicked = st.button("▶ Chạy Naive Bayes", use_container_width=True, type="primary")

    if clicked:
        _show_steps(df, target_col, feature_cols, sample_input, laplace)


def _show_steps(df, target_col, feature_cols, sample, laplace):
    priors, likelihoods, classes, _ = train_bayes(df, target_col, laplace)
    scores, breakdowns = predict_bayes(sample, priors, likelihoods, classes, feature_cols)

    formula = "P(Ci) = (|Ci|+1)/(|D|+m)" if laplace else "P(Ci) = |Ci| / |D|"
    with st.container(border=True):
        step(1, f"Ước lượng P(Ci) — {formula}")
        rows_p = []
        for c in classes:
            n_c = (df[target_col] == c).sum()
            rows_p.append({"Lớp (Ci)": c, "Số mẫu |Ci|": n_c, "P(Ci)": round(priors[c], 4)})
        st.dataframe(pd.DataFrame(rows_p), use_container_width=True, hide_index=True)

    p_formula = "P(Xk|Ci) = (count+1)/(|Ci|+r)" if laplace else "P(Xk|Ci) = count / |Ci|"
    with st.container(border=True):
        step(2, f"Ước lượng P(Xk|Ci) — {p_formula}")
        for col in feature_cols:
            with st.expander(f"Thuộc tính: **{col}**", expanded=True):
                vals = sorted(df[col].unique())
                rows_like = [
                    {"Giá trị": val, **{c: round(likelihoods[c][col].get(val, 0), 4) for c in classes}}
                    for val in vals
                ]
                st.dataframe(pd.DataFrame(rows_like), use_container_width=True, hide_index=True)
                val_x = sample.get(col)
                st.markdown(f"→ Mẫu X có `{col} = {val_x}` — dùng hàng **{val_x}**")

    with st.container(border=True):
        step(3, "Tính P(Ci|X) ∝ P(X|Ci)·P(Ci)")
        for c in classes:
            with st.expander(f"Lớp **{c}**", expanded=True):
                detail = breakdowns[c]
                parts = [f"`{label}` = {val}" for label, val in detail]
                st.markdown("  ×  ".join(parts))
                st.markdown(f"**= {scores[c]}**")

    with st.container(border=True):
        step(4, "Kết quả phân lớp")
        best_class = max(scores, key=scores.get)
        col_bar, col_result = st.columns([2, 1])
        with col_bar:
            fig = go.Figure(go.Bar(
                x=list(scores.keys()),
                y=list(scores.values()),
                marker_color=["#00CC96" if c == best_class else "#636EFA" for c in scores],
                text=[str(v) for v in scores.values()],
                textposition="outside",
            ))
            fig.update_layout(
                title="P(Ci|X) cho từng lớp",
                yaxis_title="Xác suất (chưa chuẩn hóa)", height=350,
            )
            st.plotly_chart(fig, use_container_width=True)
        with col_result:
            st.metric("Lớp được chọn (max)", best_class, f"Score = {scores[best_class]}")
            if not any(scores.values()):
                warning_box("Tất cả xác suất = 0 → Cần dùng làm trơn Laplace!")
            else:
                all_scores_str = " | ".join(f"{c}:{v}" for c, v in scores.items())
                info_box(f"Tất cả điểm: {all_scores_str}")
