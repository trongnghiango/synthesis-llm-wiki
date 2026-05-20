# Logic Analysis: Hệ thống Quản lý Audit Log (Hoạt động Hệ thống)

Hệ thống ghi nhận và hiển thị toàn bộ lịch sử thao tác của người dùng trong hệ thống STAX, hỗ trợ giám sát real-time và phân quyền truy cập theo sơ đồ tổ chức.

## 1. Mục tiêu (Objectives)
- **Giám sát tập trung:** Một trang quản trị cho phép xem mọi hành động (Create, Update, Delete, Login, etc.)
- **Phân quyền dữ liệu (Data Scope):** 
    - Admin: Xem toàn bộ hệ thống.
    - Manager: Xem thao tác của bản thân và cấp dưới trực thuộc nhánh cây thư mục của mình.
    - Staff: Chỉ xem được thao tác của chính mình.
- **Trải nghiệm Real-time:** Dòng log mới nhất luôn hiển thị ở trên cùng, hỗ trợ polling để cập nhật liên tục.
- **Truy vết thông tin:** Link trực tiếp đến Resource liên quan (Ví dụ: Click vào ID Lead -> Mở trang chi tiết Lead).

## 2. Luồng dữ liệu (Data Flow)

### A. Backend (Cần bổ sung)
- **Endpoint:** `GET /logging/audit-logs`
- **Query Params:**
    - `page`, `limit`: Phân trang.
    - `actorId`: Lọc theo người thực hiện.
    - `resource`: Lọc theo module (leads, contracts, finotes...).
    - `action`: Lọc theo hành động (CREATE, UPDATE...).
    - `fromDate`, `toDate`: Lọc theo thời gian.
- **Logic Phân quyền (Security Filter):**
    - Service sẽ lấy `userId` từ JWT.
    - Truy vấn Employee -> Position -> OrgUnit.
    - Nếu không phải Admin, tự động thêm điều kiện `WHERE actor_id IN (subordinate_ids)`.

### B. Frontend
- **Page:** `/admin/system/audit-logs`
- **State Management:** TanStack Query với `refetchInterval` để giả lập real-time.
- **UI Components:**
    - `AuditLogGrid`: Hiển thị danh sách dạng hàng (Row-based).
    - `AuditLogFilter`: Bộ lọc nâng cao (Date range, Resource, Actor).
    - `AuditLogDetail`: Modal xem chi tiết `before` và `after` (JSON Diff).

## 3. Thiết kế giao diện (UI Design Concept)
- **Màu sắc:** Sử dụng Semantic Colors để phân biệt mức độ nghiêm trọng (Severity):
    - `INFO`: Slate/Blue.
    - `WARNING`: Amber/Orange.
    - `CRITICAL`: Red/Rose.
- **Thông tin mỗi Row:**
    - Thời gian (Relative time: "5 phút trước").
    - Actor (Avatar + Name).
    - Hành động (Badge: "Cập nhật trạng thái Lead").
    - Resource (Link: "Lead #123").
    - Nội dung thay đổi (Tóm tắt ngắn gọn).

## 4. Rủi ro & Thách thức
- **Hiệu năng:** Bảng `audit_logs` có thể phình to rất nhanh. Cần tối ưu query join với bảng Employee/User.
- **Phức tạp phân quyền:** Việc tính toán danh sách cấp dưới (descendants) mỗi khi query log có thể gây chậm. Cần cân nhắc cache danh sách `subordinate_ids`.

---
Vui lòng gõ **"OK"** để tôi tiến hành thiết kế kiến trúc (Bước 2).
