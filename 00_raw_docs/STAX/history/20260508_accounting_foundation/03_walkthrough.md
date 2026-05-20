# Walkthrough: Accounting Foundation (Phase 1)

## Những gì đã hoàn thành
Chúng ta đã xây dựng xong "Xương sống" cho hệ thống kế toán STAX ERP, cho phép quản lý tài chính theo chuẩn ghi sổ kép.

### 1. Database Schema
- [x] `accounts`: Hệ thống tài khoản (COA) với hỗ trợ cây (parentId) và truy vấn nhanh (Materialized Path).
- [x] `journal_entries` & `journal_items`: Bộ lưu trữ bút toán Nhật ký chung và Sổ cái, đảm bảo nguyên tắc sổ kép.

### 2. Domain Logic
- [x] **Account Entity**: Quản lý thông tin tài khoản.
- [x] **JournalEntry Entity**: Chứa logic kiểm tra cân bằng (Tổng Nợ = Tổng Có) và quy trình Ghi sổ (Post).
- [x] **Invariants**: Đảm bảo một bút toán phải có ít nhất 2 dòng định khoản và phải cân bằng mới được phép Post.

### 3. Application & Integration
- [x] **AccountService**: Khởi tạo COA mẫu (Thông tư 133/200) và quản lý cây tài khoản.
- [x] **JournalService**: Hỗ trợ tạo bút toán thủ công và tự động.
- [x] **Finote Integration**: Lắng nghe sự kiện `PaymentAllocatedEvent` để tự động sinh bút toán DRAFT khi Finote được thanh toán đầy đủ (`PAID`).

### 4. API Endpoints
- `GET /api/accounting/accounts`: Lấy danh sách COA.
- `POST /api/accounting/accounts/initialize`: Khởi tạo dữ liệu mẫu.
- `POST /api/accounting/journal-entries`: Tạo bút toán thủ công.
- `PATCH /api/accounting/journal-entries/:id/post`: Ghi sổ chính thức.

## Kết quả Verification
- **Build**: `npx tsc --noEmit` thành công ✅.
- **Database**: Đã được đồng bộ schema thông qua `drizzle-kit push`.
- **Logic**: Các ràng buộc về Nợ/Có đã được cài đặt chặt chẽ tại tầng Domain.

---
**Trạng thái**: Hoàn thành. Thư mục context này sẽ được di chuyển sang `history/`.
