import streamlit as st
import pandas as pd
import math
import plotly.graph_objects as go
from collections import Counter
from datasets import DTREE_DATASETS
from style import step, input_header, info_box, success_box, warning_box, result_box


def entropy(labels):
    n = len(labels)
    if n == 0:
        return 0.0
    counts = Counter(labels)
    return -sum((c / n) * math.log2(c / n) for c in counts.values() if c > 0)


def information_gain(df, attribute, target):
    n = len(df)
    E_before = entropy(df[target].tolist())
    weighted = sum(
        (len(df[df[attribute] == val]) / n) * entropy(df[df[attribute] == val][target].tolist())
        for val in df[attribute].unique()
    )
    return round(E_before - weighted, 6)


def id3(df, features, target, depth=0, max_depth=10):
    labels = df[target].tolist()
    if len(set(labels)) == 1:
        return {"type": "leaf", "class": labels[0], "count": len(labels)}
    if not features or depth >= max_depth:
        majority = Counter(labels).most_common(1)[0][0]
        return {"type": "leaf", "class": majority, "count": len(labels)}

    gains = {f: information_gain(df, f, target) for f in features}
    best = max(gains, key=gains.get)

    node = {
        "type": "node",
        "attribute": best,
        "gain": gains[best],
        "entropy": round(entropy(labels), 6),
        "count": len(labels),
        "gains_all": {k: round(v, 6) for k, v in gains.items()},
        "children": {},
    }

    remaining = [f for f in features if f != best]
    for val in df[best].unique():
        subset = df[df[best] == val]
        if len(subset) == 0:
            majority = Counter(labels).most_common(1)[0][0]
            node["children"][val] = {"type": "leaf", "class": majority, "count": 0}
        else:
            node["children"][val] = id3(subset, remaining, target, depth + 1, max_depth)

    return node


def classify(node, sample):
    if node["type"] == "leaf":
        return node["class"]
    attr = node["attribute"]
    val = sample.get(attr)
    if val in node["children"]:
        return classify(node["children"][val], sample)
    return list(node["children"].values())[0]["class"] if node["children"] else "?"


def _collect_nodes(node, x=0.0, y=0.0, parent_xy=None, label="", nodes=None, edges=None,
                   x_counter=None):
    if nodes is None:
        nodes, edges, x_counter = [], [], [0]

    node_id = len(nodes)

    if node["type"] == "leaf":
        text = f"✅ {node['class']}\n({node['count']} mẫu)"
        color = "#059669"
    else:
        text = f"[{node['attribute']}]\nIG={node['gain']:.3f}\n({node['count']} mẫu)"
        color = "#1A56DB"

    nodes.append({"id": node_id, "x": x, "y": y, "text": text, "color": color})

    if parent_xy:
        edges.append({"x0": parent_xy[0], "y0": parent_xy[1], "x1": x, "y1": y, "label": label})

    if node["type"] == "node":
        children = list(node["children"].items())
        n_children = len(children)
        spacing = 2.0 ** (max(3 - abs(y), 1))
        start_x = x - spacing * (n_children - 1) / 2
        for i, (val, child) in enumerate(children):
            _collect_nodes(child, start_x + i * spacing, y - 1.5, (x, y), str(val),
                           nodes, edges, x_counter)

    return nodes, edges


def _draw_tree(tree):
    nodes, edges = _collect_nodes(tree)[:2]
    fig = go.Figure()

    for e in edges:
        fig.add_trace(go.Scatter(
            x=[e["x0"], e["x1"]], y=[e["y0"], e["y1"]],
            mode="lines", line=dict(color="#888", width=1.5),
            showlegend=False, hoverinfo="none",
        ))
        mid_x = (e["x0"] + e["x1"]) / 2
        mid_y = (e["y0"] + e["y1"]) / 2
        fig.add_annotation(
            x=mid_x, y=mid_y, text=f"<b>{e['label']}</b>",
            showarrow=False, font=dict(color="#1E3A5F", size=12),
            bgcolor="rgba(235,243,255,0.85)",
        )

    for n in nodes:
        fig.add_trace(go.Scatter(
            x=[n["x"]], y=[n["y"]],
            mode="markers+text",
            marker=dict(size=50, color=n["color"], opacity=0.85,
                        line=dict(color="white", width=1)),
            text=[n["text"].replace("\n", "<br>")],
            textposition="middle center",
            textfont=dict(size=9, color="white"),
            showlegend=False,
            hovertext=n["text"], hoverinfo="text",
        ))

    fig.update_layout(
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=520, margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor="#F0F4F8", plot_bgcolor="#F0F4F8",
    )
    return fig


def _extract_rules(node, path, rules):
    if node["type"] == "leaf":
        rule = (" & ".join(path) + f" → **{node['class']}**") if path else f"→ **{node['class']}**"
        rules.append(rule)
    else:
        for val, child in node["children"].items():
            _extract_rules(child, path + [f"{node['attribute']}={val}"], rules)


def _trace_path(node, sample, path=None):
    if path is None:
        path = []
    if node["type"] == "leaf":
        path.append(f"Lá → **{node['class']}**")
        return path
    attr = node["attribute"]
    val = sample.get(attr)
    path.append(f"Kiểm tra `{attr}` = `{val}`")
    if val in node["children"]:
        return _trace_path(node["children"][val], sample, path)
    return path


def show():
    st.title("🌳 Cây Quyết Định — Thuật Toán ID3")
    st.markdown("**Bài 5** — Phân lớp bằng cây quyết định (Entropy & Information Gain)")
    st.markdown("---")

    ds_name = st.radio("Chọn tập dữ liệu:", list(DTREE_DATASETS.keys()), horizontal=True)
    ds = DTREE_DATASETS[ds_name]
    info_box(ds["description"])

    df = ds["df"].copy()
    features = ds["features"]
    target = ds["target"]
    display_df = df[features + [target]]

    E_total = round(entropy(df[target].tolist()), 6)
    counts = Counter(df[target].tolist())
    counts_str = ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))

    # Xoá tree nếu đổi dataset
    if st.session_state.get("dt_ds_name") != ds_name:
        st.session_state.pop("dt_tree", None)

    with st.container(border=True):
        input_header("Tập dữ liệu huấn luyện")
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        st.markdown(f"**Entropy tổng thể E(S):** `{E_total}` bit — phân bố: `{counts_str}`")
        clicked = st.button("▶ Xây dựng cây ID3", use_container_width=True, type="primary")

    if clicked:
        tree = id3(display_df, features, target)
        st.session_state["dt_tree"] = tree
        st.session_state["dt_ds_name"] = ds_name

    if "dt_tree" in st.session_state:
        tree = st.session_state["dt_tree"]
        _show_ig_table(display_df, features, target)
        _show_tree(tree)


def _show_ig_table(df, features, target):
    with st.container(border=True):
        step(1, "Tính Information Gain cho tất cả thuộc tính")
        E_total = entropy(df[target].tolist())
        rows = []
        max_ig = max(information_gain(df, ft, target) for ft in features)
        for f in features:
            ig = information_gain(df, f, target)
            detail_parts = []
            for val in sorted(df[f].unique()):
                subset = df[df[f] == val]
                e_sub = round(entropy(subset[target].tolist()), 4)
                detail_parts.append(f"{val}: {len(subset)}/{len(df)}×E={e_sub}")
            rows.append({
                "Thuộc tính": f,
                "Entropy E(S)": round(E_total, 4),
                "Phân hoạch": " | ".join(detail_parts),
                "IG(S, A)": ig,
                "Chọn làm gốc?": "✅ TỐT NHẤT" if ig == max_ig else "",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        best = max(features, key=lambda f: information_gain(df, f, target))
        success_box(f"→ Chọn <strong>{best}</strong> làm nút gốc (IG cao nhất)")


def _show_tree(tree):
    with st.container(border=True):
        step(2, "Cây quyết định hoàn chỉnh")
        fig = _draw_tree(tree)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Các luật phân lớp (đọc từ cây):**")
        rules = []
        _extract_rules(tree, [], rules)
        for r in rules:
            st.markdown(f"- {r}")


def _show_classify(tree, df, features, target):
    with st.container(border=True):
        step(3, "Phân lớp mẫu mới")
        sample = {}
        cols = st.columns(len(features))
        for i, f in enumerate(features):
            vals = sorted(df[f].unique().tolist())
            with cols[i]:
                sample[f] = st.selectbox(f, vals, key=f"dt_{f}")

        if st.button("Phân lớp", key="dt_classify"):
            result = classify(tree, sample)
            path_steps = _trace_path(tree, sample)
            st.markdown("**Đường đi trên cây:**")
            for path_item in path_steps:
                st.markdown(f"  → {path_item}")
            success_box(f"Kết quả phân lớp: <strong>{target} = {result}</strong>")
