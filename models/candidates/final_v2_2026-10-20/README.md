# Model cuối — ensemble XGBoost + LightGBM (splits_v2), 2026-10-20

Xuất từ `notebooks/03_model_experiments.ipynb`, C68. Fit trên train của `splits_v2`; đã chấm test một lần (C67).

| | MAE | RMSE | R² |
|---|---|---|---|
| Validation | 0.8802 | 1.2100 | 0.6947 |
| Test | 0.8917 | 1.2188 | 0.6986 |

Tiêu chí R² test ≥ 0,7: chưa đạt. Khoảng dự đoán 80% được hiệu chỉnh riêng ở `notebooks/04_calibration.ipynb` (split conformal theo nhóm giá trên tập calibration; độ phủ test 80,0%) và lưu ở `experiments/calibration/prediction_interval.json`; file .pkl và manifest.json này không đổi.

## Nạp và dự đoán

Cài đúng phiên bản trong `requirements-model.txt` (có `cloudpickle`). Chỉ nạp file pickle từ nguồn tin cậy.

```python
import pickle
import pandas as pd

with open("house_price_ensemble.pkl", "rb") as handle:
    model = pickle.load(handle)

house = pd.DataFrame([{
    "Area": 60, "Frontage": None, "Access Road": None, "House direction": None,
    "Balcony direction": None, "Floors": 4, "Bedrooms": 3, "Bathrooms": None,
    "Legal status": "Have certificate", "Furniture state": None,
    "City": "Hà Nội", "District": "Cầu Giấy",
    "Address": "Đường Trần Thái Tông, Phường Dịch Vọng, Cầu Giấy, Hà Nội",
}])
price_ty = model.predict(house)[0]   # tổng giá, tỷ VND
print(model.metadata["metrics"])
```

- Cần đủ 12 cột: Area, Frontage, Access Road, House direction, Balcony direction, Floors, Bedrooms, Bathrooms, Legal status, Furniture state, City, District. Giá trị không biết để `None`.
- `Address` nên có phường/xã và tên đường (tên dự án nếu có). Model dựa nhiều vào hai thông tin này: trên validation, khi không có địa chỉ chi tiết, MAE là 1.138 và R² là 0.556 (có địa chỉ: MAE 0.880), thấp hơn nhiều so với model không dùng địa chỉ chi tiết (notebook 03, C55: MAE CV khoảng 0,98; khác tập đo). Vì vậy app bắt buộc nhập phường/xã.
- `Price` là giá rao trong dữ liệu (1–11,5 tỷ); model không đáng tin ngoài khoảng này.
