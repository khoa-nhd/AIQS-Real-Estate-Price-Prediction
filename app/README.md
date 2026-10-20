# App – Ứng dụng dự đoán giá bất động sản

Thư mục này chứa code giao diện người dùng, dự kiến sử dụng Streamlit.

Ứng dụng cho phép người dùng nhập thông tin bất động sản và nhận giá dự đoán từ model đã huấn luyện.

## 1. Chức năng chính

1. Nhận thông tin bất động sản từ người dùng.
2. Kiểm tra dữ liệu đầu vào.
3. Tải model/pipeline đã được team xác nhận.
4. Thực hiện dự đoán.
5. Hiển thị giá dự đoán và đơn vị tiền tệ.

## 2. Chạy ứng dụng

Từ thư mục gốc repo, trong môi trường `.venv` của project (Python 3.14):

```bash
pip install -r app/requirements.txt
```

Sau đó chạy:

```bash
streamlit run app/streamlit_app.py
```

`requirements.txt` gồm Streamlit và đúng các phiên bản thư viện mà mô hình được lưu cùng (numpy, pandas, scikit-learn, scipy, xgboost, lightgbm, cloudpickle). Thiếu hoặc lệch phiên bản thì ứng dụng báo "Mô hình chưa sẵn sàng" thay vì ước tính.

Cấu trúc:

* `streamlit_app.py`: giao diện (bố cục, theme, markup) theo hướng thiết kế design_01.
* `styles.css`: CSS của giao diện.
* `core/`: phần không phụ thuộc giao diện: các trường nhập, nội dung chữ, kiểm tra dữ liệu, trạng thái và `model_interface.py`, nơi duy nhất ứng dụng gọi model.

## Mô hình đang dùng

Ứng dụng nạp mô hình đã khoá ở `models/candidates/final_v2_2026-10-20/house_price_ensemble.pkl` (notebook 03, C68): trung bình 0,5 XGBoost + 0,5 LightGBM, học trên `data/processed/splits_v2/train.csv`. Tệp chỉ được nạp khi mã SHA-256 khớp với `manifest.json` cùng thư mục, vì pickle có thể chạy mã khi nạp.

* **Đầu vào:** 12 thông tin của căn nhà và địa chỉ. Bắt buộc: tỉnh, quận, **phường/xã**, diện tích. Tên đường và dự án là tùy chọn. `core/model_interface.py` ghép phường, đường, dự án thành chuỗi `Address` theo đúng thứ tự trong dữ liệu (`[Dự án X, ][Đường Y, ]Phường Z, Quận, Tỉnh`).
* **Vì sao bắt buộc phường/xã:** mô hình dựa nhiều vào vị trí trong quận. Khi không có phường, đường và dự án, sai số trên tập kiểm định tăng từ 0,88 lên 1,14 tỷ đồng (notebook 03, C68).
* **Danh sách phường, đường, dự án:** lấy từ địa chỉ gốc của các dòng trong tập huấn luyện (`core/reference.py`), theo từng quận.
* **Kết quả hiển thị:** sai số trung bình và R² lấy từ lần đánh giá duy nhất trên tập kiểm tra (`experiments/final_selection/test_evaluation.json`). Chưa có khoảng dao động vì chưa làm bước calibration.

Bảng "Công cụ phòng thiết kế" chỉ hiện khi mở trang với `?lab=1`, để xem các trạng thái giao diện (kết quả mẫu, lỗi mô phỏng, mô hình chưa sẵn sàng).

## 3. Phối hợp với nhóm model

Trước khi tích hợp, cần thống nhất:

* Tên, kiểu dữ liệu và thứ tự các feature.
* Cách biểu diễn vị trí.
* Cách xử lý giá trị thiếu.
* Tên và vị trí file model.
* Đơn vị giá: VND, triệu VND hoặc tỷ VND.

Ưu tiên sử dụng pipeline đã đóng gói preprocessing cùng model để tránh xử lý dữ liệu khác nhau giữa lúc train và lúc dự đoán.

## 4. Kiểm tra trước khi merge

Thử ứng dụng với:

* Dữ liệu đầu vào hợp lệ.
* Trường bị bỏ trống.
* Giá trị sai kiểu dữ liệu.
* Một số trường hợp biên.

Không hiển thị giá dự đoán như giá chắc chắn. Cần ghi rõ đây là ước lượng từ mô hình và có thể có sai số.

Không commit API key, token, thông tin đăng nhập hoặc dữ liệu người dùng.

Mục tiêu: Ứng dụng chạy được, sử dụng đúng model và cung cấp trải nghiệm đơn giản cho người dùng.
