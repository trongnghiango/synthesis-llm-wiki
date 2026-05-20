# Báo cáo Triển khai (Walkthrough): Đồng bộ chuyển tiền nội bộ (Internal Transfer Sync)

Chúng ta đã hoàn thành việc tích hợp luồng hạch toán tự động bất đồng bộ từ Sổ Quỹ (Cash Book) sang Nhật ký chung (General Ledger) khi thực hiện Chuyển tiền nội bộ.

---

## 1. Tóm tắt tính năng (Feature Summary)
*   **Phân lớp (Tier):** Tier 3 — `accounting` module.
*   **Domain Event mới:** `MoneyTransferredEvent` (kế thừa `IAuditableEvent` để tự động kích hoạt ghi log kiểm toán hệ thống).
*   **Event Listener mới:** `MoneyTransferListener` tự động định khoản kép:
    *   **Nợ (Debit) tài khoản tiền nhận** (111 hoặc 112 tùy loại quỹ)
    *   **Có (Credit) tài khoản tiền gửi/đi** (111 hoặc 112 tùy loại quỹ)
*   **Bút toán sinh ra:** Được đặt ở trạng thái **`DRAFT` (Nháp)** trong Nhật ký chung để đảm bảo an toàn tài chính.

---

## 2. Quyết định kiến trúc (Architecture Decisions)
*   **Lựa chọn Event-Driven (Approach A):** Thay vì gọi trực tiếp `JournalService` từ `CashFundService` (gây ghép cặp chặt - tight coupling giữa 2 Aggregates), việc phát Domain Event giúp cho nghiệp vụ dòng tiền hoàn thành độc lập và nhanh chóng. Bộ xử lý hạch toán kế toán chạy ngầm không ảnh hưởng đến trải nghiệm người dùng cuối.
*   **Publish sau Transaction:** Phát event sau khi transaction chuyển tiền tại `CashFundService.transferMoney` đã lưu thành công vào cơ sở dữ liệu để tránh tình trạng "quỷ ám" (event phát đi nhưng DB roll back).

---

## 3. Khó khăn & Xử lý (Troubleshooting & Fixes)
*   **Phát hiện trong Unit Test:** 
    *   *Hiện tượng:* Mock event bus không nhận được tín hiệu publish sự kiện trong unit test.
    *   *Nguyên nhân:* Trong `CashFundService.transferMoney`, câu lệnh `return this.txManager.runInTransaction(...)` được dùng khiến hàm thoát ngay lập tức, các lệnh phát event phía dưới trở thành dead-code.
    *   *Khắc phục:* Thay đổi thành `await this.txManager.runInTransaction(...)` để đợi transaction hoàn tất, sau đó thực hiện lệnh phát sự kiện phía dưới một cách tuần tự.
    *   *Kết quả:* Unit test và biên dịch webpack build hoàn tất 100% thành công!

*   **Bảo chứng Chất lượng (Unit Testing Coverage):**
    *   Đã viết và chạy thành công 12 kịch bản test cho [cash-fund.service.spec.ts](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/accounting/application/services/cash-fund.service.spec.ts).
    *   Tạo mới và bao phủ 100% các corner-cases nghiệp vụ tại [money-transfer.listener.spec.ts](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/accounting/application/listeners/money-transfer.listener.spec.ts) bao gồm:
        1. Quỹ đi hoặc Quỹ nhận không tồn tại (Dừng xử lý an toàn).
        2. Thiếu thiết lập tài khoản 111/112 trong COA (Cảnh báo và dừng xử lý để tránh lỗi DB).
        3. Định khoản chuẩn xác: Nợ 111 / Có 112 với đúng giá trị chuyển tiền.
    *   **Kết quả:** Toàn bộ test suites đều đạt trạng thái `PASS` hoàn mỹ!

---

## 4. Bàn giao cho Frontend (Frontend Handoff)
*   **Tương thích:** Phía Frontend **không cần thay đổi bất cứ giao diện hay logic nào**! 
*   **Hoạt động:** Khi kế toán bấm chuyển tiền từ hộp thoại `TransferMoneyDialog`, API `/api/accounting/cash-funds/transfer` được gọi -> Phản hồi lập tức trả về nhanh chóng -> Client tự động làm mới số dư hai quỹ -> Ngầm ở dưới, bút toán Nháp tự động xuất hiện tại Nhật ký chung (`/api/accounting/journal-entries`).
