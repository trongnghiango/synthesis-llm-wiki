```yaml
---
id: dom-org-structure-position-api
title: Triển khai API Vị trí theo Phòng ban
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "API lấy danh sách vị trí định biên theo đơn vị tổ chức (Org Unit) sử dụng Drizzle ORM và phân quyền org:read."
tags: [api, org-structure, position, drizzle, authorization]
---

### 1. Luồng xử lý & Phân rã kỹ thuật

*   **API Endpoint:** `GET /api/org-structure/positions?orgUnitId={orgUnitId}`
*   **Bảo mật:** Bảo vệ bởi Permission Guard yêu cầu quyền `org:read`.
*   **Kiến trúc:** Triển khai theo mô hình Controller -> Service -> Repository (kế thừa `[[hb-drizzle-base-repo]]`).

### 2. Thiết kế Hợp đồng & Cấu trúc Dữ liệu

#### DTO Phản hồi (`PositionResponseDto`)
```typescript
interface PositionResponseDto {
  id: string | number;
  code: string;
  name: string;
  orgUnitId: string | number;
  jobTitleId: string | number;
  gradeId: string | number;
  headcountLimit: number;
  isActive: boolean;
}
```

#### Thiết kế Interfaces
*   **Tầng Repository (`IOrgStructureRepository`):**
    ```typescript
    findPositionsByOrgUnitId(orgUnitId: string | number): Promise<Position[]>;
    ```
    *Thực thi tại `DrizzleOrgStructureRepository` qua câu lệnh query bảng `positions` lọc theo điều kiện `orgUnitId`.*

*   **Tầng Service (`OrgStructureService`):**
    ```typescript
    getPositionsByOrgUnit(orgUnitId: string | number): Promise<PositionResponseDto[]>;
    ```
```