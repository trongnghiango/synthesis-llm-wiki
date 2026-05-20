# Logic Analysis: Standardizing Accounting Counterparty (Đối tượng kế toán)

## Mục đích
Tính năng này nhằm giải quyết sự nhầm lẫn giữa **Chủ thể (Tenant/Owner)** và **Đối tượng (Counterparty/Party)** trong module Accounting. 
Hệ thống cần một cơ chế "bài bản" để định danh bất kỳ đối tượng nào tham gia vào giao dịch tài chính (Khách hàng, Nhà cung cấp, Nhân viên) mà không làm phá vỡ kiến trúc Clean Architecture.

**Tier:** 2 (Application & Domain Logic)

## Yêu cầu phi chức năng (NFR)
- **Ràng buộc toàn vẹn (Referential Integrity):** Liên kết chặt chẽ với bảng `organizations` và `employees`.
- **Bảo mật Tenancy:** Luôn lọc dữ liệu theo `tenantId` để tránh lộ thông tin giữa các công ty.
- **Hiệu năng:** Tối ưu hóa các phép JOIN trong API danh sách (List View).
- **Tính Audit:** Thông tin đối tượng tại thời điểm ký phiếu cần được ghi nhận chính xác.

## Tác động (Impact)
- **Database:** Cập nhật bảng `finotes` để hỗ trợ đa đối tượng (Polymorphic-like reference).
- **Domain:** Refactor thực thể `Finote` để sử dụng Unified Party Model.
- **Infrastructure:** Cập nhật `DrizzleFinoteRepository` để xử lý logic JOIN phức hợp.
- **Application:** Cập nhật `FinoteService` để gán đối tượng từ nhiều nguồn (Lead, Contract, Payroll).

## Open Questions
1. **Đối tượng vãng lai:** Chúng ta có cần hỗ trợ các đối tượng không nằm trong hệ thống (không có ID trong `organizations` hay `employees`) không? (Ví dụ: Chi tiền mua trà đá, không có hồ sơ NCC).
2. **Cấu trúc DTO:** Bạn muốn nhận một object `party` gộp chung hay các trường riêng biệt (`partnerName`, `partnerType`) để dễ xử lý logic hiển thị?

---
*Dừng lại để thảo luận. Hãy xác nhận phân tích này đã chính xác ý đồ của bạn chưa?*
