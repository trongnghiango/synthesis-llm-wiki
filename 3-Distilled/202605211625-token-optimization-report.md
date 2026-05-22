---
id: 202605211625-token-optimization-report
aliases:
  - "Distilled: Báo cáo Tối ưu hóa Token Đồng bộ Tri thức STAX"
tags:
  - distilled
  - insight
  - optimization
  - token-saving
date: 2026-05-21
---

# Báo Cáo Tối Ưu Hóa Chi Phí Token Trong Quy Trình Đồng Bộ Tri Thức STAX

## 1. Vấn đề tiêu thụ Token nghiêm trọng trước tối ưu hóa

Trước khi tiến hành cải tiến, quy trình đồng bộ tự động tài liệu từ dự án STAX_ASP sang wiki gặp phải hiện tượng liên tục gọi API Claude để sinh lại (regenerate) các nốt nguyên tử mặc dù nội dung thô (raw) không hề có thay đổi logic. Nguyên nhân xuất phát từ sự thiếu đồng bộ giữa tên thư mục thô và tên tệp tin nốt nguyên tử vật lý:

* **Bất đồng bộ ký tự phân tách:** Thư mục thô sử dụng dấu gạch dưới (ví dụ: `crm_analytics_service`), trong khi nốt nguyên tử vật lý sử dụng dấu gạch ngang (`dom-crm-analytics-service.md`).
* **Bất đồng bộ ngữ nghĩa ID:** AI khi viết nốt nguyên tử tự động đặt ID tối ưu hơn (ví dụ: `arch-audit-log-decoupling.md` thay vì tên gốc `arch-architecture-audit-auditlog.md`).

Khi file `sync_state.json` bị mất hoặc đặt lại trong quá trình làm việc, hệ thống hoàn toàn không thể nhận diện các nốt nguyên tử đã được tạo trước đó trên ổ đĩa. Do đó, script tự động quét và coi chúng là các chuyên đề mới, liên tục gửi yêu cầu API lên Claude, gây lãng phí chi phí token rất lớn.

---

## 2. Chiến lược Tối ưu hóa & Giải pháp Kỹ thuật

Quy trình đồng bộ đã được nâng cấp toàn diện bằng cách kết hợp hai giải pháp: **Nhận diện vật lý thông minh** và **Kiểm soát quyền quyết định gọi AI**.

### Giải pháp 1: Chuẩn hóa đường dẫn và Quét siêu dữ liệu vật lý (Robust Physical Match)
Thay vì so sánh chuỗi đơn giản dựa trên tên tệp tin thô, hàm kiểm tra đã được cải tiến để:
* Chuẩn hóa toàn bộ dấu gạch dưới `_` thành gạch ngang `-` khi đối chiếu tiền tố tên file vật lý.
* Đọc nhanh 1000 ký tự đầu tiên (vùng Frontmatter) của các nốt nguyên tử hiện có trên ổ đĩa nhằm tìm kiếm sự xuất hiện của `slug` nguyên bản hoặc `normalized_slug`. 

*Kết quả:* Kể cả khi file cache `sync_state.json` bị xóa hoàn toàn, script vẫn nhận diện chính xác 100% các nốt đã số hóa thành công, đạt tỉ lệ cache hit tuyệt đối cho các tệp thô chưa sửa đổi.

### Giải pháp 2: Kết hợp Tham số dòng lệnh và Xác nhận tương tác (CLI Skips & Prompting)
Đối với những trường hợp tệp thô thực sự có thay đổi nhưng chỉ là sửa đổi rất nhỏ (sửa lỗi chính tả, chỉnh dấu câu, thêm khoảng trắng), việc sinh lại toàn bộ nốt nguyên tử bằng AI là không cần thiết. Hệ thống cung cấp hai cơ chế bổ trợ:

1. **Tham số dòng lệnh `--skip-ai`:**
   * Cho phép bỏ qua toàn bộ việc gọi AI bằng tham số: `python3 scripts/sync_stax_docs.py --skip-ai all`
   * Hoặc bỏ qua các module cụ thể: `python3 scripts/sync_stax_docs.py --skip-ai crm_analytics_service`
   * Hệ thống sẽ bỏ qua việc sinh AI nhưng vẫn lưu mã băm mới nhất của thư mục thô vào `sync_state.json` để đồng bộ trạng thái.

2. **Xác nhận tương tác (Interactive Prompt):**
   * Nếu chạy lệnh mặc định không có tham số, khi phát hiện thay đổi ở các thư mục đã được số hóa trước đó, script sẽ tạm dừng và hỏi người dùng:
     `[?] Phát hiện thay đổi tại {slug}. Bạn có muốn gọi AI để cập nhật lại nốt nguyên tử? (y/N):`
   * Nếu người dùng chọn `y` (Yes), AI sẽ thực hiện cập nhật.
   * Nếu chọn `n` (No) hoặc nhấn Enter, AI sẽ bị bỏ qua và mã băm mới vẫn được cập nhật vào cache để tránh hỏi lại ở các phiên tiếp theo.

---

## 3. Đánh giá hiệu quả kinh tế và vận hành

| Chỉ số đánh giá | Trước tối ưu hóa | Sau tối ưu hóa | Hiệu quả cải thiện |
| :--- | :--- | :--- | :--- |
| **Token tiêu thụ khi chạy lại (Không sửa raw)** | ~25.000 - 50.000 tokens / lượt | 0 tokens | Tiết kiệm **100%** |
| **Token tiêu thụ khi sửa đổi raw nhỏ** | ~5.000 - 10.000 tokens / file | 0 tokens (chọn Skip/No) | Tiết kiệm **100%** |
| **Độ chính xác nhận diện tệp** | Thấp (Dễ bị blind khi reset cache) | Tuyệt đối (Khớp vật lý và nội dung) | Loại bỏ hoàn toàn trùng lặp |
| **Kiểm soát chi phí gọi AI** | Tự động hoàn toàn (Không kiểm soát) | Chủ động qua CLI & Interactive | Người dùng nắm toàn quyền quyết định |
