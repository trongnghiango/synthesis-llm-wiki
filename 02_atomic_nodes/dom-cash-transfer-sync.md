---
id: dom-cash-transfer-sync
title: Đồng bộ chuyển tiền nội bộ
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Cơ chế đồng bộ hóa bất đồng bộ thông qua Domain Event khi chuyển tiền nội bộ, tự động sinh bút toán nháp kép."
tags: [accounting, event-driven, money-transfer, journal-entry]
---

## 1. Kiến trúc & Luồng nghiệp vụ
* **Pattern**: Event-Driven Decoupled. Tách biệt hoàn toàn `CashFundService` khỏi `JournalService` để giảm thiểu liên kết chặt (tight coupling).
* **Luồng đi**: 
  1. `CashFundService.transferMoney` thực hiện chuyển tiền thành công.
  2. Phát đi `MoneyTransferredEvent` (kế thừa `IAuditableEvent` để kích hoạt audit log).
  3. `MoneyTransferListener` tiếp nhận bất đồng bộ -> Tự động sinh bút toán định khoản kép ở trạng thái `DRAFT` tại Nhật ký chung (`JournalEntry`).
* **Định khoản kế toán**:
  * **Nợ (Debit)**: Tài khoản tiền nhận (111 hoặc 112).
  * **Có (Credit)**: Tài khoản tiền gửi/đi (111 hoặc 112).

## 2. Chi tiết kỹ thuật & Khắc phục lỗi
* **Fix lỗi trôi Event (Dead-code)**: 
  * *Lỗi*: Trả trực tiếp `return this.txManager.runInTransaction(...)` khiến luồng xử lý thoát sớm, dòng phát event phía dưới không được chạy.
  * *Sửa*: Sử dụng `await this.txManager.runInTransaction(...)` để đợi transaction commit thành công rồi mới phát event ra ngoài Event Bus.
* **Xử lý biên (Edge Cases)**: 
  * Cắt còi, dừng xử lý an toàn nếu Quỹ đi hoặc Quỹ nhận không tồn tại trên hệ thống.
  * Dừng xử lý và cảnh báo nếu thiếu thiết lập tài khoản tương ứng (111/112) trong Hệ thống tài khoản kế toán (COA) để tránh lỗi toàn vẹn dữ liệu DB.
* **Tệp tin kiểm thử**:
  * Unit test dịch vụ: `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/accounting/application/services/cash-fund.service.spec.ts` (12 kịch bản).
  * Unit test listener: `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/accounting/application/listeners/money-transfer.listener.spec.ts` (Bao phủ 100% các corner-cases).