# Mốc hai model trên splits_v2 — 2026-10-16

Mỗi file .pkl là một dictionary chứa 3 pipeline CV đã fit (preprocessing + estimator), cấu hình, phiên bản, fold và metric. Không phải một estimator final fit toàn bộ train. Không train lại để xuất file.

- xgboost_cv_checkpoint.pkl: XGBoost_grid_round1, early stopping MAE, chọn theo mean CV R².
- lightgbm_cv_checkpoint.pkl: LightGBM_grid_round1, early stopping MAE, chọn theo mean CV R².
- Metric là trung bình 3 fold riêng, không phải điểm của ensemble trung bình dự đoán 3 pipeline.
- Pipeline fold không được train trên phần assessment của fold đó. Không dùng cả 3 pipeline để tính lại OOF vì các pipeline khác đã thấy dòng assessment.
- Target Price: tỷ VND. Chưa calibration khoảng dự đoán, chưa đánh giá test.

## Nạp lại

Giữ cả thư mục này khi bàn giao, gồm src/ và requirements-checkpoint.txt. Dùng môi trường Python/thư viện tương thích với nguồn; xem phiên bản trong source manifest. Chỉ nạp pickle do mình tạo hoặc nguồn tin cậy.

```python
from pathlib import Path
import sys, pickle
checkpoint_dir = Path("đường_dẫn_tới_thư_mục_mốc")
sys.path.insert(0, str(checkpoint_dir))
with (checkpoint_dir / "xgboost_cv_checkpoint.pkl").open("rb") as f:
    checkpoint = pickle.load(f)
print(checkpoint["mean_cv_R2"])
pipeline_fold_1 = checkpoint["folds"][0]["pipeline"]
# X_new là DataFrame gồm các cột trong source_manifest['features'].
# predicted_price = pipeline_fold_1.predict(X_new)
```

Không đổi tên dictionary này thành model final. Khi chốt model để app sử dụng, cần bước fit pipeline final và đánh giá/bàn giao riêng.

## Kiểm tra đã thực hiện

Xác minh hash model/dự đoán gốc; đối chiếu 32 dự đoán assessment mỗi fold; pickle dump/load và kiểm tra dự đoán giống hệt trước khi xuất. Không thay đổi model nguồn hoặc dataset.
