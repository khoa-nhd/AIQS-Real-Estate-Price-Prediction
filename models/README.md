# Models – Quản lý mô hình đã huấn luyện

Thư mục này dùng để quản lý các artifact của mô hình machine learning sau khi huấn luyện.

## 1. Model artifact là gì?

Model artifact là file lưu trạng thái đã học của mô hình, ví dụ cấu trúc các cây trong Random Forest.

Artifact có thể chứa cả pipeline preprocessing và model để đảm bảo dữ liệu đầu vào được biến đổi đúng cách khi dự đoán.

Artifact không phải dataset gốc và cũng không phải code dùng để huấn luyện.

## 2. Quy ước đặt tên

Ví dụ:

* `baseline_linear_v1.joblib`
* `random_forest_v1.joblib`
* `xgboost_v1.joblib`

Không ghi đè model đang được ứng dụng sử dụng mà chưa thông báo cho team.

## 3. Lưu và tải model

Ví dụ sử dụng Joblib:

```python
import joblib

# Lưu pipeline đã train
joblib.dump(
    pipeline,
    "models/random_forest_v1.joblib"
)

# Tải model đã lưu
pipeline = joblib.load(
    "models/random_forest_v1.joblib"
)
```

Chỉ tải file pickle/joblib từ nguồn đáng tin cậy vì file không đáng tin cậy có thể thực thi mã nguy hiểm.

## 4. Thông tin cần ghi lại

Với mỗi model được sử dụng chính thức, ghi lại:

* Tên model và phiên bản.
* Dataset/version sử dụng.
* Các feature đầu vào.
* Preprocessing.
* Tham số chính và random seed.
* R², MAE, RMSE.
* Phiên bản thư viện cần thiết.

## 5. Chia sẻ model

Model có thể lớn nên không commit trực tiếp lên Git nếu chưa được thống nhất.

Team cần thống nhất nơi lưu trữ model chung hoặc sử dụng Git LFS nếu phù hợp.

Nếu thay đổi model được ứng dụng sử dụng, cần thông báo cho thành viên phụ trách `app/`.

Mục tiêu: Team có thể xác định model nào được sử dụng, model được train bằng dữ liệu nào và cách tái sử dụng nó.
