# 03 Walkthrough: Professional API & System Integration (2026-04-28)

Tài liệu này tổng hợp các thay đổi trong ngày 28/04/2026, tập trung vào việc chuyên nghiệp hóa lớp Application và Infrastructure của `SystemModule`.

---

## 1. Tái cấu trúc System Module

### Thay đổi chính:
- Triển khai `LookupService` và `BootstrapService` để tách biệt logic khỏi Controller.
- `SystemController` giờ đây chỉ đóng vai trò điều hướng, tuân thủ nguyên tắc Single Responsibility.

---

## 2. Tiêu chuẩn UI/UX Interaction (`_actions`)

### Tổng quan:
- Giới thiệu chuẩn `ActionableDto` cho các thực thể có tính tương tác cao.
- **Backend-Driven UI**: Trả về object `_actions` kèm theo lý do (`reason`) nếu hành động bị chặn, giúp Frontend giảm thiểu logic kiểm tra quyền.

---

## 3. Quản lý và Báo cáo (Management API)
- Bổ sung API điều phối Lead (`PATCH /crm/leads/:id/assign`).
- Bổ sung báo cáo nhanh hiệu suất (`GET /system/my-team/summary`).

---
*Tổng hợp từ các file walkthrough cũ ngày 28/04/2026.*
