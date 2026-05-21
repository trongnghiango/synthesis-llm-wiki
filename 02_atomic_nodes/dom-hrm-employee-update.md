---
id: dom-hrm-employee-update
title: API Cập nhật Nhân sự (HRM)
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[arch-als-tenant-isolation]]"
summary: "Định nghĩa API PATCH /api/hrm/employees/:id tích hợp ràng buộc multi-tenancy và kiểm tra chéo vị trí nhân sự."
tags: [hrm, employee, api, validation, multi-tenancy]
---

### 1. API Contract & DTO
- **Endpoint:** `PATCH /api/hrm/employees/:id`
- **Request DTO (`UpdateEmployeeRequestDto`):**
  ```typescript
  type UpdateEmployeeRequestDto = Partial<{
    fullName: string; phoneNumber: string; locationId: number;
    positionId: number; managerId: number; dateOfBirth: Date;
    avatarUrl: string; joinDate: Date;
  }>
  ```

### 2. Ràng buộc Nghiệp vụ (Business Constraints)
- **Cô lập dữ liệu (Multi-tenancy):** Thực hiện thông qua `[[arch-als-tenant-isolation]]`. Chỉ cho phép cập nhật khi `employee.organizationId === currentUser.organizationId`.
- **Hợp lệ Vị trí (Position Validation):** Nếu `positionId` được truyền vào:
  1. Kiểm tra sự tồn tại của Position trong Database.
  2. Xác thực `position.organizationId === currentUser.organizationId`.
  3. (Optional) Trạng thái hoạt động `position.isActive === true`.

### 3. Luồng Xử lý Hệ thống (Execution Flow)
```typescript
async function updateEmployee(id: string, dto: UpdateEmployeeRequestDto, currentUser: User) {
  const emp = await repo.findById(id);
  if (!emp || emp.organizationId !== currentUser.organizationId) throw new ForbiddenException();
  
  if (dto.positionId) {
    const pos = await posRepo.findById(dto.positionId);
    if (!pos || pos.organizationId !== currentUser.organizationId) {
      throw new BadRequestException('Invalid Position');
    }
  }
  
  const updatedData = { ...dto, updatedAt: new Date() };
  return repo.update(id, updatedData); // Tích hợp qua [[hb-drizzle-base-repo]] nếu có
}
```