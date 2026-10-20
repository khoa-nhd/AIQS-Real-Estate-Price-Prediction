# AIQS – Dự đoán giá nhà ở Việt Nam

Dự án ước tính **tổng giá rao bán (tỷ đồng)** của một căn nhà ở Việt Nam từ diện tích, kết cấu, pháp lý và địa chỉ. Dữ liệu là Vietnam Housing Dataset 2024 (30.229 tin rao, giá 1–11,5 tỷ). Repo gồm:
* làm sạch và phân tích dữ liệu;
* so sánh và chọn mô hình không rò rỉ dữ liệu;
* hiệu chỉnh khoảng dự đoán;
* báo cáo LaTeX;
* hai bản ứng dụng ước tính giá bằng tiếng Việt.

## Kết quả chính

Mô hình cuối là trung bình **0,5 XGBoost + 0,5 LightGBM**. Phường/xã, tên đường và tên dự án được tách lại từ địa chỉ gốc và mã hoá bằng target encoding. Mô hình học trên 18.136 dòng train của `splits_v2` và được khoá ngày 20/10/2026.

| Tập đánh giá | MAE (tỷ) | RMSE (tỷ) | R² |
|---|---|---|---|
| 3-fold CV trên train (dùng để chọn) | 0,915 | 1,243 | 0,685 |
| Validation (4.535 dòng) | 0,880 | 1,210 | 0,695 |
| **Test (4.535 dòng, chấm một lần)** | **0,892** | **1,219** | **0,699** |
| Test, bỏ tin trùng với train | 0,934 | 1,266 | 0,677 |

* **Mục tiêu R² ≥ 0,7 trên test: chưa đạt** (0,6986). Cấu hình đã khoá sau khi xem test. Mọi cải tiến sau này phải được chọn bằng cross-validation và ghi rõ là tập test đã được xem trước.
* **Sai số tương đối:** 70% căn được ước lượng trong ±20% (out-of-fold trên train; 71% trên test). Quy tắc "đơn giá quận × diện tích" mà người mua và môi giới hay dùng chỉ đạt 52% (out-of-fold).
* **Khoảng dao động 80%:** dùng split conformal theo 5 nhóm giá, học trên tập calibration. Giá thật nằm trong khoảng ở 80,0% căn test (78,3% nếu bỏ tin trùng). Khoảng rộng trung bình 2,8 tỷ.
* **Tin đăng trùng:** khoảng 11% tin trùng địa chỉ, diện tích và giá với tin khác, nên điểm số hơi lạc quan.

## Ứng dụng

Cả hai bản dùng chung trường nhập, quy tắc kiểm tra, nội dung chữ và số liệu. Bắt buộc nhập tỉnh, quận, phường/xã và diện tích; các mục khác có thể để "Không rõ". Kết quả gồm giá ước tính, khoảng dao động 80%, sai số trung bình trên test, và vị trí của mức giá so với dữ liệu.

| Bản | Thư mục | Deploy | Hướng dẫn |
|---|---|---|---|
| Web tĩnh, mô hình chạy trong trình duyệt | `web/` | Vercel (`vercel.json` ở gốc repo, không có bước build) | [web/README.md](web/README.md) |
| Streamlit | `app/` | Streamlit Community Cloud (chọn **Python 3.14**) hoặc Docker (`Dockerfile`) | [app/README.md](app/README.md) |

Bản web dùng các cây của mô hình đã khoá, xuất ra JSON. Trên toàn bộ dòng validation và calibration, giá và khoảng nó tính ra trùng với file `.pkl`.

Kiểm tra nhanh sau khi deploy: chọn Hà Nội / Cầu Giấy / Phường Dịch Vọng, 60 m², 4 tầng. Kết quả phải là **8,9 tỷ đồng**, khoảng **7,4 – 10,3 tỷ đồng**.

## Cấu trúc repo

```
AIQS-Real-Estate-Price-Prediction/
├── data/
│   ├── vietnam_housing_dataset.csv   # dữ liệu gốc, không sửa
│   ├── _v1.csv                       # sau khi làm sạch, tách City/District từ Address
│   └── processed/
│       ├── splits_v1/                # train/validation/calibration/test
│       └── splits_v2/                # cùng các dòng; Frontage/Access Road về giá trị gốc (dùng cho mô hình cuối)
├── notebooks/
│   ├── cleandata_estate_aiqs.ipynb   # làm sạch, tách địa chỉ (Colab)
│   ├── 01_data_handoff_and_split.ipynb
│   ├── 02_baseline_models.ipynb      # Dummy, Linear, Random Forest
│   ├── 03_model_experiments.ipynb    # boosting, CV, cải tiến, test, xuất mô hình
│   ├── 04_calibration.ipynb          # khoảng dự đoán 80%
│   ├── boxplot_price_aiqs.ipynb      # biểu đồ phân bố giá (Colab)
│   └── evaluatePrize.ipynb           # kiểm tra cột Price
├── experiments/                      # kết quả CV từng fold, grid search, v2, final_selection, calibration
├── models/candidates/
│   ├── milestone_v2_r2_2026-10-16/   # checkpoint CV cũ + script tạo splits_v2
│   └── final_v2_2026-10-20/          # mô hình cuối (.pkl), manifest.json, requirements-model.txt
├── app/                              # ứng dụng Streamlit
├── web/                              # ứng dụng web tĩnh cho Vercel
├── tests/                            # test_app.py, test_web_model.py
├── reports/application_report/       # báo cáo: main.tex và bản PDF
├── vercel.json                       # cấu hình Vercel (phục vụ web/public)
├── Dockerfile, packages.txt          # deploy Docker / Streamlit Community Cloud
├── requirements-dev.txt              # thư viện cho notebook và test (gồm app/requirements.txt)
└── README.md
```

## Chạy lại

**Môi trường:** Python **3.14**, vì file mô hình được lưu bằng cloudpickle và chỉ nạp được trên đúng phiên bản Python này.

```bash
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r requirements-dev.txt
```

`app/requirements.txt` ghim đúng các phiên bản mà mô hình được lưu cùng: numpy 2.5.3, pandas 3.0.6, scikit-learn 1.9.1, scipy 1.18.1, xgboost 3.4.1, lightgbm 4.7.0, cloudpickle 3.1.2. `requirements-dev.txt` gồm toàn bộ `app/requirements.txt` cộng thư viện cho notebook và test (catboost, matplotlib, Jupyter kernel). Các notebook chạy trên Colab (`cleandata_estate_aiqs`, `boxplot_price_aiqs`) dùng thêm seaborn.

**Thứ tự notebook:**
1. `cleandata_estate_aiqs`.
2. `01_data_handoff_and_split`.
3. Script tạo `splits_v2` (đường dẫn ở bước M14a của notebook 01).
4. `02_baseline_models`.
5. `03_model_experiments`.
6. `04_calibration`.

Với notebook 03, **không Run All**: các ô grid search C24/C32/C35/C38 chạy nhiều giờ. Kết quả từng fold đã lưu trong `experiments/` và chạy lại sẽ đọc kết quả có sẵn. Hướng dẫn chạy nằm ở ô đầu notebook.

**Ứng dụng và kiểm thử** (từ thư mục gốc repo):

```bash
python -m streamlit run app/streamlit_app.py
```

```bash
python -m http.server 8702 --directory web/public
```

```bash
python -m unittest discover -s tests -v
```

Bộ test gồm 16 test. `tests/test_web_model.py` cần Node.js 22 trở lên. Khi đổi mô hình, chạy lại notebook 04, sau đó chạy `python web/scripts/export_web_data.py` rồi chạy test.

## Báo cáo

`reports/application_report/main.tex` (biên dịch bằng LaTeX, ví dụ trên Overleaf) cùng bản PDF trong cùng thư mục. Báo cáo gồm dữ liệu và kiểm tra chất lượng, EDA và giả thuyết, tiền xử lý, mô hình, đánh giá (cả khoảng dự đoán), ứng dụng, khuyến nghị, giới hạn và cách tái lập.

## Giới hạn

* Giá trong dữ liệu là giá rao, không phải giá giao dịch, và chỉ trong khoảng 1–11,5 tỷ. 74% tin ở Hà Nội và TP.HCM, và đây là ảnh chụp năm 2024.
* Mô hình cần địa chỉ đến phường/xã. Thiếu phường, đường và dự án thì R² trên validation giảm từ 0,695 xuống 0,556.
* Khoảng dao động 80% chỉ đúng trung bình trên nhiều căn, không bảo đảm cho từng căn.
* Kết quả là ước tính tham khảo, không thay cho thẩm định giá.
