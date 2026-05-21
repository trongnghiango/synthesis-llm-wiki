---
id: dom-org_structure_position_api
title: Triển khai API Danh sách Vị trí theo Phòng ban
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Định nghĩa API endpoint và luồng dữ liệu truy vấn danh sách Vị trí (Position) theo Đơn vị tổ chức (OrgUnit) sử dụng Drizzle ORM."
tags: [org-structure, position, drizzle, api]
---

### 1. Luồng Dữ liệu & Nghiệp vụ
Luồng truy vấn thông tin định biên vị trí của Đơn vị tổ chức (Org Unit):
`OrgStructureController` -> `OrgStructureService` -> `IOrgStructureRepository` (`DrizzleOrgStructureRepository`) -> Table `positions`.

### 2. Thiết kế API Contract
*   **Endpoint:** `GET /api/org-structure/positions`
*   **Query Params:** `orgUnitId: string` (Bắt buộc)
*   **Bảo mật:** Quyền `org:read` áp dụng qua Permission Guard.
*   **Cấu trúc dữ liệu phản hồi (`PositionResponseDto`):**
    ```typescript
    interface PositionResponseDto {
      id: string;
      code: string;
      name: string;
      orgUnitId: string;
      jobTitleId: string;
      gradeId: string;
      headcountLimit: number;
      isActive: boolean;
    }
    ```

### 3. Chi tiết triển khai Mã nguồn
*   **Repository Interface:**
    ```typescript
    // IOrgStructureRepository
    findPositionsByOrgUnitId(orgUnitId: string): Promise<Position[]>;
    ```
*   **Drizzle Implementation:** Truy vấn trực tiếp từ thực thể dữ liệu bảng `positions`, kế thừa cấu trúc chuẩn của `[[hb-drizzle-base-repo]]`.
*   **Service Layer:** `OrgStructureService.getPositionsByOrgUnit(orgUnitId)` làm nhiệm vụ điều phối và chuyển đổi dữ liệu sang định dạng DTO.