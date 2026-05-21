---
id: dom-employee-update-api
title: API Cập nhật Nhân sự và Ràng buộc Vị trí
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[arch-als-tenant-isolation]]"
  - "[[hb-drizzle-base-repo]]"
summary: "Định nghĩa API PATCH cập nhật thông tin nhân viên kèm kiểm tra ràng buộc vị trí và cô lập tenant."
tags: [hrm, employee, api, tenant-isolation, validation]
---

### 1. API Contract
- **Endpoint**: `PATCH /api/hrm/employees/:id`
- **DTO (`UpdateEmployeeRequestDto`)**:
  ```ts
  type UpdateEmployeeRequestDto = Partial<{
    fullName: string; 
    phoneNumber: string; 
    locationId: number;
    positionId: number; 
    managerId: number; 
    dateOfBirth: Date;
    avatarUrl: string; 
    joinDate: Date;
  }>;
  ```

### 2. Luồng Xử lý & Ràng buộc (Flow & Constraints)
1. **Cô lập Tenant**: Lấy `orgId` từ Context thông qua `[[arch-als-tenant-isolation]]`.
2. **Xác thực Nhân sự**: 
   - Kiểm tra nhân viên tồn tại theo `:id`.
   - Xác thực: `employee.organizationId === orgId`. Sai trả về lỗi `403 Forbidden`.
3. **Ràng buộc Vị trí** (Nếu có `positionId` trong DTO):
   - Truy vấn `Position` theo `positionId`.
   - Yêu cầu: `position.organizationId === orgId` và `position.isActive === true`.
4. **Cập nhật**:
   - Ghi đè các trường thay đổi từ DTO vào thực thể Employee.
   - Hệ thống tự động cập nhật trường `updatedAt`.
   - Thực thi lưu trữ qua `[[hb-drizzle-base-repo]]`.