import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datasets import KOHONEN_DATASETS
from style import step, input_header, info_box, success_box, result_box

COLORS = px.colors.qualitative.Plotly


def kohonen_train(data, map_rows, map_cols, alpha=0.2, epochs=200, seed=42):
    rng = np.random.default_rng(seed)
    n_features = data.shape[1]

    weights = np.full((map_rows, map_cols, n_features), 0.5)
    weights += (rng.random((map_rows, map_cols, n_features)) - 0.5) * 0.2

    hood_size = max(map_rows, map_cols) // 2
    hood_drop = max(epochs // max(hood_size, 1), 1)
    alpha_decr = alpha / epochs
    snapshot_weights = [weights.copy()]

    for epoch in range(epochs):
        idx = rng.permutation(len(data))
        for t in idx:
            sample = data[t]
            dists = np.linalg.norm(weights - sample, axis=2)
            win_i, win_j = np.unravel_index(dists.argmin(), dists.shape)

            lo_i = max(0, win_i - hood_size)
            hi_i = min(map_rows, win_i + hood_size + 1)
            lo_j = max(0, win_j - hood_size)
            hi_j = min(map_cols, win_j + hood_size + 1)
            for i in range(lo_i, hi_i):
                for j in range(lo_j, hi_j):
                    weights[i][j] += alpha * (sample - weights[i][j])

        if alpha > 0.01:
            alpha -= alpha_decr
        if (epoch + 1) % hood_drop == 0 and hood_size > 1:
            hood_size -= 1

        if epoch in [0, epochs // 4, epochs // 2, epochs - 1]:
            snapshot_weights.append(weights.copy())

    return weights, snapshot_weights


def assign_to_neurons(data, weights, labels):
    assignments = {}
    for pt, lb in zip(data, labels):
        dists = np.linalg.norm(weights - pt, axis=2)
        win_i, win_j = np.unravel_index(dists.argmin(), dists.shape)
        assignments.setdefault((win_i, win_j), []).append(lb)
    return assignments


def show():
    st.title("🧠 Gom Cụm — Mạng Kohonen (SOM)")
    st.markdown("**Bài 8** — Self-Organizing Map: học không giám sát")
    st.markdown("---")

    ds_name = st.radio("Chọn tập dữ liệu:", list(KOHONEN_DATASETS.keys()), horizontal=True)
    ds = KOHONEN_DATASETS[ds_name]
    info_box(ds["description"])

    points_dict = ds["points"]
    labels = ds["labels"]
    data_raw = np.array([points_dict[lb] for lb in labels], dtype=float)
    default_map = ds["default_map"]

    with st.container(border=True):
        input_header("Tập điểm dữ liệu đầu vào")
        df_pts = pd.DataFrame(
            [[lb] + list(points_dict[lb]) for lb in labels],
            columns=["Điểm", "Feature 1", "Feature 2"],
        )
        st.dataframe(df_pts, use_container_width=True, hide_index=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            map_rows = st.number_input("Số dòng (map rows):", 2, 10, default_map[0])
        with col2:
            map_cols = st.number_input("Số cột (map cols):", 2, 10, default_map[1])
        with col3:
            alpha = st.number_input("Learning rate (α):", 0.01, 1.0, 0.2, 0.01)
        with col4:
            epochs = st.number_input("Số epochs:", 10, 1000, 200, 10)
        clicked = st.button("▶ Chạy Kohonen SOM", use_container_width=True, type="primary")

    if clicked:
        _show_kohonen(data_raw, labels, int(map_rows), int(map_cols), alpha, int(epochs))


def _show_kohonen(data, labels, map_rows, map_cols, alpha, epochs):
    with st.spinner("Đang huấn luyện mạng Kohonen..."):
        weights, snapshots = kohonen_train(data, map_rows, map_cols, alpha, epochs)

    with st.container(border=True):
        step(1, "Khởi tạo trọng số")
        st.markdown(
            f"Tạo mảng Map **{map_rows}×{map_cols}** = **{map_rows*map_cols} nơron**.\n\n"
            f"Mỗi nơron có vector trọng số kích thước = số features = **{data.shape[1]}**\n\n"
            f"Khởi tạo: `w[i][j][k] = 0.5 ± giá trị nhỏ ngẫu nhiên` (theo bài giảng)"
        )
        _show_weight_map(snapshots[0], map_rows, map_cols, "Trọng số ban đầu (trước khi học)")

    with st.container(border=True):
        step(2, "Quá trình học")
        st.markdown("""
**Mỗi vòng lặp:**
1. Đưa mẫu học `v(t)` vào mạng
2. Tính khoảng cách Euclidean đến tất cả nơron → chọn **nơron chiến thắng** (min distance)
3. Cập nhật trọng số: `w(t+1) = w(t) + α × [x(t) - w(t)]`
4. Giảm dần α và vùng lân cận theo thời gian
        """)
        if len(snapshots) > 1:
            mid = len(snapshots) // 2
            _show_weight_map(snapshots[mid], map_rows, map_cols, "Trọng số giữa quá trình học")

    with st.container(border=True):
        step(3, "Trọng số sau khi học")
        _show_weight_map(weights, map_rows, map_cols, "Trọng số cuối cùng")

    with st.container(border=True):
        step(4, "Gán điểm dữ liệu vào nơron chiến thắng")
        assignments = assign_to_neurons(data, weights, labels)
        _show_cluster_result(data, labels, assignments, weights, map_rows, map_cols)


def _show_weight_map(weights, map_rows, map_cols, title):
    w_mean = weights.mean(axis=2)
    fig = go.Figure(go.Heatmap(
        z=w_mean,
        colorscale=[[0, "#EBF3FF"], [0.4, "#93C5FD"], [0.7, "#1A56DB"], [1, "#1E3A5F"]],
        text=[[f"({weights[i][j][0]:.3f},\n{weights[i][j][1]:.3f})"
               for j in range(map_cols)] for i in range(map_rows)],
        texttemplate="%{text}",
        textfont={"size": 9},
        showscale=True,
    ))
    fig.update_layout(title=title, height=320, xaxis_title="Cột", yaxis_title="Dòng")
    st.plotly_chart(fig, use_container_width=True)


def _show_cluster_result(data, labels, assignments, weights, map_rows, map_cols):
    neuron_color_idx = {}
    color_counter = 0
    for key in sorted(assignments.keys()):
        if key not in neuron_color_idx:
            neuron_color_idx[key] = color_counter
            color_counter += 1

    point_neuron = {lb: key for key, pts in assignments.items() for lb in pts}

    rows = []
    for lb in labels:
        key = point_neuron.get(lb, ("?", "?"))
        win_row, win_col = key
        members_in_neuron = assignments.get(key, [])
        rows.append({
            "Điểm": lb,
            "Feature 1": data[labels.index(lb)][0],
            "Feature 2": data[labels.index(lb)][1],
            "Nơron chiến thắng": f"({win_row},{win_col})",
            "Cùng nơron với": ", ".join(m for m in members_in_neuron if m != lb) or "—",
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    fig = go.Figure()
    for key, pts in assignments.items():
        color = COLORS[neuron_color_idx[key] % len(COLORS)]
        xs = [data[labels.index(lb)][0] for lb in pts]
        ys = [data[labels.index(lb)][1] for lb in pts]
        win_row, win_col = key
        fig.add_trace(go.Scatter(
            x=xs, y=ys,
            mode="markers+text",
            name=f"Nơron ({win_row},{win_col})",
            text=pts, textposition="top center",
            marker=dict(size=14, color=color, opacity=0.85),
        ))
        fig.add_trace(go.Scatter(
            x=[weights[win_row][win_col][0]],
            y=[weights[win_row][win_col][1]],
            mode="markers",
            name=f"Nơron ({win_row},{win_col}) — trọng số",
            marker=dict(size=18, color=color, symbol="x",
                        line=dict(color="white", width=2)),
            showlegend=False,
        ))
    fig.update_layout(
        title="Phân cụm kết quả (màu = nơron chiến thắng)",
        height=420, xaxis_title="Feature 1", yaxis_title="Feature 2",
    )
    st.plotly_chart(fig, use_container_width=True)

    total_neurons_used = len(assignments)
    result_box(
        f"Kết quả: {len(labels)} điểm được phân vào "
        f"<strong>{total_neurons_used} nơron</strong> trên Map {map_rows}×{map_cols}."
    )
