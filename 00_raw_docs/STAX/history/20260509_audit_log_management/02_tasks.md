# Checklist Thực thi: Hệ thống Quản lý Audit Log

Trình tự các bước triển khai tính năng Quản trị Audit Log.

## 1. Cơ sở dữ liệu & Hợp đồng (Contracts)
- [ ] Tạo `shared/contracts/system.ts`: Định nghĩa `AuditLog` interface và `auditLogQuerySchema`.
- [ ] Export `system` contract trong `shared/index.ts`.

## 2. API & Hooks
- [ ] Tạo module `client/src/modules/system/api/system.api.ts`.
- [ ] Tạo `client/src/modules/system/hooks/useAuditLogs.ts`.
- [ ] Export module `system` trong `client/src/modules/index.ts` (nếu có).

## 3. Định tuyến (Routing)
- [ ] Đăng ký route `/admin/system/audit-logs` trong file định tuyến của dự án.

## 4. Giao diện (UI Components)
- [ ] Implement trang chính `client/src/pages/admin/system/audit-logs.tsx`.
- [ ] Implement bộ lọc `AuditLogFilters.tsx`.
- [ ] Implement modal chi tiết `AuditLogDetailModal.tsx`.
- [ ] Tích hợp logic so sánh Delta (JSON/Object comparison).

## 5. Kiểm thử & Hoàn thiện
- [ ] Kiểm tra phân trang và bộ lọc.
- [ ] Kiểm tra chế độ "Live Mode" (Polling).
- [ ] Kiểm tra tính responsive trên mobile (Table scroll).
- [ ] Tạo báo cáo `03_walkthrough.md` và lưu trữ lịch sử.

---
Bạn đã sẵn sàng để tôi bắt đầu viết **CODE** chưa?
