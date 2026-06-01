import streamlit as st
import pandas as pd
from itertools import combinations
from datasets import APRIORI_DATASETS
from style import step, input_header, info_box, success_box, warning_box, result_box


def get_transactions(ds):
    return [list(t.values())[0] for t in ds["transactions"]]


def support(transactions, itemset):
    count = sum(1 for t in transactions if itemset.issubset(t))
    return count / len(transactions)


def apriori(transactions, items, min_sup):
    steps = []
    C1 = {frozenset([item]): support(transactions, frozenset([item])) for item in items}
    L1 = {k: v for k, v in C1.items() if v >= min_sup}
    steps.append({"k": 1, "C": C1, "L": L1})

    k = 2
    prev_L = list(L1.keys())
    while prev_L:
        Ck = {}
        for i in range(len(prev_L)):
            for j in range(i + 1, len(prev_L)):
                candidate = prev_L[i] | prev_L[j]
                if len(candidate) == k:
                    if all(frozenset(s) in prev_L for s in combinations(candidate, k - 1)):
                        Ck[candidate] = support(transactions, candidate)

        Lk = {ks: v for ks, v in Ck.items() if v >= min_sup}
        steps.append({"k": k, "C": Ck, "L": Lk})
        prev_L = list(Lk.keys())
        k += 1

    return steps


def gen_rules(freq_itemsets, transactions, min_conf):
    rules = []
    for itemset in freq_itemsets:
        if len(itemset) < 2:
            continue
        for size in range(1, len(itemset)):
            for antecedent in combinations(itemset, size):
                ant = frozenset(antecedent)
                con = itemset - ant
                sup_all = support(transactions, itemset)
                sup_ant = support(transactions, ant)
                conf = sup_all / sup_ant if sup_ant > 0 else 0
                if conf >= min_conf:
                    rules.append({
                        "Vế trái (X)": ", ".join(sorted(ant)),
                        "Vế phải (Y)": ", ".join(sorted(con)),
                        "Support(X∪Y)": round(sup_all, 3),
                        "Support(X)": round(sup_ant, 3),
                        "Confidence": round(conf, 3),
                    })
    return rules


def show():
    st.title("🛒 Luật Kết Hợp — Thuật Toán Apriori")
    st.markdown("**Bài 2** — Tập phổ biến và luật kết hợp")
    st.markdown("---")

    ds_name = st.radio("Chọn tập dữ liệu:", list(APRIORI_DATASETS.keys()), horizontal=True)
    ds = APRIORI_DATASETS[ds_name]
    info_box(ds["description"])

    transactions = get_transactions(ds)
    items = sorted(ds["items"])
    tid_labels = [f"T{i+1}" for i in range(len(transactions))]

    with st.container(border=True):
        input_header("Bảng giao dịch")
        matrix = {item: ["✓" if item in t else "" for t in transactions] for item in items}
        df_matrix = pd.DataFrame(matrix, index=tid_labels)
        st.dataframe(df_matrix, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            min_sup = st.slider(
                "min_support:", 0.1, 1.0, ds["default_minsup"], 0.05,
                help="Ngưỡng hỗ trợ tối thiểu (tỉ lệ số hóa đơn)",
            )
        with col2:
            min_conf = st.slider(
                "min_confidence:", 0.1, 1.0, ds["default_minconf"], 0.05,
                help="Ngưỡng độ tin cậy tối thiểu",
            )
        clicked = st.button("▶ Chạy Apriori", use_container_width=True, type="primary")

    if clicked:
        ap_steps = apriori(transactions, items, min_sup)
        _show_steps(ap_steps, transactions, min_sup, min_conf, items, tid_labels)


def _show_steps(ap_steps, transactions, min_sup, min_conf, items, tid_labels):
    all_frequent = []

    with st.container(border=True):
        step(1, "Tìm tập phổ biến")
        for s in ap_steps:
            k = s["k"]
            C = s["C"]
            L = s["L"]

            if not C:
                break

            with st.expander(
                f"Bước k={k}: Tập ứng cử viên C{k} → Tập phổ biến L{k}", expanded=True
            ):
                col_c, col_l = st.columns(2)
                with col_c:
                    st.markdown(f"**C{k} — tất cả ứng cử viên ({len(C)} tập):**")
                    rows_c = []
                    for iset, sup in sorted(C.items(), key=lambda x: sorted(x[0])):
                        freq = int(sup * len(transactions))
                        is_freq = "✅ Phổ biến" if sup >= min_sup else "❌ Loại"
                        rows_c.append({
                            "Tập mặt hàng": "{" + ", ".join(sorted(iset)) + "}",
                            "Support": f"{freq}/{len(transactions)} = {sup:.2f}",
                            "Trạng thái": is_freq,
                        })
                    st.dataframe(pd.DataFrame(rows_c), use_container_width=True, hide_index=True)

                with col_l:
                    st.markdown(f"**L{k} — tập phổ biến (sup ≥ {min_sup}):**")
                    if L:
                        rows_l = []
                        for iset, sup in sorted(L.items(), key=lambda x: sorted(x[0])):
                            rows_l.append({
                                "Tập phổ biến": "{" + ", ".join(sorted(iset)) + "}",
                                "Support": round(sup, 3),
                            })
                        st.dataframe(pd.DataFrame(rows_l), use_container_width=True, hide_index=True)
                        all_frequent.extend(list(L.keys()))
                    else:
                        warning_box("Không có tập phổ biến nào ở bước này → Dừng thuật toán.")

            if not L:
                break

    if all_frequent:
        with st.container(border=True):
            step(2, "Tập phổ biến tối đại")
            maximal = [s for s in all_frequent if not any(s < s2 for s2 in all_frequent)]
            for s in sorted(maximal, key=lambda x: (-len(x), sorted(x))):
                result_box("{" + ", ".join(sorted(s)) + "}")

    with st.container(border=True):
        step(3, "Sinh luật kết hợp")
        info_box(
            f"Công thức: CF(X→Y) = SP(X∪Y) / SP(X), chỉ giữ luật có CF ≥ {min_conf}"
        )
        rules = gen_rules(all_frequent, transactions, min_conf)
        if rules:
            df_rules = pd.DataFrame(rules).sort_values("Confidence", ascending=False)
            st.dataframe(df_rules, use_container_width=True, hide_index=True)
            success_box(f"Tìm được <strong>{len(rules)} luật hợp lệ</strong> với min_conf = {min_conf}")
        else:
            warning_box("Không có luật nào thỏa min_confidence.")
