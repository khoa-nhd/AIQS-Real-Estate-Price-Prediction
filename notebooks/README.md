# Notebooks – Khám phá và thử nghiệm

Thư mục này chứa các notebook Jupyter dùng để EDA, trực quan hóa dữ liệu và thử nghiệm mô hình.

## 1. Cấu trúc gợi ý

* `01_eda.ipynb`: Khám phá dữ liệu, phân tích phân phối, missing values và outliers.
* `02_preprocessing_experiments.ipynb`: Thử nghiệm các phương pháp xử lý dữ liệu.
* `03_baseline_models.ipynb`: Xây dựng mô hình baseline.
* `04_model_comparison.ipynb`: So sánh các mô hình và phân tích kết quả.

Có thể bổ sung notebook khi cần. Không bắt buộc tạo tất cả ngay từ đầu.

## 2. Quy trình làm việc

1. Mỗi notebook nên có một mục tiêu rõ ràng.
2. Ghi mục tiêu, nguồn dữ liệu và phương pháp trong Markdown cell.
3. Chạy notebook từ đầu đến cuối trước khi gửi Pull Request.
4. Sử dụng đường dẫn tương đối từ thư mục gốc repo.
5. Khi code trở nên ổn định và cần tái sử dụng, chuyển code sang `src/`.

## 3. Quy tắc cộng tác

* Tránh nhiều người cùng sửa một notebook trong cùng thời điểm vì Git khó hợp nhất thay đổi bên trong file `.ipynb`.
* Thông báo cho team trước khi sửa notebook đang được thành viên khác sử dụng.
* Xóa output lớn hoặc thông tin nhạy cảm trước khi commit.
* Không dùng notebook làm nơi duy nhất chứa code cần chạy trong ứng dụng chính thức.

## 4. Báo cáo kết quả thí nghiệm

Với mỗi thử nghiệm quan trọng, cần ghi lại:

* Mục tiêu thử nghiệm.
* Dataset và cách chia train/validation/test.
* Phương pháp preprocessing.
* Mô hình và tham số chính.
* R², MAE, RMSE.
* Kết luận và hướng cải thiện.

Không so sánh trực tiếp metric của các mô hình nếu chúng được đánh giá trên các tập test khác nhau.

Mục tiêu: Notebook giúp team hiểu dữ liệu, kiểm chứng giả thuyết và lựa chọn phương pháp dựa trên kết quả thực nghiệm.
