---
id: dom-org_structure_recursion_strategy
title: Chiến lược truy vấn đệ quy cơ cấu tổ chức
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Giải pháp truy vấn gộp nhân sự/vị trí cho các đơn vị trực thuộc bằng cơ chế so khớp chuỗi đường dẫn (LIKE path%) tối ưu hiệu năng."
tags: [org-structure, recursion, drizzle-orm, hrm-api]
---

### 1. Backend Layer (Drizzle ORM)
Truy vấn đệ quy thông qua Materialized Path (`path` dạng `/root/parent/child`) thay vì đệ quy CTE phức tạp:

```typescript
// OrgStructureRepository.ts
if (query.includeDescendants && query.orgUnitId) {
  const parentUnit = await db.query.orgUnits.findFirst({ 
    where: eq(orgUnits.id, query.orgUnitId) 
  });
  if (!parentUnit) throw new Error("OrgUnit not found");

  return db.select().from(positions)
    .innerJoin(orgUnits, eq(positions.orgUnitId, orgUnits.id))
    .where(like(orgUnits.path, `${parentUnit.path}%`));
}
```

### 2. Infrastructure Layer (Frontend API)
*   **File:** `/home/ka/temps/DentalCarePortal/client/src/modules/hrm/api/hrm.api.ts`
*   **Contract:** Bổ sung `includeDescendants?: boolean` vào interface query của `getPositions` và `getEmployees`.

### 3. Presentation Layer (UI Components)
*   **OrgChart.tsx (`OrgNode`):** Hiển thị song song 2 chỉ số: `Direct` (chỉ số trực tiếp tại đơn vị) và `Total` (tổng lũy kế bao gồm cả đơn vị con).
*   **org-structure.tsx (`DeptDetails`):** Tích hợp Switch "Bao gồm đơn vị con" để trigger tham số `includeDescendants` khi gọi API.