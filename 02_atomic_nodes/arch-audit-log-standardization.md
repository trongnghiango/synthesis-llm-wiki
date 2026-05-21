---
id: arch-audit-log-standardization
title: Chuẩn hóa Audit Log, CamelCase và Activity Feed
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
  - "[[hb-delta-logging]]"
summary: "Hoàn thiện hạ tầng DrizzleAuditLogService, chuẩn hóa camelCase toàn hệ thống và triển khai Omnichannel Activity Feed."
tags: [audit-log, refactoring, activity-feed, drizzle, camel-case]
---

### 1. Hạ tầng Audit Log (Nhật ký hành động)
*   **Cơ chế:** `DrizzleAuditLogService` thực thi `AUDIT_LOG_PORT` dạng fire-and-forget.
*   **Bảng DB:** `audit_logs` (được lập chỉ mục đầy đủ).
*   **Tích hợp nghiệp vụ:** Tự động hóa ghi log cho các sự kiện lõi: Lead Won, Payment Allocated, Role Assigned, và User Provisioned (tham chiếu cấu trúc tại `[[hb-delta-logging]]`).

### 2. Chuẩn hóa Naming Convention (DB to TS)
*   **Quy tắc:** Ánh xạ tự động trong Drizzle Schemas từ `snake_case` (Database) sang `camelCase` (TypeScript) qua `[[hb-drizzle-base-repo]]`.
*   **Phạm vi refactor:** Loại bỏ hoàn toàn rò rỉ `snake_case` tại Controllers, DTOs, Mappers và hệ thống Unit Tests (đạt 0 lỗi TypeScript compile).

### 3. Kiến trúc Omnichannel Activity Feed & Onboarding
*   **Hội tụ dữ liệu:** `ActivityFeedService` gộp dữ liệu từ 2 nguồn: log hệ thống (`audit_logs`) và ghi chú tương tác thủ công (`interaction_notes`).
*   **API Contract:** `GET /organizations/:orgId/timeline` - Trả về dòng thời gian hội tụ của tổ chức.
*   **Tự động hóa Onboarding:** Kích hoạt luồng gửi thông báo và thiết lập dữ liệu ban đầu ngay khi tài khoản khách hàng mới được active.