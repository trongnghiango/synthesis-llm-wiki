---
id: dom-org-position-crud
title: Triển khai CRUD Vị trí (Positions)
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Hoàn thiện CRUD thực thể Positions với kiểm tra ràng buộc khóa ngoại và cơ chế bảo vệ ngăn xóa khi có nhân sự đang đảm nhiệm."
tags: [domain, org-structure, position, crud, drizzle]
---

### 1. Luồng Nghiệp vụ & Ràng buộc (Business Rules)
*   **Tạo mới (`createPosition`)**:
    *   Kiểm tra tính duy nhất của mã `code`.
    *   Validate sự tồn tại của các thực thể liên kết: `OrgUnitId`, `JobTitleId`, và `GradeId`.
*   **Cập nhật (`updatePosition`)**: Hỗ trợ cập nhật từng phần (Partial Update) qua phương thức `PATCH`.
*   **Xóa (`deletePosition`)**: Cơ chế bảo vệ toàn vẹn dữ liệu. Từ chối xóa vị trí (`Positions`) nếu đang có nhân sự (`Employee/User`) đảm nhiệm (kiểm tra qua `isPositionInUse`).

### 2. Thay đổi tại các Layer
*   **Repository Layer (Drizzle ORM)**:
    *   Cập nhật interface `IOrgStructureRepository` kế thừa từ `[[hb-drizzle-base-repo]]`.
    *   Thực thi các hàm kiểm tra ràng buộc: `isPositionInUse`, `findGradeById`, `findJobTitleById` trong `DrizzleOrgStructureRepository`.
*   **Application Layer**:
    *   Tách biệt dữ liệu bằng `PositionDto` (Agnostic DTO) độc lập với Database Schema.
    *   Xử lý logic nghiệp vụ chính tại `OrgStructureService`.
*   **Infrastructure Layer (API Controller)**:
    *   DTO đầu vào: `PositionRequestDto` tích hợp NestJS `class-validator` và Swagger.
    *   Endpoints:
        *   `POST /api/org-structure/positions` (Tạo mới)
        *   `PATCH /api/org-structure/positions/:id` (Cập nhật)
        *   `DELETE /api/org-structure/positions/:id` (Xóa)