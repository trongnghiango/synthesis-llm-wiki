---
id: hb-stax-safe-update-pattern
title: Thiết kế Safe-Update Pattern cho Drizzle Base Repository
layer: 3-atomic
parent: "[[03_technical_handbooks]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Giải pháp Safe-Update tự động lọc bỏ các trường bất biến (id, audit, tenant) khi cập nhật dữ liệu để tránh lỗi ràng buộc Database."
tags: [drizzle, repository, safe-update, database-constraint, refactoring]
---

## 1. Vấn đề & Mục tiêu
Khắc phục triệt để lỗi vi phạm ràng buộc bảo vệ Khóa chính và các trường bất biến (`Database Update Constraint Violation`) khi thực hiện cập nhật thực thể (UPDATE) qua Drizzle ORM.

## 2. Thiết kế Phương thức `mapToUpdate`
Tích hợp trực tiếp vào `DrizzleBaseRepository` (chi tiết tại `[[hb-drizzle-base-repo]]`) để tự động loại bỏ các trường hệ thống không cho phép cập nhật:

```typescript
protected mapToUpdate<T extends Record<string, any>>(data: T): Partial<T> {
  const protectedKeys = ['id', 'createdAt', 'organizationId', 'sourceOrgId'];
  const updatedData = { ...data };
  protectedKeys.forEach((key) => {
    delete updatedData[key];
  });
  return updatedData;
}
```

### Luồng xử lý trong Repository:
1. Nhận Payload cập nhật từ Entity.
2. Đi qua bộ lọc `mapToUpdate(payload)` để làm sạch dữ liệu.
3. Thực thi câu lệnh `db.update().set(cleanPayload).where(...)`.

## 3. Phạm vi Áp dụng (8 Repositories)
Mẫu thiết kế này đã được áp dụng đồng bộ trên các phân hệ:
- **CRM**: `Organization`, `Lead`, `Contact`, `Quote`
- **HRM**: `Employee`
- **Core**: `User`, `Notification`
- **Accounting**: `[[dom-accounting-finote]]`

## 4. Kiểm thử Tích hợp
- **Môi trường**: PGLite (In-memory Postgres).
- **Kết quả**: Kiểm thử thành công `DrizzleOrganizationRepository` với kịch bản `save (UPDATE)` -> Đạt trạng thái **PASS ✅** (toàn bộ 6/6 test cases vượt qua).