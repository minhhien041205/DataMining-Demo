"""
Tất cả tập dữ liệu được lấy từ ví dụ trong bài giảng của thầy Mai Xuân Hùng
Môn: Khai Phá Dữ Liệu (Data Mining)
"""
import pandas as pd
import numpy as np

# ============================================================
# BÀI 1-2: TIỀN XỬ LÝ DỮ LIỆU
# ============================================================

PREPROCESS_DATASETS = {
    "Dữ liệu sinh viên (có giá trị thiếu)": {
        "description": "Tập dữ liệu sinh viên dùng để demo xử lý giá trị thiếu, chuẩn hóa và rời rạc hóa.",
        "df": pd.DataFrame({
            "MSSV":          ["SV01","SV02","SV03","SV04","SV05","SV06","SV07","SV08","SV09","SV10"],
            "Điểm TB":       [7.5,  None,  8.0,  5.5,   9.0,   6.5,  7.0,   8.5,   4.0,   7.5],
            "Chiều cao (cm)":[165.0,175.0,158.0,170.0, 180.0,  None, 162.0,168.0, 177.0, 163.0],
            "Thu nhập (tr)": [8.0,  15.0, None,  12.0,   3.0,  20.0,  7.0,   9.5,  11.0,   6.0],
        }),
        "numeric_cols": ["Điểm TB", "Chiều cao (cm)", "Thu nhập (tr)"],
    },
    "Ví dụ Binning (Bài 1-2)": {
        "description": "Dãy số minh họa kỹ thuật Binning để giảm nhiễu (noisy data).",
        "values": [4, 8, 15, 21, 21, 24, 25, 28, 34],
        "df": pd.DataFrame({
            "STT":   list(range(1, 10)),
            "Giá trị": [4, 8, 15, 21, 21, 24, 25, 28, 34],
        }),
    },
}

# ============================================================
# BÀI 2: TẬP PHỔ BIẾN & LUẬT KẾT HỢP (APRIORI)
# Ví dụ: ngữ cảnh (O, I, R) với I = {i1, i2, i3, i4}
# ============================================================

APRIORI_DATASETS = {
    "Ví dụ bài học (Bài 2) — {i1,i2,i3,i4}": {
        "description": (
            "Ngữ cảnh khai thác dữ liệu với 5 hóa đơn và 4 mặt hàng {i1,i2,i3,i4}. "
            "Kết quả: tập phổ biến tối đại là {i1,i2,i3} và {i2,i3,i4} (minsupp=0.4)."
        ),
        "transactions": [
            {"T1": frozenset(["i1","i2","i3"])},
            {"T2": frozenset(["i1","i2","i3"])},
            {"T3": frozenset(["i2","i3","i4"])},
            {"T4": frozenset(["i2","i3","i4"])},
            {"T5": frozenset(["i3","i4"])},
        ],
        "items": ["i1","i2","i3","i4"],
        "default_minsup": 0.4,
        "default_minconf": 0.67,
    },
    "Ví dụ siêu thị (minh họa thực tế)": {
        "description": (
            "Hóa đơn siêu thị với các mặt hàng thực tế: Bia, Khăn, Sữa, Bánh mì, Bơ."
        ),
        "transactions": [
            {"T1": frozenset(["Bia","Khăn","Sữa"])},
            {"T2": frozenset(["Bia","Khăn","Sữa"])},
            {"T3": frozenset(["Sữa","Bánh mì","Bơ"])},
            {"T4": frozenset(["Sữa","Bánh mì","Bơ"])},
            {"T5": frozenset(["Bánh mì","Bơ"])},
        ],
        "items": ["Bia","Khăn","Sữa","Bánh mì","Bơ"],
        "default_minsup": 0.4,
        "default_minconf": 0.67,
    },
}

# ============================================================
# BÀI 3: TẬP THÔ (ROUGH SETS / REDUCT)
# ============================================================

ROUGH_DATASETS = {
    "Ví dụ Thi đậu (Bài 3 — trang 5-19)": {
        "description": (
            "Hệ quyết định 7 đối tượng: Tuổi & Số buổi học → Thi đậu. "
            "Tập mục tiêu W = {x1,x4,x6} (thi đậu = Yes)."
        ),
        "df": pd.DataFrame({
            "Đối tượng": ["x1","x2","x3","x4","x5","x6","x7"],
            "Tuổi":      ["16-30","16-30","31-45","31-45","46-60","16-30","46-60"],
            "Số buổi":   ["50","0","1-25","1-25","26-49","26-49","26-49"],
            "Thi đậu":   ["yes","no","no","yes","no","yes","no"],
        }).set_index("Đối tượng"),
        "condition_attrs": ["Tuổi","Số buổi"],
        "decision_attr": "Thi đậu",
        "target_class": "yes",
    },
    "Ví dụ Dự báo thời tiết (Bài 3 — Bài tập trang 30)": {
        "description": (
            "Hệ quyết định 8 đối tượng: Trời, Gió, Áp suất → Kết quả mua hàng. "
            "Tập mục tiêu X = {O1,O3,O4} (Kết quả = Kmua)."
        ),
        "df": pd.DataFrame({
            "Đối tượng": ["O1","O2","O3","O4","O5","O6","O7","O8"],
            "Trời":      ["Trong","Mây","Mây","Trong","Mây","Mây","Mây","Trong"],
            "Gió":       ["Bắc","Nam","Bắc","Bắc","Bắc","Bắc","Nam","Nam"],
            "Áp suất":   ["Cao","Cao","TB","Thấp","Thấp","Cao","Thấp","Cao"],
            "Kết quả":   ["Kmua","Mua","Mua","Kmua","Mua","Mua","Kmua","Kmua"],
        }).set_index("Đối tượng"),
        "condition_attrs": ["Trời","Gió","Áp suất"],
        "decision_attr": "Kết quả",
        "target_class": "Kmua",
    },
    "Ví dụ Kem chống nắng (Bài 3 — Bài tập trang 35)": {
        "description": (
            "Hệ quyết định 8 đối tượng: Màu tóc, Chiều cao, Cân nặng, Dùng thuốc → Kết quả. "
            "Reduct: B1={Màu tóc, Dùng thuốc} và B2={Màu tóc, Chiều cao, Cân nặng}."
        ),
        "df": pd.DataFrame({
            "Đối tượng":  ["O1","O2","O3","O4","O5","O6","O7","O8"],
            "Màu tóc":    ["Đen","Đen","Râm","Đen","Bạc","Râm","Râm","Đen"],
            "Chiều cao":  ["Tầm thước","Cao","Thấp","Thấp","Tầm thước","Cao","Tầm thước","Thấp"],
            "Cân nặng":   ["Nhẹ","Vừa","Vừa","Vừa","Nặng","Nặng","Nặng","Nhẹ"],
            "Dùng thuốc": ["Không","Có","Có","Không","Không","Không","Không","Có"],
            "Kết quả":    ["Bị rám","Không","Không","Bị rám","Bị rám","Không","Không","Không"],
        }).set_index("Đối tượng"),
        "condition_attrs": ["Màu tóc","Chiều cao","Cân nặng","Dùng thuốc"],
        "decision_attr": "Kết quả",
        "target_class": "Bị rám",
    },
}

# ============================================================
# BÀI 4 & 7: PHÂN LỚP NAIVE BAYES
# ============================================================

BAYES_DATASETS = {
    "Ví dụ Đi chơi (Bài 4 — 9 mẫu)": {
        "description": (
            "9 mẫu dữ liệu thời tiết. Câu hỏi: 'Hôm nay Nắng và Nóng — có nên đi chơi không?' "
            "Kết quả: P(No|Nắng,Nóng)=0.133 > P(Yes|Nắng,Nóng)=0.028 → Không đi chơi."
        ),
        "df": pd.DataFrame({
            "Thời tiết":  ["Nắng","Nắng","Ám","Mưa","Mưa","Mưa","Ám","Nắng","Nắng"],
            "Nhiệt độ":   ["Nóng","Nóng","Nóng","Mát","Lạnh","Lạnh","Lạnh","Mát","Lạnh"],
            "Độ ẩm":      ["Cao","Cao","Cao","Cao","Cao","Bình thường","Bình thường","Cao","Bình thường"],
            "Gió":        ["Yếu","Mạnh","Mạnh","Yếu","Mạnh","Mạnh","Yếu","Yếu","Yếu"],
            "Đi chơi":    ["No","No","Yes","Yes","No","No","Yes","No","Yes"],
        }),
        "target_col": "Đi chơi",
        "test_sample": {"Thời tiết": "Nắng", "Nhiệt độ": "Nóng", "Độ ẩm": "Cao", "Gió": "Yếu"},
        "test_label": "X = (Nắng, Nóng, Cao, Yếu)",
    },
    "Ví dụ Golf (Bài 4 — 14 mẫu, Laplace)": {
        "description": (
            "14 mẫu dữ liệu golf. Phân lớp mẫu X=(Overcast, Cool, High, Strong) "
            "với làm trơn Laplace. Kết quả: Play=Yes."
        ),
        "df": pd.DataFrame({
            "Outlook":    ["Sunny","Sunny","Overcast","Rainy","Rainy","Rainy","Overcast",
                           "Sunny","Sunny","Rainy","Sunny","Overcast","Overcast","Rainy"],
            "Temp":       ["Hot","Hot","Hot","Mild","Cool","Cool","Cool",
                           "Mild","Cold","Mild","Mild","Mild","Hot","Mild"],
            "Humidity":   ["High","High","High","High","Normal","Normal","Normal",
                           "High","Normal","Normal","Normal","High","Normal","High"],
            "Wind":       ["Weak","Strong","Weak","Weak","Weak","Strong","Strong",
                           "Weak","Weak","Weak","Strong","Strong","Weak","Strong"],
            "Play":       ["No","No","Yes","Yes","Yes","No","Yes",
                           "No","Yes","Yes","Yes","Yes","Yes","No"],
        }),
        "target_col": "Play",
        "test_sample": {"Outlook": "Overcast", "Temp": "Cool", "Humidity": "High", "Wind": "Strong"},
        "test_label": "X = (Overcast, Cool, High, Strong)",
        "laplace": True,
    },
    "Ví dụ Laptop (Bài 7 — dự đoán laptop)": {
        "description": (
            "10 mẫu dữ liệu. Câu hỏi: 'Thiện (18-22, Sinh viên, Học tập) nên mua laptop hãng nào?' "
            "Kết quả: Samsung (P=0.200 — cao nhất)."
        ),
        "df": pd.DataFrame({
            "Tuổi":            ["Trên 40","18-22","31-40","18-22","31-40","Trên 40","18-22","31-40","18-22","Trên 40"],
            "Nghề nghiệp":     ["Bác sĩ","Sinh viên","Kỹ sư","Sinh viên","Kỹ sư","Kỹ sư","Sinh viên","Bác sĩ","Sinh viên","Bác sĩ"],
            "Mục đích":        ["Đánh văn bản","Học tập","Thiết kế đồ họa","Học tập","Thiết kế đồ họa","Thiết kế đồ họa","Học tập","Đánh văn bản","Học tập","Đánh văn bản"],
            "Laptop":          ["Acer","Samsung","Dell","Samsung","Asus","Apple","Acer","Acer","Dell","Dell"],
        }),
        "target_col": "Laptop",
        "test_sample": {"Tuổi": "18-22", "Nghề nghiệp": "Sinh viên", "Mục đích": "Học tập"},
        "test_label": "Thiện = (18-22, Sinh viên, Học tập)",
        "laplace": False,
    },
}

# ============================================================
# BÀI 5: PHÂN LỚP CÂY QUYẾT ĐỊNH (ID3)
# ============================================================

DTREE_DATASETS = {
    "Ví dụ Golf — David (Bài 5 — 14 mẫu)": {
        "description": (
            "David muốn dự đoán khi nào khách đến chơi golf dựa vào thời tiết. "
            "Cây kết quả: gốc = Outlook, nhánh Sunny → Humidity, nhánh Rainy → Wind."
        ),
        "df": pd.DataFrame({
            "Ngày":     list(range(1, 15)),
            "Outlook":  ["Sunny","Sunny","Overcast","Rainy","Rainy","Rainy","Overcast",
                         "Sunny","Sunny","Rainy","Sunny","Overcast","Overcast","Rainy"],
            "Temp":     ["Hot","Hot","Hot","Mild","Cool","Cool","Cool",
                         "Mild","Cold","Mild","Mild","Mild","Hot","Mild"],
            "Humidity": ["High","High","High","High","Normal","Normal","Normal",
                         "High","Normal","Normal","Normal","High","Normal","High"],
            "Wind":     ["Weak","Strong","Weak","Weak","Weak","Strong","Strong",
                         "Weak","Weak","Weak","Strong","Strong","Weak","Strong"],
            "Play":     ["No","No","Yes","Yes","Yes","No","Yes",
                         "No","Yes","Yes","Yes","Yes","Yes","No"],
        }),
        "features": ["Outlook","Temp","Humidity","Wind"],
        "target": "Play",
    },
    "Ví dụ Trốn thuế (Bài 5 — 10 mẫu)": {
        "description": (
            "Dự đoán khả năng trốn thuế dựa vào Refund, Marital Status và Thu nhập (đã rời rạc hóa). "
            "Ví dụ: Ông A (Tid=10) có trốn thuế không?"
        ),
        "df": pd.DataFrame({
            "Tid":            list(range(1, 11)),
            "Refund":         ["Yes","No","No","Yes","No","No","Yes","No","No","No"],
            "Marital Status": ["Single","Married","Single","Married","Divorced","Married","Divorced","Single","Married","Single"],
            "Thu nhập":       ["Cao","Cao","Thấp","Cao","Trung bình","Thấp","Rất cao","Trung bình","Thấp","Trung bình"],
            "Evade":          ["No","No","No","No","Yes","No","No","Yes","No","Yes"],
        }),
        "features": ["Refund","Marital Status","Thu nhập"],
        "target": "Evade",
    },
}

# ============================================================
# BÀI 6: GOM CỤM K-MEANS
# ============================================================

KMEANS_DATASETS = {
    "Ví dụ 4 điểm (Bài 6 — trang 18)": {
        "description": (
            "4 điểm dữ liệu 2D. Gom cụm với k=2, khởi tạo: C1={x1}, C2={x2,x3,x4}. "
            "Kết quả hội tụ: C1={x1,x2,x3}, C2={x4}."
        ),
        "points": {
            "x1": [1.0,   3.0],
            "x2": [1.5,   3.2],
            "x3": [1.3,   2.8],
            "x4": [3.0,   1.0],
        },
        "initial_assignment": [0, 1, 1, 1],  # x1→C1, x2,x3,x4→C2
        "default_k": 2,
        "labels": ["x1","x2","x3","x4"],
    },
    "Ví dụ 6 điểm (minh họa thêm)": {
        "description": "6 điểm dữ liệu 2D tạo thành 2 cụm tự nhiên. Gom cụm với k=2.",
        "points": {
            "A": [1.0, 1.0],
            "B": [1.5, 2.0],
            "C": [3.0, 4.0],
            "D": [5.0, 7.0],
            "E": [3.5, 5.0],
            "F": [4.5, 5.0],
        },
        "initial_assignment": [0, 0, 1, 1, 1, 1],
        "default_k": 2,
        "labels": ["A","B","C","D","E","F"],
    },
}

# ============================================================
# BÀI 8: GOM CỤM BẰNG MẠNG KOHONEN
# ============================================================

KOHONEN_DATASETS = {
    "Ví dụ 9 điểm (Bài 8 — Bài tập trang 27)": {
        "description": (
            "9 điểm 2D từ bài tập bài 8. "
            "Dùng mạng Kohonen Map 5×5 để gom cụm."
        ),
        "points": {
            "x1": [0.7,  0.45],
            "x2": [2.8,  1.0],
            "x3": [2.6,  1.0],
            "x4": [1.0,  0.8],
            "x5": [2.5,  1.2],
            "x6": [1.3,  1.4],
            "x7": [0.4,  0.7],
            "x8": [1.7,  1.8],
            "x9": [2.0,  2.0],
        },
        "default_map": (5, 5),
        "labels": ["x1","x2","x3","x4","x5","x6","x7","x8","x9"],
    },
    "Ví dụ 3 cụm (minh họa SOM)": {
        "description": "15 điểm 2D tạo thành 3 cụm rõ ràng. Mạng Kohonen Map 4×4.",
        "points": {
            "p1":  [1.0, 1.0], "p2":  [1.2, 0.8], "p3":  [0.8, 1.2],
            "p4":  [4.0, 1.0], "p5":  [4.2, 0.8], "p6":  [3.8, 1.2],
            "p7":  [2.5, 4.0], "p8":  [2.7, 3.8], "p9":  [2.3, 4.2],
            "p10": [1.1, 0.9], "p11": [4.1, 0.9], "p12": [2.6, 4.1],
            "p13": [0.9, 1.1], "p14": [3.9, 1.1], "p15": [2.4, 3.9],
        },
        "default_map": (4, 4),
        "labels": [f"p{i}" for i in range(1, 16)],
    },
}
