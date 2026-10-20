"""All interface copy for the app, in one place.

Vietnamese strings are proposed copy and need review by the team.

Terms, used the same way everywhere (the audience is the general public, not ML practitioners):
- "ước tính" / "giá ước tính" for what the app gives; never "dự đoán" in user-facing text.
- "mô hình" for the model; "tập huấn luyện" for the training split it learned from.
- "khoảng" only ever means a range: "khoảng dao động" is the estimate's range (the brief's term), and the
  price in words says "tức", never "khoảng", so the two cannot be confused. Comparisons with the data use
  shares ("cao hơn giá của 49% số căn"), not a second pair of numbers next to the price.
- "dữ liệu" on the estimate tab; "tập huấn luyện" only where the data and accuracy tabs explain it.
- "Không rõ" for a field the person left unknown.
"""

# Working title only. The product name is undecided (brief OD-9).
TITLE = "Ước tính giá nhà"
LEAD = (
    "Nhập thông tin căn nhà để nhận mức giá ước tính từ mô hình. "
    "Đây là con số tham khảo, không phải kết quả thẩm định."
)

NAV = ("Ước tính giá", "Độ chính xác của mô hình", "Dữ liệu và giới hạn")
VIEW_IDS = ("uoc-tinh", "do-chinh-xac", "du-lieu")

REQUIRED_LEGEND = "* Mục bắt buộc"
SUBMIT = "Ước tính giá"
RESET = "Xoá thông tin đã nhập"  # it clears every field, so the label says so
RETRY = "Thử lại"
UNDO = "Hoàn tác xoá"  # replaces the reset button right after a reset, so one click brings everything back
DISABLED_REASON = "Nút ước tính tạm khoá vì mô hình chưa sẵn sàng."
RANGE_HELP = "Trong dữ liệu: {low} – {high}{unit}"  # the values the model has seen
# Help on the optional address parts; the lists only hold names seen in the training data for that district.
ADDRESS_HELP = {
    "street": "Đường hoặc phố mà căn nhà nằm trên hoặc rẽ vào. Danh sách gồm các đường có trong dữ liệu của quận này.",
    "project": "Chỉ chọn nếu căn nhà thuộc một dự án. Danh sách gồm các dự án có trong dữ liệu của quận này.",
}
WARD_FEW_ROWS = (
    "Phường / xã này chỉ có {n} căn trong dữ liệu, nên mô hình chủ yếu dựa vào mức giá của quận "
    "và kết quả có thể kém tin cậy hơn."
)

# System banners
BANNER_PREVIEW = "Chế độ xem trước giao diện — giá trên trang này là số mẫu, không phải giá ước tính."
BANNER_UNAVAILABLE = "Mô hình chưa sẵn sàng. Ứng dụng chưa thể ước tính giá."

# Validation
SUMMARY_HEADING = "Chưa thể ước tính. Cần điền hoặc sửa {n} mục:"

# Result panel
RESULT_LABEL = "Giá ước tính"
PRICE_UNIT = "tỷ đồng"
SAMPLE_TAG = "Dữ liệu mẫu"
REAL_TAG = "Kết quả từ mô hình"
SAMPLE_STATEMENT = (
    "Đây là số mẫu để xem trước giao diện: nó không đổi theo thông tin bạn nhập "
    "và không phải giá ước tính."
)
REAL_STATEMENT = (
    "Đây là mức giá do mô hình ước tính từ dữ liệu, "
    "không phải giá thẩm định hay giá giao dịch."
)
UNCERTAINTY_LABEL = "Khoảng dao động"
UNCERTAINTY_NONE = "Chưa có"
UNCERTAINTY_NONE_TEXT = (
    "Chưa có khoảng giá đã được kiểm chứng cho từng căn, nên ứng dụng không hiển thị khoảng."
)
UNCERTAINTY_INTERVAL = "{low} – {high} tỷ đồng"
UNCERTAINTY_INTERVAL_TEXT = "Khoảng {coverage}, lấy từ bước kiểm tra độ tin cậy của mô hình."
RECAP_LABEL = "Thông tin bạn đã nhập"

# Where an estimate sits among the training prices (the strip under the price). Every sentence follows
# from the training split's min, quartiles and max; nothing here is a claim about the property itself.
MARKET_LABEL = "So với {n} căn trong dữ liệu"
MARKET_SHARE = "Cao hơn giá của {pct} số căn trong dữ liệu."
MARKET_LOWEST = "Ở mức giá thấp nhất có trong dữ liệu."
MARKET_OUTSIDE = "Nằm ngoài mức giá có trong dữ liệu (từ {low} đến {high} tỷ đồng), nên không có cơ sở so sánh."
MARKET_BIN = "{low} – {high} tỷ đồng: {n} căn"
MARKET_AXIS = "{value} tỷ"
# How far the estimate can be trusted, from the single evaluation on the test split (its MAE).
# It is an average error, not an interval: the copy never puts it next to the price as "± ...".
TRUST_LABEL = "Mô hình thường lệch bao nhiêu"
TRUST_VALUE = "{mae} tỷ đồng"
TRUST_TEXT = (
    "Sai số trung bình khi thử một lần trên {n} căn mô hình chưa từng thấy. "
    "Chi tiết ở tab «Độ chính xác của mô hình»."
)
TRUST_NONE = "Chưa có"
TRUST_NONE_TEXT = "Chưa có kết quả thử mô hình."
UNKNOWN_NONE = "Không có mục nào để «Không rõ»."
UNKNOWN_SOME = "{n} mục để «Không rõ»: {names}."
PROVENANCE_LABEL = "Nguồn kết quả"
PROVENANCE_SAMPLE = (
    "Số mẫu: mức giá ở giữa (trung vị) của {n} căn trong tập huấn luyện. "
    "Con số này không do mô hình tính ra."
)
PROVENANCE_UNKNOWN = "Không có thông tin phiên bản mô hình."
PROVENANCE_REAL = (
    "Trung bình hai mô hình cây quyết định (XGBoost và LightGBM), khoá ngày {created}, học từ tập huấn luyện. "
    "Khi thử một lần trên tập kiểm tra: lệch trung bình {mae} tỷ đồng, R² = {r2}."
)
STALE = "Thông tin đã thay đổi sau lần ước tính này. Chọn «Ước tính giá» để cập nhật."

STATE_TEXT = {
    "initial": ("Chưa có kết quả", "Điền thông tin căn nhà rồi chọn «Ước tính giá»."),
    "invalid": ("Chưa thể ước tính", "Sửa các mục được đánh dấu trong biểu mẫu, rồi chọn «Ước tính giá» lại."),
    "fixed": ("Chưa có kết quả", "Thông tin đã đủ. Chọn «Ước tính giá» để xem kết quả."),
    "unavailable": (
        "Mô hình chưa sẵn sàng",
        "Hiện chưa thể ước tính vì ứng dụng không nạp được mô hình. "
        "Thông tin bạn nhập vẫn được giữ nguyên.",
    ),
    "error": (
        "Không ước tính được",
        "Đã xảy ra lỗi khi mô hình xử lý thông tin. Thông tin bạn nhập vẫn được giữ nguyên. Hãy thử lại.",
    ),
}
STATE_ICON = {
    "initial": "info",
    "invalid": "error",
    "fixed": "info",
    "unavailable": "cloud_off",
    "error": "warning",
    "sample": "science",
    "result": "check_circle",
}
SIMULATED_NOTE = "Lỗi mô phỏng để xem trước giao diện; không có mô hình nào chạy."

# Model accuracy view
EVAL_INTRO = (
    "Số liệu đọc trực tiếp từ tệp kết quả của nhóm, cho mô hình đang dùng trong ứng dụng."
)
# The one answer this tab owes the public, built from the test evaluation and the training prices.
ACC_TEXT = (
    "Khi thử trên {n} căn nó chưa từng thấy, mô hình ước tính lệch trung bình {mae} tỷ đồng "
    "so với giá trong dữ liệu. Với căn có giá ở giữa dữ liệu ({median} tỷ đồng), mức lệch này bằng {share} giá."
)
ACC_NOTE = (
    "Đây là mức trung bình: với từng căn, giá ước tính có thể lệch nhiều hơn hoặc ít hơn. "
    "Khoảng {twin} số căn thử nghiệm là tin đăng trùng với dữ liệu huấn luyện; "
    "chỉ tính những căn còn lại, mức lệch trung bình là {mae_new} tỷ đồng."
)
TEAM_DETAILS = "Chi tiết cho nhóm: các lần đo của mô hình đang dùng và {n} mô hình ứng viên"
EVAL_FINAL_LABEL = "Đánh giá cuối cùng trên tập kiểm tra"
EVAL_FINAL_VALUE = "R² = {r2}"
EVAL_FINAL_TEXT = (
    "Thử một lần trên {n} căn mô hình chưa từng thấy, sau khi đã chọn xong mô hình. "
    "Mục tiêu của dự án là R² từ 0,7 trở lên: {verdict}"
)
EVAL_FINAL_PASS = "đã đạt."
EVAL_FINAL_FAIL = "chưa đạt."
EVAL_NO_FINAL = "Chưa có"
EVAL_NO_FINAL_TEXT = "Chưa có tệp kết quả đánh giá cuối cùng."
EVAL_MODEL_HEADING = "Mô hình đang dùng"
EVAL_MODEL_COLUMNS = ("Lần đo", "MAE (tỷ đồng)", "RMSE (tỷ đồng)", "R²")
EVAL_MODEL_ROWS = {
    "cv": "Kiểm định chéo 3 lần trên tập huấn luyện (dùng để chọn)",
    "validation": "Tập kiểm định",
    "test": "Tập kiểm tra (một lần)",
    "test_new": "Tập kiểm tra, bỏ tin trùng với dữ liệu huấn luyện",
}
EVAL_MODEL_SOURCE = (
    "experiments/final_selection/test_evaluation.json, "
    "models/candidates/final_v2_2026-10-20/manifest.json, experiments/ensemble_oof/blend_summary.csv"
)
EVAL_CV_HEADING = "So sánh các mô hình ứng viên"
EVAL_CV_KIND = (
    "Kết quả kiểm định chéo ở giai đoạn chọn loại mô hình, trên dữ liệu trước khi sửa và chưa có phường, đường; "
    "không so trực tiếp với mô hình đang dùng."
)
EVAL_CV_FOLDS = "Mỗi ứng viên được thử {k} lần, mỗi lần ước tính một phần của tập huấn luyện mà nó chưa được học."
EVAL_SOURCE = "Nguồn: {path}"
EVAL_MISSING = "Chưa có kết quả đánh giá. Khi nhóm lưu tệp kết quả, số liệu sẽ hiện ở đây."
EVAL_CHART_AXIS = "Sai số trung bình – MAE (tỷ đồng)"
EVAL_COLUMNS = ("Ứng viên (tên trong tệp)", "MAE (tỷ đồng)", "RMSE (tỷ đồng)", "R²")
METRIC_LABELS = {"mae": "MAE", "rmse": "RMSE", "r2": "R²"}
METRIC_HELP = (
    ("MAE", "mức lệch trung bình giữa giá ước tính và giá trong dữ liệu, tính bằng tỷ đồng. Càng thấp càng tốt."),
    ("RMSE", "giống MAE nhưng tính nặng hơn các lần lệch lớn. Càng thấp càng tốt."),
    ("R²", "phần biến động giá mà mô hình giải thích được. Càng gần 1 càng tốt."),
)

# Data and limits view
DATA_INTRO = "Mô hình học từ một bộ dữ liệu nhà ở tại Việt Nam. Dưới đây là những gì dữ liệu đó có và không có."
DATA_SOURCE = "Vietnam Housing Dataset 2024"
DATA_FACTS = {
    "source": "Bộ dữ liệu",
    "rows": "Số căn trong tập huấn luyện",
    "range": "Khoảng giá trong dữ liệu",
    "middle": "Một nửa số căn có giá",
}
DATA_RANGE = "{low} – {high} tỷ đồng"
DATA_HIST_HEADING = "Phân bố giá trong tập huấn luyện"
DATA_HIST_X = "Giá (tỷ đồng)"
DATA_HIST_Y = "Số căn"
DATA_MIDDLE_LABEL = "Một nửa số căn"  # the shaded Q1–Q3 band on the price histogram
DATA_LIMITS_HEADING = "Giới hạn cần biết"
DATA_LIMITS = (
    "Giá trong dữ liệu chưa được xác minh là giá rao bán hay giá giao dịch.",
    "Mô hình không có cơ sở để ước tính ngoài khoảng giá có trong dữ liệu.",
    "Kết quả là ước tính của mô hình, không thay cho thẩm định giá.",
    "Danh sách tỉnh, quận trong biểu mẫu chỉ gồm nơi có đủ dữ liệu huấn luyện; "
    "phường, đường và dự án chỉ gồm tên đã xuất hiện trong dữ liệu của quận đó.",
    "Khoảng một phần mười tin trong dữ liệu là tin đăng trùng, và một số tin có giá hoặc diện tích nghi ghi sai; "
    "nhóm giữ nguyên các tin này vì chưa xác minh được.",
)
DATA_MISSING_HEADING = "Thông tin thường bị thiếu trong dữ liệu"
DATA_MISSING_COLUMNS = ("Thông tin", "Tỷ lệ thiếu")
DATA_PROBLEM = "Không đọc được dữ liệu tham chiếu: {problem}"

