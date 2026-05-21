---
id: dom-user_entity_org_context_refactor
title: Chuẩn hóa truy cập Organization ID qua User Domain Entity
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[arch-als-tenant-isolation]]"
summary: "Tập trung logic xác định Tenant/Organization ID vào User Domain Entity thay vì xử lý thủ công tại Controllers/Services."
tags: [domain-driven-design, multi-tenancy, authentication, user-entity, refactoring]
---

### 1. Vấn đề & Thiết kế Domain (DDD)
Tránh phân tán logic Multi-tenancy (lấy từ `employee` hoặc `organization` context) và triệt tiêu bug hardcode `|| 1` bằng cách áp dụng *Single Point of Truth* tại `User` Domain Entity.

### 2. Chi tiết Triển khai Kỹ thuật

#### Domain Entity (`src/modules/user/domain/entities/user.entity.ts`)
```typescript
get organizationId(): number | undefined {
  return this._profileContext.employee?.organizationId || this._profileContext.organization?.id;
}
get isInternal(): boolean {
  return !!(this._profileContext.employee?.isInternal || this._profileContext.organization?.isInternal);
}
```

#### Tác động hệ thống (System Impact)
- **Infrastructure (JWT Payload)**: `JwtPayload` bổ sung `orgId?: number`. `AuthenticationService` (login/register/refresh) tự động nhúng `user.organizationId` vào token payload.
- **Drizzle Repository**: `DrizzleUserRepository.findByUsername()` bắt buộc load eager/join đầy đủ `employeeProfile` và `organizationProfile` để mapper có đủ context.
- **Refactor Controllers/Services**: 
  - Thay thế toàn bộ các pattern truy cập thủ công thành `user.organizationId` tại: `hrm-master-data.controller.ts`, `org-structure.controller.ts`, `company-import.controller.ts`, `lead-query.service.ts`.
  - Loại bỏ hoàn toàn fallback hardcode (`|| 1`) tại `employee.controller.ts` để đảm bảo an toàn dữ liệu Multi-tenancy.

### 3. Liên kết chéo
- Cơ chế cô lập Tenant: `[[arch-als-tenant-isolation]]`
- Chuẩn triển khai Repository: `[[hb-drizzle-base-repo]]`