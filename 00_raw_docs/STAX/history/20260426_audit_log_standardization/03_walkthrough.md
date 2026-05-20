# 03 Walkthrough: Audit Log, Naming Standardization & Activity Feed (2026-04-26)

Tài liệu này tổng hợp các thay đổi quan trọng trong ngày 26/04/2026, tập trung vào việc hoàn thiện hạ tầng giám sát và chuẩn hóa mã nguồn.

---

## 1. Hoàn tất kiến trúc AuditLog (Nhật ký hành động)

### Tổng quan
Triển khai hệ thống ghi nhật ký hành động toàn diện cho các luồng nghiệp vụ chính, sử dụng `DrizzleAuditLogService` với cơ chế Fire-and-forget.

### Kết quả:
- ✅ **Bảng `audit_logs`**: Đã được tạo và index đầy đủ.
- ✅ **Service**: Thực thi `AUDIT_LOG_PORT` thành công.
- ✅ **Tích hợp**: Đã áp dụng cho Lead Won, Payment Allocated, Role Assigned, và User Provisioned.

---

## 2. Chuẩn hóa Naming (Snake_case to CamelCase)

### Tổng quan
Chiến dịch refactoring quy mô lớn để loại bỏ hoàn toàn sự rò rỉ của `snake_case` từ Database lên tầng Application/Infrastructure.

### Thay đổi chính:
- Cập nhật toàn bộ Drizzle Schemas để map `snake_case` (DB) sang `camelCase` (TS).
- Sửa lỗi hàng ngàn biến rò rỉ trong Controller, DTO, Mappers và Unit Tests.
- Kết quả: **0 lỗi TypeScript**, hệ thống chạy ổn định 100%.

---

## 3. Triển khai Omnichannel Activity Feed

### Tổng quan
Hệ thống dòng thời gian hội tụ, cho phép xem cả log hệ thống tự động và ghi chú tương tác thủ công của nhân viên trên cùng một timeline của Tổ chức.

### Thành phần mới:
- `interaction-notes`: Bảng lưu trữ ghi chú cuộc gọi/họp.
- `ActivityFeedService`: Logic hội tụ dữ liệu từ 2 nguồn.
- `GET /organizations/:orgId/timeline`: API endpoint phục vụ giao diện Timeline.

---

## 4. Unified Onboarding Automation

### Tổng quan
Tự động hóa các hành động khi một khách hàng mới được kích hoạt (onboarded), bao gồm gửi thông báo và thiết lập dữ liệu ban đầu.

---
*Tổng hợp từ các file walkthrough cũ ngày 26/04/2026.*
