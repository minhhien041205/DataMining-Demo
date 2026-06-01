import streamlit as st
import pandas as pd
from itertools import combinations
from datasets import ROUGH_DATASETS
from style import step, substep, result_header, input_header, info_box, success_box, warning_box, result_box


def compute_IND(df, attributes):
    groups = {}
    for obj in df.index:
        key = tuple(df.loc[obj, a] for a in attributes)
        groups.setdefault(key, set()).add(obj)
    return groups


def lower_approx(partition, target_set):
    lower = set()
    for cls in partition.values():
        if cls.issubset(target_set):
            lower.update(cls)
    return lower


def upper_approx(partition, target_set):
    upper = set()
    for cls in partition.values():
        if cls & target_set:
            upper.update(cls)
    return upper


def discernibility_matrix(df, cond_attrs, dec_attr):
    objs = list(df.index)
    matrix = {}
    for i in range(len(objs)):
        for j in range(i + 1, len(objs)):
            oi, oj = objs[i], objs[j]
            if df.loc[oi, dec_attr] != df.loc[oj, dec_attr]:
                diff_attrs = frozenset(
                    a for a in cond_attrs if df.loc[oi, a] != df.loc[oj, a]
                )
                if diff_attrs:
                    matrix[(oi, oj)] = diff_attrs
    return matrix


def find_reducts(matrix, all_attrs):
    sets = list(matrix.values())
    if not sets:
        return [frozenset()]

    found = []
    visited = set()
    all_attrs_set = frozenset(all_attrs)

    for size in range(1, len(all_attrs) + 1):
        for candidate in combinations(all_attrs, size):
            cand = frozenset(candidate)
            if cand in visited:
                continue
            if any(r.issubset(cand) for r in found):
                continue
            if all(cand & s for s in sets):
                found.append(cand)
        if found:
            break

    return found if found else [all_attrs_set]


def show():
    st.title("🔍 Tập Thô — Rough Sets")
    st.markdown("**Bài 3** — Xấp xỉ tập hợp, vùng biên và tìm Reduct")
    st.markdown("---")

    ds_name = st.radio("Chọn tập dữ liệu:", list(ROUGH_DATASETS.keys()))
    ds = ROUGH_DATASETS[ds_name]
    info_box(ds["description"])

    df = ds["df"].copy()
    cond_attrs = ds["condition_attrs"]
    dec_attr = ds["decision_attr"]
    target_class = ds["target_class"]
    target_set = set(df[df[dec_attr] == target_class].index)

    with st.container(border=True):
        input_header("Hệ quyết định (Decision System)")
        df_display = df.copy()
        df_display.index.name = "Đối tượng"
        st.dataframe(df_display, use_container_width=True)
        st.markdown(
            f"**Tập mục tiêu X** (lớp `{target_class}`): "
            f"`{{{', '.join(sorted(target_set))}}}`"
        )

    with st.container(border=True):
        step(1, "Chọn tập thuộc tính B để phân tích")
        selected_attrs = st.multiselect("Tập thuộc tính B:", cond_attrs, default=cond_attrs)
        if not selected_attrs:
            warning_box("Vui lòng chọn ít nhất một thuộc tính.")
            return
        clicked_approx = st.button("▶ Tính xấp xỉ", use_container_width=True, type="primary")

    if clicked_approx:
        _show_approximation(df, selected_attrs, dec_attr, target_set, target_class)

    with st.container(border=True):
        step(2, "Tìm Reduct")
        clicked_reduct = st.button("▶ Tính Reduct (tất cả thuộc tính)", use_container_width=True)

    if clicked_reduct:
        _show_reduct(df, cond_attrs, dec_attr, target_set)


def _show_approximation(df, attrs, dec_attr, target_set, target_class):
    partition = compute_IND(df, attrs)
    lower = lower_approx(partition, target_set)
    upper = upper_approx(partition, target_set)
    boundary = upper - lower
    outside = set(df.index) - upper

    with st.container(border=True):
        result_header(f"Kết quả xấp xỉ với B = {{{', '.join(attrs)}}}")

        substep(1, f"Quan hệ bất khả phân biệt IND({{{', '.join(attrs)}}})")
        rows_ind = []
        for key, cls in sorted(partition.items(), key=lambda x: sorted(x[1])):
            vals = " & ".join(f"{a}={v}" for a, v in zip(attrs, key))
            rows_ind.append({
                "Lớp tương đương": "{" + ", ".join(sorted(cls)) + "}",
                "Giá trị thuộc tính": vals,
            })
        st.dataframe(pd.DataFrame(rows_ind), use_container_width=True, hide_index=True)

        substep(2, f"Xấp xỉ tập X = {{{', '.join(sorted(target_set))}}}")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Xấp xỉ dưới B_(X):** các đối tượng *chắc chắn* thuộc X")
            st.markdown("`[x]_B ⊆ X`")
            if lower:
                success_box("{" + ", ".join(sorted(lower)) + "}")
            else:
                warning_box("∅ (rỗng)")
            for key, cls in partition.items():
                if cls.issubset(target_set):
                    st.markdown(f"  - `{{{', '.join(sorted(cls))}}}` ⊆ X ✅")
        with col2:
            st.markdown("**Xấp xỉ trên B^(X):** các đối tượng *có thể* thuộc X")
            st.markdown("`[x]_B ∩ X ≠ ∅`")
            result_box("{" + ", ".join(sorted(upper)) + "}")
            for key, cls in partition.items():
                if cls & target_set:
                    st.markdown(f"  - `{{{', '.join(sorted(cls))}}}` ∩ X ≠ ∅ ✅")

        substep(3, "Vùng biên và độ chính xác")
        col3, col4, col5 = st.columns(3)
        with col3:
            st.metric(
                "Vùng biên BN(X) = B^(X) − B_(X)",
                "{" + ", ".join(sorted(boundary)) + "}" if boundary else "∅",
            )
        with col4:
            st.metric(
                "Vùng ngoài U − B^(X)",
                "{" + ", ".join(sorted(outside)) + "}" if outside else "∅",
            )
        with col5:
            alpha = round(len(lower) / len(upper), 4) if upper else 1.0
            st.metric(
                "Độ chính xác α(X) = |B_(X)| / |B^(X)|",
                f"|{len(lower)}| / |{len(upper)}| = {alpha}",
            )
        if alpha == 1.0:
            success_box("Tập X là <strong>rõ</strong> (crisp) — vùng biên rỗng")
        else:
            warning_box("Tập X là <strong>thô</strong> (rough) — vùng biên khác rỗng")


def _show_reduct(df, cond_attrs, dec_attr, target_set):
    matrix = discernibility_matrix(df, cond_attrs, dec_attr)

    with st.container(border=True):
        result_header("Kết quả tìm Reduct")

        substep(1, "Ma trận phân biệt (Discernibility Matrix)")
        st.markdown(
            "c_ij = tập thuộc tính phân biệt x_i và x_j (chỉ với cặp có quyết định khác nhau)"
        )
        rows_m = []
        for (oi, oj), diff in sorted(matrix.items()):
            rows_m.append({
                "Cặp đối tượng": f"({oi}, {oj})",
                "Thuộc tính phân biệt": "{" + ", ".join(sorted(diff)) + "}",
            })
        if rows_m:
            st.dataframe(pd.DataFrame(rows_m), use_container_width=True, hide_index=True)
        else:
            info_box("Ma trận phân biệt rỗng — mọi cặp có cùng quyết định.")
            return

        reducts = find_reducts(matrix, cond_attrs)

        substep(2, "Reduct tối tiểu")
        info_box("Reduct là tập thuộc tính <strong>nhỏ nhất</strong> vẫn đảm bảo phân biệt đầy đủ.")
        for r in reducts:
            success_box("Reduct: {" + ", ".join(sorted(r)) + "}")
        for r in reducts:
            r_list = sorted(r)
            part = compute_IND(df, r_list)
            lower = lower_approx(part, target_set)
            upper = upper_approx(part, target_set)
            alpha = round(len(lower) / len(upper), 4) if upper else 1.0
            st.markdown(
                f"  → Với `B = {{{', '.join(r_list)}}}`: độ chính xác α = **{alpha}**"
            )
