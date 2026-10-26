# Web – Bản web tĩnh của ứng dụng ước tính giá nhà (deploy trên Vercel)

Bản này có cùng chức năng với ứng dụng Streamlit trong `app/`: cùng trường nhập, quy tắc kiểm tra, nội dung chữ và số liệu, giao diện design_01. Điểm khác là **mô hình chạy ngay trong trình duyệt**, nên trang chỉ gồm các tệp tĩnh. Vercel phục vụ trực tiếp, không cần máy chủ Python, và thông tin người dùng nhập không được gửi đi đâu.

## Cách hoạt động

Vercel không chạy được máy chủ Streamlit. Nếu chạy mô hình trong Python Function của Vercel thì phải mang theo numpy, pandas, scikit-learn, XGBoost và LightGBM, và LightGBM còn cần thư viện hệ thống OpenMP. Vì vậy nhóm xuất mô hình đã khoá sang JSON:

1. `scripts/export_web_data.py` nạp `models/candidates/final_v3_group_2026-10-26/house_price_ensemble.pkl`, theo đúng cách app Streamlit nạp (kiểm tra mã SHA-256, Python 3.14 và phiên bản thư viện). Script ghi ra:
   * `public/data/model.json`: mọi tham số đã học của hai pipeline (StandardScaler, imputer, one-hot, target encoding của phường/đường/dự án) và toàn bộ 1.043 cây XGBoost, 683 cây LightGBM;
   * `public/data/reference.json`: danh sách tỉnh/quận/phường/đường/dự án, khoảng giá trị, phân bố giá, kết quả đánh giá, cùng nội dung chữ và danh sách trường lấy từ `app/core/`.

   Script cũng kiểm tra rằng mọi lựa chọn phường/đường/dự án trên trang, khi đi qua bộ tách địa chỉ của chính mô hình, cho ra đúng khoá mà trang gửi.
2. `public/model.js` áp các tham số đó theo đúng cách của scikit-learn, XGBoost và LightGBM. Ma trận tiền xử lý là ma trận thưa: XGBoost coi ô trống là thiếu, còn LightGBM coi là 0. XGBoost so sánh và cộng dồn bằng float32. Giá = 0,5 × XGBoost + 0,5 × LightGBM. Hàm `predictInterval` tính **khoảng dao động 80%** từ `experiments/group_split/prediction_interval.json` (notebook 05), dùng cùng quy tắc với `app/core/model_interface.py`.
3. `tests/test_web_model.py` chạy `model.js` bằng Node và so với file `.pkl`. Trên toàn bộ 4.268 dòng validation và 2.807 dòng calibration của `splits_v3`, chênh lệch giá bằng 0, và khoảng dao động trùng với bản Python. Test còn chạy trên mọi phường có trong biểu mẫu, với các mục tùy chọn để trống.
4. Khi tải trang, `model.js` tự tính lại ba căn mẫu có giá lấy từ file `.pkl`. Nếu lệch, trang khoá nút ước tính và báo "Mô hình chưa sẵn sàng".

## Deploy lên Vercel

`web/vercel.json` đã cấu hình sẵn: không cài đặt, không build, phục vụ thẳng thư mục `web/public` dưới dạng file tĩnh. (`vercel.json` ở gốc repo làm việc tương tự nếu Root Directory là gốc repo.)

1. Push repo lên GitHub (các tệp trong `web/public/data/` phải được commit, vì Vercel không tự tạo chúng).
2. Vào https://vercel.com/new, chọn **Import** repo `khoa-nhd/AIQS-Real-Estate-Price-Prediction`.
3. Framework Preset **Other**, **Root Directory `web`**, không bật Override cho Build/Output/Install Command. Vercel đọc `web/vercel.json`. Không đặt Root Directory là `app` (đó là bản Streamlit, Vercel không chạy được).
4. Bấm **Deploy**. Kiểm tra sau khi deploy: chọn Hà Nội / Cầu Giấy / Phường Dịch Vọng, 60 m², 4 tầng. Kết quả phải là **9,0 tỷ đồng**, khoảng dao động **7,6 – 10,4 tỷ đồng**.

Mỗi lần push lên `main`, Vercel tự deploy lại.

## Chạy trên máy

```bash
python -m http.server 8702 --directory web/public
```

Sau đó mở http://localhost:8702. Phải mở qua máy chủ, không mở trực tiếp file `index.html`, vì trình duyệt chặn việc đọc `data/*.json` từ `file://`.

## Khi đổi mô hình hoặc dữ liệu

Từ thư mục gốc repo, trong môi trường cài `app/requirements.txt` (Python 3.14):

Học lại khoảng dao động trước (`notebooks/05_group_split.ipynb`, ô C06 và C10), vì khoảng gắn với mã băm của mô hình. Sau đó:

```bash
python web/scripts/export_web_data.py
python -m unittest tests.test_web_model -v
```

Test cần Node.js 22 trở lên (Node tự nhận `model.js` là ES module). Commit lại `web/public/data/` sau khi test đạt.

## Tệp

| Tệp | Vai trò |
|---|---|
| `public/index.html`, `public/styles.css` | Khung trang và giao diện (design_01) |
| `public/app.js` | Biểu mẫu, kiểm tra đầu vào, kết quả, tab độ chính xác và dữ liệu (theo `app/streamlit_app.py` và `app/core/`) |
| `public/model.js` | Tính giá từ `model.json` (không phụ thuộc thư viện nào; trình duyệt và Node đều dùng được) |
| `public/data/` | `model.json` (~11 MB), `reference.json` |
| `scripts/export_web_data.py` | Tạo `public/data/` từ mô hình đã khoá |
| `scripts/predict.mjs` | Dự đoán hàng loạt bằng Node, dùng cho test |
