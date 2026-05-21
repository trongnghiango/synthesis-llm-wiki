---
id: dom-org-structure-recursion-strategy
title: Chiến lược truy vấn đệ quy cơ cấu tổ chức
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Cơ chế truy vấn đệ quy qua Materialized Path (LIKE path%) hỗ trợ tổng hợp dữ liệu phòng ban con."
tags: [org-structure, recursion, drizzle-orm, api]
---

### 1. API Contract & Database Schema
- **Query Params**: Bổ sung `includeDescendants?: boolean` vào API truy vấn nhân sự/vị trí.
- **Cơ chế lọc**: Dựa trên trường `path` (Materialized Path) của bảng `org_units`.

### 2. Backend Implementation (Drizzle ORM)
Tích hợp logic truy vấn đệ quy tại `OrgStructureRepository` (kế thừa từ `[[hb-drizzle-base-repo]]`):

```typescript
if (query.includeDescendants && query.orgUnitId) {
  const parent = await db.query.orgUnits.findFirst({ where: eq(orgUnits.id, query.orgUnitId) });
  if (!parent) return [];
  
  return db.select().from(positions)
    .innerJoin(orgUnits, eq(positions.orgUnitId, orgUnits.id))
    .where(like(orgUnits.path, `${parent.path}%`));
}
```

### 3. Frontend Integration
- **API (`hrm.api.ts`)**: Cập nhật Interface tham số `getPositions` và `getEmployees` để truyền `includeDescendants`.
- **UI (`OrgChart.tsx` & `org-structure.tsx`)**:
  - `OrgNode`: Hiển thị đồng thời hai chỉ số: `Direct` (nhân sự trực tiếp) và `Total` (bao gồm con).
  - `DeptDetails`: Thêm Toggle `Switch` để kích hoạt trạng thái xem "Bao gồm đơn vị con".