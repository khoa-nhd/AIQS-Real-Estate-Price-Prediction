# Tests – Kiểm thử dự án

Thư mục này chứa các kiểm thử nhằm phát hiện lỗi khi thay đổi preprocessing, model hoặc ứng dụng.

## 1. Những phần cần kiểm thử

### Preprocessing

* Đầu ra có đúng các cột và kiểu dữ liệu dự kiến không?
* Giá trị thiếu được xử lý đúng không?
* Có vô tình làm thay đổi thứ tự feature không?

### Model

* Pipeline có nhận được dữ liệu đúng schema không?
* Model có trả về giá trị dự đoán hữu hạn không?
* Model có hoạt động với các trường hợp đầu vào hợp lệ không?

### App

* Ứng dụng có tải được model không?
* Input sai định dạng có được thông báo rõ ràng không?
* Kết quả có hiển thị đúng đơn vị giá không?

## 2. Quy ước viết test

* Đặt tên file theo dạng `test_*.py`.
* Dùng dữ liệu mẫu nhỏ hoặc dữ liệu giả lập.
* Không phụ thuộc đường dẫn tuyệt đối trên máy cá nhân.
* Không cần đưa dataset thật lên Git chỉ để chạy test.
* Không đặt ngưỡng R² cố định trên một tập mẫu rất nhỏ; ưu tiên kiểm tra chức năng và điều kiện đầu vào/đầu ra.

## 3. Chạy kiểm thử

Nếu team sử dụng pytest, chạy từ thư mục gốc repo:

```bash
pytest
```

Nếu chưa cài pytest:

```bash
pip install pytest
```

## 4. Khi gửi Pull Request

* Chạy các test liên quan trước khi tạo PR.
* Ghi lại test nào đã chạy và kết quả.
* Nếu thay đổi làm test cũ không còn phù hợp, cập nhật test và giải thích lý do.

Mục tiêu: Phát hiện lỗi sớm và đảm bảo các phần của dự án vẫn hoạt động sau khi tích hợp code từ nhiều thành viên.
