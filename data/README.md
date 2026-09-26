# Quản lý dữ liệu

Thư mục này chứa dataset sử dụng trong dự án Dự đoán giá bất động sản (Real Estate Price Prediction).

## 1. Cấu trúc thư mục

* `raw/`: Chứa dữ liệu gốc tải từ nguồn. Không chỉnh sửa trực tiếp.
* `processed/`: Chứa dữ liệu sau khi làm sạch và biến đổi.
* `external/`: Chứa dữ liệu bổ sung từ nguồn bên ngoài (nếu có).

## 2. Quy trình làm việc

1. Ghi lại nguồn dataset, đường dẫn tải, ngày tải và điều kiện sử dụng.
2. Lưu dataset gốc vào `raw/`.
3. Khám phá và kiểm tra dữ liệu bằng notebook trong `notebooks/`.
4. Thực hiện làm sạch và xử lý dữ liệu bằng code trong `src/`.
5. Lưu dữ liệu đã xử lý vào `processed/`.
6. Ghi lại những thay đổi quan trọng để thành viên khác có thể tái tạo quy trình.

## 3. Quy tắc sử dụng

* Không chỉnh sửa trực tiếp dataset gốc.
* Không tự ý xóa hàng, đổi tên cột hoặc thay đổi định dạng dữ liệu dùng chung.
* Không lưu dữ liệu cá nhân hoặc dữ liệu không được phép chia sẻ lên GitHub.
* Không commit dataset lớn vào Git nếu chưa được team thống nhất.
* Nếu dữ liệu không được đưa lên GitHub, ghi rõ cách tải hoặc nơi lưu trữ chung.

## 4. Thông tin dataset

| Tên dataset                | Nguồn | File | Ghi chú |
| -------------------------- | ----- | ---- | ------- |
| Cập nhật sau khi team chốt |       |      |         |

## 5. Khi cập nhật dữ liệu

Trong Pull Request, cần ghi rõ:

* Nguồn dữ liệu.
* Lý do cập nhật.
* Những thay đổi về cấu trúc hoặc số lượng bản ghi.
* Cách tải hoặc tái tạo dữ liệu.

Mục tiêu: Mọi thành viên sử dụng cùng một phiên bản dữ liệu và có thể tái tạo các bước xử lý.
