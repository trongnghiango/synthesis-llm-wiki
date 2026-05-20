# Implementation Plan: Hệ thống Quản lý Audit Log

Kế hoạch triển khai giao diện quản trị lịch sử hoạt động hệ thống dựa trên API `/api/system/audit-logs`.

## 1. Shared Contracts (Zod & Interfaces)
Tạo file `shared/contracts/system.ts`:
- `AuditLog` interface: Khớp với response từ backend.
- `auditLogQuerySchema`: Schema cho bộ lọc (pagination, dates, resource, action, severity).

## 2. API Client Integration
Tạo module `client/src/modules/system`:
- `system.api.ts`: 
    - `getAuditLogs(params: AuditLogQueryParams)`: Gọi API lấy danh sách log.
- `system.hooks.ts`:
    - `useAuditLogs(params)`: Hook sử dụng `useQuery`.

## 3. Component Architecture
- **Page Component:** `client/src/pages/admin/system/audit-logs.tsx`
    - Quản lý state của bộ lọc.
    - Tích hợp `DataGrid` để hiển thị danh sách.
- **Filter Component:** `AuditLogFilters`
    - Các field: DatePicker (Range), Select (Severity), Select (Resource), Search (Actor).
- **Detail Component:** `AuditLogDetailModal`
    - Hiển thị thông tin chi tiết của một log entry.
    - Hiển thị so sánh `before` vs `after` sử dụng định dạng JSON đẹp mắt hoặc Diff view đơn giản.

## 4. State & Real-time (Polling vs WebSocket)
- **Quyết định:** Sử dụng **Polling (TanStack Query refetchInterval)** cho bản MVP.
- **Lý do:** 
    - API hiện tại là RESTful, việc thêm WebSocket yêu cầu thay đổi lớn ở cả Gateway Backend và logic sync ở Frontend.
    - Audit Log không yêu cầu độ trễ cực thấp (sub-second). Polling mỗi 30-60s là đủ để giám sát (Monitor) mà không gây áp lực lên server.
- **Triển khai:** Thêm chế độ "Live Mode" (Toggle) để kích hoạt `refetchInterval: 30000` (30 giây).

## 5. UI/UX Detail
- Cột **Severity**: Badge màu (Blue, Amber, Red).
- Cột **Action**: Hiển thị nhãn thân thiện (Ví dụ: `LEAD.CREATED` -> "Tạo Lead mới").
- Cột **Resource ID**: Link thông minh (Nếu là `leads` thì link đến `/admin/crm/leads/$id`).

---
Thiết kế này đã chuẩn chưa? Nếu OK, tôi sẽ xuất Checklist (Bước 3).
