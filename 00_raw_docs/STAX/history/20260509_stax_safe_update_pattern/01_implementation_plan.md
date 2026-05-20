# Implementation Plan: STAX Safe-Update Pattern

Mẫu thiết kế này tập trung vào việc bảo vệ tính toàn vẹn dữ liệu ở lớp hạ tầng, ngăn chặn việc cập nhật các trường bất biến (Immutable Fields) trong PostgreSQL thông qua Drizzle ORM.

## A. Database & Schema
- Không thay đổi Schema.
- Các bảng bị ảnh hưởng gián tiếp qua Repository: `organizations`, `leads`, `contacts`, `employees`, `finotes`, `notifications`, `users`.

## B. Domain Layer
- Không thay đổi Domain Layer. Pattern này chỉ tác động vào cách thức Persistence hạch toán dữ liệu.

## C. Infrastructure Layer (Trọng tâm)

### 1. Cập nhật `DrizzleBaseRepository`
Bổ sung helper method hỗ trợ lọc dữ liệu an toàn.

```typescript
// src/core/shared/infrastructure/persistence/drizzle-base.repository.ts
protected mapToUpdate<T extends { 
    id?: any; 
    createdAt?: any; 
    organizationId?: any; 
    sourceOrgId?: any 
}>(data: T): Omit<T, 'id' | 'createdAt' | 'organizationId' | 'sourceOrgId'> {
    const { id, createdAt, organizationId, sourceOrgId, ...updateData } = data;
    return updateData;
}
```

### 2. Refactor 7 Repositories
Thay thế việc truyền trực tiếp `data` vào `.set()` bằng `this.mapToUpdate(data)`.

- **Danh sách file:**
  1. `src/modules/crm/infrastructure/persistence/drizzle-organization.repository.ts`
  2. `src/modules/crm/infrastructure/persistence/drizzle-lead.repository.ts`
  3. `src/modules/crm/infrastructure/persistence/drizzle-contact.repository.ts`
  4. `src/modules/employee/infrastructure/persistence/drizzle-employee.repository.ts`
  5. `src/modules/accounting/infrastructure/persistence/drizzle-finote.repository.ts`
  6. `src/modules/notification/infrastructure/persistence/drizzle-notification.repository.ts`
  7. `src/modules/user/infrastructure/persistence/drizzle-user.repository.ts`

## D. API Contracts
- Không thay đổi API Contract. Frontend vẫn gửi dữ liệu bình thường, Backend sẽ tự lọc để đảm bảo an toàn.

## E. Testing Strategy
- **Integration Test (PGLite):** Sử dụng các file `.spec.ts` hiện có của các Repository để verify.
- **Test Case quan trọng:** 
  - Thực hiện lệnh `save()` trên một Entity đã có ID.
  - Verify rằng lệnh SQL sinh ra không gây lỗi `500` (hiện tại đang lỗi).
  - Verify rằng giá trị `id` và `createdAt` sau khi update vẫn giữ nguyên giá trị cũ.

## F. Decision Log
- **Tại sao chọn `Omit` ở tầng Base?** Đảm bảo tính nhất quán (Consistency). Nếu mỗi Repository tự dùng destructuring `{id, ...updateData}`, lập trình viên rất dễ quên bỏ `createdAt` hoặc `organizationId`, dẫn đến rò rỉ dữ liệu hoặc lỗi DB.
- **Tên `mapToUpdate`:** Rõ ràng về mục đích (ánh xạ để cập nhật), dễ đọc khi kết hợp với `.set()`.
