# Database Schema Optimization Audit (2026-05-08)

## 1. Tổng quan
Đợt tối ưu hóa này nhằm mục đích giải quyết các vấn đề về đặt tên không đồng nhất, lỗi mapping quan hệ, và chuẩn bị hạ tầng cho Multi-tenancy.

## 2. Các thay đổi chi tiết

### Phase 1: Chuẩn hóa & Hiệu suất
- **Naming Convention**: Toàn bộ field trong `quotes.schema.ts` chuyển sang `camelCase`. Cập nhật `DrizzleQuoteRepository` để khớp.
- **Actor Accuracy**: `attachments.uploadedById` đổi từ `employees` sang `users` (Actor thực sự đăng nhập).
- **Accounting Performance**: Thêm 5 composite indexes vào bảng `finotes` (`status`, `source_org_id`, `requested_by_id`, `deadline_at`, `type`).
- **Data Integrity**: Thêm Foreign Key `manager_id` -> `employees.id` với `onDelete: 'set null'`.

### Phase 2: Refactoring Kiến trúc
- **Unified Attachments**: Hợp nhất `finote_attachments` vào bảng `attachments` dùng chung. Thêm `category` (enum) và `tags` (text) để phân loại đa năng.
- **Lead Assignment (Option B+)**: Thêm `assignedEmployeeId` vào `leads` để gán việc trực tiếp, đồng thời giữ `assignedPositionId` cho báo cáo phòng ban.
- **HRM Foundation**: Tạo bảng `employee_tasks` làm nền tảng cho quản lý công việc.

### Sửa lỗi Seeder & Multi-tenant
- **Issue**: Lỗi `ON CONFLICT` trong Seeder do thiếu unique constraint sau khi gỡ bỏ unique global.
- **Fix**:
    - Thêm `uniqueIndex` trên `(organization_id, code)` cho `locations`, `grades`.
    - Thêm `uniqueIndex` trên `(organization_id, name)` cho `job_titles`.
    - Cập nhật `DrizzleOrgStructureRepository` và `CompanyImportService` để truyền `organizationId`.

## 3. Technical Debt Resolved
- Khắc phục lỗi `TS2488` trong `DrizzleEmployeeRepository` bằng cách thay đổi cách destructuring kết quả `.returning()` của Drizzle.

## 4. Trạng thái Database
Database đã được đồng bộ thủ công bằng script `quick-fix.ts` để đảm bảo khớp hoàn toàn với Code mà không bị lỗi TTY của `drizzle-kit`.

---
**Người thực hiện**: Antigravity AI
**Trạng thái**: ✅ Hoàn thành
