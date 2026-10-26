# Kiểm thử ứng dụng với người dùng: kịch bản và câu hỏi

Tài liệu này trả lời góp ý của phản biện: hỏi những người sẽ dùng app xem họ có nhập được thông tin không, có hiểu khoảng giá không, khoảng rộng như hiện nay có giúp họ quyết định gì không, và họ có biết dữ liệu là năm 2024 không.

**Trạng thái:** chưa thực hiện. Khi có kết quả, nhóm ghi vào phiếu ở cuối tài liệu và cập nhật mục "Kiểm thử với người dùng" trong `reports/application_report/main.tex`. Không đưa vào báo cáo con số nào chưa đo thật.

## 1. Bốn câu hỏi cần trả lời

1. Người dùng có tự nhập được thông tin không, nhất là phường/xã, tên đường, mặt tiền và đường vào?
2. Họ có hiểu "khoảng dao động 80%" (ví dụ 7,4 – 10,3 tỷ đồng) đúng nghĩa không?
3. Khoảng rộng như hiện nay (trung bình gần 3 tỷ) có giúp họ quyết định gì không, và hẹp đến mức nào thì mới hữu ích?
4. Họ có nhận ra rằng giá được ước tính từ tin rao năm 2024 không?

## 2. Người tham gia

* 6–8 người, chia ba nhóm: người đang tìm mua nhà (3 người), chủ nhà đang hoặc sắp bán (2–3 người), môi giới (1–2 người).
* Không cần biết gì về học máy. Ưu tiên người ở các tỉnh khác nhau, không chỉ Hà Nội và TP.HCM.
* Mỗi người cần nghĩ sẵn **một căn nhà họ biết rõ** (đang ở, đang xem, hoặc đã mua/bán) và biết giá rao hoặc giá giao dịch của căn đó.
* Xin đồng ý trước khi bắt đầu. Không ghi tên, số điện thoại hay địa chỉ cụ thể của căn nhà; chỉ ghi tỉnh/quận và khoảng giá.

## 3. Chuẩn bị

* Link app trên Vercel, mở được trên điện thoại hoặc máy tính của người tham gia (để thấy họ dùng trên thiết bị quen thuộc).
* Hai người phụ trách: một người dẫn và hỏi, một người ghi chép. Mỗi buổi 20–30 phút.
* Không hướng dẫn cách dùng app. Chỉ giúp khi người tham gia bế tắc quá 1 phút, và ghi lại là đã giúp.
* Yêu cầu người tham gia vừa làm vừa nói ra suy nghĩ ("bây giờ tôi đang tìm...").

## 4. Kịch bản

### Phần A: Nhập thông tin (khoảng 8 phút)

**Nhiệm vụ:** "Hãy dùng app để ước tính giá căn nhà bạn đã nghĩ tới."

Người ghi chép theo dõi:
* thời gian từ lúc mở app đến lúc thấy kết quả;
* mục nào làm người dùng lúng túng, dừng lại hoặc hỏi;
* có tìm thấy phường/xã, tên đường trong danh sách không; nếu không thấy thì họ làm gì;
* mục nào họ để "Không rõ", và vì sao;
* các thông báo lỗi họ gặp và họ có tự sửa được không.

**Câu hỏi sau nhiệm vụ:**
1. Mục nào khó trả lời nhất? Vì sao?
2. Có thông tin nào về căn nhà mà bạn biết nhưng app không hỏi (ví dụ mặt phố hay trong ngõ, năm xây, nhà dự án hay thổ cư)?

### Phần B: Hiểu khoảng giá (khoảng 7 phút)

Chỉ vào ô "Khoảng dao động" trên màn hình kết quả.

3. "Theo bạn, khoảng này nghĩa là gì?" Ghi lại nguyên văn câu trả lời.
4. "Bạn tin con số ở giữa hay tin cả khoảng hơn? Vì sao?"
5. "Dòng 'Mô hình thường lệch bao nhiêu' nói gì với bạn?"

**Cách chấm câu 3:**
* **Đúng:** với khoảng 8/10 căn tương tự, giá thật nằm trong khoảng này. Nói cách khác, vẫn có khả năng giá nằm ngoài khoảng.
* **Sai thường gặp:** "giá chắc chắn nằm trong khoảng", "đây là giá thấp nhất/cao nhất có thể", "đây là giá ngân hàng định giá", "giá đã được thẩm định".

### Phần C: Khoảng có giúp quyết định không (khoảng 7 phút)

6. "Giả sử căn này đang rao **[một mức trong khoảng]**. Bạn sẽ làm gì với kết quả của app?"
7. "Còn nếu căn này đang rao **[một mức cao hơn đầu trên của khoảng khoảng 2 tỷ]**?"
8. "Khoảng rộng gần 3 tỷ có đủ hẹp để giúp bạn không? Hẹp đến khoảng bao nhiêu thì bạn thấy hữu ích?"
9. Chấm từ 1 (không giúp gì) đến 5 (rất hữu ích), mức độ khoảng giá giúp bạn:
   * (a) nhận ra căn rao quá cao hoặc quá thấp;
   * (b) có cơ sở để thương lượng;
   * (c) quyết định giá mua hoặc bán.
10. "Bạn muốn app cho thấy thêm gì để tin hơn (ví dụ các căn tương tự trong cùng phường, giá theo phường, lý do vì sao khoảng rộng)?"

### Phần D: Dữ liệu năm 2024 (khoảng 3 phút)

11. Hỏi trước khi nhắc tới năm: "Theo bạn, giá này dựa trên dữ liệu ở thời điểm nào?" Ghi lại họ có tự nhận ra năm 2024 không.
12. "Khi biết dữ liệu là tin rao năm 2024, bạn có dùng con số này khác đi không?"

### Phần E: Tổng kết (khoảng 3 phút)

13. Chấm từ 1 đến 5: bạn tin kết quả của app đến mức nào?
14. Bạn có dùng lại app không? Dùng trong tình huống nào?
15. Nếu chỉ được sửa một điều, bạn muốn sửa điều gì?

## 5. Chỉ số tổng hợp và mức mong muốn

| Chỉ số | Cách tính | Mức mong muốn (nhóm tự đặt, có thể chỉnh) |
|---|---|---|
| Tự nhập xong | Số người ra được kết quả mà không cần giúp / tổng số người | ≥ 80% |
| Thời gian nhập | Trung vị số phút từ lúc mở app đến lúc có kết quả | ≤ 3 phút |
| Hiểu đúng khoảng | Số người trả lời câu 3 đúng nghĩa / tổng số người | ≥ 70% |
| Khoảng hữu ích để loại giá quá xa | Trung vị điểm câu 9a | ≥ 4 |
| Khoảng hữu ích để chốt giá | Trung vị điểm câu 9c | Để biết, không đặt mức |
| Nhận ra dữ liệu năm 2024 | Số người tự trả lời đúng ở câu 11 / tổng số người | ≥ 70% |

Nếu một chỉ số dưới mức mong muốn, ghi lại các lý do người dùng nêu và đề xuất cách sửa: đổi cách diễn đạt trên app, thêm ví dụ, hoặc thu hẹp khoảng bằng mô hình tốt hơn.

## 6. Phiếu ghi cho mỗi người

| Mục | Ghi chép |
|---|---|
| Mã người tham gia | P1, P2, ... |
| Nhóm | Người mua / Chủ nhà / Môi giới |
| Thiết bị | Điện thoại / Máy tính |
| Tỉnh, quận của căn nhà | |
| Giá người đó biết (tỷ) và loại giá | Giá rao / Giá giao dịch |
| Kết quả app: giá và khoảng | |
| Thời gian nhập (phút) | |
| Có cần giúp không, giúp ở mục nào | |
| Mục lúng túng | |
| Mục để "Không rõ" | |
| Câu 3: diễn giải khoảng (nguyên văn) | Đúng / Sai |
| Câu 6–8: sẽ làm gì; độ rộng mong muốn | |
| Câu 9: điểm (a) / (b) / (c) | |
| Câu 11: tự nhận ra năm 2024 | Có / Không |
| Câu 13: điểm tin tưởng | |
| Câu 15: điều muốn sửa nhất | |

## 7. Cách đưa kết quả vào báo cáo

* Bảng chỉ số ở mục 5, ghi rõ số người tham gia trong từng nhóm.
* Ba đến năm phát hiện quan trọng nhất, mỗi phát hiện kèm một câu nói nguyên văn của người tham gia.
* Các thay đổi đã làm trên app sau buổi kiểm thử, hoặc lý do chưa làm.
* So sánh giá người tham gia biết với giá app ước tính là thông tin tham khảo; với 6–8 căn thì không đủ để đánh giá độ chính xác của mô hình.
