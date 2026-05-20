# Implementation Plan: Chiến lược truy vấn đệ quy

Kế hoạch này tập trung vào việc bổ sung tham số `includeDescendants` vào các API hiện có để cho phép lấy dữ liệu tổng hợp.

## 1. Backend Layer (Drizzle ORM)
Cần cập nhật Repository để xử lý logic `LIKE path%`.

### [ACTION] Update OrgStructureRepository
Bổ sung logic vào hàm `getPositions` và `getEmployees`:
```typescript
if (query.includeDescendants && query.orgUnitId) {
  // 1. Lấy path của đơn vị cha
  const parentUnit = await db.query.orgUnits.findFirst({ where: eq(orgUnits.id, query.orgUnitId) });
  // 2. Query tất cả đơn vị có path LIKE 'parentPath%'
  return db.select().from(positions)
    .innerJoin(orgUnits, eq(positions.orgUnitId, orgUnits.id))
    .where(like(orgUnits.path, `${parentUnit.path}%`));
}
```

---

## 2. Infrastructure Layer (Frontend API)
Cập nhật `hrm.api.ts` để truyền thêm tham số.

### [MODIFY] [hrm.api.ts](file:///home/ka/temps/DentalCarePortal/client/src/modules/hrm/api/hrm.api.ts)
- Cập nhật interface tham số cho `getPositions` và `getEmployees`.

---

## 3. Presentation Layer (UI Component)
Cập nhật hiển thị số liệu trên Sơ đồ.

### [MODIFY] [OrgChart.tsx](file:///home/ka/temps/DentalCarePortal/client/src/components/hrm/OrgChart.tsx)
- Cập nhật Component `OrgNode` để hiển thị cả 2 chỉ số: `Direct` và `Total`.

### [MODIFY] [DeptDetails (in org-structure.tsx)](file:///home/ka/temps/DentalCarePortal/client/src/pages/admin/hrm/org-structure.tsx)
- Thêm Toggle (Switch) "Bao gồm đơn vị con" để người dùng chủ động chọn cách xem dữ liệu nhân sự.
