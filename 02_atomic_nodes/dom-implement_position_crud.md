---
id: dom-implement_position_crud
title: Triển khai CRUD Positions (Cơ cấu tổ chức)
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Chi tiết kỹ thuật triển khai nghiệp vụ CRUD Vị trí (Positions) tích hợp kiểm tra ràng buộc nhân sự và Drizzle ORM."
tags: [positions, crud, drizzle, org-structure]
---

## 1. Nghiệp vụ & Ràng buộc (Business Rules)
Triển khai tại `OrgStructureService` đảm bảo:
- **Tạo mới (`createPosition`)**: Kiểm tra trùng `code` (Unique); xác thực sự tồn tại của `OrgUnitId`, `JobTitleId`, `GradeId`.
- **Cập nhật (`updatePosition`)**: Cho phép cập nhật từng phần (Partial Update).
- **Xóa (`deletePosition`)**: Cơ chế Soft-guard. Từ chối xóa bằng `isPositionInUse` nếu có nhân sự đang gán với vị trí này.

## 2. API Contracts
Base Route: `/api/org-structure/positions`

| Method | Endpoint | Request DTO / Params | Mô tả |
| :--- | :--- | :--- | :--- |
| **POST** | `/` | `PositionRequestDto` | Tạo mới Vị trí |
| **PATCH** | `/:id` | `Partial<PositionRequestDto>` | Cập nhật một phần |
| **DELETE** | `/:id` | `id: UUID` | Xóa vị trí (nếu không có nhân sự) |

*DTOs được định nghĩa độc lập ở tầng Application (`PositionDto`) để đảm bảo tính agnostic.*

## 3. Database Layer (`IOrgStructureRepository`)
Sử dụng Drizzle ORM tích hợp qua `DrizzleOrgStructureRepository`:
- `updatePosition(id: string, data: PartialPosition): Promise<Position>`
- `deletePosition(id: string): Promise<void>`
- `isPositionInUse(id: string): Promise<boolean>` -> Kiểm tra liên kết bảng `Employees`.
- `findGradeById(id: string)`, `findJobTitleById(id: string)` -> Xác thực FK.