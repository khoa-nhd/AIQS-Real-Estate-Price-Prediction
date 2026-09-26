# Reports – Báo cáo và kết quả dự án

Thư mục này lưu các báo cáo, biểu đồ và kết quả thực nghiệm có thể chia sẻ trong team.

## 1. Nội dung

* Báo cáo EDA và chất lượng dữ liệu.
* Biểu đồ phân tích đặc trưng.
* Bảng so sánh các mô hình.
* Phân tích lỗi dự đoán.
* Báo cáo tiến độ hàng tuần.
* Báo cáo tổng kết dự án.

## 2. Quy ước đặt tên

Ví dụ:

* `eda_summary.md`
* `model_comparison.csv`
* `error_analysis.md`
* `weekly_report_01.md`

Tên file cần thể hiện rõ nội dung và phiên bản nếu có.

## 3. Quy tắc báo cáo kết quả

Mỗi báo cáo thực nghiệm nên ghi:

* Ngày thực hiện.
* Dataset/version.
* Phương pháp.
* Mô hình và cấu hình.
* Kết quả R², MAE, RMSE.
* Kết luận và hướng tiếp theo.

Phân biệt rõ kết quả trên train, validation và test.

Không liên tục lựa chọn mô hình dựa trên test set. Test set cần được giữ riêng để đánh giá cuối cùng theo quy trình đã thống nhất.

Không chỉnh sửa số liệu hoặc biểu đồ theo cách làm sai lệch kết quả.

## 4. Chia sẻ

Ưu tiên Markdown, CSV và ảnh có dung lượng hợp lý.

Không lưu bản sao dataset lớn hoặc thông tin nhạy cảm trong báo cáo.

Mục tiêu: Mọi thành viên có thể theo dõi tiến độ, kiểm tra kết quả và sử dụng báo cáo để chuẩn bị sản phẩm cuối dự án.
