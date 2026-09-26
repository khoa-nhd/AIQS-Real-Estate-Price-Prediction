# Source Code – Xử lý và huấn luyện mô hình

Thư mục `src/` chứa code Python chính thức có thể tái sử dụng trong pipeline machine learning.

## 1. Cấu trúc gợi ý

* `preprocessing.py`: Làm sạch và biến đổi đặc trưng.
* `train.py`: Huấn luyện mô hình và lưu model.
* `evaluate.py`: Đánh giá mô hình và xuất metric.

Có thể tách thêm module khi code phát triển.

## 2. Trách nhiệm của từng phần

### Preprocessing

* Xử lý giá trị thiếu.
* Xử lý outliers theo phương pháp đã thống nhất.
* Mã hóa đặc trưng phân loại, ví dụ vị trí.
* Thực hiện các phép biến đổi cần thiết.

### Training

* Sử dụng dữ liệu train.
* Thử nghiệm các mô hình đã thống nhất.
* Lưu pipeline/model sau khi huấn luyện.
* Ghi lại cấu hình và kết quả.

### Evaluation

* Đánh giá trên validation/test.
* Tính R², MAE và RMSE.
* Phân tích sai số và so sánh mô hình.

## 3. Nguyên tắc viết code

* Viết hàm có đầu vào và đầu ra rõ ràng.
* Không sử dụng đường dẫn tuyệt đối trên máy cá nhân.
* Cố định random seed khi phù hợp.
* Không để code training tự chạy chỉ vì một module được import.
* Không fit preprocessing trên tập validation/test.
* Đảm bảo dữ liệu lúc dự đoán được xử lý giống dữ liệu lúc train.

## 4. Quy trình làm việc

1. Tạo branch riêng cho nhiệm vụ.
2. Viết hoặc chỉnh sửa module cần thiết.
3. Chạy thử trên dữ liệu phù hợp.
4. Kiểm tra ảnh hưởng đến các module khác.
5. Tạo Pull Request và mô tả cách kiểm tra.

Nếu thay đổi tên hàm, schema hoặc cách gọi module mà thành viên khác đang sử dụng, cần thông báo và cập nhật các phần liên quan.

Mục tiêu: Code trong `src/` phải dễ tái sử dụng, kiểm thử và tích hợp vào ứng dụng.
