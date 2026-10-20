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

Từ thư mục gốc repo:

```bash
pip install -r app/requirements.txt
```

Sau đó chạy:

```bash
streamlit run app/streamlit_app.py
```

Nếu file khởi chạy có tên khác, cập nhật hướng dẫn này.

Cấu trúc:

* `streamlit_app.py`: giao diện (bố cục, theme, markup) theo hướng thiết kế design_01.
* `styles.css`: CSS của giao diện.
* `core/`: phần không phụ thuộc giao diện: các trường nhập, nội dung chữ, kiểm tra dữ liệu, trạng thái và `model_interface.py`, nơi duy nhất ứng dụng gọi model.

Hiện repo chưa có model đã lưu, nên ứng dụng chạy ở chế độ xem trước: con số giá là dữ liệu mẫu (trung vị giá của tập huấn luyện) và được ghi rõ là mẫu, không phải dự đoán. Bảng "Công cụ phòng thiết kế" ở cuối trang chỉ dùng để xem các trạng thái giao diện và nên bỏ khi đã có model.

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
