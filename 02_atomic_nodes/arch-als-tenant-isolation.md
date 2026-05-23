---
id: arch-als-tenant-isolation
title: Cô lập Tenant qua Async Local Storage (ALS) & VisibilityContext
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[arch-clean-boundaries]]"
summary: "Cơ chế cô lập dữ liệu đa doanh nghiệp (Multi-tenancy) tự động bằng cách kết hợp dynamic VisibilityContext qua JWT Payload và Async Local Storage (ALS)."
tags: [architecture, security, multi-tenancy, als, tenant-isolation, visibility-context]
---

# Cô lập Tenant qua Async Local Storage (ALS) & VisibilityContext

Để cách ly dữ liệu giữa các doanh nghiệp (Tenants) tuyệt đối, STAX áp dụng mô hình **Stateless Multi-Tenancy** kết hợp **Dynamic Scoping** qua `VisibilityContext` và `AsyncLocalStorage (ALS)`.

## 1. Hiến pháp Đa thuê (Stateless Multi-Tenancy Law)
*   **Bảo vệ dữ liệu động:** Bảng `sessions` vật lý và thực thể `Session` cố ý **không** lưu trường `organizationId`. Việc này ngăn chặn triệt để rủi ro rò rỉ dữ liệu do thông tin doanh nghiệp bị lỗi thời (Data Stale) khi nhân sự chuyển tổ chức hoặc thay đổi quyền.
*   **Cơ chế động:** Toàn bộ ngữ cảnh xác thực doanh nghiệp của người dùng được tính toán động tại thời điểm đăng nhập/quay vòng token và lưu trữ an toàn trong JWT Payload.

## 2. Cấu trúc ngữ cảnh VisibilityContext
Hệ thống xác định phạm vi truy cập dữ liệu thông qua 3 cấp độ trong `VisibilityContext`:
*   `ALL` (Admin hệ thống): Truy cập toàn bộ dữ liệu hệ thống mà không áp dụng bộ lọc Tenant.
*   `ASSIGNED_ONLY` (Chuyên viên/Kỹ sư hỗ trợ): Được cấp phép truy cập danh sách các `allowedOrganizationIds` được gán trực tiếp.
*   `SELF_ONLY` (Khách thuê độc lập / Nhân viên thường): Chỉ có quyền truy cập duy nhất vào ID doanh nghiệp của họ (`allowedOrganizationIds[0]`).

## 3. Sơ đồ luồng xử lý động 3 bước
1.  **Tính toán ngữ cảnh (Login):** `AuthenticationService` gọi `IVisibilityResolverService.resolve(userId, orgId)` để sinh ra `VisibilityContext` tương ứng (so sánh các roles của user sau khi đã chuyển sang CHỮ IN HOA như `ADMIN`, `SUPER_ADMIN`, `MANAGER` để khớp chính xác với CSDL) và nhúng nó cùng `orgId` vào **JWT Payload**.
2.  **Đẩy vào ALS (Request Gate):** Tại mỗi HTTP Request, `JwtStrategy` giải mã JWT Payload và nạp `VisibilityContext` vào **AsyncLocalStorage** thông qua `RequestContextService.setVisibilityContext(payload.visibilityContext)`.
3.  **Tự động Scoping (Persistence):** Tại tầng CSDL, `DrizzleBaseRepository` tự động kiểm tra sự tồn tại của `VisibilityContext` từ ALS.

## 4. Thực thi Lọc tự động (applyTenantIsolation)
Hàm `applyTenantIsolation()` ở lớp cha `DrizzleBaseRepository` tự động kiểm tra sự tồn tại của `VisibilityContext` từ ALS. Từ đó, hàm nhận diện loại bảng thông qua thuộc tính đặc trưng và tự động chọn cột lọc (`columnToFilter`) tương ứng:
- Nếu bảng là `organizations` (nhận diện qua `'organizationName' in table`): Lọc theo khóa chính `id`.
- Nếu bảng là `finotes` (nhận diện qua `'tenantId' in table`): Lọc theo khóa ngoại `tenantId`.
- Các bảng con khác (nhận diện qua `'organizationId' in table`): Lọc theo khóa ngoại `organizationId`.

Sau đó, hàm tự động chèn mệnh đề điều kiện thích hợp (`eq` hoặc `inArray` theo `allowedOrganizationIds`) trực tiếp vào mảng truy vấn Drizzle ORM:
```typescript
protected applyTenantIsolation<T extends { organizationId?: any; id?: any; tenantId?: any }>(
  conditions: any[],
  table: T
): void {
  const hasOrgId = 'organizationId' in table;
  const hasTenantId = 'tenantId' in table;
  const isOrgTable = 'organizationName' in table; // Nhận diện bảng organizations
  
  if (!hasOrgId && !hasTenantId && !isOrgTable) {
    return; // Bảng không chia theo Tenant
  }

  const visibility = RequestContextService.getContext()?.visibilityContext;
  if (!visibility) {
    return;
  }

  const columnToFilter = hasTenantId 
    ? (table as any).tenantId 
    : (hasOrgId ? (table as any).organizationId : (table as any).id);

  if (visibility.scope === 'SELF_ONLY') {
    conditions.push(eq(columnToFilter, visibility.allowedOrganizationIds[0]));
  } else if (visibility.scope === 'ASSIGNED_ONLY') {
    if (visibility.allowedOrganizationIds.length > 0) {
      conditions.push(inArray(columnToFilter, visibility.allowedOrganizationIds));
    } else {
      // Chuyên viên nhưng chưa được gán Org nào -> Chốt chặn an toàn chặn truy cập
      conditions.push(eq(columnToFilter, -1));
    }
  }
}
```

## 5. Liên kết chéo
*   [[arch-clean-boundaries]]: Ranh giới Clean Architecture đảm bảo ALS cô lập riêng biệt.
*   [[hb-drizzle-base-repo]]: Kế thừa `DrizzleBaseRepository` để tự động hưởng cơ chế lọc Tenant.
*   [[hb-http-request-flow]]: Xem vị trí của `JwtStrategy` và ALS Init trong luồng chạy request.
