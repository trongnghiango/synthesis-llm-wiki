---
title: "ORM Mapping & Repository Pattern"
summary: "Hướng dẫn kỹ thuật về Drizzle ORM, Base Repository và kỹ thuật Mapping trong STAX"
description: |
  Tài liệu này mô tả cách STAX sử dụng Drizzle ORM để tương tác với PostgreSQL.
  Tập trung vào DrizzleBaseRepository, quản lý Transaction qua ALS và cách sử dụng Mapper 
  để tách biệt Domain Entity khỏi Persistence Model.
tags:
  - drizzle
  - postgresql
  - repository
  - mapping
  - clean-architecture
status: current
last_updated: "2026-05-10"
---

# 📂 ORM Mapping & Repository Pattern

## 1. Triết lý Persistence
STAX tuân thủ nguyên tắc **Persistence Ignorance**. Domain Layer không biết gì về Drizzle. Sự kết nối được thực hiện ở tầng Infrastructure thông qua:
1. **Repository Implementation**: Kế thừa từ `DrizzleBaseRepository`.
2. **Mappers**: Chuyển đổi dữ liệu qua lại giữa Domain Entity và Database Row.

## 2. DrizzleBaseRepository
Lớp cơ sở này (`core/shared/infrastructure/persistence/drizzle-base.repository.ts`) cung cấp các tiện ích quan trọng:

### 2.1. Quản lý Transaction (ALS)
Phương thức `getDb()` tự động kiểm tra xem có Transaction nào đang chạy trong Context hiện tại (thông qua Async Local Storage) hay không:
```typescript
protected getDb(): NodePgDatabase<typeof schema> {
  const tx = TransactionContextService.getTx();
  return tx ? (tx as unknown as NodePgDatabase<typeof schema>) : this.db;
}
```
**Lợi ích:** Bạn không cần truyền biến `tx` xuyên qua các hàm. Chỉ cần gọi `this.getDb()` và Drizzle sẽ tự động thực thi trong transaction nếu có.

### 2.2. Bảo vệ dữ liệu bất biến (mapToUpdate)
Sử dụng `this.mapToUpdate(data)` khi thực hiện lệnh `.set()` để loại bỏ các trường không được phép sửa (id, createdAt, organizationId):
```typescript
await db.update(schema.finotes)
    .set(this.mapToUpdate(data))
    .where(eq(schema.finotes.id, data.id));
```

## 3. Quy trình Mapping (The Mapper Pattern)
Mỗi module đều có thư mục `persistence/mappers/`. Mapper có 2 nhiệm vụ chính:

### 3.1. toPersistence (Domain -> Database)
Chuẩn hóa dữ liệu từ Entity sang định dạng bảng.
- Xử lý Value Objects (VD: `Money` -> `amount` + `currency`).
- Phẳng hóa (Flatten) các cấu trúc lồng nhau.

### 3.2. toDomain (Database -> Domain)
Khởi tạo Entity từ dữ liệu thô.
- Sử dụng hàm tạo hoặc Static Factory Method của Entity.
- Đảm bảo tính đóng gói (Encapsulation).

## 4. Best Practices
1. **Luôn sử dụng returning():** Khi insert hoặc update để lấy dữ liệu mới nhất từ DB (bao gồm các giá trị mặc định của DB như timestamps).
2. **Check Tenant ID:** Mọi truy vấn phải đi kèm `eq(schema.table.tenantId, orgId)` để đảm bảo cô lập dữ liệu đa thuê bao (Multi-tenancy).
3. **Sử dụng Relational Queries:** Drizzle hỗ trợ `.query.findFirst({ with: { ... } })`, hãy ưu tiên dùng khi cần lấy dữ liệu liên quan mà không muốn viết Join thủ công.

---
*Tham khảo code mẫu tại: `backend/src/modules/accounting/infrastructure/persistence/drizzle-finote.repository.ts`*
