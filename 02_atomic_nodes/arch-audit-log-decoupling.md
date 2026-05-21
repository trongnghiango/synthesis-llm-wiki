---
id: arch-audit-log-decoupling
title: Thiết kế Hệ thống Audit Log Bất đối xứng
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
  - "[[hb-delta-logging]]"
summary: "Kiến trúc Audit Log phi tập trung dùng Event-Driven, Decorator không xâm lấn, lưu trữ JSONB và Materialized Path."
tags: [architecture, audit-log, event-driven, performance]
---

## 1. Kiến trúc Bất đối xứng (Non-Invasive EDA)
- **Capture:** Dùng `@AuditLog()` Decorator trên Service Method để phát Domain Event ngay sau khi method thực thi thành công.
- **Transport:** Đẩy Event vào Event Bus (In-memory/RabbitMQ) phi tuần tự (Non-blocking).
- **Process:** `AuditLogModule` độc lập tiêu thụ event và persist dữ liệu. Không import ngược `AuditLogService` vào các Domain Service khác.

## 2. Repository Interface & Storage
```typescript
export interface IAuditLogRepository {
  save(log: AuditLog): Promise<void>;
  findWithFilters(query: AuditLogQuery): Promise<PaginatedResult<AuditLog>>;
}
```
- **Database:** Hiện tại dùng Drizzle ORM (PostgreSQL `jsonb` để lưu cấu trúc snapshot dữ liệu), sẵn sàng chuyển đổi MongoDB.
- **Schema Rules:** Lưu `before/after` dạng `jsonb` (`[[hb-delta-logging]]`). Denormalize thông tin User (tên, email) trực tiếp vào bảng Log để triệt tiêu lệnh `JOIN` khi truy vấn.

## 3. Tối ưu hóa Hiệu năng (Performance Optimization)
- **Write Path:** Sử dụng `setImmediate()` hoặc Event Bus để tách biệt luồng ghi log. Tuyệt đối không dùng `await` khi phát tán Log Event nhằm giải phóng luồng xử lý chính.
- **Read Path (Hierarchical Query):** Áp dụng **Materialized Path** cho phân quyền đơn vị (`OrgUnit`).
  - Cột `org_path` lưu dạng chuỗi định danh đường dẫn (Ví dụ: `/Stax/Sales/HCM`).
  - Truy vấn cấp dưới bằng: `WHERE org_path LIKE '/Stax/Sales/%'` thay thế hoàn toàn cho đệ quy SQL.

## 4. Quy tắc Nghiêm ngặt (Anti-patterns)
- Không liên kết trực tiếp (Tight Coupling) giữa bảng Nghiệp vụ và bảng Log.
- Không chặn luồng HTTP Request của User để chờ ghi Log thành công.