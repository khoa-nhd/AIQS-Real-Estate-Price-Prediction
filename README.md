# AIQS – Dự đoán giá nhà ở Việt Nam

Dự án ước tính **tổng giá rao bán (tỷ đồng)** của một căn nhà ở Việt Nam từ diện tích, kết cấu, pháp lý và địa chỉ. Dữ liệu là Vietnam Housing Dataset 2024 (30.229 tin rao, giá 1–11,5 tỷ). Repo gồm:
* làm sạch và phân tích dữ liệu;
* so sánh và chọn mô hình không rò rỉ dữ liệu;
* chia lại dữ liệu theo nhóm tin cùng căn nhà và đánh giá lại;
* hiệu chỉnh khoảng dự đoán;
* báo cáo LaTeX;
* hai bản ứng dụng ước tính giá bằng tiếng Việt.

## Kết quả chính

Mô hình cuối là trung bình **0,5 XGBoost + 0,5 LightGBM**. Phường/xã, tên đường và tên dự án được tách lại từ địa chỉ gốc và mã hoá bằng target encoding. Cấu hình được chọn và khoá ngày 20/10/2026 trên `splits_v2` (chia ngẫu nhiên theo dòng). Vì khoảng 11% tin là tin đăng lại của cùng căn nhà, nhóm chia lại dữ liệu theo nhóm tin cùng căn (`splits_v3`, notebook 05, 26/10/2026), fit lại đúng cấu hình đó trên 18.880 dòng train và đánh giá lại. Ứng dụng dùng mô hình này.

| Tập đánh giá | MAE (tỷ) | RMSE (tỷ) | R² |
|---|---|---|---|
| *Chia ngẫu nhiên (`splits_v2`, notebook 03)* | | | |
| 3-fold CV trên train | 0,915 | 1,243 | 0,685 |
| Test (4.535 dòng) | 0,892 | 1,219 | 0,699 |
| Test, bỏ tin trùng với train | 0,934 | 1,266 | 0,677 |
| *Chia theo nhóm tin cùng căn (`splits_v3`, notebook 05), dùng trong ứng dụng* | | | |
| 3-fold CV theo nhóm trên train | 0,930 | 1,260 | 0,676 |
| Validation (4.268 dòng) | 0,894 | 1,224 | 0,686 |
| **Test (4.274 dòng, đánh giá lại)** | **0,921** | **1,248** | **0,686** |
| Test, chỉ căn không có tin cùng địa chỉ và diện tích trong train (77,9%) | 0,979 | 1,318 | 0,660 |

* **Mục tiêu R² ≥ 0,7 trên test: chưa đạt** (0,686 khi chia theo nhóm; 0,699 khi chia ngẫu nhiên). Cấu hình không được chỉnh sau khi xem test. Mọi cải tiến sau này phải được chọn bằng cross-validation theo nhóm và ghi rõ là tập test đã được xem trước.
* **Sai số tương đối:** 70% căn được ước lượng trong ±20% (out-of-fold theo nhóm; 70% trên test). Quy tắc "đơn giá quận × diện tích" mà người mua và môi giới hay dùng chỉ đạt 51–52%.
* **Khoảng dao động 80%:** split conformal theo 5 nhóm giá, học trên tập calibration. Giá thật nằm trong khoảng ở 78,9% căn test (76,5% với căn không có tin cùng địa chỉ và diện tích trong train). Khoảng rộng trung bình 2,85 tỷ, đủ để nhận ra mức giá rao quá xa nhưng không đủ hẹp để chốt giá.
* **Kết luận về biến** (pháp lý, hướng nhà, nội thất…) chỉ nói về dữ liệu này: mô hình dùng ít một biến không có nghĩa biến đó không quan trọng ngoài thực tế.
* **Dữ liệu là tin rao bán năm 2024**; ứng dụng ghi rõ điều này. Kiểm thử với người dùng đã có kịch bản (`reports/user_testing.md`) nhưng **chưa thực hiện**.

## Ứng dụng

Cả hai bản dùng chung trường nhập, quy tắc kiểm tra, nội dung chữ và số liệu. Bắt buộc nhập tỉnh, quận, phường/xã và diện tích; các mục khác có thể để "Không rõ". Kết quả gồm giá ước tính, khoảng dao động 80%, sai số trung bình trên test, và vị trí của mức giá so với dữ liệu.

| Bản | Thư mục | Deploy | Hướng dẫn |
|---|---|---|---|
| Web tĩnh, mô hình chạy trong trình duyệt | `web/` | Vercel (Root Directory `web`, không có bước build) | [web/README.md](web/README.md) |
| Streamlit | `app/` | Streamlit Community Cloud (chọn **Python 3.14**) hoặc Docker (`Dockerfile`) | [app/README.md](app/README.md) |

Bản web dùng các cây của mô hình đã khoá, xuất ra JSON. Trên toàn bộ dòng validation và calibration, giá và khoảng nó tính ra trùng với file `.pkl`.

Kiểm tra nhanh sau khi deploy: chọn Hà Nội / Cầu Giấy / Phường Dịch Vọng, 60 m², 4 tầng. Kết quả phải là **9,0 tỷ đồng**, khoảng **7,6 – 10,4 tỷ đồng**.

## Cấu trúc repo

```
AIQS-Real-Estate-Price-Prediction/
├── data/
│   ├── vietnam_housing_dataset.csv   # dữ liệu gốc, không sửa
│   ├── _v1.csv                       # sau khi làm sạch, tách City/District từ Address
│   └── processed/
│       ├── splits_v1/                # train/validation/calibration/test
│       ├── splits_v2/                # cùng các dòng; Frontage/Access Road về giá trị gốc
│       └── splits_v3/                # như v2, chia theo nhóm tin cùng căn (dùng cho mô hình cuối)
├── notebooks/
│   ├── cleandata_estate_aiqs.ipynb   # làm sạch, tách địa chỉ (Colab)
│   ├── 01_data_handoff_and_split.ipynb
│   ├── 02_baseline_models.ipynb      # Dummy, Linear, Random Forest
│   ├── 03_model_experiments.ipynb    # boosting, CV, cải tiến, test, xuất mô hình
│   ├── 04_calibration.ipynb          # chọn cách tính khoảng dự đoán 80%
│   ├── 05_group_split.ipynb          # chia theo nhóm, CV, fit, khoảng, test, xuất mô hình cuối
│   ├── boxplot_price_aiqs.ipynb      # biểu đồ phân bố giá (Colab)
│   └── evaluatePrize.ipynb           # kiểm tra cột Price
├── experiments/                      # kết quả CV từng fold, grid search, v2, final_selection, calibration, group_split
├── models/candidates/
│   ├── milestone_v2_r2_2026-10-16/   # checkpoint CV cũ + script tạo splits_v2
│   ├── final_v2_2026-10-20/          # mô hình của lần chia ngẫu nhiên
│   └── final_v3_group_2026-10-26/    # mô hình cuối (.pkl), manifest.json, requirements-model.txt
├── app/                              # ứng dụng Streamlit
├── web/                              # ứng dụng web tĩnh cho Vercel
├── tests/                            # test_app.py, test_web_model.py
├── reports/
│   ├── application_report/           # báo cáo: main.tex và bản PDF
│   └── user_testing.md               # kịch bản kiểm thử với người dùng
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
7. `05_group_split` (tạo `splits_v3` và mô hình cuối; chạy được từ đầu đến cuối).

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

Bộ test gồm 16 test. `tests/test_web_model.py` cần Node.js 22 trở lên. Khi đổi mô hình, học lại khoảng dao động (notebook 05), sau đó chạy `python web/scripts/export_web_data.py` rồi chạy test.

## Báo cáo

`reports/application_report/main.tex` (biên dịch bằng LaTeX, ví dụ trên Overleaf) cùng bản PDF trong cùng thư mục. Báo cáo gồm dữ liệu và kiểm tra chất lượng, EDA và giả thuyết, tiền xử lý, mô hình, đánh giá (cả khoảng dự đoán), ứng dụng, khuyến nghị, giới hạn và cách tái lập.

## Giới hạn

* Giá trong dữ liệu là giá rao, không phải giá giao dịch, và chỉ trong khoảng 1–11,5 tỷ. 74% tin ở Hà Nội và TP.HCM, và đây là ảnh chụp năm 2024.
* Mô hình cần địa chỉ đến phường/xã. Thiếu phường, đường và dự án thì R² trên validation giảm từ 0,695 xuống 0,556.
* Khoảng dao động 80% chỉ đúng trung bình trên nhiều căn, không bảo đảm cho từng căn.
* Kết quả là ước tính tham khảo, không thay cho thẩm định giá.
