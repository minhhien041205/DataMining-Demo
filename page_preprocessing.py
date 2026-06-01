import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datasets import PREPROCESS_DATASETS
from style import step, input_header, info_box, success_box, warning_box, result_box


def _fill_missing(df, numeric_cols, method):
    df2 = df.copy()
    for col in numeric_cols:
        if df2[col].isna().any():
            if method == "Mean (trung bình)":
                val = round(df2[col].mean(), 2)
            elif method == "Median (trung vị)":
                val = df2[col].median()
            else:
                val = df2[col].mode()[0]
            df2[col] = df2[col].fillna(val)
            st.markdown(f"- Cột **{col}**: điền bằng **{method}** = `{val}`")
    return df2


def _normalize_minmax(series, new_min=0.0, new_max=1.0):
    mn, mx = series.min(), series.max()
    if mx == mn:
        return series * 0
    return (series - mn) / (mx - mn) * (new_max - new_min) + new_min


def _normalize_zscore(series):
    return (series - series.mean()) / series.std()


def _equal_width_bins(values, k):
    mn, mx = min(values), max(values)
    width = (mx - mn) / k
    boundaries = [mn + i * width for i in range(k + 1)]
    bins = [[] for _ in range(k)]
    for v in values:
        idx = min(int((v - mn) / width), k - 1)
        bins[idx].append(v)
    return bins, boundaries


def _equal_freq_bins(values, k):
    sorted_v = sorted(values)
    n = len(sorted_v)
    size = n // k
    bins = [sorted_v[i * size: (i + 1) * size] for i in range(k)]
    for i, v in enumerate(sorted_v[k * size:]):
        bins[i].append(v)
    return bins


def show():
    st.title("🧹 Tiền Xử Lý Dữ Liệu")
    st.markdown("**Bài 1-2** — Làm sạch, chuẩn hóa và rời rạc hóa dữ liệu")
    st.markdown("---")

    ds_name = st.radio("Chọn ví dụ:", list(PREPROCESS_DATASETS.keys()), horizontal=True)
    ds = PREPROCESS_DATASETS[ds_name]
    info_box(ds["description"])

    if ds_name == "Ví dụ Binning (Bài 1-2)":
        _show_binning(ds)
    else:
        _show_student(ds)


def _show_binning(ds):
    values = ds["values"]

    with st.container(border=True):
        step(1, "Rời Rạc Hóa (Binning)")
        st.markdown(f"**Dãy giá trị (đã sắp xếp):** `{sorted(values)}`")
        k = st.slider("Số bin (k):", 2, 5, 3)
        method = st.selectbox(
            "Phương pháp:",
            ["Equal-Width (chiều rộng bằng nhau)", "Equal-Frequency (tần số bằng nhau)"],
        )
        st.markdown("---")
        if "Equal-Width" in method:
            bins, boundaries = _equal_width_bins(sorted(values), k)
            st.markdown(f"**Chiều rộng mỗi bin:** `{round(boundaries[1]-boundaries[0], 2)}`")
            st.markdown(f"**Ranh giới:** `{[round(b,2) for b in boundaries]}`")
        else:
            bins = _equal_freq_bins(sorted(values), k)

        rows = []
        for i, b in enumerate(bins):
            rows.append({
                "Bin": f"Bin {i+1}",
                "Các giá trị": str(b),
                "Min (boundary)": min(b),
                "Max (boundary)": max(b),
                "Mean → bin means": round(np.mean(b), 2),
                "Median → bin median": np.median(b),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

        colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"]
        fig = go.Figure()
        for i, b in enumerate(bins):
            fig.add_trace(go.Scatter(
                x=list(range(len(b))), y=b,
                mode="markers+lines",
                name=f"Bin {i+1}",
                marker=dict(size=10, color=colors[i % len(colors)]),
            ))
        fig.update_layout(
            title="Phân bố giá trị theo bin",
            xaxis_title="Vị trí trong bin", yaxis_title="Giá trị",
        )
        st.plotly_chart(fig, use_container_width=True)


def _show_student(ds):
    df_raw = ds["df"].copy()
    numeric_cols = ds["numeric_cols"]

    with st.container(border=True):
        input_header("Dữ Liệu Gốc (có giá trị thiếu)")
        st.dataframe(df_raw.style.highlight_null(color="#FCA5A5"), use_container_width=True)
        missing = df_raw[numeric_cols].isna().sum()
        missing_counts = {col: int(count) for col, count in missing.items() if count > 0}
        missing_text = ", ".join(f"{col}: {count}" for col, count in missing_counts.items())
        result_box(f"Giá trị thiếu: {missing_text}")

    with st.container(border=True):
        step(1, "Xử Lý Giá Trị Thiếu")
        fill_method = st.selectbox(
            "Phương pháp điền giá trị thiếu:",
            ["Mean (trung bình)", "Median (trung vị)", "Mode (giá trị phổ biến nhất)"],
        )
        df_clean = _fill_missing(df_raw, numeric_cols, fill_method)
        st.dataframe(df_clean, use_container_width=True)

    with st.container(border=True):
        step(2, "Chuẩn Hóa Dữ Liệu")
        norm_col = st.selectbox("Chọn cột để chuẩn hóa:", numeric_cols)
        norm_method = st.radio(
            "Phương pháp chuẩn hóa:", ["Min-Max (0–1)", "Z-score"], horizontal=True,
        )
        series = df_clean[norm_col]
        if norm_method == "Min-Max (0–1)":
            normalized = _normalize_minmax(series)
            formula = f"x' = (x − {series.min()}) / ({series.max()} − {series.min()})"
        else:
            normalized = _normalize_zscore(series)
            formula = f"z = (x − {series.mean():.2f}) / {series.std():.2f}"

        st.markdown(f"**Công thức:** `{formula}`")
        df_norm = df_clean.copy()
        df_norm[f"{norm_col} (chuẩn hóa)"] = normalized.round(4)
        st.dataframe(
            df_norm[["MSSV", norm_col, f"{norm_col} (chuẩn hóa)"]],
            use_container_width=True,
        )

        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=[f"{norm_col} (gốc)", f"{norm_col} (sau chuẩn hóa)"],
        )
        fig.add_trace(
            go.Bar(y=df_clean[norm_col], x=df_clean["MSSV"], name="Gốc",
                   marker_color="#636EFA"), row=1, col=1,
        )
        fig.add_trace(
            go.Bar(y=normalized, x=df_clean["MSSV"], name="Chuẩn hóa",
                   marker_color="#00CC96"), row=1, col=2,
        )
        fig.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig, use_container_width=True)

    with st.container(border=True):
        step(3, "Rời Rạc Hóa (Binning)")
        bin_col = st.selectbox("Chọn cột để rời rạc hóa:", numeric_cols, key="bin_col")
        k_bin = st.slider("Số khoảng (k):", 2, 5, 3, key="k_bin")
        bin_method = st.radio(
            "Phương pháp:", ["Equal-Width", "Equal-Frequency"], horizontal=True, key="bin_method",
        )
        vals = sorted(df_clean[bin_col].tolist())
        if bin_method == "Equal-Width":
            bins, boundaries = _equal_width_bins(vals, k_bin)
            width = round(boundaries[1] - boundaries[0], 2)
            st.markdown(
                f"Chiều rộng mỗi khoảng: **{width}** | Ranh giới: `{[round(b,2) for b in boundaries]}`"
            )
        else:
            bins = _equal_freq_bins(vals, k_bin)

        rows = []
        for i, b in enumerate(bins):
            rows.append({
                "Bin": f"Bin {i+1}",
                "Giá trị": str(b),
                "Min": min(b), "Max": max(b),
                "Mean": round(np.mean(b), 2),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
