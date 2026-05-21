```yaml
---
id: arch-audit-log-standardization
title: Chuẩn Hóa Audit Log, Naming & Activity Feed
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
  - "[[hb-delta-logging]]"
  - "[[arch-als-tenant-isolation]]"
summary: "Chuẩn hóa ánh xạ snake_case sang camelCase, thực thi DrizzleAuditLogService qua port, và hợp nhất dữ liệu Omnichannel Activity Feed."
tags: [audit-log, naming-standardization, activity-feed, drizzle, onboarding]
---

### 1. Hệ Thống Audit Log & Chuẩn Hóa Naming
* **Audit Log Architecture**: 
  * Triển khai `DrizzleAuditLogService` bất đồng bộ (fire-and-forget) dựa trên interface `AUDIT_LOG_PORT`.
  * Áp dụng thành công cho 4 sự kiện cốt lõi: Lead Won, Payment Allocated, Role Assigned, và User Provisioned. Chi tiết kỹ thuật ghi log xem tại `[[hb-delta-logging]]`.
* **Database Mapping (Snake to Camel)**:
  * Áp dụng cơ chế map cấu trúc `snake_case` dưới Database thành `camelCase` trên tầng TypeScript/Drizzle Schema (tham chiếu `[[hb-drizzle-base-repo]]`).
  * Loại bỏ triệt để rò rỉ cú pháp `snake_case` tại Controllers, DTOs, Mappers và hệ thống Unit Test.

### 2. Omnichannel Activity Feed & Onboarding Automation
* **Cấu trúc Dữ liệu Timeline**:
  * Bảng `interaction_notes`: Lưu trữ các hoạt động thủ công (ghi chú cuộc gọi, biên bản họp).
  * Bảng `audit_logs`: Lưu trữ các sự kiện hệ thống tự động.
* **Hợp nhất dòng thời gian (Timeline)**:
  * Triển khai `ActivityFeedService` chịu trách nhiệm gộp và sắp xếp dữ liệu từ hai nguồn trên.
  * API Contract: `GET /organizations/:orgId/timeline` - Phục vụ hiển thị dòng thời gian hội tụ của Tổ chức.
* **Onboarding Tự động**: Kích hoạt chuỗi hành động (gửi thông báo, khởi tạo cấu hình mặc định) khi một tổ chức/Tenant được kích hoạt thành công (tuân thủ nguyên tắc cách ly dữ liệu tại `[[arch-als-tenant-isolation]]`).
```