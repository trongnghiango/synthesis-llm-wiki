# 🛠️ Refactoring & Implementation Plan: Audit Log System

Dựa trên bản blueprint đã thống nhất, đây là lộ trình triển khai chi tiết.

## P1: Hạ tầng (Critical Fixes & Infrastructure)

### 1. Tối ưu OrgUnit cho Hierarchical Query
- **Mục tiêu:** Tránh đệ quy khi tìm log của cấp dưới.
- **Hành động:** 
    - Thêm cột `path` (varchar) vào bảng `organizations`.
    - Viết script đồng bộ `path` dựa trên `parent_id` (ví dụ: `1.5.10`).

### 2. Cấu hình Event Bus
- **Mục tiêu:** Đảm bảo ghi log không làm chậm request chính.
- **Hành động:** Sử dụng `setImmediate` hoặc `EventEmitter2` trong `EventBusModule` để chạy task ở background.

---

## P2: Lõi Module Audit Log (Core Implementation)

### 3. Khởi tạo Module `audit-log`
- **Vị trí:** `src/modules/logging/audit-log/`.
- **Thành phần:**
    - `AuditLog` Entity & Domain Model.
    - `IAuditLogRepository` (Interface).
    - `DrizzleAuditLogRepository` (Postgres implementation).

### 4. Cơ chế Capture (Non-invasive Logging)
- **Mục tiêu:** Ghi log mà không sửa code Service.
- **Hành động:** 
    - Tạo `@AuditLog(action, resource)` Decorator.
    - Tạo `AuditLogInterceptor` để bắt dữ liệu `before` và `after`.
    - Hoặc sử dụng `Domain Events` nếu Service đã phát tán sự kiện.

---

## P3: API & Phân quyền dữ liệu (Query Layer)

### 5. Audit Log Query Service
- **Mục tiêu:** Trả về danh sách log theo đúng phân quyền.
- **Logic:**
    - Nếu là Admin: `SELECT *`.
    - Nếu là Manager: `SELECT * WHERE organization_id IN (subordinates)`. (Sử dụng Materialized Path để lấy list IDs).
    - Nếu là Staff: `SELECT * WHERE actor_id = current_user_id`.

---

## P4: Frontend (UI Implementation)

### 6. Audit Log Dashboard
- **Trang:** `/admin/system/audit-logs`.
- **Tính năng:**
    - List view với server-side pagination.
    - Filter theo Actor, Resource, Date.
    - Modal xem chi tiết JSON Diff (sử dụng thư viện hiển thị code/json).

---

## 🏗️ Kiểm tra sau thực hiện (Verification)
- [ ] Chạy `npx tsc --noEmit` để đảm bảo không lỗi type.
- [ ] Test hiệu năng: Ghi 1000 logs liên tục xem server có bị treo không.
- [ ] Test phân quyền: Staff không được xem log của Manager.
