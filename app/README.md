# App – Ứng dụng ước tính giá nhà

Ứng dụng Streamlit cho phép nhập thông tin một căn nhà và nhận giá ước tính từ mô hình đã khoá của dự án (notebook 03). Ứng dụng có 3 tab: **Ước tính giá**, **Độ chính xác của mô hình** và **Dữ liệu và giới hạn**.

Muốn deploy trên **Vercel**, dùng bản web tĩnh trong `web/` (xem `web/README.md`). Bản đó có cùng chức năng, mô hình chạy trong trình duyệt và cho kết quả trùng với file `.pkl`.

> **Bắt buộc dùng Python 3.14.** Tệp mô hình được lưu bằng cloudpickle. Các class và hàm viết trong notebook được lưu dưới dạng bytecode của Python 3.14, nên chỉ nạp được trên Python 3.14. Thư viện cũng phải đúng phiên bản trong `app/requirements.txt`.

## 1. Chạy trên máy

Từ thư mục gốc repo:

```bash
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r app/requirements.txt
.venv\Scripts\python -m streamlit run app/streamlit_app.py
```

Trên macOS/Linux, dùng `python3.14 -m venv .venv` và `.venv/bin/python` cho các lệnh trên. Ứng dụng mở ở http://localhost:8501. Lần mở đầu mất khoảng 10 giây để nạp mô hình.

`app/requirements.txt` pin đúng mọi thư viện, kể cả các thư viện gián tiếp, theo bộ đã kiểm thử. Nhờ vậy máy chủ cài đúng những gì đã chạy trên máy nhóm.

## 2. Deploy lên Streamlit Community Cloud

1. Push repo lên GitHub. Các tệp ứng dụng cần (mục 6) đều đã được git theo dõi; không cần tải thêm gì.
2. Vào https://share.streamlit.io, đăng nhập bằng tài khoản GitHub có quyền với repo → **Create app** → chọn deploy từ GitHub.
3. Chọn repo `khoa-nhd/AIQS-Real-Estate-Price-Prediction`, branch `main`, **Main file path** `app/streamlit_app.py`.
4. Mở **Advanced settings** và chọn **Python version 3.14**. Phiên bản Python không đổi được sau khi deploy; nếu chọn sai, phải xoá app và deploy lại.
5. Bấm **Deploy**. Community Cloud tự đọc:
   * `app/requirements.txt`, vì tệp nằm cạnh file chính;
   * `packages.txt` ở gốc repo, để cài `libgomp1` (thư viện OpenMP mà LightGBM và XGBoost cần).
6. Kiểm tra sau khi deploy: chọn Hà Nội / Cầu Giấy / Phường Dịch Vọng, diện tích 60 m², 4 tầng, các mục khác để «Không rõ». Kết quả phải là **8,9 tỷ đồng**.

Nếu trang báo "Mô hình chưa sẵn sàng", xem mục 5.

## 3. Deploy bằng Docker

Dùng cho các nơi chạy container như Render, Railway, Fly.io, Google Cloud Run hay Hugging Face Spaces. `Dockerfile` ở gốc repo dùng `python:3.14-slim` và chỉ chép những tệp ứng dụng cần.

```bash
docker build -t aiqs-house-price .
docker run -p 8501:8501 aiqs-house-price
```

* Cổng mặc định là 8501. Nơi nào tự cấp cổng qua biến `PORT` (Render, Cloud Run, Railway) thì ứng dụng dùng cổng đó.
* Kiểm tra sức khoẻ: `GET /_stcore/health` trả về `ok`.
* Với Hugging Face Spaces: chọn loại Space **Docker** và thêm `app_port: 8501` vào phần metadata đầu README của Space.

## 4. Kiểm thử

Từ thư mục gốc repo, trong môi trường đã cài `app/requirements.txt`:

```bash
python -m unittest discover -s tests -v
```

`tests/test_app.py` chạy ứng dụng không cần trình duyệt (`streamlit.testing`) và kiểm tra những điểm sau:

* phiên bản thư viện trong `app/requirements.txt` khớp với manifest của mô hình, và môi trường hiện tại khớp với lúc lưu mô hình;
* ứng dụng nạp được mô hình thật và có đủ 3 tab;
* bấm ước tính khi form trống thì báo các mục bắt buộc;
* giá ứng dụng hiển thị bằng đúng giá khi gọi mô hình trực tiếp;
* giá đi kèm khoảng dao động đã hiệu chỉnh, và quy tắc tính khoảng giống notebook 04;
* đổi tỉnh thì xoá quận và phường đã chọn;
* khi mô hình không dùng được, trang nói rõ lý do và khoá nút ước tính.

## 5. Khi ứng dụng báo "Mô hình chưa sẵn sàng"

Ứng dụng không bao giờ đoán giá khi không chạy được mô hình. Banner đầu trang ghi dòng "Chi tiết cho người quản trị", và cùng nội dung đó được ghi vào log máy chủ (trên Community Cloud: **Manage app** → log).

| Chi tiết | Cách sửa |
|---|---|
| `cần Python 3.14, máy chủ đang chạy Python 3.x` | Deploy lại và chọn Python 3.14 (mục 2, bước 4). |
| `cần <thư viện> <phiên bản>, đang có ...` | Cài lại đúng theo `app/requirements.txt`. |
| `Tệp mô hình không khớp mã kiểm tra trong manifest.json` | Tệp `.pkl` bị thay đổi hoặc tải về không đầy đủ. Lấy lại đúng tệp từ git. |
| `Chưa có tệp mô hình ...` | Thiếu thư mục `models/candidates/final_v2_2026-10-20/`. |
| `Không nạp được mô hình (... OSError: libgomp ...)` | Máy chủ thiếu OpenMP: thêm `libgomp1` (đã có trong `packages.txt` và `Dockerfile`). |

## 6. Cấu trúc và các tệp đọc khi chạy

* `streamlit_app.py`: giao diện (bố cục, theme, markup) theo hướng thiết kế design_01.
* `styles.css`: CSS của giao diện.
* `core/`: phần không phụ thuộc giao diện, gồm các trường nhập (`schema.py`), nội dung chữ (`content.py`), kiểm tra dữ liệu (`validation.py`), trạng thái (`state.py`), và `model_interface.py` là nơi duy nhất ứng dụng gọi mô hình.

Khi chạy, ứng dụng đọc các tệp sau. Mọi đường dẫn tính từ vị trí mã nguồn nên chạy từ thư mục nào cũng được.

| Tệp | Dùng để |
|---|---|
| `models/candidates/final_v2_2026-10-20/house_price_ensemble.pkl`, `manifest.json` | Mô hình và mã kiểm tra, phiên bản thư viện, số liệu |
| `data/processed/splits_v2/train.csv` | Danh sách tỉnh/quận, khoảng giá trị, phân bố giá |
| `data/vietnam_housing_dataset.csv` | Địa chỉ gốc của các dòng train, để lấy danh sách phường, đường, dự án |
| `experiments/final_selection/test_evaluation.json` | Kết quả lần đánh giá duy nhất trên tập test |
| `experiments/calibration/prediction_interval.json` | Khoảng dao động 80% (notebook 04); chỉ dùng khi mã băm khớp với mô hình |
| `experiments/ensemble_oof/blend_summary.csv` | Số liệu cross-validation của mô hình đang dùng |
| `experiments/model_comparison_cv/recovered_model_cv_*.csv` | Bảng so sánh các mô hình ứng viên (Phần A) |

## 7. Mô hình đang dùng

Ứng dụng nạp mô hình đã khoá ở `models/candidates/final_v2_2026-10-20/house_price_ensemble.pkl` (notebook 03, C68): trung bình 0,5 XGBoost + 0,5 LightGBM, học trên `data/processed/splits_v2/train.csv`. Vì pickle có thể chạy mã khi nạp, tệp chỉ được nạp khi mã SHA-256 khớp với `manifest.json` cùng thư mục, và khi Python cùng các thư viện đúng phiên bản ghi trong manifest.

* **Đầu vào:** 12 thông tin của căn nhà và địa chỉ. Bắt buộc: tỉnh, quận, **phường/xã**, diện tích. Tên đường và dự án là tùy chọn. `core/model_interface.py` ghép phường, đường, dự án thành chuỗi `Address` theo đúng thứ tự trong dữ liệu (`[Dự án X, ][Đường Y, ]Phường Z, Quận, Tỉnh`).
* **Vì sao bắt buộc phường/xã:** mô hình dựa nhiều vào vị trí trong quận. Khi không có phường, đường và dự án, sai số trên tập kiểm định tăng từ 0,88 lên 1,14 tỷ đồng (notebook 03, C68).
* **Danh sách tỉnh, quận, phường, đường, dự án:** lấy từ các dòng trong tập huấn luyện (`core/reference.py`). Chỉ đưa ra các cặp tỉnh–quận có ít nhất 10 dòng train, để loại các chuỗi địa danh rác và những nơi mô hình gần như chưa thấy.
* **Kết quả hiển thị:** sai số trung bình và R² lấy từ lần đánh giá duy nhất trên tập kiểm tra (`experiments/final_selection/test_evaluation.json`).
* **Khoảng dao động 80%:** do `notebooks/04_calibration.ipynb` tạo bằng split conformal theo 5 nhóm giá, học trên tập calibration. Độ phủ đo một lần trên test là 80,0% (78,3% với tin không trùng train); độ rộng trung bình 2,8 tỷ. App dùng khoảng chỉ khi mã SHA-256 ghi trong file khớp với mô hình đang chạy; nếu không, app hiện "Chưa có". Khi đổi mô hình phải chạy lại notebook 04.
* Giá luôn được trình bày là **ước tính của mô hình**, không phải giá thẩm định.

Bảng "Công cụ phòng thiết kế" chỉ hiện khi mở trang với `?lab=1`, dùng để xem các trạng thái giao diện (kết quả mẫu, lỗi mô phỏng, mô hình chưa sẵn sàng). Có thể mở thẳng một trạng thái bằng `?state=...`, ví dụ `?state=unavailable`.
