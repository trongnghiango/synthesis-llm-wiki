---
id: dom-org-structure-recursion-strategy
title: Chiến lược truy vấn đệ quy cơ cấu tổ chức
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Giải pháp truy vấn đệ quy cây cơ cấu tổ chức sử dụng thuộc tính path và toán tử LIKE trên Drizzle ORM"
tags: [org-structure, recursion, drizzle-orm, hierarchical-data, hrm-api]
---

### 1. Nguyên lý Thiết kế (Path-based Hierarchy)
- Sử dụng mô hình Materialized Path (`orgUnits.path`) để quản lý cấu trúc cây phân cấp của đơn vị tổ chức.
- Truy vấn đệ quy tất cả các đơn vị con (descendants) bằng toán tử `LIKE 'parentPath%'` thay thế cho CTE đệ quy nhằm tối ưu hóa hiệu năng truy vấn.

### 2. Thiết kế API Contract
Cập nhật interface query tham số cho API `getPositions` và `getEmployees` trong `hrm.api.ts`:
```typescript
interface OrgQueryDto {
  orgUnitId?: string;
  includeDescendants?: boolean; // Thêm cờ toggle truy vấn gộp
}
```

### 3. Logic Xử lý Backend (Drizzle ORM)
Bổ sung logic tìm kiếm đệ quy tại Repository Layer:
```typescript
if (query.includeDescendants && query.orgUnitId) {
  const parentUnit = await db.query.orgUnits.findFirst({ where: eq(orgUnits.id, query.orgUnitId) });
  if (!parentUnit) throw new Error("Org unit not found");

  return db.select().from(positions)
    .innerJoin(orgUnits, eq(positions.orgUnitId, orgUnits.id))
    .where(like(orgUnits.path, `${parentUnit.path}%`));
}
```

### 4. Giao diện (Presentation Layer)
- **`OrgChart.tsx`**: Component `OrgNode` hiển thị song song hai chỉ số: `Direct` (nhân sự trực tiếp tại đơn vị) và `Total` (nhân sự tổng bao gồm cả đơn vị con).
- **`org-structure.tsx` (DeptDetails)**: Tích hợp Toggle Switch "Bao gồm đơn vị con" để thay đổi tham số `includeDescendants` khi gọi API.