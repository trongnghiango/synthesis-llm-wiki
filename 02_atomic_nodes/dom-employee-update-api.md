---
id: dom-employee-update-api
title: API Cập nhật Nhân sự (Employee Update)
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[arch-tenant-isolation]]"
  - "[[hb-drizzle-base-repo]]"
summary: "Quy trình nghiệp vụ và API contract cập nhật thông tin nhân sự bảo mật đa thuê bao (multi-tenancy) và ràng buộc vị trí."
tags: [hrm, employee, api-patch, multi-tenancy, validation]
---

# Nghiệp vụ Cập nhật Nhân sự (PATCH /api/hrm/employees/:id)

Giải quyết lỗi `404` bằng việc cung cấp API cập nhật thông tin nhân viên, tích hợp kiểm soát đa chi nhánh `[[arch-tenant-isolation]]`.

## 1. API Contract (DTO)
```typescript
export class UpdateEmployeeRequestDto {
  fullName?: string;
  phoneNumber?: string;
  locationId?: number;
  positionId?: number;
  managerId?: number;
  dateOfBirth?: Date;
  avatarUrl?: string;
  joinDate?: Date;
}
```

## 2. Quy trình Xử lý & Ràng buộc (Service Layer)
Áp dụng qua Repository tuần tự (`[[hb-drizzle-base-repo]]`):
1. **Kiểm tra Quyền sở hữu (Multi-tenancy):**
   * Truy vấn `employee` theo `id`.
   * Bắt buộc `employee.organizationId == currentUser.organizationId`. Sai lệch -> Ném `ForbiddenError`.
2. **Xác thực Vị trí (Position Validation):**
   * Nếu có `positionId`: Truy vấn `position` tương ứng.
   * Yêu cầu `position.organizationId == currentUser.organizationId` và `position.isActive == true`.
3. **Cập nhật Dữ liệu:**
   * Ghi đè các trường thay đổi từ DTO vào Entity.
   * Tự động cập nhật thuộc tính `updatedAt`.
   * Lưu thay đổi thông qua Repo và kích hoạt ghi log (`[[hb-delta-logging]]`).