---
id: arch-audit-log-decoupling
title: Thiết kế Hệ thống Audit Log Tách biệt (Decoupled Audit Log)
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
  - "[[hb-delta-logging]]"
summary: "Kiến trúc Audit Log phi xâm lấn qua Event-Driven Architecture (EDA), tối ưu hóa ghi bất đồng bộ và lưu trữ lai."
tags: [architecture, audit-log, eda, performance, postgres-jsonb]
---

## 1. Cơ chế Phi xâm lấn (Non-Invasive) & EDA
- **Capture**: Sử dụng `@AuditLog()` Decorator tại Service lớp nghiệp vụ để tự động phát hành `Domain Event` khi hoàn tất tác vụ.
- **Transport**: Đẩy event qua `EventBus` thuộc `CoreModule` (In-memory/RabbitMQ).
- **Process**: `AuditLogService` tiêu thụ event độc lập, chụp snapshot dữ liệu và lưu trữ.

## 2. API Contract & Khả năng Chuyển đổi (Hybrid DB)
Tách biệt lớp nghiệp vụ khỏi Database Engine (sử dụng PostgreSQL `jsonb` hiện tại, sẵn sàng chuyển đổi MongoDB).
```typescript
export interface IAuditLogRepository {
  save(log: AuditLog): Promise<void>;
  findWithFilters(query: AuditLogQuery): Promise<PaginatedResult<AuditLog>>;
}
```
- **Vị trí Module**: Khu trú tại `src/modules/system/audit-log/`. Sở hữu schema riêng, cấm phụ thuộc ngược vào module nghiệp vụ.

## 3. Tối ưu hóa Hiệu năng (Performance)
- **Ghi (Write - Non-blocking)**: Áp dụng cơ chế *Fire-and-forget* thông qua `setImmediate()` hoặc hàng đợi xử lý nền. Không chặn luồng HTTP response chính.
- **Đọc (Read - Org Hierarchy)**: Lưu trữ OrgUnit dưới dạng Materialized Path (`org_path` ví dụ `/Stax/Sales/HCM`).
  - *Truy vấn nhanh*: `WHERE org_path LIKE '/Stax/Sales/%'` (loại bỏ hoàn toàn truy vấn đệ quy).

## 4. Nguyên tắc Thực thi Nghiêm ngặt (Anti-patterns)
- ❌ **Cấm** import trực tiếp `AuditLogService` vào các dịch vụ nghiệp vụ khác (e.g., `LeadService`).
- ❌ **Cấm** sử dụng toán tử `await` khi phát tán Log Event.
- ❌ **Cấm** lưu trữ trạng thái trước/sau (`before/after`) bằng các trường văn bản phân mảnh (bắt buộc dùng `jsonb`).
- ❌ **Cấm** JOIN bảng Log với bảng User khi query (phải denormalize `user_name`, `user_role` trực tiếp vào bản ghi log).