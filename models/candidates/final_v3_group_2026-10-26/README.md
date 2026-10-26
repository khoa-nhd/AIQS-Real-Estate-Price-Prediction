# Mô hình cuối, chia tập theo nhóm tin cùng căn nhà (2026-10-26)

`house_price_ensemble.pkl`: trung bình 0,5 XGBoost + 0,5 LightGBM, **cùng cấu hình** với `final_v2_2026-10-20` (notebook 03), fit lại trên `data/processed/splits_v3/train.csv` (18.880 dòng). `splits_v3` giữ các tin cùng căn nhà (cùng địa chỉ và diện tích, và cùng giá hoặc cùng số tầng, phòng ngủ, phòng tắm) trong cùng một tập. Tạo và đánh giá ở `notebooks/05_group_split.ipynb`.

| Lần đo | MAE (tỷ) | RMSE | R² |
|---|---|---|---|
| CV 3 fold theo nhóm | 0,930 | 1,260 | 0,676 |
| Validation | 0,894 | 1,224 | 0,686 |
| Test (đánh giá lại) | 0,921 | 1,248 | 0,686 |
| Test, căn không có tin cùng địa chỉ + diện tích trong train | 0,979 | 1,318 | 0,660 |

Mục tiêu R² test ≥ 0,7: chưa đạt. Khoảng dự đoán 80%: `experiments/group_split/prediction_interval.json` (độ phủ test 78,9%, rộng trung bình 2,85 tỷ).

- File là cloudpickle, chỉ nạp được trên Python 3.14 với đúng phiên bản trong `requirements-model.txt`; app kiểm tra SHA-256 trong `manifest.json` trước khi nạp.
- Đầu vào: 12 cột gốc và cột `Address` (`[Dự án X, ][Đường Y, ]Phường Z, Quận, Tỉnh`). Giá là giá rao năm 2024, 1–11,5 tỷ.
