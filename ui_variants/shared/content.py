"""All interface copy, shared word for word by every variant.

Vietnamese strings are proposed copy and need review by the team.
"""

# Working title only. The product name is undecided (brief OD-9).
TITLE = "Ước tính giá nhà"
LEAD = (
    "Nhập thông tin căn nhà để nhận mức giá ước tính từ mô hình. "
    "Đây là con số tham khảo, không phải kết quả thẩm định."
)

NAV = ("Ước tính giá", "Độ chính xác của mô hình", "Dữ liệu và giới hạn")
VIEW_IDS = ("uoc-tinh", "do-chinh-xac", "du-lieu")

FORM_HEADING = "Thông tin căn nhà"
REQUIRED_LEGEND = "* Mục bắt buộc"
SUBMIT = "Ước tính giá"
RESET = "Nhập lại"
RETRY = "Thử lại"
DISABLED_REASON = "Nút ước tính tạm khoá vì mô hình chưa sẵn sàng."
RANGE_HELP = "Mô hình đã học: {low} – {high}{unit}"

# System banners
BANNER_PREVIEW = "Chế độ xem trước giao diện — các con số là dữ liệu mẫu, không phải kết quả dự đoán."
BANNER_UNAVAILABLE = "Mô hình chưa sẵn sàng. Ứng dụng chưa thể ước tính giá."

# Validation
SUMMARY_HEADING = "Chưa thể ước tính. Vui lòng kiểm tra {n} mục sau:"

# Result panel
RESULT_LABEL = "Giá ước tính"
PRICE_UNIT = "tỷ đồng"
SAMPLE_TAG = "Dữ liệu mẫu"
REAL_TAG = "Kết quả từ mô hình"
SAMPLE_STATEMENT = (
    "Con số trên là dữ liệu mẫu để xem bố cục. Nó không thay đổi theo thông tin bạn nhập "
    "và không phải kết quả dự đoán."
)
REAL_STATEMENT = (
    "Đây là mức giá do mô hình ước tính từ dữ liệu, "
    "không phải giá thẩm định hay giá giao dịch."
)
UNCERTAINTY_LABEL = "Khoảng dao động"
UNCERTAINTY_NONE = "Chưa có"
UNCERTAINTY_NONE_TEXT = (
    "Mô hình chưa có khoảng ước lượng được hiệu chỉnh nên ứng dụng không hiển thị khoảng giá."
)
UNCERTAINTY_INTERVAL = "{low} – {high} tỷ đồng"
UNCERTAINTY_INTERVAL_TEXT = "Khoảng ước lượng {coverage} lấy từ bước hiệu chỉnh của mô hình."
RECAP_LABEL = "Dựa trên thông tin bạn nhập"
UNKNOWN_NONE = "Không có mục nào để «Không rõ»."
UNKNOWN_SOME = "{n} mục để «Không rõ»: {names}."
PROVENANCE_LABEL = "Nguồn kết quả"
PROVENANCE_SAMPLE = (
    "Dữ liệu mẫu: trung vị giá của {n} căn trong tập huấn luyện. Không có mô hình nào được gọi."
)
PROVENANCE_UNKNOWN = "Không có thông tin phiên bản mô hình."
STALE = "Thông tin đã thay đổi sau lần ước tính này. Chọn «Ước tính giá» để cập nhật."

STATE_TEXT = {
    "initial": ("Chưa có kết quả", "Điền thông tin căn nhà rồi chọn «Ước tính giá»."),
    "invalid": ("Chưa thể ước tính", "Vui lòng kiểm tra các mục được đánh dấu trong biểu mẫu."),
    "fixed": ("Chưa có kết quả", "Các mục đã hợp lệ. Chọn «Ước tính giá» để tiếp tục."),
    "unavailable": (
        "Mô hình chưa sẵn sàng",
        "Hiện chưa thể ước tính giá vì mô hình chưa được tải lên hệ thống. "
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
SIMULATED_NOTE = "Trạng thái mô phỏng để xem giao diện. Không có mô hình nào được gọi."

# Model accuracy view
EVAL_INTRO = (
    "Trang này chỉ hiển thị số liệu đọc trực tiếp từ tệp kết quả của nhóm. "
    "Chưa có mô hình nào được chốt để dùng trong ứng dụng."
)
EVAL_NO_FINAL_LABEL = "Đánh giá cuối cùng trên tập kiểm tra"
EVAL_NO_FINAL = "Chưa có"
EVAL_NO_FINAL_TEXT = "Nhóm chưa chạy đánh giá cuối cùng, nên chưa có con số nào về độ chính xác khi dùng thật."
EVAL_CV_HEADING = "Kết quả kiểm định chéo"
EVAL_CV_KIND = (
    "Kết quả kiểm định chéo trên tập huấn luyện, dùng để chọn mô hình — chưa phải đánh giá cuối cùng."
)
EVAL_CV_FOLDS = "Mỗi ứng viên được kiểm định chéo {k} phần."
EVAL_BEST = "Ứng viên có sai số thấp nhất trong kiểm định chéo: {model}."
EVAL_SOURCE = "Nguồn: {path}"
EVAL_MISSING = "Chưa có kết quả đánh giá. Khi nhóm lưu tệp kết quả, số liệu sẽ hiện ở đây."
EVAL_CHART_AXIS = "MAE kiểm định chéo (tỷ đồng)"
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
DATA_LIMITS_HEADING = "Giới hạn cần biết"
DATA_LIMITS = (
    "Giá trong dữ liệu chưa được xác minh là giá rao bán hay giá giao dịch.",
    "Mô hình không có cơ sở để ước tính ngoài khoảng giá có trong dữ liệu.",
    "Kết quả là ước tính của mô hình, không thay cho thẩm định giá.",
    "Danh sách tỉnh, quận trong biểu mẫu chỉ gồm nơi có đủ dữ liệu huấn luyện.",
)
DATA_MISSING_HEADING = "Thông tin thường bị thiếu trong dữ liệu"
DATA_MISSING_COLUMNS = ("Thông tin", "Tỷ lệ thiếu")
DATA_PROBLEM = "Không đọc được dữ liệu tham chiếu: {problem}"

# Used by the concepts that show the journey or put several scopes on one screen
WORKFLOW = ("Nhập thông tin", "Kiểm tra", "Kết quả")
CHECK_HEADING = "Kiểm tra"
CHECK_REQUIRED_OK = "Đã đủ {n}/{n} mục bắt buộc."
CHECK_REQUIRED_MISSING = "Còn thiếu {k}/{n} mục bắt buộc: {names}."
SCOPE_NOTE = {
    "uoc-tinh": "Con số cho riêng căn nhà bạn nhập.",
    "do-chinh-xac": "Số liệu về mô hình nói chung, không phải về căn nhà này.",
    "du-lieu": "Mô tả dữ liệu mà mô hình đã học.",
}
BEST_CAPTION = "Ứng viên {model}, kiểm định chéo"

# Questions and answers built only from facts in the repository (used by design_05)
FAQ = (
    ("Giá ước tính là giá rao bán hay giá giao dịch?",
     "Chưa xác định. Nhóm chưa xác minh dữ liệu là giá rao bán hay giá giao dịch, "
     "nên con số không được gọi là giá giao dịch."),
    ("Vì sao chưa có khoảng dao động?",
     "Mô hình chưa có khoảng ước lượng được hiệu chỉnh. Dữ liệu có sẵn một tập hiệu chỉnh "
     "(calibration) nhưng nhóm chưa dùng đến."),
    ("Độ chính xác của mô hình đã được kiểm tra chưa?",
     "Mới có kết quả kiểm định chéo trên tập huấn luyện, dùng để chọn mô hình. "
     "Chưa có đánh giá cuối cùng trên tập kiểm tra."),
    ("Biểu mẫu hỗ trợ những khu vực nào?",
     "Chỉ những cặp tỉnh – quận có ít nhất {min_rows} căn trong dữ liệu huấn luyện: "
     "{offered} cặp, tại {cities} tỉnh / thành phố."),
)
