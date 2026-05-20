# Checklist Thực thi: Đồng bộ chuyển tiền nội bộ (Internal Transfer Sync)

Dưới đây là danh sách chi tiết các đầu việc đã triển khai tuần tự theo đúng quy tắc kỹ thuật và Hiến pháp của hệ thống STAX.

---

## 📋 Danh sách công việc (Checklist)

- [x] **1. Định nghĩa Domain Event**
    - Tạo file `backend/src/modules/accounting/domain/events/money-transferred.event.ts`
    - Kế thừa `IAuditableEvent` và triển khai method `toAuditEntry()`.

- [x] **2. Tích hợp EventBus vào CashFundService**
    - Cập nhật `backend/src/modules/accounting/application/services/cash-fund.service.ts`
    - Inject `IEventBus` thông qua constructor.
    - Tại hàm `transferMoney`, thực hiện phát `MoneyTransferredEvent` ngay sau khi lưu số dư và giao dịch Sổ Quỹ thành công.

- [x] **3. Xây dựng Bộ xử lý sự kiện (MoneyTransferListener)**
    - Tạo file `backend/src/modules/accounting/application/listeners/money-transfer.listener.ts`
    - Sử dụng `@EventHandler(MoneyTransferredEvent)` để lắng nghe sự kiện bất đồng bộ.
    - Tìm kiếm tài khoản kế toán dựa trên loại quỹ nguồn (`111` / `112`) và quỹ nhận (`111` / `112`).
    - Gọi `journalService.createManualEntry` để ghi nhận bút toán Nháp (`DRAFT`).

- [x] **4. Đấu nối NestJS Module**
    - Cập nhật `backend/src/modules/accounting/accounting.module.ts`
    - Khai báo `MoneyTransferListener` trong mảng `providers` để kích hoạt việc đăng ký sự kiện của EventBus.

- [x] **5. Kiểm thử Biên dịch & Unit Test**
    - Đảm bảo dự án NestJS biên dịch không có lỗi TypeScript (`npm run build:prod` hoặc `tsc`).
    - Bổ sung kịch bản Unit Test cho `CashFundService` để xác nhận event được publish chính xác khi chuyển tiền.

- [x] **6. Nghiệm thu Thực tế**
    - Chạy thử tính năng chuyển tiền từ giao diện Frontend và xác nhận số dư cập nhật.
    - Kiểm tra bảng Nhật ký chung để xác nhận bút toán Nháp (`DRAFT`) được sinh ra tự động, chính xác các tài khoản Nợ/Có.
