# 02 Task List: Audit Log & Naming Standardization (2026-04-26)

- [x] Đăng ký Schema `audit_logs` vào Database Index.
- [x] Triển khai `DrizzleAuditLogService` (Fire-and-forget).
- [x] Đấu nối `AUDIT_LOG_PORT` vào `LoggingModule`.
- [x] Tích hợp ghi log vào 4 luồng nghiệp vụ: CRM, Accounting, RBAC, User.
- [x] Refactor toàn bộ Schema: Chuyển `snake_case` sang `camelCase`.
- [x] Fix lỗi logic mapping trong các Repository cũ sau khi refactor.
- [x] Triển khai bảng `interaction_notes` và `ActivityFeedService`.
- [x] Tạo script kiểm chứng (`verify-audit-log.ts`, `verify-activity-feed.ts`).
