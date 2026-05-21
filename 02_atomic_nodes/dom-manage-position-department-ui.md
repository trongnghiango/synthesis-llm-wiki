```yaml
---
id: dom-manage-position-department-ui
title: UI Quản lý Vị trí và Bổ nhiệm Phòng ban
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
  - "[[arch-als-tenant-isolation]]"
  - "[[hb-delta-logging]]"
summary: "Thiết kế giao diện Staffing Board dạng Kanban và chuẩn hóa API quản lý vị trí, bổ nhiệm nhân sự."
tags: [hrm, staffing-board, org-structure, api-standardization, kanban-ui]
---
```

## 1. API Contract Chuẩn hóa (`hrm.api.ts`)
```typescript
// Quản lý Position (Chức vụ)
export type PositionPayload = { name: string; code: string; departmentId: string; maxStaff: number };
export const createPosition = (payload: PositionPayload): Promise<Position> => {};
export const updatePosition = (id: string, payload: Partial<PositionPayload>): Promise<Position> => {};

// Bổ nhiệm/Điều chuyển Nhân sự (Assignment)
export type AssignPayload = { employeeId: string; positionId: string; departmentId: string; isPrimary: boolean };
export const assignEmployee = (payload: AssignPayload): Promise<Assignment> => {};
```

## 2. Kiến trúc Thành phần UI (Staffing Board)
*   **Staffing Board (Kanban View):** Tích hợp trực tiếp tại `OrgStructurePage`. Mỗi cột đại diện cho một `Position`. Hỗ trợ kéo thả (Drag-and-Drop) thẻ nhân viên giữa các vị trí để trigger API `assignEmployee`.
*   **PositionModal:** Form tạo/sửa Position trực tiếp từ Sidebar cấu trúc tổ chức.
*   **AssignmentModal:** Component độc lập, tái sử dụng để tìm kiếm nhanh nhân viên và gán vào vị trí nghiệp vụ kèm kiểm tra điều kiện ràng buộc `maxStaff`.

## 3. Ràng buộc & Tích hợp Hệ thống
*   **Tenant Isolation:** Mọi truy vấn phòng ban/vị trí phải đi qua middleware cô lập dữ liệu `[[arch-als-tenant-isolation]]`.
*   **Audit Trail:** Mọi thao tác điều chuyển nhân sự phải được ghi nhận lịch sử thay đổi thông qua hệ thống `[[hb-delta-logging]]`.
*   **State Management:** Đồng bộ danh sách nhân sự tại Board sau khi kết thúc kéo thả bằng cách refetch query key của `[[hb-drizzle-base-repo]]`.