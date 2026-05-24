---
id: 20260524-dom-schema-optimization
aliases:
  - "Domain: Schema Optimization Audit"
tags:
  - distilled
  - insight
  - database
  - schema
  - optimization
date: 2026-05-24
---

# Domain: Database Schema Optimization Audit (2026-05-08)

## Phase 1 — Chuẩn hóa & Hiệu suất
- **Naming Convention**: `quotes.schema.ts` → camelCase hoàn toàn.
- **Actor Accuracy**: `attachments.uploadedById` đổi FK từ `employees` → `users` (đúng actor đăng nhập).
- **Accounting Indexes**: 5 composite indexes trên `finotes` (`status`, `source_org_id`, `requested_by_id`, `deadline_at`, `type`).
- **Data Integrity**: FK `manager_id` → `employees.id` với `onDelete: 'set null'`.

## Phase 2 — Refactoring Kiến trúc Schema
- **Unified Attachments**: Hợp nhất `finote_attachments` vào bảng `attachments` chung. Thêm `category` (enum) và `tags` (text) để phân loại đa năng.
- **Lead Assignment (Option B+)**: Thêm `assignedEmployeeId` vào `leads` (gán trực tiếp), giữ `assignedPositionId` (báo cáo phòng ban) — dual reference.
- **HRM Foundation**: Bảng `employee_tasks` làm nền tảng quản lý công việc.

## Multi-tenant Seeder Fix
- Lỗi `ON CONFLICT` do thiếu unique tenant-scoped constraint.
- Fix: Thêm `uniqueIndex` trên `(organization_id, code)` cho `locations`, `grades`; `(organization_id, name)` cho `job_titles`.
- Cập nhật `DrizzleOrgStructureRepository` và `CompanyImportService` truyền `organizationId`.

## Kỹ thuật
- Khắc phục lỗi `TS2488` trong `DrizzleEmployeeRepository` bằng cách thay đổi destructuring kết quả `.returning()`.

---
**Source**: `[[20260508_schema_optimization.md]]`
