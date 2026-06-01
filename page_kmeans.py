import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datasets import KMEANS_DATASETS
from style import step, input_header, info_box, success_box, warning_box, result_box

COLORS = ["#1A56DB", "#EF553B", "#059669", "#AB63FA", "#FFA15A", "#19D3F3"]


def kmeans_run(data, k, initial_assignment):
    data = np.array(data, dtype=float)
    assignments = np.array(initial_assignment, dtype=int)
    history = []

    for _ in range(50):
        centroids = []
        for c in range(k):
            pts = data[assignments == c]
            centroids.append(pts.mean(axis=0) if len(pts) > 0 else data[np.random.randint(len(data))])
        centroids = np.array(centroids)

        new_assign = np.array([
            int(np.argmin([np.linalg.norm(p - cent) for cent in centroids]))
            for p in data
        ])

        history.append({
            "centroids": centroids.tolist(),
            "assignments": new_assign.tolist(),
            "changed": not np.array_equal(assignments, new_assign),
        })

        if np.array_equal(assignments, new_assign):
            break
        assignments = new_assign

    return history


def show():
    st.title("🎯 Gom Cụm — Thuật Toán K-Means")
    st.markdown("**Bài 6** — Gom cụm theo vector trọng tâm")
    st.markdown("---")

    ds_name = st.radio("Chọn tập dữ liệu:", list(KMEANS_DATASETS.keys()), horizontal=True)
    ds = KMEANS_DATASETS[ds_name]
    info_box(ds["description"])

    points_dict = ds["points"]
    labels = ds["labels"]
    data = [points_dict[lb] for lb in labels]
    k = ds["default_k"]
    initial = ds["initial_assignment"]

    with st.container(border=True):
        input_header("Tập điểm dữ liệu")
        df_pts = pd.DataFrame(
            [[lb] + pt for lb, pt in zip(labels, data)],
            columns=["Điểm", "x1", "x2"],
        )
        st.dataframe(df_pts, use_container_width=True, hide_index=True)
        st.markdown(f"**Tham số:** k = {k}")
        st.markdown(
            "**Khởi tạo ban đầu:** "
            + ", ".join(f"{lb}→C{a+1}" for lb, a in zip(labels, initial))
        )
        clicked = st.button("▶ Chạy K-Means từng bước", use_container_width=True, type="primary")

    if clicked:
        history = kmeans_run(data, k, initial)
        _show_iterations(data, labels, k, initial, history)


def _show_iterations(data, labels, k, initial_assignment, history):
    data_np = np.array(data)

    with st.container(border=True):
        step(1, "Khởi tạo ban đầu (U⁰)")
        _show_partition_table(data, labels, k, initial_assignment)
        fig = _scatter(data_np, labels, initial_assignment, k, centroids=None,
                       title="Phân hoạch ban đầu")
        st.plotly_chart(fig, use_container_width=True)

    for i, iter_data in enumerate(history):
        cents = iter_data["centroids"]
        assigns = iter_data["assignments"]
        changed = iter_data["changed"]

        with st.container(border=True):
            step(i + 2, f"Iteration {i+1}" + (" — Hội tụ ✅" if not changed else ""))
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Vector trọng tâm mới:**")
                for c in range(k):
                    cx, cy = cents[c]
                    members = [labels[j] for j in range(len(data)) if assigns[j] == c]
                    st.markdown(f"- C{c+1}: `({cx:.4f}, {cy:.4f})` — gồm: `{{{', '.join(members)}}}`")

                st.markdown("**Khoảng cách Euclidean từng điểm đến các trọng tâm:**")
                rows_d = []
                for j, (lb, pt) in enumerate(zip(labels, data)):
                    row = {"Điểm": lb}
                    for c in range(k):
                        d = round(np.linalg.norm(np.array(pt) - np.array(cents[c])), 4)
                        row[f"d(,C{c+1})"] = d
                    row["→ Cụm"] = f"C{assigns[j]+1}"
                    rows_d.append(row)
                st.dataframe(pd.DataFrame(rows_d), use_container_width=True, hide_index=True)

            with col2:
                fig = _scatter(data_np, labels, assigns, k, cents, title=f"Iteration {i+1}")
                st.plotly_chart(fig, use_container_width=True)

            if not changed:
                success_box("Không có phép gán lại nào → Thuật toán <strong>hội tụ</strong>!")
                break

    final = history[-1]
    with st.container(border=True):
        step(len(history) + 2, "Kết quả cuối cùng")
        for c in range(k):
            members = [labels[j] for j in range(len(data)) if final["assignments"][j] == c]
            cx, cy = final["centroids"][c]
            result_box(f"Cụm C{c+1}: {{{', '.join(members)}}} — Trọng tâm: ({cx:.4f}, {cy:.4f})")


def _show_partition_table(data, labels, k, assignment):
    matrix = {f"C{c+1}": [] for c in range(k)}
    for lb, a in zip(labels, assignment):
        matrix[f"C{a+1}"].append(lb)
    max_len = max(len(v) for v in matrix.values())
    for key in matrix:
        matrix[key] += [""] * (max_len - len(matrix[key]))
    st.dataframe(pd.DataFrame(matrix), use_container_width=True, hide_index=True)


def _scatter(data, labels, assignments, k, centroids=None, title=""):
    fig = go.Figure()
    for c in range(k):
        idxs = [i for i, a in enumerate(assignments) if a == c]
        if idxs:
            fig.add_trace(go.Scatter(
                x=[data[i][0] for i in idxs],
                y=[data[i][1] for i in idxs],
                mode="markers+text",
                name=f"C{c+1}",
                text=[labels[i] for i in idxs],
                textposition="top center",
                marker=dict(size=14, color=COLORS[c % len(COLORS)], opacity=0.9),
            ))
    if centroids:
        for c, cent in enumerate(centroids):
            fig.add_trace(go.Scatter(
                x=[cent[0]], y=[cent[1]],
                mode="markers+text",
                name=f"Centroid C{c+1}",
                text=[f"v{c+1}"],
                textposition="bottom center",
                marker=dict(size=18, color=COLORS[c % len(COLORS)], symbol="x",
                            line=dict(color="white", width=2)),
            ))
    fig.update_layout(title=title, height=380, xaxis_title="x1", yaxis_title="x2")
    return fig
