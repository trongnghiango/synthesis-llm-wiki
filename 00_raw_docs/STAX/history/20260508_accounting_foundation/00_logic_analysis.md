# Logic Analysis: Accounting Foundation (Phase 1)

## 1. Mục tiêu (Goals)
Xây dựng nền tảng kế toán ghi sổ kép (Double-Entry Bookkeeping) cho STAX ERP. Chuyển đổi từ mô hình quản lý thu chi đơn lẻ sang mô hình hạch toán kế toán chuyên nghiệp, hỗ trợ báo cáo tài chính trong tương lai.

- **Vị trí Tier**: Tier 3 (Domain/Business Module).
- **Phạm vi**: Hệ thống tài khoản (COA), Nhật ký chung (Journal Entries), Bút toán chi tiết (Journal Items), và tích hợp tự động với Finote.

## 2. Ràng buộc nghiệp vụ (Business Rules)

### A. Nguyên tắc Ghi sổ kép
- Mọi giao dịch (`JournalEntry`) phải bao gồm ít nhất 2 định khoản (`JournalItem`).
- **Ràng buộc cứng**: Tổng số tiền Nợ (Debit) phải luôn bằng Tổng số tiền Có (Credit). Nếu không bằng, hệ thống phải từ chối ghi sổ (Ném `BusinessRuleValidationException`).

### B. Hệ thống tài khoản (COA)
- Quản lý theo cấu trúc cây (Parent-Child). 
- Multi-tenancy: Mỗi Organization có bộ tài khoản riêng (có thể kế thừa từ Template).
- Các tài khoản hệ thống (VD: 111 - Tiền mặt) không được phép xóa để đảm bảo các tiến trình tự động không bị gãy.

### C. Tích hợp Finote
- Khi Finote đạt trạng thái `PAID`, hệ thống sẽ tự động kích hoạt tiến trình hạch toán.
- Việc hạch toán tự động cần linh hoạt: Ghi sổ trực tiếp hoặc tạo bản nháp (Draft) tùy cấu hình hệ thống.

## 3. Tác động hệ thống (System Impact)

- **Database**: Thêm các bảng `accounts`, `journal_entries`, `journal_items`.
- **Module Communication**: `Accounting` module sẽ lắng nghe sự kiện `FinoteStatusChangedEvent` từ module kế toán (hoặc gọi trực tiếp qua service nếu cùng module, nhưng nên qua EventBus để đảm bảo Decoupling).
- **Multi-tenancy**: Mọi truy vấn phải bao gồm `organizationId`.

## 4. Open Questions

1. **Sub-accounting (Chi tiết đối tượng)**: Trong Phase 1, chúng ta có cần hạch toán chi tiết cho từng Khách hàng/Nhà cung cấp (Account Receivable/Payable) hay chỉ ghi nhận vào tài khoản tổng (131/331)? 
   - *Đề xuất*: Phase 1 tập trung vào COA tổng quát, chi tiết đối tượng sẽ được lưu trong `referenceId` của Journal Entry.

2. **Cơ chế hạch toán từ Finote**: Nên để hệ thống tự động "Post" (Ghi sổ) ngay lập tức hay tạo `JournalEntry` ở trạng thái `DRAFT` để kế toán kiểm tra lại?
   - *Đề xuất*: Tạo `DRAFT` Journal Entry để đảm bảo tính an toàn và quy trình kiểm soát (Review process).

---
**Trạng thái**: Đang chờ xác nhận từ User (Sync).
